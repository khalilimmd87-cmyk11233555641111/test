# state.py — تیم آزادی Gateway v10.0 - نسخه کامل با رفرال
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
    except Exception:
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

# ═══════════════════════════════════════════════════════════════
# ✅ تنظیمات عضویت اجباری
# ═══════════════════════════════════════════════════════════════
JOIN_SETTINGS = {
    "enabled": True,
    "channel_username": "TimAzadi",
    "channel_required": True,
    "grant_gb": 100,
    "grant_days": 0,
    "max_devices": 1,
    "bot_username": "",
    "welcome_text": """🎉 خوش اومدی به تیم آزادی!

✅ کانفیگ اختصاصی برات ساخته شد.
📦 حجم: {volume}
⏰ اعتبار: {expiry}

📢 کانال ما:
https://t.me/{channel}

لینک ساب تو:
`{sub_link}`

🚀 از سرویس لذت ببر!""",
    "welcome_text_enabled": True,
}

# ═══════════════════════════════════════════════════════════════
# 🔥 تنظیمات کامل رفرال
# ═══════════════════════════════════════════════════════════════
REFERRAL_SETTINGS = {
    "enabled": True,
    "referrer_reward_gb": 50,
    "referrer_reward_money": 5000,
    "referee_reward_gb": 100,
    "referee_reward_money": 2000,
    "referee_expire_days": 30,
    "referrer_expire_days": 30,
    "min_withdraw": 10000,
    "withdraw_enabled": True,
    "withdraw_methods": ["کارت به کارت", "واریز به شماره شبا", "شارژ سیمکارت", "کیف پول دیجیتال"],
    "referral_text_enabled": True,
    "referral_text": """🎁 *سیستم رفرال تیم آزادی*

سلام دوست عزیز! 👋

با دعوت از دوستانت به تیم آزادی، هم به خودت جایزه می‌دی و هم به دوستت!

✅ *جایزه تو (رفرال‌دهنده):*
- {referrer_gb} گیگ اینترنت رایگان
- {referrer_money:,} تومان پول نقد

✅ *جایزه دوستت (رفرال‌گیرنده):*
- {referee_gb} گیگ اینترنت رایگان
- {referee_money:,} تومان پول نقد

✅ *لینک مخصوص تو:*
`{referral_link}`

هر کس با لینک تو عضو شود، هر دو جایزه می‌گیرید!
هرچقدر دوست بیشتری بیاری، جایزه‌ات بیشتر میشه!

📊 *آمار تو:*
- تعداد دعوت‌ها: {referrals_count}
- حجم دریافت‌شده: {total_volume} GB
- پول دریافت‌شده: {total_money:,} تومان
- موجودی قابل برداشت: {balance:,} تومان

🚀 *همین حالا شروع کن و درآمدزایی کن!*

📢 کانال تیم آزادی:
https://t.me/{channel}""",
    "referral_success_text": """🎉 *تبریک!*

شما یک کاربر جدید رو با لینک رفرال خودتون دعوت کردید!

👤 کاربر جدید: `{referee_id}`

🏆 *جایزه شما:*
- {referrer_gb} گیگ اینترنت
- {referrer_money:,} تومان پول نقد

📊 *موجودی جدید شما:*
{balance:,} تومان

🚀 به دعوت کردن ادامه بدید!""",
    "referee_success_text": """🎉 *تبریک!*

شما با لینک رفرال وارد شدید!

🏆 *جایزه شما:*
- {referee_gb} گیگ اینترنت
- {referee_money:,} تومان پول نقد

✅ کانفیگ اختصاصی برات ساخته شد.
لینک ساب تو:
`{sub_link}`

📢 کانال تیم آزادی:
https://t.me/{channel}""",
}

# ═══════════════════════════════════════════════════════════════
# 📊 دیتابیس کاربران
# ═══════════════════════════════════════════════════════════════
USERS: dict = {}  # user_id -> {referral_code, referrer_id, referrals_count, total_volume_gb, total_money, balance, is_banned, created_at, last_activity, withdraw_requests}
USER_LINKS: dict = {}  # user_id -> uid
USER_REFERRALS: dict = {}  # user_id -> [list of referred user_ids]
WITHDRAW_REQUESTS: dict = {}  # request_id -> {user_id, amount, method, status, created_at, processed_at}

# ═══════════════════════════════════════════════════════════════

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
    global LINKS, AUTH, SUBS, USER_LINKS, JOIN_SETTINGS, PUBLIC_SETTINGS, USERS, USER_REFERRALS, REFERRAL_SETTINGS, WITHDRAW_REQUESTS
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
            if "referral_settings" in data:
                REFERRAL_SETTINGS.update(data["referral_settings"])
            if "users" in data:
                USERS.update(data["users"])
            if "user_referrals" in data:
                USER_REFERRALS.update(data["user_referrals"])
            if "withdraw_requests" in data:
                WITHDRAW_REQUESTS.update(data["withdraw_requests"])
            if "user_links" in data:
                loaded_ul = data["user_links"]
                fixed_ul = {}
                for uid_key, val in loaded_ul.items():
                    fixed_ul[uid_key] = val[-1] if isinstance(val, list) and val else val
                USER_LINKS.update(fixed_ul)
            if "public_settings" in data:
                PUBLIC_SETTINGS.update(data["public_settings"])
            logger.info(f"State loaded: {len(LINKS)} links, {len(SUBS)} subs, {len(USERS)} users")
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
                "referral_settings": REFERRAL_SETTINGS,
                "users": dict(USERS),
                "user_referrals": dict(USER_REFERRALS),
                "withdraw_requests": dict(WITHDRAW_REQUESTS),
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

def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"

def generate_referral_code() -> str:
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    code = ''.join(secrets.choice(chars) for _ in range(6))
    while any(u.get("referral_code") == code for u in USERS.values()):
        code = ''.join(secrets.choice(chars) for _ in range(6))
    return code

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

def format_money(amount: int) -> str:
    return f"{amount:,}".replace(",", "٬")

ACTIVE_PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up", "trojan-ws")
_PROTOCOL_TAG = {"vless-ws": "WS", "xhttp-packet-up": "XHTTP-P", "xhttp-stream-up": "XHTTP-S", "trojan-ws": "TROJAN"}

def quota_suffix(used_bytes: int, limit_bytes: int) -> str:
    used = fmt_bytes(used_bytes).replace(" ", "")
    limit = "∞" if not limit_bytes else fmt_bytes(limit_bytes).replace(" ", "")
    return f"{used}/{limit}"

def generate_all_vless_links(uuid: str, host: str, label: str, used_bytes: int = 0, limit_bytes: int = 0, brand: bool = True, flag: str = "") -> list[dict]:
    quota = quota_suffix(used_bytes, limit_bytes)
    prefix = "تیم-آزادی-" if brand else ""
    flag_prefix = f"{flag}-" if flag else ""
    out = []
    for proto in ACTIVE_PROTOCOLS:
        remark = f"{flag_prefix}{prefix}{label}-{_PROTOCOL_TAG[proto]}-{quota}"
        out.append({
            "protocol": proto,
            "vless_link": generate_vless_link(uuid, host, remark=remark, protocol=proto),
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

# ═══════════════════════════════════════════════════════════════
# ✅ توابع رفرال، عضویت و مدیریت کاربران
# ═══════════════════════════════════════════════════════════════

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
                JOIN_SETTINGS[key] = str(value)

def get_referral_settings() -> dict:
    return dict(REFERRAL_SETTINGS)

def update_referral_settings(data: dict):
    for key, value in data.items():
        if key in REFERRAL_SETTINGS:
            if isinstance(REFERRAL_SETTINGS[key], bool):
                REFERRAL_SETTINGS[key] = bool(value)
            elif isinstance(REFERRAL_SETTINGS[key], int):
                REFERRAL_SETTINGS[key] = int(value)
            else:
                REFERRAL_SETTINGS[key] = str(value)

async def get_or_create_user(user_id: str, referrer_code: str = None) -> dict:
    """دریافت یا ساخت کاربر جدید با پشتیبانی از رفرال"""
    if user_id not in USERS:
        referral_code = generate_referral_code()
        USERS[user_id] = {
            "referral_code": referral_code,
            "referrer_id": None,
            "referrals_count": 0,
            "total_volume_gb": 0,
            "total_money": 0,
            "balance": 0,
            "withdraw_count": 0,
            "is_banned": False,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
        }
        
        # اگر کد رفرال داده شده، پردازش کن
        if referrer_code:
            await process_referral(user_id, referrer_code)
        
        await save_state()
    else:
        # بروزرسانی last_activity
        USERS[user_id]["last_activity"] = datetime.now().isoformat()
    
    return USERS[user_id]

async def process_referral(referee_id: str, referrer_code: str) -> dict:
    """پردازش کامل رفرال"""
    if not REFERRAL_SETTINGS.get("enabled", True):
        return {"success": False, "message": "سیستم رفرال غیرفعال است"}

    # پیدا کردن رفرال‌دهنده
    referrer_id = None
    for uid, u in USERS.items():
        if u.get("referral_code") == referrer_code:
            referrer_id = uid
            break

    if not referrer_id:
        return {"success": False, "message": "کد رفرال نامعتبر است"}

    if referrer_id == referee_id:
        return {"success": False, "message": "نمیتونی خودت رو دعوت کنی!"}

    referee = await get_or_create_user(referee_id)
    if referee.get("referrer_id"):
        return {"success": False, "message": "شما قبلاً توسط شخص دیگری دعوت شده‌اید"}

    referrer = USERS[referrer_id]
    referrer["referrals_count"] = referrer.get("referrals_count", 0) + 1
    referrer["total_volume_gb"] = referrer.get("total_volume_gb", 0) + REFERRAL_SETTINGS.get("referrer_reward_gb", 50)
    referrer["total_money"] = referrer.get("total_money", 0) + REFERRAL_SETTINGS.get("referrer_reward_money", 5000)
    referrer["balance"] = referrer.get("balance", 0) + REFERRAL_SETTINGS.get("referrer_reward_money", 5000)

    referee["referrer_id"] = referrer_id
    referee["total_volume_gb"] = referee.get("total_volume_gb", 0) + REFERRAL_SETTINGS.get("referee_reward_gb", 100)
    referee["total_money"] = referee.get("total_money", 0) + REFERRAL_SETTINGS.get("referee_reward_money", 2000)
    referee["balance"] = referee.get("balance", 0) + REFERRAL_SETTINGS.get("referee_reward_money", 2000)

    if referrer_id not in USER_REFERRALS:
        USER_REFERRALS[referrer_id] = []
    if referee_id not in USER_REFERRALS[referrer_id]:
        USER_REFERRALS[referrer_id].append(referee_id)

    # ساخت کانفیگ برای رفرال‌گیرنده
    referee_gb = REFERRAL_SETTINGS.get("referee_reward_gb", 100)
    referee_days = REFERRAL_SETTINGS.get("referee_expire_days", 30)
    uid = generate_uuid()
    limit_bytes = int(referee_gb * 1024 * 1024 * 1024)
    expires_at = (datetime.now() + timedelta(days=referee_days)).isoformat() if referee_days > 0 else None

    async with LINKS_LOCK:
        LINKS[uid] = {
            "label": f"رفرال-{referee_id[:8]}",
            "limit_bytes": limit_bytes,
            "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "expires_at": expires_at,
            "note": f"کانفیگ رفرال برای کاربر {referee_id}",
            "is_default": False,
            "sub_id": None,
            "protocol": DEFAULT_PROTOCOL,
            "parent_id": None,
            "white_label": False,
            "flag": "🇺🇸",
            "max_devices": JOIN_SETTINGS.get("max_devices", 1),
            "quota_notified": False,
            "expiry_notified": False,
            "referral_user": referee_id,
        }
        USER_LINKS[referee_id] = uid

    await save_state()
    log_activity("referral", f"کاربر {referee_id} توسط {referrer_id} دعوت شد", "ok")

    # ارسال پیام‌ها
    await send_referral_notifications(referrer_id, referee_id, uid)

    return {
        "success": True,
        "referrer_id": referrer_id,
        "referee_id": referee_id,
        "referrer_reward_gb": REFERRAL_SETTINGS.get("referrer_reward_gb", 50),
        "referrer_reward_money": REFERRAL_SETTINGS.get("referrer_reward_money", 5000),
        "referee_reward_gb": REFERRAL_SETTINGS.get("referee_reward_gb", 100),
        "referee_reward_money": REFERRAL_SETTINGS.get("referee_reward_money", 2000),
        "link_uid": uid,
    }

async def send_referral_notifications(referrer_id: str, referee_id: str, uid: str):
    """ارسال پیام‌های رفرال به هر دو طرف"""
    token = TELEGRAM_SETTINGS.get("bot_token")
    if not token:
        return

    host = get_host()
    channel = JOIN_SETTINGS.get("channel_username", "TimAzadi")
    sub_link = f"https://{host}/sub/{uid}"
    
    # پیام به رفرال‌دهنده
    referrer_text = REFERRAL_SETTINGS.get("referral_success_text", "").format(
        referee_id=referee_id[:8],
        referrer_gb=REFERRAL_SETTINGS.get("referrer_reward_gb", 50),
        referrer_money=format_money(REFERRAL_SETTINGS.get("referrer_reward_money", 5000)),
        balance=format_money(USERS.get(referrer_id, {}).get("balance", 0)),
    )
    
    # پیام به رفرال‌گیرنده
    referee_text = REFERRAL_SETTINGS.get("referee_success_text", "").format(
        referee_gb=REFERRAL_SETTINGS.get("referee_reward_gb", 100),
        referee_money=format_money(REFERRAL_SETTINGS.get("referee_reward_money", 2000)),
        sub_link=sub_link,
        channel=channel,
    )

    try:
        import httpx
        async with httpx.AsyncClient() as client:
            # ارسال به رفرال‌دهنده
            if referrer_id and referrer_id.startswith("1") or referrer_id.startswith("2"):
                await client.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={"chat_id": referrer_id, "text": referrer_text, "parse_mode": "Markdown"},
                    timeout=10
                )
            
            # ارسال به رفرال‌گیرنده
            if referee_id and referee_id.startswith("1") or referee_id.startswith("2"):
                await client.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={"chat_id": referee_id, "text": referee_text, "parse_mode": "Markdown"},
                    timeout=10
                )
    except Exception as e:
        logger.warning(f"send_referral_notifications error: {e}")

async def create_referral_link(user_id: str) -> str:
    """ساخت لینک رفرال برای کاربر"""
    host = get_host()
    bot_username = JOIN_SETTINGS.get("bot_username") or TELEGRAM_SETTINGS.get("bot_username") or "timazadi_bot"
    user = await get_or_create_user(user_id)
    return f"https://t.me/{bot_username}?start=ref_{user['referral_code']}"

async def get_user_stats(user_id: str) -> dict:
    """دریافت آمار کامل یک کاربر"""
    user = await get_or_create_user(user_id)
    referrals = USER_REFERRALS.get(user_id, [])
    referred_users = []
    for ref_id in referrals:
        if ref_id in USERS:
            referred_users.append({
                "user_id": ref_id,
                "joined_at": USERS[ref_id].get("created_at"),
                "status": "فعال" if not USERS[ref_id].get("is_banned") else "مسدود",
            })
    
    return {
        "user_id": user_id,
        "referral_code": user.get("referral_code"),
        "referrer_id": user.get("referrer_id"),
        "referrals_count": user.get("referrals_count", 0),
        "total_volume_gb": user.get("total_volume_gb", 0),
        "total_money": user.get("total_money", 0),
        "balance": user.get("balance", 0),
        "is_banned": user.get("is_banned", False),
        "created_at": user.get("created_at"),
        "last_activity": user.get("last_activity"),
        "referred_users": referred_users,
        "can_withdraw": user.get("balance", 0) >= REFERRAL_SETTINGS.get("min_withdraw", 10000) and REFERRAL_SETTINGS.get("withdraw_enabled", True),
    }

async def create_withdraw_request(user_id: str, amount: int, method: str, details: str) -> dict:
    """ایجاد درخواست برداشت"""
    if not REFERRAL_SETTINGS.get("withdraw_enabled", True):
        return {"success": False, "message": "سیستم برداشت غیرفعال است"}
    
    user = await get_or_create_user(user_id)
    min_withdraw = REFERRAL_SETTINGS.get("min_withdraw", 10000)
    
    if amount < min_withdraw:
        return {"success": False, "message": f"حداقل مبلغ برداشت {format_money(min_withdraw)} تومان است"}
    
    if user.get("balance", 0) < amount:
        return {"success": False, "message": "موجودی شما کافی نیست"}
    
    request_id = generate_uuid()[:8]
    WITHDRAW_REQUESTS[request_id] = {
        "user_id": user_id,
        "amount": amount,
        "method": method,
        "details": details,
        "status": "pending",  # pending, approved, rejected, paid
        "created_at": datetime.now().isoformat(),
        "processed_at": None,
        "note": "",
    }
    
    # کم کردن از موجودی
    USERS[user_id]["balance"] = user.get("balance", 0) - amount
    USERS[user_id]["withdraw_count"] = user.get("withdraw_count", 0) + 1
    
    await save_state()
    log_activity("withdraw", f"درخواست برداشت {format_money(amount)} تومان از کاربر {user_id}", "info")
    
    return {
        "success": True,
        "request_id": request_id,
        "amount": amount,
        "status": "pending",
        "new_balance": USERS[user_id]["balance"],
    }

async def check_channel_membership(user_id: str, bot_token: str | None = None) -> bool:
    if not JOIN_SETTINGS.get("channel_required", True):
        return True
    token = bot_token or TELEGRAM_SETTINGS.get("bot_token", "")
    channel = JOIN_SETTINGS.get("channel_username", "TimAzadi").strip().lstrip("@")
    if not token:
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
    except Exception:
        return False

async def create_join_link(user_id: str, label: str = None, is_referral: bool = False) -> str | None:
    if not JOIN_SETTINGS.get("enabled", True):
        return None
    
    existing = USER_LINKS.get(user_id)
    if existing and existing in LINKS:
        return existing

    uid = generate_uuid()
    
    if is_referral:
        grant_gb = REFERRAL_SETTINGS.get("referee_reward_gb", 100)
        grant_days = REFERRAL_SETTINGS.get("referee_expire_days", 30)
    else:
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
        }
        USER_LINKS[user_id] = uid

    await save_state()
    return uid
