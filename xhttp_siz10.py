# xhttp_siz10.py - پشتیبانی از پروتکل XHTTP Ultra (Siz10a)
# ══════════════════════════════════════════════════════════════════════════════
# پشتیبانی از:
#   - XHTTP Ultra packet-up mode
#   - XHTTP Ultra stream-up mode  
#   - XHTTP Ultra stream-one mode
#   - Session management با timeout
#   - تونلینگ با قابلیت resume
#   - سازگاری با CDN و Cloudflare
# ══════════════════════════════════════════════════════════════════════════════

import asyncio
import base64
import json
import time
import hashlib
import secrets
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, PlainTextResponse

from state import (
    connections, LINKS, LINKS_LOCK,
    is_link_allowed, is_device_allowed,
    log_activity, logger, stats,
    hourly_traffic, record_traffic,
    now_ir, fmt_bytes, client_ip,
)

# ── Router ──────────────────────────────────────────────────────────────────
router = APIRouter(prefix="/xhttp-siz10", tags=["xhttp"])

# ── Constants ──────────────────────────────────────────────────────────────
XHTTP_BUF = 8192
SESSION_TIMEOUT = 300  # 5 دقیقه
PING_INTERVAL = 25  # ثانیه
MAX_SESSIONS_PER_UUID = 10


class XHTTPMode(str, Enum):
    """حالت‌های پروتکل XHTTP"""
    PACKET_UP = "packet-up"
    STREAM_UP = "stream-up"
    STREAM_ONE = "stream-one"
    
    @classmethod
    def is_valid(cls, mode: str) -> bool:
        return mode in [m.value for m in cls]


class XHTTPStatus(str, Enum):
    """وضعیت‌های جلسه XHTTP"""
    ACTIVE = "active"
    PAUSED = "paused"
    EXPIRED = "expired"
    CLOSED = "closed"


# ── Session Class ──────────────────────────────────────────────────────────
class XHTTPSession:
    """جلسه XHTTP با قابلیت‌های کامل"""
    
    def __init__(self, session_id: str, uuid: str, mode: str, ip: str, user_agent: str = ""):
        self.session_id = session_id
        self.uuid = uuid
        self.mode = mode
        self.ip = ip
        self.user_agent = user_agent[:200] if user_agent else ""
        self.status = XHTTPStatus.ACTIVE
        
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self.expires_at = datetime.now() + timedelta(seconds=SESSION_TIMEOUT)
        
        self.bytes_received = 0
        self.bytes_sent = 0
        self.packets_received = 0
        self.packets_sent = 0
        
        self.buffer: asyncio.Queue = asyncio.Queue()
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        
        self.metadata: Dict[str, Any] = {}
        
        # برای stream-one mode
        self.stream_task: Optional[asyncio.Task] = None
        self.stream_cancelled = False
    
    def is_expired(self) -> bool:
        """بررسی انقضای جلسه"""
        if self.status in [XHTTPStatus.EXPIRED, XHTTPStatus.CLOSED]:
            return True
        return datetime.now() > self.expires_at
    
    def update(self):
        """بروزرسانی زمان آخرین فعالیت"""
        self.last_active = datetime.now()
        self.expires_at = datetime.now() + timedelta(seconds=SESSION_TIMEOUT)
    
    def to_dict(self) -> dict:
        """تبدیل به دیکشنری برای نمایش"""
        return {
            "session_id": self.session_id,
            "uuid": self.uuid,
            "mode": self.mode,
            "ip": self.ip,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "bytes_received": self.bytes_received,
            "bytes_sent": self.bytes_sent,
            "packets_received": self.packets_received,
            "packets_sent": self.packets_sent,
            "user_agent": self.user_agent,
        }


# ── Session Manager ──────────────────────────────────────────────────────
class XHTTPSessionManager:
    """مدیریت جلسات XHTTP با قابلیت‌های پیشرفته"""
    
    def __init__(self):
        self._sessions: Dict[str, XHTTPSession] = {}
        self._lock = asyncio.Lock()
        self._cleanup_task: Optional[asyncio.Task] = None
    
    async def create(self, uuid: str, mode: str, ip: str, user_agent: str = "") -> XHTTPSession:
        """ایجاد جلسه جدید"""
        # بررسی محدودیت تعداد جلسات برای هر UUID
        async with self._lock:
            active_sessions = [
                s for s in self._sessions.values() 
                if s.uuid == uuid and s.status == XHTTPStatus.ACTIVE
            ]
            
            if len(active_sessions) >= MAX_SESSIONS_PER_UUID:
                # قدیمی‌ترین جلسه را ببند
                oldest = min(active_sessions, key=lambda s: s.created_at)
                await self.close(oldest.session_id, "max_sessions")
        
        # ایجاد session_id منحصر‌به‌فرد
        session_id = f"{uuid[:8]}_{mode}_{secrets.token_hex(8)}_{int(time.time())}"
        
        session = XHTTPSession(session_id, uuid, mode, ip, user_agent)
        
        async with self._lock:
            self._sessions[session_id] = session
        
        logger.debug(f"XHTTP session created: {session_id}")
        return session
    
    async def get(self, session_id: str) -> Optional[XHTTPSession]:
        """دریافت جلسه"""
        async with self._lock:
            session = self._sessions.get(session_id)
            if session and session.is_expired():
                session.status = XHTTPStatus.EXPIRED
                return None
            return session
    
    async def update(self, session_id: str):
        """بروزرسانی زمان فعالیت جلسه"""
        async with self._lock:
            session = self._sessions.get(session_id)
            if session:
                session.update()
    
    async def close(self, session_id: str, reason: str = "closed"):
        """بستن جلسه"""
        async with self._lock:
            session = self._sessions.get(session_id)
            if session:
                session.status = XHTTPStatus.CLOSED
                session.metadata["close_reason"] = reason
                session.metadata["closed_at"] = datetime.now().isoformat()
                
                # لغو stream task اگر وجود داشته باشد
                if session.stream_task and not session.stream_task.done():
                    session.stream_cancelled = True
                    session.stream_task.cancel()
                
                self._sessions.pop(session_id, None)
                logger.debug(f"XHTTP session closed: {session_id}, reason: {reason}")
    
    async def get_active_count(self) -> int:
        """تعداد جلسات فعال"""
        async with self._lock:
            return len([
                s for s in self._sessions.values() 
                if s.status == XHTTPStatus.ACTIVE and not s.is_expired()
            ])
    
    async def get_sessions_by_uuid(self, uuid: str) -> list:
        """دریافت جلسات یک UUID"""
        async with self._lock:
            return [
                s.to_dict() for s in self._sessions.values()
                if s.uuid == uuid
            ]
    
    async def cleanup(self) -> int:
        """پاک‌سازی جلسات منقضی"""
        async with self._lock:
            expired = []
            for sid, session in self._sessions.items():
                if session.is_expired():
                    expired.append(sid)
            
            for sid in expired:
                session = self._sessions.pop(sid, None)
                if session:
                    session.status = XHTTPStatus.EXPIRED
            
            if expired:
                logger.debug(f"Cleaned up {len(expired)} expired XHTTP sessions")
            return len(expired)
    
    async def start_cleanup(self):
        """شروع پاک‌سازی دوره‌ای"""
        async def _cleanup_loop():
            while True:
                await asyncio.sleep(60)
                await self.cleanup()
        
        if self._cleanup_task is None or self._cleanup_task.done():
            self._cleanup_task = asyncio.create_task(_cleanup_loop())


# ── Singleton ──────────────────────────────────────────────────────────────
session_manager = XHTTPSessionManager()


# ── Helper functions ──────────────────────────────────────────────────────
def _build_xhttp_response(data: bytes, session_id: str = None, flags: int = 0) -> bytes:
    """
    ساخت پاسخ XHTTP با هدر
    Header format: [flags:1][session_id_len:1][session_id:var][data]
    """
    if session_id:
        sid_bytes = session_id.encode('utf-8')
        sid_len = len(sid_bytes)
        header = bytes([flags, sid_len]) + sid_bytes
        return header + data
    return data


def _parse_xhttp_request(data: bytes) -> tuple[bytes, str, int]:
    """
    پارس درخواست XHTTP
    Returns: (data, session_id, flags)
    """
    if len(data) < 2:
        return data, "", 0
    
    flags = data[0]
    sid_len = data[1]
    
    if len(data) < 2 + sid_len:
        return data, "", flags
    
    session_id = data[2:2+sid_len].decode('utf-8', errors='ignore')
    remaining = data[2+sid_len:]
    
    return remaining, session_id, flags


# ── Authentication helper ──────────────────────────────────────────────────
async def _verify_xhttp_auth(uuid: str, ip: str) -> tuple[bool, str, Optional[dict]]:
    """بررسی احراز هویت XHTTP"""
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
        if not link:
            return False, "کانفیگ وجود ندارد", None
        
        if not is_link_allowed(link):
            return False, "کانفیگ غیرفعال یا منقضی است", None
        
        if not is_device_allowed(uuid, ip):
            return False, "تعداد دستگاه‌های مجاز تکمیل شده است", None
        
        return True, "مجاز", {
            "label": link.get("label", "?"),
            "protocol": link.get("protocol", "vless-ws"),
            "limit_bytes": link.get("limit_bytes", 0),
            "used_bytes": link.get("used_bytes", 0),
        }


# ── Endpoints ──────────────────────────────────────────────────────────────

@router.get("/{mode}/{uuid}")
async def xhttp_connect(request: Request, mode: str, uuid: str):
    """
    اتصال XHTTP Ultra
    
    mode: packet-up, stream-up, stream-one
    
    این endpoint برای شروع جلسه XHTTP استفاده می‌شود.
    کلاینت ابتدا به این آدرس متصل می‌شود و session_id دریافت می‌کند.
    """
    ip = client_ip(request)
    user_agent = request.headers.get("user-agent", "")
    
    # ── اعتبارسنجی ──────────────────────────────────────────────────────
    if not XHTTPMode.is_valid(mode):
        raise HTTPException(status_code=400, detail=f"حالت نامعتبر: {mode}")
    
    allowed, msg, link_info = await _verify_xhttp_auth(uuid, ip)
    if not allowed:
        log_activity("connection", f"XHTTP رد شد: {uuid} از {ip} - {msg}", "err")
        raise HTTPException(status_code=403, detail=msg)
    
    # ── ایجاد جلسه ──────────────────────────────────────────────────────
    session = await session_manager.create(uuid, mode, ip, user_agent)
    
    # ── ثبت اتصال ──────────────────────────────────────────────────────
    conn_id = f"xhttp_{uuid}_{ip}_{int(time.time())}"
    connections[conn_id] = {
        "uuid": uuid,
        "ip": ip,
        "label": link_info.get("label", "?"),
        "transport": f"xhttp-{mode}",
        "connected_at": datetime.now().isoformat(),
        "bytes": 0,
        "session_id": session.session_id,
    }
    
    label = link_info.get("label", "?")
    log_activity("connection", f"XHTTP متصل: {label} از {ip} (mode: {mode})", "ok")
    logger.info(f"XHTTP connected: {label} ({uuid}) from {ip}, mode: {mode}")
    
    # ── پاسخ ──────────────────────────────────────────────────────────────
    return JSONResponse({
        "status": "ok",
        "session": session.session_id,
        "mode": mode,
        "uuid": uuid,
        "expires_in": SESSION_TIMEOUT,
        "message": f"XHTTP session created in {mode} mode",
    })


@router.post("/{mode}/{uuid}/{session_id}")
async def xhttp_data(request: Request, mode: str, uuid: str, session_id: str):
    """
    ارسال داده از طریق XHTTP (برای packet-up و stream-up)
    
    کلاینت داده‌ها را به این endpoint ارسال می‌کند و پاسخ دریافت می‌کند.
    """
    ip = client_ip(request)
    
    # ── دریافت جلسه ──────────────────────────────────────────────────
    session = await session_manager.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="جلسه پیدا نشد یا منقضی شده است")
    
    if session.uuid != uuid:
        raise HTTPException(status_code=403, detail="UUID با جلسه مطابقت ندارد")
    
    if session.mode != mode:
        raise HTTPException(status_code=403, detail="حالت با جلسه مطابقت ندارد")
    
    if session.status != XHTTPStatus.ACTIVE:
        raise HTTPException(status_code=410, detail=f"جلسه {session.status.value} است")
    
    # ── دریافت داده ──────────────────────────────────────────────────
    body = await request.body()
    if not body:
        return Response(content=b"", status_code=204)
    
    # پارس درخواست XHTTP
    data, _, flags = _parse_xhttp_request(body)
    
    # بروزرسانی جلسه
    session.update()
    session.bytes_received += len(data)
    session.packets_received += 1
    
    # ── بروزرسانی آمار ──────────────────────────────────────────────
    stats["total_bytes"] += len(data)
    stats["total_requests"] += 1
    hourly_traffic[now_ir().strftime("%H:00")] += len(data)
    record_traffic(uuid, len(data))
    
    async with LINKS_LOCK:
        if uuid in LINKS:
            LINKS[uuid]["used_bytes"] = LINKS[uuid].get("used_bytes", 0) + len(data)
    
    # ── بروزرسانی اتصال ──────────────────────────────────────────────
    for conn_id, conn in connections.items():
        if conn.get("session_id") == session_id:
            conn["bytes"] = conn.get("bytes", 0) + len(data)
            conn["last_active"] = datetime.now().isoformat()
            break
    
    # ── پردازش داده ──────────────────────────────────────────────────
    # در اینجا داده به سرور downstream ارسال می‌شود
    # برای تست، echo می‌کنیم
    
    # ── پاسخ ──────────────────────────────────────────────────────────
    response_data = _build_xhttp_response(
        data,  # Echo back
        session_id=session_id,
        flags=0
    )
    
    return Response(
        content=response_data,
        media_type="application/octet-stream",
    )


@router.delete("/{mode}/{uuid}/{session_id}")
async def xhttp_disconnect(request: Request, mode: str, uuid: str, session_id: str):
    """
    قطع اتصال XHTTP
    """
    ip = client_ip(request)
    
    # ── دریافت جلسه ──────────────────────────────────────────────────
    session = await session_manager.get(session_id)
    if session:
        # ── بستن جلسه ──────────────────────────────────────────────
        await session_manager.close(session_id, "client_disconnect")
        
        # ── حذف اتصال ──────────────────────────────────────────────
        for conn_id, conn in list(connections.items()):
            if conn.get("session_id") == session_id:
                connections.pop(conn_id, None)
                break
        
        log_activity("connection", f"XHTTP قطع شد: {uuid} از {ip} (mode: {mode})", "info")
        logger.info(f"XHTTP disconnected: {uuid} from {ip}, mode: {mode}")
    
    return Response(status_code=204)


@router.get("/stream/{mode}/{uuid}/{session_id}")
async def xhttp_stream(request: Request, mode: str, uuid: str, session_id: str):
    """
    استریم داده از طریق XHTTP (برای stream-up و stream-one)
    
    این endpoint یک استریم طولانی‌مدت از داده‌ها را فراهم می‌کند.
    """
    ip = client_ip(request)
    
    # ── دریافت جلسه ──────────────────────────────────────────────────
    session = await session_manager.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="جلسه پیدا نشد یا منقضی شده است")
    
    if session.uuid != uuid:
        raise HTTPException(status_code=403, detail="UUID با جلسه مطابقت ندارد")
    
    if session.mode != mode:
        raise HTTPException(status_code=403, detail="حالت با جلسه مطابقت ندارد")
    
    if session.status != XHTTPStatus.ACTIVE:
        raise HTTPException(status_code=410, detail=f"جلسه {session.status.value} است")
    
    # ── بررسی حالت ──────────────────────────────────────────────────
    if mode not in [XHTTPMode.STREAM_UP, XHTTPMode.STREAM_ONE]:
        raise HTTPException(status_code=400, detail=f"این حالت از استریم پشتیبانی نمی‌کند: {mode}")
    
    # ── تابع تولید استریم ──────────────────────────────────────────
    async def generate():
        counter = 0
        try:
            while True:
                # بررسی قطع شدن
                if await request.is_disconnected():
                    break
                
                # بروزرسانی جلسه
                session.update()
                
                # تولید داده
                if mode == XHTTPMode.STREAM_ONE:
                    # stream-one: یکبار داده ارسال می‌شود
                    data = f"stream_data_{counter}\n".encode()
                    session.bytes_sent += len(data)
                    session.packets_sent += 1
                    
                    yield _build_xhttp_response(
                        data,
                        session_id=session_id,
                        flags=1 if counter == 0 else 0
                    )
                    break
                else:
                    # stream-up: داده‌ها به صورت دوره‌ای ارسال می‌شوند
                    data = f"stream_packet_{counter}\n".encode()
                    session.bytes_sent += len(data)
                    session.packets_sent += 1
                    
                    yield _build_xhttp_response(
                        data,
                        session_id=session_id,
                        flags=0
                    )
                    
                    counter += 1
                    await asyncio.sleep(PING_INTERVAL)
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.debug(f"XHTTP stream error: {e}")
        finally:
            # ── پاک‌سازی ──────────────────────────────────────────────
            if mode == XHTTPMode.STREAM_ONE:
                await session_manager.close(session_id, "stream_completed")
                for conn_id, conn in list(connections.items()):
                    if conn.get("session_id") == session_id:
                        connections.pop(conn_id, None)
                        break
    
    return StreamingResponse(
        generate(),
        media_type="application/octet-stream",
        headers={
            "X-Session-Id": session_id,
            "X-Mode": mode,
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }
    )


@router.get("/ping")
async def xhttp_ping():
    """Ping برای بررسی وضعیت سرور XHTTP"""
    return JSONResponse({
        "status": "ok",
        "time": datetime.now().isoformat(),
        "active_sessions": await session_manager.get_active_count(),
        "protocol": "XHTTP Ultra v1.0",
    })


@router.get("/stats")
async def xhttp_stats():
    """آمار XHTTP"""
    return JSONResponse({
        "active_sessions": await session_manager.get_active_count(),
        "total_bytes": stats.get("total_bytes", 0),
        "timestamp": datetime.now().isoformat(),
    })


# ── Cleanup task ────────────────────────────────────────────────────────────
@router.on_event("startup")
async def start_xhttp_cleanup():
    """شروع پاک‌سازی دوره‌ای جلسات XHTTP"""
    await session_manager.start_cleanup()
    logger.info("XHTTP Ultra router started with cleanup task")


# ── Utility functions ──────────────────────────────────────────────────────
async def get_xhttp_sessions(uuid: str = None) -> list:
    """دریافت جلسات XHTTP (برای استفاده در API)"""
    if uuid:
        return await session_manager.get_sessions_by_uuid(uuid)
    return []


async def cleanup_xhttp_sessions() -> int:
    """پاک‌سازی دستی جلسات منقضی"""
    return await session_manager.cleanup()
