# ══════════════════════════════════════════════════════════════════════════════
# state.py — تیم آزادی Gateway v10.1
# ══════════════════════════════════════════════════════════════════════════════

import asyncio
import hashlib
import hmac
import ipaddress
import json
import logging
import os
import re
import secrets
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import aiofiles

# ── لاگینگ ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("team-azadi-gw")

IRAN_TZ = ZoneInfo("Asia/Tehran")

# ── پاک‌سازی ورودی متنی کاربر (دفاع در عمق) ────────────────────────────────
_HTML_TAG_RE = re.compile(r"<[^>]*>")
_CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def sanitize_text(value: str | None, max_len: int = 60) -> str:
    """هر ورودی متنی کاربر (label, name, note, desc …) باید از این عبور کند.
    تگ‌های HTML/اسکریپت را کامل حذف می‌کند و طول را محدود می‌کند."""
    if not value:
        return ""
    s = str(value).strip()
    s = _HTML_TAG_RE.sub("", s)
    s = _CONTROL_CHARS_RE.sub("", s)
    s = s.replace("<", "").replace(">", "")
    return s.strip()[:max_len]


# ── تنظیمات پایه ────────────────────────────────────────────────────────────
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
        logger.warning(
            "Could not persist secret key (%s); using ephemeral one — "
            "set SECRET_KEY env var to avoid this", e,
        )
        return secrets.token_urlsafe(32)


CONFIG = {
    "port": int(os.environ.get("PORT", 8000)),
    "secret": _load_or_create_secret(),
    "host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"),
}

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
DATA_FILE = DATA_DIR / "rvg_state.json"
SAVE_LOCK = asyncio.Lock()

# ─ـ آمار و وضعیت زنده ─────────────────────────────────────────────────────
connections: dict = {}
stats: dict = {
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

# ─ـ لینک‌ها (کانفیگ‌ها) ───────────────────────────────────────────────────
LINKS: dict = {}
LINKS_LOCK = asyncio.Lock()

# ─ـ گروه‌های ساب ──────────────────────────────────────────────────────────
SUBS: dict = {}
SUBS_LOCK = asyncio.Lock()

# ─ـ تنظیمات تلگرام ────────────────────────────────────────────────────────
TELEGRAM_SETTINGS: dict = {
    "enabled": False,
    "bot_token": "",
    "chat_id": "",
    "notify_quota_pct": 90,
    "notify_expiry_hours": 24,
    "api_ip": "",
    "bot_username": "",
}

# ─ـ تنظیمات عضویت / ورود از بات ───────────────────────────────────────────
JOIN_SETTINGS: dict = {
    "enabled": True,
    "channel_username": "TimAzadi",
    "channel_required": True,
    "grant_gb": 100,
    "grant_days": 0,
    "max_devices": 1,
    "bot_username": "",
}
USER_LINKS: dict = {}

# ─ـ تنظیمات عمومی (پنل وب) ───────────────────────────────────────────────
PUBLIC_SETTINGS: dict = {
    "allow_public_create": True,
    "allow_public_delete": True,
    "allow_public_toggle": True,
}

# ─ـ سیستم رفرال ──────────────────────────────────────────────────────────
REFERRAL_SETTINGS: dict = {
    "enabled": True,
    "bonus_gb": 5,
    "max_daily_credits": 0,
    "points_per_referral": 1,
    "message_template": (
        "🎁 <b>دعوت از دوستان</b>\n\n"
        "به ازای هر دوستی که با لینک اختصاصی تو وارد بات بشه و عضو کانال بشه، "
        "{bonus_gb} گیگ به کانفیگت اضافه می‌شه.\n\n"
        "🔗 لینک اختصاصی تو:\n<code>{ref_link}</code>\n\n"
        "✅ تعداد رفرال موفق تو تا الان: <b>{ref_count}</b>"
    ),
}

REFERRALS: dict = {}


def _referral_entry(user_id: str, name: str = "", username: str = "") -> dict:
    entry = REFERRALS.setdefault(user_id, {
        "name": name, "username": username,
        "count": 0, "points": 0, "credited_uids": [], "daily": {},
    })
    if name:
        entry["name"] = name
    if username:
        entry["username"] = username
    return entry


def record_referral(
    referrer_id: str, referred_user_id: str, referred_uid: str,
    referrer_name: str = "", referrer_username: str = "",
) -> bool:
    if not REFERRAL_SETTINGS.get("enabled", True):
        return False
    if not referrer_id or referrer_id == referred_user_id:
        return False
    entry = _referral_entry(referrer_id, referrer_name, referrer_username)
    if referred_uid in entry["credited_uids"]:
        return False
    day_key = now_ir().strftime("%Y-%m-%d")
    today = entry["daily"].get(day_key, 0)
    daily_cap = REFERRAL_SETTINGS.get("max_daily_credits", 0)
    if daily_cap > 0 and today >= daily_cap:
        return False
    entry["count"] += 1
    entry["points"] = entry.get("points", 0) + REFERRAL_SETTINGS.get("points_per_referral", 1)
    entry["credited_uids"].append(referred_uid)
    entry["daily"][day_key] = today + 1
    return True


def adjust_points(user_id: str, delta: int, name: str = "", username: str = "") -> int:
    entry = _referral_entry(user_id, name, username)
    entry["points"] = entry.get("points", 0) + delta
    return entry["points"]


def top_referrers(n: int = 10) -> list[dict]:
    items = sorted(REFERRALS.items(), key=lambda kv: kv[1].get("count", 0), reverse=True)
    return [{"user_id": uid, **data} for uid, data in items[:n]]


def top_by_points(n: int = 10) -> list[dict]:
    items = sorted(REFERRALS.items(), key=lambda kv: kv[1].get("points", 0), reverse=True)
    return [{"user_id": uid, **data} for uid, data in items[:n]]


def rank_of(user_id: str) -> tuple[int, int, dict]:
    items = sorted(REFERRALS.items(), key=lambda kv: kv[1].get("points", 0), reverse=True)
    total = len(items)
    for idx, (uid, data) in enumerate(items, 1):
        if uid == user_id:
            return idx, total, data
    return 0, total, REFERRALS.get(user_id, {"count": 0, "points": 0})


def record_traffic(uid: str, n: int):
    day_key = now_ir().strftime("%Y-%m-%d")
    daily_traffic[day_key] += n
    link_daily_traffic[uid][day_key] += n


# ══════════════════════════════════════════════════════════════════════════════
# فیلتر محتوا — مسدودسازی تبلیغات و محتوای بزرگسال
# ⚠️ این دو متغیر حتماً باید قبل از load_state() تعریف شوند
# ══════════════════════════════════════════════════════════════════════════════

FILTER_SETTINGS: dict = {
    "block_ads": False,
    "block_adult": False,
}

_BUILTIN_AD_DOMAINS: frozenset = frozenset({
    "doubleclick.net", "googlesyndication.com", "googleadservices.com",
    "google-analytics.com", "googletagmanager.com", "googletagservices.com",
    "adnxs.com", "adsrvr.org", "adservice.google.com", "ads.yahoo.com",
    "taboola.com", "outbrain.com", "criteo.com", "criteo.net", "pubmatic.com",
    "rubiconproject.com", "openx.net", "scorecardresearch.com", "quantserve.com",
    "moatads.com", "amazon-adsystem.com", "media.net", "adform.net",
    "bidswitch.net", "casalemedia.com", "contextweb.com", "smartadserver.com",
    "yieldmo.com", "advertising.com", "adtechus.com", "mopub.com",
    "app-measurement.com", "adjust.com", "appsflyer.com", "unityads.unity3d.com",
})

ADULT_BLOCKLIST_URL = (
    "https://raw.githubusercontent.com/StevenBlack/hosts/"
    "master/alternates/porn-only/hosts"
)
ADULT_BLOCK_DOMAINS: set[str] = set()
CUSTOM_BLOCK_DOMAINS: dict[str, set[str]] = {"ads": set(), "adult": set()}


def _looks_like_ip(hostname: str) -> bool:
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def _domain_suffix_match(hostname: str, domain_set: set[str]) -> bool:
    hostname = hostname.lower().rstrip(".")
    parts = hostname.split(".")
    for i in range(len(parts)):
        if ".".join(parts[i:]) in domain_set:
            return True
    return False


def is_domain_blocked(hostname: str) -> tuple[bool, str]:
    if not hostname or _looks_like_ip(hostname):
        return False, ""
    if FILTER_SETTINGS.get("block_ads") and _domain_suffix_match(
        hostname, _BUILTIN_AD_DOMAINS | CUSTOM_BLOCK_DOMAINS["ads"]
    ):
        return True, "ads"
    if FILTER_SETTINGS.get("block_adult") and _domain_suffix_match(
        hostname, ADULT_BLOCK_DOMAINS | CUSTOM_BLOCK_DOMAINS["adult"]
    ):
        return True, "adult"
    return False, ""


def add_custom_blocked_domain(domain: str, category: str = "ads") -> bool:
    domain = domain.strip().lower().lstrip("*.")
    if not domain or "." not in domain or category not in CUSTOM_BLOCK_DOMAINS:
        return False
    CUSTOM_BLOCK_DOMAINS[category].add(domain)
    return True


async def refresh_adult_blocklist() -> int:
    global ADULT_BLOCK_DOMAINS
    try:
        import httpx
        async with httpx.AsyncClient(timeout=25.0) as client:
            resp = await client.get(ADULT_BLOCKLIST_URL)
            resp.raise_for_status()
            text = resp.text
    except Exception as e:
        logger.warning("refresh_adult_blocklist failed: %s", e)
        return -1
    domains: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1"):
            d = parts[1].strip().lower()
            if d and d not in ("localhost", "local", "localhost.localdomain"):
                domains.add(d)
    if domains:
        ADULT_BLOCK_DOMAINS = domains
        logger.info("adult blocklist refreshed: %d domains", len(domains))
    return len(domains)


# ── پروتکل‌ها ──────────────────────────────────────────────────────────────
PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up", "xhttp-stream-one", "trojan-ws")
DEFAULT_PROTOCOL = "vless-ws"
ACTIVE_PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up", "xhttp-stream-one", "trojan-ws")
_PROTOCOL_TAG = {
    "vless-ws": "WS", "xhttp-packet-up": "XHTTP-P", "xhttp-stream-up": "XHTTP-S",
    "xhttp-stream-one": "XHTTP-S1", "trojan-ws": "TROJAN",
}


def log_activity(kind: str, message: str, level: str = "info"):
    activity_logs.append({
        "kind": kind, "level": level, "message": message,
        "time": datetime.now().isoformat(),
    })


# ── احراز هویت وب ─────────────────────────────────────────────────────────
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


def _initial_admin_password() -> str:
    env_pw = os.environ.get("ADMIN_PASSWORD")
    if env_pw:
        return env_pw
    logger.warning(
        "⚠️  ADMIN_PASSWORD not set — using insecure default. "
        "Change it from the panel or set ADMIN_PASSWORD env var immediately."
    )
    return "mohammad"


AUTH: dict = {"password_hash": hash_password(_initial_admin_password())}

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


async def require_auth(request):
    from fastapi import HTTPException
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        raise HTTPException(status_code=401, detail="unauthorized")
    return token


# ── ذخیره / بارگذاری وضعیت ────────────────────────────────────────────────
async def load_state():
    global LINKS, AUTH, SUBS, USER_LINKS, JOIN_SETTINGS, PUBLIC_SETTINGS
    global REFERRAL_SETTINGS, REFERRALS

    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            return
        async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = await f.read()
        data = json.loads(raw)

        if "links" in data:
            LINKS.update(data["links"])
        if "subs" in data:
            SUBS.update(data["subs"])

        # اگر ADMIN_PASSWORD در env ست شده، همیشه اولویت دارد (مسیر بازیابی)
        if not os.environ.get("ADMIN_PASSWORD") and "password_hash" in data:
            AUTH["password_hash"] = data["password_hash"]

        if "telegram_settings" in data:
            TELEGRAM_SETTINGS.update(data["telegram_settings"])
        if "join_settings" in data:
            JOIN_SETTINGS.update(data["join_settings"])
        if "user_links" in data:
            for uid_key, val in data["user_links"].items():
                fixed = val[-1] if isinstance(val, list) and val else val
                USER_LINKS[uid_key] = fixed
        if "public_settings" in data:
            PUBLIC_SETTINGS.update(data["public_settings"])
        if "referral_settings" in data:
            REFERRAL_SETTINGS.update(data["referral_settings"])
        if "referrals" in data:
            REFERRALS.update(data["referrals"])
        if "filter_settings" in data:
            FILTER_SETTINGS.update(data["filter_settings"])
        if "custom_block_domains" in data:
            cbd = data["custom_block_domains"]
            CUSTOM_BLOCK_DOMAINS["ads"] = set(cbd.get("ads", []))
            CUSTOM_BLOCK_DOMAINS["adult"] = set(cbd.get("adult", []))

        logger.info("State loaded: %d links, %d subs", len(LINKS), len(SUBS))
    except Exception as e:
        logger.warning("Could not load state: %s", e)


async def save_state():
    async with SAVE_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = {
                "links": dict(LINKS),
                "subs": dict(SUBS),
                "password_hash": AUTH["password_hash"],
                "telegram_settings": dict(TELEGRAM_SETTINGS),
                "join_settings": dict(JOIN_SETTINGS),
                "user_links": dict(USER_LINKS),
                "public_settings": dict(PUBLIC_SETTINGS),
                "referral_settings": dict(REFERRAL_SETTINGS),
                "referrals": dict(REFERRALS),
                "filter_settings": dict(FILTER_SETTINGS),
                "custom_block_domains": {
                    "ads": sorted(CUSTOM_BLOCK_DOMAINS["ads"]),
                    "adult": sorted(CUSTOM_BLOCK_DOMAINS["adult"]),
                },
                "saved_at": datetime.now().isoformat(),
            }
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning("Could not save state: %s", e)


# ── هاست / دامنه ──────────────────────────────────────────────────────────
def get_host() -> str:
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])


def get_extra_hosts() -> list[str]:
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


# ── تولید UUID / لینک ─────────────────────────────────────────────────────
def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def now_ir() -> datetime:
    return datetime.now(IRAN_TZ)


def generate_vless_link(
    uuid: str, host: str, remark: str = "تیم-آزادی",
    protocol: str = DEFAULT_PROTOCOL,
) -> str:
    from urllib.parse import quote
    if protocol == "trojan-ws":
        path = f"/ws/{uuid}"
        params = {
            "security": "tls", "type": "ws", "host": host,
            "path": path, "sni": host, "fp": "chrome", "alpn": "http/1.1",
        }
        query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
        return f"trojan://{uuid}@{host}:443?{query}#{quote(remark)}"

    if protocol == "vless-ws":
        path = f"/ws/{uuid}"
        params = {
            "encryption": "none", "security": "tls", "type": "ws",
            "host": host, "path": path, "sni": host, "fp": "chrome",
            "alpn": "http/1.1",
        }
    else:
        mode = protocol.replace("xhttp-", "")
        path = f"/xhttp-siz10/{mode}/{uuid}"
        params = {
            "encryption": "none", "security": "tls", "type": "xhttp",
            "mode": mode, "host": host, "path": path, "sni": host,
            "fp": "chrome", "alpn": "h2,http/1.1",
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
    if b < 1024 ** 2:
        return f"{b / 1024:.1f} KB"
    if b < 1024 ** 3:
        return f"{b / 1024 ** 2:.2f} MB"
    return f"{b / 1024 ** 3:.2f} GB"


def quota_suffix(used_bytes: int, limit_bytes: int) -> str:
    used = fmt_bytes(used_bytes).replace(" ", "")
    limit = "∞" if not limit_bytes else fmt_bytes(limit_bytes).replace(" ", "")
    return f"{used}/{limit}"


def generate_all_vless_links(
    uuid: str, host: str, label: str,
    used_bytes: int = 0, limit_bytes: int = 0,
    brand: bool = True, flag: str = "",
) -> list[dict]:
    quota = quota_suffix(used_bytes, limit_bytes)
    prefix = "تیم-آزادی-" if brand else ""
    flag_prefix = f"{flag}-" if flag else ""
    hosts = [host] + get_extra_hosts()
    out: list[dict] = []
    for idx, h in enumerate(hosts):
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


# ── پارس حجم / انقضا ──────────────────────────────────────────────────────
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
    if value is None or value <= 0:
        return None
    unit = (unit or "days").lower()
    if unit in ("hour", "hours", "h", "ساعت"):
        return timedelta(hours=value)
    if unit in ("day", "days", "d", "روز"):
        return timedelta(days=value)
    if unit in ("minute", "minutes", "m", "دقیقه"):
        return timedelta(minutes=value)
    return timedelta(days=value)


# ── بررسی وضعیت لینک ─────────────────────────────────────────────────────
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


# ── IP کلاینت ─────────────────────────────────────────────────────────────
def client_ip(conn) -> str:
    fwd = conn.headers.get("x-forwarded-for")
    if fwd:
        parts = [p.strip() for p in fwd.split(",") if p.strip()]
        if parts:
            return parts[-1]
    real_ip = conn.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    c = getattr(conn, "client", None)
    return c.host if c else "unknown"


# ── محافظت SSRF ───────────────────────────────────────────────────────────
_BLOCKED_PROXY_HOSTNAMES = frozenset({
    "metadata.google.internal", "metadata", "metadata.azure.com",
    "instance-data", "localhost",
})


def _is_blocked_ip(ip: ipaddress._BaseAddress) -> bool:
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


# ── لینک پیش‌فرض ──────────────────────────────────────────────────────────
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
                    "limit_bytes": 0, "used_bytes": 0,
                    "created_at": datetime.now().isoformat(),
                    "active": True, "expires_at": None, "note": "",
                    "is_default": True, "sub_id": None,
                    "protocol": DEFAULT_PROTOCOL, "parent_id": None,
                    "white_label": False, "flag": "🇺🇸",
                }
                asyncio.create_task(save_state())
    _default_link_created = True


# ─ـ عضویت کانال ──────────────────────────────────────────────────────────
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
    status = await check_channel_membership_status(user_id, bot_token)
    return status is True


async def check_channel_membership_status(
    user_id: str, bot_token: str | None = None,
) -> bool | None:
    """سه‌حالته: True=عضو | False=عضو نیست | None=نامعلوم"""
    if not JOIN_SETTINGS.get("channel_required", True):
        return True
    token = bot_token or TELEGRAM_SETTINGS.get("bot_token", "")
    channel = JOIN_SETTINGS.get("channel_username", "TimAzadi").strip().lstrip("@")
    if not token:
        logger.warning("check_channel_membership: no bot_token available")
        return None
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{token}/getChatMember",
                json={"chat_id": f"@{channel}", "user_id": int(user_id)},
                timeout=10.0,
            )
            data = resp.json()
            if data.get("ok"):
                status = data.get("result", {}).get("status")
                if status in ("member", "administrator", "creator"):
                    return True
                if status in ("left", "kicked", "restricted"):
                    return False
                return None
            logger.warning("check_channel_membership: API error: %s", data)
            return None
    except Exception as e:
        logger.warning("check_channel_membership error: %s", e)
        return None


async def create_join_link(user_id: str, label: str | None = None) -> str | None:
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
    safe_label = sanitize_text(label or f"کاربر-{user_id[:8]}")
    async with LINKS_LOCK:
        LINKS[uid] = {
            "label": safe_label,
            "limit_bytes": limit_bytes, "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "active": True, "expires_at": expires_at,
            "note": sanitize_text(f"بات - کاربر {user_id}", max_len=120),
            "is_default": False, "sub_id": None,
            "protocol": DEFAULT_PROTOCOL, "parent_id": None,
            "white_label": False, "flag": "🇺🇸",
            "max_devices": JOIN_SETTINGS.get("max_devices", 1),
            "quota_notified": False, "expiry_notified": False,
            "join_user": user_id, "disabled_by_leave": False,
        }
        USER_LINKS[user_id] = uid
    await save_state()
    return uid
