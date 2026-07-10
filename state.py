# state.py — تیم آزادی Gateway v10.0
import asyncio
import ipaddress
import json
import os
import hashlib
import hmac
import secrets
import time
import aiofiles
import logging
from datetime import datetime, timedelta
from urllib.parse import urlparse
from zoneinfo import ZoneInfo
from collections import deque, defaultdict
from pathlib import Path
from fastapi import Request, HTTPException

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("تیم-آزادی-Gateway")

IRAN_TZ = ZoneInfo("Asia/Tehran")

def _load_or_create_secret() -> str:
    env_secret = os.environ.get("SECRET_KEY")
    if env_secret:
        return env_secret
    secret_dir = Path(os.environ.get("DATA_DIR", "/data"))
    secret_file = secret_dir / ".secret_key"
    try:
        secret_dir.mkdir(parents=True, exist_ok=True)
        if secret_file.exists():
            return secret_file.read_text(encoding="utf-8").strip()
        new_secret = secrets.token_urlsafe(32)
        secret_file.write_text(new_secret, encoding="utf-8")
        return new_secret
    except Exception as e:
        # اگر اینجا افتاد یعنی /data (یا DATA_DIR) روی Railway به یک Volume دائمی وصل نیست
        # و SECRET_KEY هم در env تنظیم نشده. در این حالت این مقدار در هر ری‌استارت عوض می‌شود
        # که باعث می‌شود «لینک پیش‌فرض» تکراری ساخته شود. بهتره SECRET_KEY رو در Railway Variables ست کنی.
        print(f"[warn] could not persist secret key ({e}); using an ephemeral one — set SECRET_KEY env var to avoid this")
        return secrets.token_urlsafe(32)

CONFIG = {
    "port": int(os.environ.get("PORT", 8000)),
    "secret": _load_or_create_secret(),
    "host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"),
}

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
DATA_FILE = DATA_DIR / "rvg_state.json"
SAVE_LOCK = asyncio.Lock()

connections: dict = {}
stats = {
    "total_bytes": 0,
    "total_requests": 0,
    "total_errors": 0,
    "start_time": time.time(),
}
error_logs: deque = deque(maxlen=50)
activity_logs: deque = deque(maxlen=200)
hourly_traffic: dict = defaultdict(int)
daily_traffic: dict = defaultdict(int)
link_daily_traffic: dict = defaultdict(lambda: defaultdict(int))

LINKS: dict = {}
LINKS_LOCK = asyncio.Lock()

SUBS: dict = {}
SUBS_LOCK = asyncio.Lock()

TELEGRAM_SETTINGS = {
    "enabled": False,
    "bot_token": "",
    "chat_id": "",
    "notify_quota_pct": 90,
    "notify_expiry_hours": 24,
    "api_ip": "",
    "bot_username": "",
}

JOIN_SETTINGS = {
    "enabled": True,
    "channel_username": "TimAzadi",
    "channel_required": True,
    "grant_gb": 100,
    "grant_days": 0,
    "max_devices": 1,
    "bot_username": "",
}
USER_LINKS: dict = {}

PUBLIC_SETTINGS = {
    "allow_public_create": True,
    "allow_public_delete": True,
    "allow_public_toggle": True,
}

def record_traffic(uid: str, n: int):
    day_key = now_ir().strftime("%Y-%m-%d")
    daily_traffic[day_key] += n
    link_daily_traffic[uid][day_key] += n

PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up", "xhttp-stream-one", "trojan-ws")
DEFAULT_PROTOCOL = "vless-ws"

def log_activity(kind: str, message: str, level: str = "info"):
    activity_logs.append({
        "kind": kind,
        "level": level,
        "message": message,
        "time": datetime.now().isoformat(),
    })

SESSION_COOKIE = "rvg_session"
SESSION_TTL = 60 * 60 * 24 * 7
PBKDF2_ITERATIONS = 260_000

def hash_password(pw: str, salt: bytes | None = None) -> str:
    if salt is None:
        salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2${PBKDF2_ITERATIONS}${salt.hex()}${dk.hex()}"

def _hash_password_legacy(pw: str) -> str:
    return hashlib.sha256(f"{pw}{CONFIG['secret']}".encode()).hexdigest()

def verify_password(pw: str, stored: str | None) -> bool:
    if not stored:
        return False
    if stored.startswith("pbkdf2$"):
        try:
            _, iters_s, salt_hex, hash_hex = stored.split("$")
            salt = bytes.fromhex(salt_hex)
            dk = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), salt, int(iters_s))
            return hmac.compare_digest(dk.hex(), hash_hex)
        except Exception:
            return False
    return hmac.compare_digest(_hash_password_legacy(pw), stored)

def is_legacy_hash(stored: str | None) -> bool:
    return bool(stored) and not stored.startswith("pbkdf2$")

AUTH = {"password_hash": hash_password(os.environ.get("ADMIN_PASSWORD", "TimAzadi"))}

SESSIONS: dict = {}
SESSIONS_LOCK = asyncio.Lock()

LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300
LOGIN_ATTEMPTS: dict = defaultdict(deque)
LOGIN_RATE_LOCK = asyncio.Lock()

async def check_login_rate_limit(ip: str) -> bool:
    now = time.time()
    async with LOGIN_RATE_LOCK:
        dq = LOGIN_ATTEMPTS[ip]
        while dq and now - dq[0] > LOGIN_WINDOW_SECONDS:
            dq.popleft()
        return len(dq) < LOGIN_MAX_ATTEMPTS

async def record_login_attempt(ip: str):
    async with LOGIN_RATE_LOCK:
        LOGIN_ATTEMPTS[ip].append(time.time())

async def create_session() -> str:
    token = secrets.token_urlsafe(32)
    async with SESSIONS_LOCK:
        SESSIONS[token] = time.time() + SESSION_TTL
    return token

async def is_valid_session(token: str | None) -> bool:
    if not token:
        return False
    async with SESSIONS_LOCK:
        exp = SESSIONS.get(token)
        if exp is None:
            return False
        if exp < time.time():
            SESSIONS.pop(token, None)
            return False
        return True

async def destroy_session(token: str | None):
    if not token:
        return
    async with SESSIONS_LOCK:
        SESSIONS.pop(token, None)

async def require_auth(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        raise HTTPException(status_code=401, detail="unauthorized")
    return token

async def load_state():
    global LINKS, AUTH, SUBS, USER_LINKS, JOIN_SETTINGS, PUBLIC_SETTINGS
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if DATA_FILE.exists():
            async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = await f.read()
            data = json.loads(raw)
            LINKS.update(data.get("links", {}))
            SUBS.update(data.get("subs", {}))
            if "password_hash" in data:
                AUTH["password_hash"] = data["password_hash"]
            if "telegram_settings" in data:
                TELEGRAM_SETTINGS.update(data["telegram_settings"])
            if "join_settings" in data:
                JOIN_SETTINGS.update(data["join_settings"])
            if "user_links" in data:
                loaded_ul = data["user_links"]
                fixed_ul = {}
                for uid_key, val in loaded_ul.items():
                    fixed_ul[uid_key] = val[-1] if isinstance(val, list) and val else val
                USER_LINKS.update(fixed_ul)
            if "public_settings" in data:
                PUBLIC_SETTINGS.update(data["public_settings"])
            logger.info(f"State loaded: {len(LINKS)} links, {len(SUBS)} subs")
    except Exception as e:
        logger.warning(f"Could not load state: {e}")

async def save_state():
    async with SAVE_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = {
                "links": dict(LINKS),
                "subs": dict(SUBS),
                "password_hash": AUTH["password_hash"],
                "telegram_settings": TELEGRAM_SETTINGS,
                "join_settings": JOIN_SETTINGS,
                "user_links": USER_LINKS,
                "public_settings": dict(PUBLIC_SETTINGS),
                "saved_at": datetime.now().isoformat(),
            }
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning(f"Could not save state: {e}")

def get_host() -> str:
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])

def get_extra_hosts() -> list[str]:
    """
    دامنه‌های پشتیبان اضافی (مثلاً چند دامنه‌ی دیگر Railway یا دامنه‌ی شخصی که به همین
    سرویس اشاره می‌کنند). با EXTRA_DOMAINS در Railway Variables تنظیم می‌شود، جدا شده با
    کاما، مثلاً: EXTRA_DOMAINS=backup1.up.railway.app,backup2.up.railway.app
    هدف: اگر یک دامنه فیلتر/بلاک شد، کاربر همین الان در همون ساب‌اسکریپشن یک سرور
    جایگزین دارد و منتظر آپدیت دستی نمی‌ماند.
    """
    raw = os.environ.get("EXTRA_DOMAINS", "").strip()
    if not raw:
        return []
    primary = get_host()
    seen, out = set(), []
    for h in raw.split(","):
        h = h.strip()
        if h and h != primary and h not in seen:
            seen.add(h)
            out.append(h)
    return out

def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"

def now_ir() -> datetime:
    return datetime.now(IRAN_TZ)

def generate_vless_link(uuid: str, host: str, remark: str = "تیم-آزادی", protocol: str = DEFAULT_PROTOCOL) -> str:
    from urllib.parse import quote
    if protocol == "trojan-ws":
        path = f"/ws/{uuid}"
        params = {
            "security": "tls",
            "type": "ws",
            "host": host,
            "path": path,
            "sni": host,
            "fp": "chrome",
            "alpn": "http/1.1",
        }
        query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
        return f"trojan://{uuid}@{host}:443?{query}#{quote(remark)}"
    if protocol == "vless-ws":
        path = f"/ws/{uuid}"
        params = {
            "encryption": "none",
            "security": "tls",
            "type": "ws",
            "host": host,
            "path": path,
            "sni": host,
            "fp": "chrome",
            "alpn": "http/1.1",
        }
    else:
        mode = protocol.replace("xhttp-", "")
        path = f"/xhttp-siz10/{mode}/{uuid}"
        params = {
            "encryption": "none",
            "security": "tls",
            "type": "xhttp",
            "mode": mode,
            "host": host,
            "path": path,
            "sni": host,
            "fp": "chrome",
            "alpn": "h2,http/1.1",
        }
    query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    return f"vless://{uuid}@{host}:443?{query}#{quote(remark)}"

def uptime() -> str:
    secs = int(time.time() - stats["start_time"])
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def fmt_bytes(b: int) -> str:
    if b < 1024:
        return f"{b} B"
    if b < 1024**2:
        return f"{b/1024:.1f} KB"
    if b < 1024**3:
        return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

ACTIVE_PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up", "xhttp-stream-one", "trojan-ws")
_PROTOCOL_TAG = {
    "vless-ws": "WS", "xhttp-packet-up": "XHTTP-P", "xhttp-stream-up": "XHTTP-S",
    "xhttp-stream-one": "XHTTP-S1", "trojan-ws": "TROJAN",
}

def quota_suffix(used_bytes: int, limit_bytes: int) -> str:
    used = fmt_bytes(used_bytes).replace(" ", "")
    limit = "∞" if not limit_bytes else fmt_bytes(limit_bytes).replace(" ", "")
    return f"{used}/{limit}"

def generate_all_vless_links(uuid: str, host: str, label: str, used_bytes: int = 0, limit_bytes: int = 0, brand: bool = True, flag: str = "") -> list[dict]:
    quota = quota_suffix(used_bytes, limit_bytes)
    prefix = "تیم-آزادی-" if brand else ""
    flag_prefix = f"{flag}-" if flag else ""
    hosts = [host] + get_extra_hosts()
    out = []
    for idx, h in enumerate(hosts):
        # به دامنه‌های پشتیبان یک برچسب می‌زنیم تا کاربر توی لیست سرورهای اپ کلاینتش
        # بفهمه این‌ها جایگزین همدیگه‌ان، نه کانفیگ‌های جدا
        backup_tag = "" if idx == 0 else f"-پشتیبان{idx}"
        for proto in ACTIVE_PROTOCOLS:
            remark = f"{flag_prefix}{prefix}{label}-{_PROTOCOL_TAG[proto]}{backup_tag}-{quota}"
            out.append({
                "protocol": proto,
                "host": h,
                "is_backup": idx > 0,
                "vless_link": generate_vless_link(uuid, h, remark=remark, protocol=proto),
            })
    return out

def parse_size_to_bytes(value: float, unit: str) -> int:
    unit = unit.upper()
    if unit == "GB":
        return int(value * 1024 ** 3)
    if unit == "MB":
        return int(value * 1024 ** 2)
    if unit == "KB":
        return int(value * 1024)
    return int(value)

def parse_expiry_to_timedelta(value: float, unit: str):
    from datetime import timedelta as _td
    unit = (unit or "days").lower()
    if value is None or value <= 0:
        return None
    if unit in ("hour", "hours", "h", "ساعت"):
        return _td(hours=value)
    if unit in ("day", "days", "d", "روز"):
        return _td(days=value)
    if unit in ("minute", "minutes", "m", "دقیقه"):
        return _td(minutes=value)
    return _td(days=value)

def is_link_expired(link: dict) -> bool:
    exp = link.get("expires_at")
    if not exp:
        return False
    try:
        return datetime.now() > datetime.fromisoformat(exp)
    except Exception:
        return False

def is_link_allowed(link: dict | None) -> bool:
    if link is None:
        return False
    if not link.get("active", True):
        return False
    if is_link_expired(link):
        return False
    lb = link.get("limit_bytes", 0)
    if lb > 0 and link.get("used_bytes", 0) >= lb:
        return False
    sub_id = link.get("sub_id")
    if sub_id:
        sub = SUBS.get(sub_id)
        if sub and sub.get("locked"):
            return False
    return True

def is_device_allowed(uid: str, ip: str) -> bool:
    link = LINKS.get(uid)
    if not link:
        return False
    max_devices = int(link.get("max_devices") or 0)
    if max_devices <= 0:
        return True
    current_ips = {c.get("ip") for c in connections.values() if c.get("uuid") == uid}
    if ip in current_ips:
        return True
    return len(current_ips) < max_devices

def sub_permissions(sub_id: str | None) -> dict:
    if not sub_id:
        return {"client_can_delete": True, "client_can_disable": True}
    sub = SUBS.get(sub_id)
    if not sub:
        return {"client_can_delete": True, "client_can_disable": True}
    return {
        "client_can_delete": sub.get("client_can_delete", True),
        "client_can_disable": sub.get("client_can_disable", True),
    }

def client_ip(conn) -> str:
    fwd = conn.headers.get("x-forwarded-for")
    if fwd:
        parts = [p.strip() for p in fwd.split(",") if p.strip()]
        if parts:
            return parts[-1]
    real_ip = conn.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    client = getattr(conn, "client", None)
    return client.host if client else "نامشخص"

_BLOCKED_PROXY_HOSTNAMES = {
    "metadata.google.internal", "metadata", "metadata.azure.com",
    "instance-data", "localhost",
}

def _is_blocked_ip(ip: ipaddress._BaseAddress) -> bool:
    # آدرس‌های IPv4-mapped داخل IPv6 (مثل ::ffff:127.0.0.1) را هم باز کن و چک کن،
    # وگرنه یک راه دور زدن ساده برای SSRF به آدرس‌های داخلی باقی می‌ماند.
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        ip = ip.ipv4_mapped
    return (
        ip.is_private or ip.is_loopback or ip.is_link_local or
        ip.is_reserved or ip.is_multicast or ip.is_unspecified
    )

async def is_blocked_proxy_target(url: str) -> bool:
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return True
    if not host:
        return True
    if host in _BLOCKED_PROXY_HOSTNAMES:
        return True
    try:
        ip = ipaddress.ip_address(host)
        return _is_blocked_ip(ip)
    except ValueError:
        pass
    try:
        loop = asyncio.get_event_loop()
        infos = await loop.getaddrinfo(host, None)
        for info in infos:
            addr = info[4][0]
            try:
                if _is_blocked_ip(ipaddress.ip_address(addr)):
                    return True
            except ValueError:
                continue
        return False
    except Exception:
        return True

_default_link_created = False

async def ensure_default_link():
    global _default_link_created
    if _default_link_created:
        return
    async with LINKS_LOCK:
        if not any(l.get("is_default") for l in LINKS.values()):
            uid = hashlib.sha256(f"default{CONFIG['secret']}".encode()).hexdigest()
            uid = f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"
            if uid not in LINKS:
                LINKS[uid] = {
                    "label": "لینک پیش‌فرض",
                    "limit_bytes": 0,
                    "used_bytes": 0,
                    "created_at": datetime.now().isoformat(),
                    "active": True,
                    "expires_at": None,
                    "note": "",
                    "is_default": True,
                    "sub_id": None,
                    "protocol": DEFAULT_PROTOCOL,
                    "parent_id": None,
                    "white_label": False,
                    "flag": "🇺🇸",
                }
                asyncio.create_task(save_state())
    _default_link_created = True

def get_join_settings() -> dict:
    return dict(JOIN_SETTINGS)

def update_join_settings(data: dict):
    for key, value in data.items():
        if key in JOIN_SETTINGS:
            if isinstance(JOIN_SETTINGS[key], bool):
                JOIN_SETTINGS[key] = bool(value)
            elif isinstance(JOIN_SETTINGS[key], int):
                JOIN_SETTINGS[key] = int(value)
            else:
                JOIN_SETTINGS[key] = str(value).strip()

async def check_channel_membership(user_id: str, bot_token: str | None = None) -> bool:
    if not JOIN_SETTINGS.get("channel_required", True):
        return True
    token = bot_token or TELEGRAM_SETTINGS.get("bot_token", "")
    channel = JOIN_SETTINGS.get("channel_username", "TimAzadi").strip().lstrip("@")
    if not token:
        logger.warning("check_channel_membership: هیچ bot_token ای در دسترس نیست")
        return False
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            url = f"https://api.telegram.org/bot{token}/getChatMember"
            resp = await client.post(url, json={
                "chat_id": f"@{channel}",
                "user_id": int(user_id)
            }, timeout=10.0)
            data = resp.json()
            if data.get("ok"):
                status = data.get("result", {}).get("status")
                return status in ("member", "administrator", "creator")
            return False
    except Exception as e:
        logger.warning(f"check_channel_membership error: {e}")
        return False

async def create_join_link(user_id: str, label: str = None) -> str | None:
    if not JOIN_SETTINGS.get("enabled", True):
        return None
    existing = USER_LINKS.get(user_id)
    if existing and existing in LINKS:
        return existing
    uid = generate_uuid()
    grant_gb = JOIN_SETTINGS.get("grant_gb", 100)
    grant_days = JOIN_SETTINGS.get("grant_days", 0)
    limit_bytes = int(grant_gb * 1024 * 1024 * 1024)
    expires_at = None
    if grant_days and grant_days > 0:
        expires_at = (datetime.now() + timedelta(days=grant_days)).isoformat()
    async with LINKS_LOCK:
        LINKS[uid] = {
            "label": label or f"کاربر-{user_id[:8]}",
            "limit_bytes": limit_bytes,
            "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "expires_at": expires_at,
            "note": f"ساخته‌شده هنگام ورود به بات - کاربر {user_id}",
            "is_default": False,
            "sub_id": None,
            "protocol": DEFAULT_PROTOCOL,
            "parent_id": None,
            "white_label": False,
            "flag": "🇺🇸",
            "max_devices": JOIN_SETTINGS.get("max_devices", 1),
            "quota_notified": False,
            "expiry_notified": False,
            "join_user": user_id,
            "disabled_by_leave": False,
        }
        USER_LINKS[user_id] = uid
    await save_state()
    return uid
