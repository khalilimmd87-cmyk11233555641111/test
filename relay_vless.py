# ══════════════════════════════════════════════════════════════════════════════
# relay_vless.py — تونل VLESS / Trojan روی WebSocket
# ══════════════════════════════════════════════════════════════════════════════

import asyncio
import hashlib
import secrets
import socket
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect

from state import (
    LINKS, LINKS_LOCK, stats, hourly_traffic, connections,
    error_logs, logger, is_link_allowed, save_state, log_activity,
    now_ir, client_ip, is_device_allowed, record_traffic,
    is_domain_blocked,
)

RELAY_BUF = 512 * 1024   # 512 KB
IDLE_TIMEOUT = 180        # ثانیه — بدون هیچ بایت ردوبدل


async def parse_vless_header(chunk: bytes):
    if len(chunk) < 24:
        raise ValueError("chunk too small for VLESS header")
    pos = 1           # نسخه (بایت ۰)
    pos += 16         # UUID
    addon_len = chunk[pos]
    pos += 1 + addon_len
    command = chunk[pos]; pos += 1
    port = int.from_bytes(chunk[pos:pos + 2], "big"); pos += 2
    addr_type = chunk[pos]; pos += 1

    if addr_type == 1:    # IPv4
        address = ".".join(str(b) for b in chunk[pos:pos + 4]); pos += 4
    elif addr_type == 2:  # دامنه
        dlen = chunk[pos]; pos += 1
        address = chunk[pos:pos + dlen].decode("utf-8", errors="ignore"); pos += dlen
    elif addr_type == 3:  # IPv6
        ab = chunk[pos:pos + 16]; pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown VLESS addr type: {addr_type}")

    return command, address, port, chunk[pos:]


# ── پروتکل Trojan ──────────────────────────────────────────────────────────
def trojan_expected_hex(uuid: str) -> str:
    return hashlib.sha224(uuid.encode()).hexdigest()


async def parse_trojan_header(chunk: bytes, expected_hex: str):
    min_len = 56 + 2 + 1 + 1 + 2 + 2
    if len(chunk) < min_len:
        raise ValueError("chunk too small for Trojan header")
    if chunk[:56].decode("ascii", errors="ignore") != expected_hex:
        raise ValueError("bad trojan password")
    pos = 56 + 2  # ۵۶ هگز + CRLF
    _cmd = chunk[pos]; pos += 1
    atyp = chunk[pos]; pos += 1

    if atyp == 1:
        address = ".".join(str(b) for b in chunk[pos:pos + 4]); pos += 4
    elif atyp == 3:
        dlen = chunk[pos]; pos += 1
        address = chunk[pos:pos + dlen].decode("utf-8", errors="ignore"); pos += dlen
    elif atyp == 4:
        ab = chunk[pos:pos + 16]; pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown Trojan atyp: {atyp}")

    port = int.from_bytes(chunk[pos:pos + 2], "big"); pos += 2
    pos += 2  # CRLF پایانی
    return address, port, chunk[pos:]


# ── کوتا / مصرف ────────────────────────────────────────────────────────────
async def check_and_use(uid: str, n: int) -> bool:
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if link is None:
            return False
        if not is_link_allowed(link):
            return False
        link["used_bytes"] += n
        stats["total_bytes"] += n
        hourly_traffic[now_ir().strftime("%H:00")] += n
        record_traffic(uid, n)
    return True


# ── تیون سوکت ────────────────────────────────────────────────────────────
def _tune_socket(writer: asyncio.StreamWriter):
    sock = writer.transport.get_extra_info("socket")
    if not sock:
        return
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2 * 1024 * 1024)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 * 1024 * 1024)
        if hasattr(socket, "TCP_QUICKACK"):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
    except OSError:
        pass


# ─ـ رله دوطرفه ───────────────────────────────────────────────────────────
async def relay_ws_to_tcp(
    ws: WebSocket, writer: asyncio.StreamWriter, conn_id: str, uid: str,
):
    try:
        while True:
            try:
                msg = await asyncio.wait_for(ws.receive(), timeout=IDLE_TIMEOUT)
            except asyncio.TimeoutError:
                logger.info("⏱ WS [%s] idle timeout", conn_id)
                break
            if msg["type"] == "websocket.disconnect":
                break
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue
            if not await check_and_use(uid, len(data)):
                await ws.close(code=1008, reason="quota")
                break
            stats["total_requests"] += 1
            connections[conn_id]["bytes"] += len(data)
            writer.write(data)
            if writer.transport.get_write_buffer_size() > RELAY_BUF:
                await writer.drain()
    except (WebSocketDisconnect, Exception):
        pass
    finally:
        try:
            writer.write_eof()
        except Exception:
            pass


async def relay_tcp_to_ws(
    ws: WebSocket, reader: asyncio.StreamReader,
    conn_id: str, uid: str, reply_prefix: bytes = b"\x00\x00",
):
    first = True
    try:
        while True:
            try:
                data = await asyncio.wait_for(reader.read(RELAY_BUF), timeout=IDLE_TIMEOUT)
            except asyncio.TimeoutError:
                logger.info("⏱ TCP [%s] idle timeout", conn_id)
                break
            if not data:
                break
            if not await check_and_use(uid, len(data)):
                await ws.close(code=1008, reason="quota")
                break
            connections[conn_id]["bytes"] += len(data)
            payload = (reply_prefix + data) if (first and reply_prefix) else data
            first = False
            await ws.send_bytes(payload)
    except Exception:
        pass


# ── نقطه‌ی ورودی اصلی ────────────────────────────────────────────────────
async def websocket_tunnel(ws: WebSocket, uuid: str):
    await ws.accept()

    async with LINKS_LOCK:
        link = LINKS.get(uuid)

    if not is_link_allowed(link):
        await ws.close(code=1000)
        return

    ip = client_ip(ws)

    if not is_device_allowed(uuid, ip):
        logger.warning("🚫 WS rejected uuid=%s… (device limit, ip=%s)", uuid[:8], ip)
        log_activity("connection", f"رد شد: سقف دستگاه از {ip}", "warn")
        await ws.close(code=1000)
        return

    conn_id = secrets.token_urlsafe(6)
    connections[conn_id] = {
        "uuid": uuid, "ip": ip,
        "transport": "vless-ws",
        "connected_at": datetime.now().isoformat(),
        "bytes": 0,
    }
    logger.info("✅ WS [%s] uuid=%s… ip=%s total=%d", conn_id, uuid[:8], ip, len(connections))
    log_activity("connection", f"اتصال جدید از {ip} ({link.get('label', '?')})", "info")
    writer = None

    try:
        first_msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        # تشخیص پروتکل از روی بایت‌ها
        expected_hex = trojan_expected_hex(uuid).encode()
        is_trojan = first_chunk[:56] == expected_hex
        connections[conn_id]["transport"] = "trojan-ws" if is_trojan else "vless-ws"

        if is_trojan:
            address, port, payload = await parse_trojan_header(first_chunk, trojan_expected_hex(uuid))
        else:
            _command, address, port, payload = await parse_vless_header(first_chunk)

        if not await check_and_use(uuid, len(first_chunk)):
            await ws.close(code=1008, reason="quota")
            return

        blocked, category = is_domain_blocked(address)
        if blocked:
            logger.info("🚫 [%s] blocked (%s): %s", conn_id, category, address)
            log_activity("connection", f"مسدود: {address} ({category})", "warn")
            await ws.close(code=1000)
            return

        stats["total_requests"] += 1
        connections[conn_id]["bytes"] += len(first_chunk)
        logger.info("➡️  [%s] → %s:%d", conn_id, address, port)

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port), timeout=10.0,
        )
        _tune_socket(writer)

        if payload:
            writer.write(payload)
            await writer.drain()

        done, pending = await asyncio.wait(
            {
                asyncio.create_task(relay_ws_to_tcp(ws, writer, conn_id, uuid)),
                asyncio.create_task(relay_tcp_to_ws(
                    ws, reader, conn_id, uuid,
                    reply_prefix=(b"" if is_trojan else b"\x00\x00"),
                )),
            },
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass

        try:
            await ws.close()
        except Exception:
            pass

        asyncio.create_task(save_state())

    except WebSocketDisconnect:
        pass
    except asyncio.TimeoutError:
        stats["total_errors"] += 1
        error_logs.append({"error": "connection timeout", "time": datetime.now().isoformat()})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
        logger.error("WS error [%s]: %s", conn_id, exc)
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        connections.pop(conn_id, None)
        logger.info("🔌 WS closed [%s] total=%d", conn_id, len(connections))
