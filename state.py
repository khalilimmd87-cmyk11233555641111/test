# state.py — تیم آزادی Gateway v10.0
# ══════════════════════════════════════════════════════════════════════════════
# تمام state مشترک (LINKS، SUBS، stats، connections، ...) و توابع کمکی که هم
# main.py و هم relay_vless.py و هم xhttp_siz10.py بهشون نیاز دارن، اینجا زندگی
# می‌کنن. این فایل عمداً از main.py، relay_vless.py یا xhttp_siz10.py هیچی
# ایمپورت نمی‌کنه تا حلقه‌ی وارداتی (circular import) که باعث خطای
# "cannot import name 'router' from 'xhttp_siz10'" می‌شد، دیگه پیش نیاد.
# ══════════════════════════════════════════════════════════════════════════════

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
from datetime import datetime
from urllib.parse import urlparse
from zoneinfo import ZoneInfo
from collections import deque, defaultdict
from pathlib import Path

from fastapi import Request, HTTPException

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("تیم-آزادی-Gateway")

IRAN_TZ = ZoneInfo("Asia/Tehran")

# ── Secret / Config ──────────────────────────────────────────────────────────
def _load_or_create_secret() -> str:
    """اگر SECRET_KEY در env تنظیم نشده باشد، آن را یک‌بار می‌سازد و روی دیسک
    ذخیره می‌کند تا با هر ری‌استارت سرور عوض نشود (که باعث نامعتبر شدن
    session‌ها و هش‌های وابسته به secret می‌شد)."""
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
        # اگر دیسک در دسترس نبود (مثلاً محیط فقط-خواندنی)، حداقل برای طول عمر
        # همین پردازه یک مقدار ثابت داشته باشیم.
        return secrets.token_urlsafe(32)

CONFIG = {
    "port": int(os.environ.get("PORT", 8000)),
    "secret": _load_or_create_secret(),
    "host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"),
}

# ── Persistence ───────────────────────────────────────────────────────────────
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
DATA_FILE = DATA_DIR / "rvg_state.json"
SAVE_LOCK = asyncio.Lock()

# ── In-memory state ───────────────────────────────────────────────────────────
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
LINKS: dict = {}
LINKS_LOCK = asyncio.Lock()
SUBS: dict = {}
SUBS_LOCK = asyncio.Lock()

# پروتکل‌های پشتیبانی‌شده برای هر کانفیگ
PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up", "xhttp-stream-one")
DEFAULT_PROTOCOL = "vless-ws"

def log_activity(kind: str, message: str, level: str = "info"):
    """ثبت یک رخداد در لاگ فعالیت‌ها (ساخت/حذف/ویرایش کانفیگ، ورود، و...)."""
    activity_logs.append({
        "kind": kind,
        "level": level,
        "message": message,
        "time": datetime.now().isoformat(),
    })

# ── Auth ──────────────────────────────────────────────────────────────────────
SESSION_COOKIE = "rvg_session"
SESSION_TTL = 60 * 60 * 24 * 7

# ✅ امنیت: هش رمز از SHA256 ساده (سریع و در برابر brute-force ضعیف) به
# PBKDF2-HMAC-SHA256 با salt تصادفی و ۲۶۰٬۰۰۰ round تغییر کرد. فرمت ذخیره:
#   pbkdf2$<iterations>$<salt-hex>$<hash-hex>
# سازگاری با نصب‌های قبلی حفظ شده: اگر هش ذخیره‌شده فرمت قدیمی
# (sha256(pw+secret)) باشد، verify_password آن را هم قبول می‌کند و طبق کد
# لاگین در main.py، بعد از اولین ورود موفق به‌صورت خودکار به فرمت جدید
# ارتقا (migrate) پیدا می‌کند.
PBKDF2_ITERATIONS = 260_000

def hash_password(pw: str, salt: bytes | None = None) -> str:
    if salt is None:
        salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2${PBKDF2_ITERATIONS}${salt.hex()}${dk.hex()}"

def _hash_password_legacy(pw: str) -> str:
    """فرمت قدیمی، فقط برای سازگاری با نصب‌های قبلی نگه داشته شده."""
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
    # فرمت قدیمی (legacy) — sha256(pw + secret)
    return hmac.compare_digest(_hash_password_legacy(pw), stored)

def is_legacy_hash(stored: str | None) -> bool:
    return bool(stored) and not stored.startswith("pbkdf2$")

AUTH = {"password_hash": hash_password(os.environ.get("ADMIN_PASSWORD", "TimAzadi"))}
SESSIONS: dict = {}
SESSIONS_LOCK = asyncio.Lock()

# ── Login rate limiting ───────────────────────────────────────────────────────
# ✅ امنیت: محدودیت تلاش ورود بر اساس IP، برای مقابله با brute-force روی
# رمز پنل (به‌خصوص وقتی رمز پیش‌فرض عوض نشده باشد).
LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300  # ۵ دقیقه
LOGIN_ATTEMPTS: dict = defaultdict(deque)
LOGIN_RATE_LOCK = asyncio.Lock()

async def check_login_rate_limit(ip: str) -> bool:
    """True = هنوز اجازه‌ی تلاش دارد. تلاش‌های قدیمی‌تر از پنجره‌ی زمانی پاک می‌شوند."""
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

# ── Persistence I/O ───────────────────────────────────────────────────────────
async def load_state():
    global LINKS, AUTH, SUBS
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
                "saved_at": datetime.now().isoformat(),
            }
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning(f"Could not save state: {e}")

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_host() -> str:
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])

def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"

def now_ir() -> datetime:
    return datetime.now(IRAN_TZ)

def generate_vless_link(uuid: str, host: str, remark: str = "تیم-آزادی", protocol: str = DEFAULT_PROTOCOL) -> str:
    """می‌سازد VLESS share-link متناسب با پروتکل انتخاب‌شده (WS کلاسیک یا یکی از مدهای XHTTP)."""
    from urllib.parse import quote
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
        # xhttp-packet-up / xhttp-stream-up / xhttp-stream-one
        mode = protocol.replace("xhttp-", "")  # packet-up | stream-up | stream-one
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
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    if b < 1024**3: return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

# پروتکل‌هایی که واقعاً روی این استک کار می‌کنند (xhttp-stream-one در PROTOCOLS
# نگه داشته شده برای سازگاری با نصب‌های قبلی، ولی route ندارد و همیشه 404
# می‌دهد — عمداً از باندل خودکار ساب کنار گذاشته شده تا کانفیگ خراب پخش نشود).
ACTIVE_PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up")
_PROTOCOL_TAG = {"vless-ws": "WS", "xhttp-packet-up": "XHTTP-P", "xhttp-stream-up": "XHTTP-S"}

def quota_suffix(used_bytes: int, limit_bytes: int) -> str:
    """رشته‌ی حجم دقیق برای نمایش در remark لینک/QR، مثلاً «12.3GB/100GB» یا «12.3GB/∞»."""
    used = fmt_bytes(used_bytes).replace(" ", "")
    limit = "∞" if not limit_bytes else fmt_bytes(limit_bytes).replace(" ", "")
    return f"{used}/{limit}"

def generate_all_vless_links(uuid: str, host: str, label: str, used_bytes: int = 0, limit_bytes: int = 0) -> list[dict]:
    """برای یک لینک، هر سه پروتکل کارکردی (WS + دو مد XHTTP) را با remark
    یکسان (شامل حجم دقیق مصرف/سهمیه) می‌سازد — همان چیزی که در ساب باندل
    می‌شود تا کلاینت هر سه را همزمان ببیند و اگر یکی فیلتر شد، بقیه در دسترس
    باشند."""
    quota = quota_suffix(used_bytes, limit_bytes)
    out = []
    for proto in ACTIVE_PROTOCOLS:
        remark = f"تیم‌آزادی-{label}-{_PROTOCOL_TAG[proto]}-{quota}"
        out.append({
            "protocol": proto,
            "vless_link": generate_vless_link(uuid, host, remark=remark, protocol=proto),
        })
    return out

def parse_size_to_bytes(value: float, unit: str) -> int:
    unit = unit.upper()
    if unit == "GB": return int(value * 1024 ** 3)
    if unit == "MB": return int(value * 1024 ** 2)
    if unit == "KB": return int(value * 1024)
    return int(value)

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
    return True

def client_ip(conn) -> str:
    """آی‌پی واقعی کلاینت رو با احتساب هدرهای پراکسی (Railway/Cloudflare) برمی‌گردونه.
    ✅ یکی‌سازی شد: قبلاً این منطق در main.py/state.py، relay_vless.py و
    xhttp_siz10.py سه بار جدا تکرار شده بود. هم برای fastapi.Request و هم
    برای fastapi.WebSocket کار می‌کند (هر دو .headers و .client دارند).

    🐛 باگ امنیتی رفع‌شده: قبلاً اولین مقدار X-Forwarded-For (`split(",")[0]`)
    برداشته می‌شد. در یک زنجیره‌ی X-Forwarded-For، اولین مقدار همان چیزی است
    که خودِ کلاینت (یا هر پراکسی قبلی) اعلام کرده و کاملاً قابل جعل است —
    مثلاً با curl -H "X-Forwarded-For: 1.2.3.4" هرکسی می‌توانست IP دلخواه
    نشان‌داده‌شده در داشبورد را تغییر بدهد و مهم‌تر از آن، rate-limit ورود به
    پنل (که بر اساس IP است) را با چرخوندن این هدر در هر تلاش، کاملاً دور بزند.
    فقط یک پراکسی مورد اعتماد (لبه‌ی Railway/Cloudflare) بین کلاینت و این
    سرویس وجود دارد و آن پراکسی IP واقعی را به‌عنوان آخرین مقدار زنجیره
    اضافه می‌کند؛ پس آخرین مقدار قابل‌اعتماد است، نه اولین."""
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

# ── SSRF protection برای /proxy ────────────────────────────────────────────────
# ✅ امنیت: قبلاً /proxy/{target_url} با هر URL دلخواه (حتی IPهای داخلی/متادیتای
# کلود مثل 169.254.169.254) کار می‌کرد. این تابع IPهای خصوصی/لوکال/متادیتا رو
# چه به‌صورت literal و چه بعد از DNS resolve مسدود می‌کند.
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
        pass  # هاست‌نیم است نه IP لیترال؛ باید resolve کنیم (محافظت در برابر DNS rebinding)
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
        # اگر resolve نشد، برای احتیاط مسدودش کن
        return True

# ── Default link ──────────────────────────────────────────────────────────────
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
                }
                asyncio.create_task(save_state())
        _default_link_created = True
