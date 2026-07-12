# ══════════════════════════════════════════════════════════════════════════════
# telegram_bot.py — مدیریت پنل از طریق بات تلگرام
# دو-طرفه: پنل ادمین + دریافت کانفیگ خودکار کاربر + رفرال + نظارت عضویت
# ══════════════════════════════════════════════════════════════════════════════

import asyncio
import html
import time
from datetime import datetime

from state import (
    LINKS, LINKS_LOCK, SUBS, SUBS_LOCK,
    TELEGRAM_SETTINGS, connections, stats,
    generate_uuid, generate_all_vless_links,
    is_link_allowed, is_link_expired, fmt_bytes, parse_size_to_bytes,
    parse_expiry_to_timedelta, get_host, log_activity, logger,
    DEFAULT_PROTOCOL, uptime,
    JOIN_SETTINGS, USER_LINKS,
    check_channel_membership, check_channel_membership_status,
    create_join_link, save_state,
    REFERRAL_SETTINGS, REFERRALS, record_referral,
    top_referrers, top_by_points, rank_of, adjust_points,
    FILTER_SETTINGS, CUSTOM_BLOCK_DOMAINS,
    add_custom_blocked_domain, refresh_adult_blocklist,
    sanitize_text,
)

PAGE_SIZE = 6

# رفرال در انتظار — فقط حافظه (نیازی به ماندگاری نیست)
_pending_referrer: dict[str, str] = {}

# کش نام‌نمایشی
_display_names: dict[str, dict] = {}

# ویزارد ساخت کانفیگ
_wizard: dict[str, dict] = {}

# آفست برای polling
_offset = 0
_running = False


def _remember_display_name(chat_id, from_user: dict | None):
    if not from_user:
        return
    name = " ".join(filter(None, [
        from_user.get("first_name"), from_user.get("last_name"),
    ])).strip()
    _display_names[str(chat_id)] = {
        "name": name or str(chat_id),
        "username": from_user.get("username") or "",
    }


def _allowed_chats() -> set[str]:
    raw = (TELEGRAM_SETTINGS.get("chat_id") or "").strip()
    if not raw:
        return set()
    return {p.strip() for p in raw.replace(";", ",").split(",") if p.strip()}


def _is_admin(chat_id) -> bool:
    return str(chat_id) in _allowed_chats()


# ── یوزرنیم بات (از API) ──────────────────────────────────────────────────
_bot_username_cache: str | None = None


async def _get_bot_username() -> str | None:
    global _bot_username_cache
    if _bot_username_cache:
        return _bot_username_cache
    result = await _api("getMe")
    if result and result.get("username"):
        _bot_username_cache = result["username"]
        return _bot_username_cache
    return None


# ── اکشن‌های فقط ادمین ────────────────────────────────────────────────────
ADMIN_ONLY_PREFIXES = (
    "m:new", "m:list:", "m:stats", "m:search", "m:subs:",
    "q:", "e:", "l:", "lt:", "lr:", "li:", "lg:", "ld", "st:",
    "sup:reply:", "m:ref", "m:broadcast",
    "ref:toggle", "ref:setbonus", "ref:setdaily", "ref:settemplate",
    "ref:givepoints",
    "m:filter", "filter:",
)


def _is_admin_only_action(data: str) -> bool:
    return any(data == p or data.startswith(p) for p in ADMIN_ONLY_PREFIXES)


def _channel_username() -> str:
    return (JOIN_SETTINGS.get("channel_username", "TimAzadi") or "TimAzadi").strip().lstrip("@")


def _safe_host() -> str:
    host = get_host()
    if not host or host == "localhost":
        logger.warning("RAILWAY_PUBLIC_DOMAIN not set — links may be incorrect")
    return host


# ── API تلگرام ─────────────────────────────────────────────────────────────
async def _api(method: str, payload: dict | None = None) -> dict | None:
    from main import http_client
    token = TELEGRAM_SETTINGS.get("bot_token")
    if not token or http_client is None:
        return None
    api_ip = (TELEGRAM_SETTINGS.get("api_ip") or "").strip()
    try:
        if api_ip:
            host_for_url = f"[{api_ip}]" if ":" in api_ip else api_ip
            url = f"https://{host_for_url}/bot{token}/{method}"
            resp = await http_client.post(
                url, json=payload or {},
                headers={"Host": "api.telegram.org"},
                extensions={"sni_hostname": "api.telegram.org"},
                timeout=35.0,
            )
        else:
            url = f"https://api.telegram.org/bot{token}/{method}"
            resp = await http_client.post(url, json=payload or {}, timeout=35.0)
        data = resp.json()
        if not data.get("ok"):
            logger.warning("telegram_bot: %s failed: %s", method, data)
            return None
        return data.get("result")
    except Exception as e:
        logger.warning("telegram_bot: %s error: %s", method, e)
        return None


async def _send(chat_id, text, kb=None, photo=None):
    payload = {"chat_id": chat_id, "parse_mode": "HTML"}
    if kb is not None:
        payload["reply_markup"] = {"inline_keyboard": kb}
    if photo:
        payload["photo"] = photo
        payload["caption"] = text
        return await _api("sendPhoto", payload)
    payload["text"] = text
    return await _api("sendMessage", payload)


async def _edit(chat_id, message_id, text, kb=None):
    payload = {
        "chat_id": chat_id, "message_id": message_id,
        "text": text, "parse_mode": "HTML",
    }
    if kb is not None:
        payload["reply_markup"] = {"inline_keyboard": kb}
    res = await _api("editMessageText", payload)
    if res is None:
        await _send(chat_id, text, kb)


async def _answer_cb(cb_id, text=None):
    payload = {"callback_query_id": cb_id}
    if text:
        payload["text"] = text
        payload["show_alert"] = False
    await _api("answerCallbackQuery", payload)


# ── فرمت خط لینک ──────────────────────────────────────────────────────────
def _link_line(uid: str, d: dict) -> str:
    ok = is_link_allowed(d)
    dot = "🟢" if ok else "🔴"
    used = fmt_bytes(d.get("used_bytes", 0))
    limit = "∞" if not d.get("limit_bytes") else fmt_bytes(d["limit_bytes"])
    return f"{dot} {d.get('label', '?')} — {used}/{limit}"


# ── کیبوردها ──────────────────────────────────────────────────────────────
def _main_menu_kb():
    return [
        [
            {"text": "➕ کانفیگ جدید", "callback_data": "m:new"},
            {"text": "📋 لیست کانفیگ‌ها", "callback_data": "m:list:0"},
        ],
        [
            {"text": "📊 آمار سیستم", "callback_data": "m:stats"},
            {"text": "🔍 جستجو", "callback_data": "m:search"},
        ],
        [{"text": "📂 گروه‌های ساب", "callback_data": "m:subs:0"}],
        [
            {"text": "🏆 رفرال", "callback_data": "m:ref"},
            {"text": "📢 پیام همگانی", "callback_data": "m:broadcast"},
        ],
        [{"text": "🛡️ فیلتر محتوا", "callback_data": "m:filter"}],
    ]


async def _show_main_menu(chat_id, message_id=None):
    text = "🤖 <b>پنل مدیریت تیم آزادی</b>\nیکی از گزینه‌ها رو انتخاب کن:"
    kb = _main_menu_kb()
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


# ── لیست کانفیگ‌ها ────────────────────────────────────────────────────────
async def _show_list(chat_id, message_id, page: int):
    async with LINKS_LOCK:
        items = sorted(
            LINKS.items(),
            key=lambda kv: kv[1].get("created_at", ""),
            reverse=True,
        )
    total = len(items)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, pages - 1))
    chunk = items[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]

    kb = [
        [{"text": _link_line(uid, d), "callback_data": f"l:{uid}"}]
        for uid, d in chunk
    ]
    nav = []
    if page > 0:
        nav.append({"text": "◀️ قبلی", "callback_data": f"m:list:{page - 1}"})
    nav.append({"text": f"{page + 1}/{pages}", "callback_data": "noop"})
    if page < pages - 1:
        nav.append({"text": "بعدی ▶️", "callback_data": f"m:list:{page + 1}"})
    kb.append(nav)
    kb.append([{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}])

    text = (
        f"📋 <b>لیست کانفیگ‌ها</b> ({total} مورد)\n"
        "روی هرکدام بزن برای مدیریت:"
    ) if total else "هیچ کانفیگی هنوز ساخته نشده."
    await _edit(chat_id, message_id, text, kb)


# ── جزئیات لینک ───────────────────────────────────────────────────────────
async def _show_link_detail(chat_id, message_id, uid: str):
    async with LINKS_LOCK:
        d = LINKS.get(uid)
    if not d:
        await _edit(
            chat_id, message_id, "این کانفیگ دیگر وجود ندارد.",
            [[{"text": "⬅️ لیست", "callback_data": "m:list:0"}]],
        )
        return

    ok = is_link_allowed(d)
    expired = is_link_expired(d)
    used = fmt_bytes(d.get("used_bytes", 0))
    limit = "∞" if not d.get("limit_bytes") else fmt_bytes(d["limit_bytes"])
    exp_txt = "بدون انقضا"
    if d.get("expires_at"):
        try:
            exp_txt = datetime.fromisoformat(d["expires_at"]).strftime("%Y-%m-%d %H:%M")
        except Exception:
            exp_txt = str(d["expires_at"])
    gift_txt = "\n🎁 این یک کانفیگ هدیه‌داده‌شده است." if d.get("parent_id") else ""

    text = (
        f"🔧 <b>{html.escape(d.get('label', '?'))}</b>\n\n"
        f"وضعیت: {'🟢 فعال' if ok else ('⏰ منقضی' if expired else '🔴 غیرفعال/اتمام حجم')}\n"
        f"مصرف: {used} از {limit}\n"
        f"انقضا: {exp_txt}\n"
        f"پروتکل پیش‌فرض: {d.get('protocol', DEFAULT_PROTOCOL)}"
        f"{gift_txt}"
    )
    kb = [
        [
            {"text": ("🔒 غیرفعال کن" if d.get("active", True) else "🔓 فعال کن"), "callback_data": f"lt:{uid}"},
            {"text": "♻️ ریست مصرف", "callback_data": f"lr:{uid}"},
        ],
        [
            {"text": "➕ افزایش حجم", "callback_data": f"li:{uid}"},
            {"text": "🔗 دریافت لینک/QR", "callback_data": f"lg:{uid}"},
        ],
        [{"text": "🗑 حذف کامل", "callback_data": f"ld:{uid}"}],
        [{"text": "⬅️ لیست", "callback_data": "m:list:0"}],
    ]
    await _edit(chat_id, message_id, text, kb)


async def _send_link_and_qr(chat_id, uid: str):
    try:
        async with LINKS_LOCK:
            d = LINKS.get(uid)
        if not d:
            await _send(chat_id, "❌ این کانفیگ دیگر وجود ندارد.")
            return
        host = _safe_host()
        label = html.escape(d.get("label", "کانفیگ"))
        sub_url = f"https://{host}/sub/{uid}"
        text = f"🔗 <b>{label}</b>\n\n📡 لینک ساب:\n<code>{sub_url}</code>"
        kb = [[{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}]]
        await _send(chat_id, text, kb)
    except Exception:
        await _send(chat_id, "❌ خطا در دریافت لینک.")


# ── ویزارد ساخت کانفیگ ───────────────────────────────────────────────────
QUOTA_OPTIONS = [
    ("1GB", 1), ("5GB", 5), ("10GB", 10), ("20GB", 20),
    ("50GB", 50), ("100GB", 100), ("∞ نامحدود", 0),
]
EXPIRY_OPTIONS = [
    ("بدون انقضا", None), ("۱ روز", 1), ("۷ روز", 7), ("۳۰ روز", 30),
]


async def _wizard_start(chat_id, message_id):
    _wizard[str(chat_id)] = {"step": "label", "data": {}}
    await _edit(
        chat_id, message_id,
        "✏️ اسم این کانفیگ رو بفرست (مثلاً: کاربر علی):",
        [[{"text": "❌ انصراف", "callback_data": "m:main"}]],
    )


async def _wizard_ask_quota(chat_id, message_id=None):
    kb = [
        [{"text": t, "callback_data": f"q:{v}"}
         for t, v in QUOTA_OPTIONS[i:i + 2]]
        for i in range(0, len(QUOTA_OPTIONS), 2)
    ]
    kb.append([{"text": "✏️ مقدار دلخواه (GB)", "callback_data": "q:custom"}])
    kb.append([{"text": "❌ انصراف", "callback_data": "m:main"}])
    if message_id:
        await _edit(chat_id, message_id, "📦 چه مقدار حجم بدیم؟", kb)
    else:
        await _send(chat_id, "📦 چه مقدار حجم بدیم؟", kb)


async def _wizard_ask_expiry(chat_id, message_id=None):
    kb = [
        [{"text": t, "callback_data": f"e:{v if v is not None else 0}"}
         for t, v in EXPIRY_OPTIONS[i:i + 2]]
        for i in range(0, len(EXPIRY_OPTIONS), 2)
    ]
    kb.append([{"text": "✏️ مقدار دلخواه (روز)", "callback_data": "e:custom"}])
    kb.append([{"text": "❌ انصراف", "callback_data": "m:main"}])
    if message_id:
        await _edit(chat_id, message_id, "⏰ تا کِی معتبر باشه؟", kb)
    else:
        await _send(chat_id, "⏰ تا کِی معتبر باشه؟", kb)


async def _wizard_finish(chat_id, message_id=None):
    w = _wizard.pop(str(chat_id), None)
    if not w:
        return
    d = w["data"]
    label = sanitize_text(d.get("label", "کانفیگ جدید"))
    limit_bytes = parse_size_to_bytes(d.get("quota_gb", 0), "GB") if d.get("quota_gb", 0) else 0
    exp_days = d.get("expiry_days")
    expires_at = None
    if exp_days:
        td = parse_expiry_to_timedelta(float(exp_days), "days")
        if td:
            expires_at = (datetime.now() + td).isoformat()

    uid = generate_uuid()
    async with LINKS_LOCK:
        LINKS[uid] = {
            "label": label,
            "limit_bytes": limit_bytes, "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "active": True, "expires_at": expires_at,
            "note": "از بات تلگرام ساخته شد",
            "is_default": False, "sub_id": None,
            "protocol": DEFAULT_PROTOCOL, "parent_id": None,
            "white_label": False, "flag": "🇺🇸",
            "max_devices": 0,
            "quota_notified": False, "expiry_notified": False,
        }
    from main import schedule_save
    await schedule_save()
    log_activity("link", f"کانفیگ «{label}» از بات ساخته شد", "ok")

    limit_txt = "∞" if not limit_bytes else fmt_bytes(limit_bytes)
    exp_txt = "بدون انقضا" if not expires_at else f"{exp_days} روز دیگر"
    text = (
        f"✅ کانفیگ ساخته شد!\n\n"
        f"<b>{html.escape(label)}</b>\n"
        f"حجم: {limit_txt}\nانقضا: {exp_txt}"
    )
    kb = [
        [{"text": "🔗 دریافت لینک/QR", "callback_data": f"lg:{uid}"}],
        [{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}],
    ]
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


# ── لیدربورد رفرال ───────────────────────────────────────────────────────
_MEDALS = ["🥇", "🥈", "🥉"]


def _display_name_for(entry: dict, fallback_id: str) -> str:
    name = html.escape(str(entry.get("name") or fallback_id))
    uname = f" (@{html.escape(str(entry['username']))})" if entry.get("username") else ""
    return f"{name}{uname}"


async def _send_leaderboard(chat_id):
    top = top_by_points(10)
    if not top:
        await _send(
            chat_id,
            "🏆 <b>لیست برترین‌ها</b>\n\n"
            "هنوز کسی امتیازی کسب نکرده — اولین نفر تو باش!",
        )
        return

    lines = ["🏆 <b>لیست برترین‌های تیم آزادی</b>", "━━━━━━━━━━━━━━━", ""]
    for i, r in enumerate(top, 1):
        medal = _MEDALS[i - 1] if i <= 3 else f"{i}."
        name = _display_name_for(r, r["user_id"])
        lines.append(
            f"{medal} {name}\n"
            f"     🎯 {r.get('points', 0)} امتیاز · "
            f"👥 {r.get('count', 0)} دعوت"
        )
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━")

    user_id = str(chat_id)
    rank, total, mine = rank_of(user_id)
    if rank:
        lines.append(
            f"📍 جایگاه تو: <b>#{rank}</b> از {total} نفر — "
            f"{mine.get('points', 0)} امتیاز · {mine.get('count', 0)} دعوت"
        )
    else:
        lines.append("📍 هنوز جایگاهی نداری — با دعوت دوستات وارد لیست شو!")

    await _send(chat_id, "\n".join(lines))


# ── پنل رفرال ادمین ──────────────────────────────────────────────────────
async def _show_referral_admin(chat_id, message_id):
    top = top_referrers(10)
    lines = []
    for i, r in enumerate(top, 1):
        name = html.escape(str(r.get("name") or r["user_id"]))
        uname = f" (@{html.escape(str(r['username']))})" if r.get("username") else ""
        lines.append(f"{i}. {name}{uname} — <code>{r['user_id']}</code> — {r.get('count', 0)} رفرال")
    board = "\n".join(lines) if lines else "هنوز هیچ رفرالی ثبت نشده."

    status = "🟢 فعال" if REFERRAL_SETTINGS.get("enabled", True) else "🔴 غیرفعال"
    daily_cap = REFERRAL_SETTINGS.get("max_daily_credits", 0)
    daily_txt = "بدون سقف" if daily_cap <= 0 else f"{daily_cap} رفرال در روز"

    text = (
        "🏆 <b>سیستم رفرال</b>\n\n"
        f"وضعیت: {status}\n"
        f"هدیه‌ی هر رفرال: {REFERRAL_SETTINGS.get('bonus_gb', 5)} گیگ\n"
        f"سقف روزانه: {daily_txt}\n\n"
        f"🥇 <b>برترین‌ها:</b>\n{board}"
    )
    kb = [
        [{"text": "🔴 غیرفعال" if REFERRAL_SETTINGS.get("enabled") else "🟢 فعال", "callback_data": "ref:toggle"}],
        [{"text": "✏️ تغییر مقدار هدیه", "callback_data": "ref:setbonus"}],
        [{"text": "✏️ تغییر سقف روزانه", "callback_data": "ref:setdaily"}],
        [{"text": "✏️ تغییر متن پیام رفرال", "callback_data": "ref:settemplate"}],
        [{"text": "🏅 امتیاز دادن به کاربر", "callback_data": "ref:givepoints"}],
        [{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}],
    ]
    await _edit(chat_id, message_id, text, kb)


# ── پنل فیلتر ادمین ──────────────────────────────────────────────────────
async def _show_filter_admin(chat_id, message_id):
    ads_on = FILTER_SETTINGS.get("block_ads", False)
    adult_on = FILTER_SETTINGS.get("block_adult", False)
    custom_ads = len(CUSTOM_BLOCK_DOMAINS.get("ads", set()))
    custom_adult = len(CUSTOM_BLOCK_DOMAINS.get("adult", set()))

    text = (
        "🛡️ <b>فیلتر محتوای ساب‌ها</b>\n\n"
        f"مسدودسازی تبلیغات: {'🟢 فعال' if ads_on else '🔴 غیرفعال'} (+{custom_ads} دامنه‌ی دستی)\n"
        f"مسدودسازی بزرگسال: {'🟢 فعال' if adult_on else '🔴 غیرفعال'} (+{custom_adult} دامنه‌ی دستی)\n\n"
        "فیلتر روی سطح اتصال کار می‌کنه: قبل از وصل‌شدن، دامنه چک می‌شه."
    )
    kb = [
        [{"text": ("🔴 خاموش" if ads_on else "🟢 روشن") + " — تبلیغات", "callback_data": "filter:toggle:ads"}],
        [{"text": ("🔴 خاموش" if adult_on else "🟢 روشن") + " — بزرگسال", "callback_data": "filter:toggle:adult"}],
        [{"text": "🔄 بروزرسانی لیست بزرگسال", "callback_data": "filter:refreshadult"}],
        [{"text": "➕ افزودن دامنه‌ی دلخواه", "callback_data": "filter:addcustom"}],
        [{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}],
    ]
    await _edit(chat_id, message_id, text, kb)


# ── آمار ──────────────────────────────────────────────────────────────────
async def _show_stats(chat_id, message_id):
    async with LINKS_LOCK:
        total = len(LINKS)
        active = sum(1 for d in LINKS.values() if is_link_allowed(d))
    text = (
        "📊 <b>آمار سیستم</b>\n\n"
        f"کل کانفیگ‌ها: {total}\n"
        f"فعال: {active}\n"
        f"اتصالات زنده: {len(connections)}\n"
        f"کل ترافیک: {fmt_bytes(stats.get('total_bytes', 0))}\n"
        f"کل درخواست‌ها: {stats.get('total_requests', 0)}\n"
        f"آپ‌تایم: {uptime()}"
    )
    await _edit(
        chat_id, message_id, text,
        [[{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}]],
    )


# ══════════════════════════════════════════════════════════════════════════════
# فلوی ورود کاربر عادی (عضویت کانال → دریافت کانفیگ)
# ══════════════════════════════════════════════════════════════════════════════
async def _handle_join_start(chat_id, message_id=None):
    user_id = str(chat_id)
    existing_uid = USER_LINKS.get(user_id)
    if existing_uid and existing_uid in LINKS:
        await _grant_join_link(chat_id, message_id)
        return

    if JOIN_SETTINGS.get("channel_required", True):
        is_member = await check_channel_membership(user_id, TELEGRAM_SETTINGS.get("bot_token"))
        if not is_member:
            channel = _channel_username()
            text = (
                "❌ برای دریافت کانفیگ رایگان، ابتدا باید عضو کانال شوید.\n\n"
                f"📢 عضو کانال:\n👉 https://t.me/{channel}\n\n"
                "سپس روی دکمه‌ی زیر بزنید."
            )
            kb = [
                [{"text": "🔄 بررسی مجدد عضویت", "callback_data": "j:check"}],
                [{"text": "📩 پیام به پشتیبانی", "callback_data": "sup:start"}],
            ]
            if message_id:
                await _edit(chat_id, message_id, text, kb)
            else:
                await _send(chat_id, text, kb)
            return

    await _grant_join_link(chat_id, message_id)


async def _credit_pending_referral(user_id: str):
    referrer_id = _pending_referrer.pop(user_id, None)
    if not referrer_id:
        return
    referrer_uid = USER_LINKS.get(referrer_id)
    if not referrer_uid or referrer_uid not in LINKS:
        return

    disp = _display_names.get(referrer_id, {})
    ok = record_referral(
        referrer_id, user_id, USER_LINKS.get(user_id, ""),
        disp.get("name", ""), disp.get("username", ""),
    )
    if not ok:
        return

    bonus_gb = REFERRAL_SETTINGS.get("bonus_gb", 5)
    if bonus_gb > 0:
        async with LINKS_LOCK:
            rlink = LINKS.get(referrer_uid)
            if rlink and rlink.get("limit_bytes", 0) > 0:
                rlink["limit_bytes"] += parse_size_to_bytes(bonus_gb, "GB")
    await save_state()

    new_count = REFERRALS.get(referrer_id, {}).get("count", 0)
    log_activity("system", f"رفرال موفق: {referrer_id} (مجموع {new_count})", "ok")

    if bonus_gb > 0:
        await _send(
            referrer_id,
            f"🎉 یکی از دوستات با لینک تو وارد شد!\n\n"
            f"🎁 {bonus_gb} گیگ به کانفیگت اضافه شد.\n"
            f"✅ مجموع رفرال: {new_count}",
        )
    else:
        await _send(referrer_id, f"🎉 یکی از دوستات با لینک تو وارد شد!\n✅ مجموع رفرال: {new_count}")


async def _grant_join_link(chat_id, message_id=None):
    user_id = str(chat_id)
    uid = USER_LINKS.get(user_id)
    is_new_user = not uid or uid not in LINKS

    if is_new_user:
        uid = await create_join_link(user_id)

    d = LINKS.get(uid) if uid else None
    if not uid or not d:
        text = "❌ خطا در ساخت کانفیگ. لطفاً بعداً تلاش کنید."
        kb = [[{"text": "🔄 تلاش مجدد", "callback_data": "j:check"}]]
        if message_id:
            await _edit(chat_id, message_id, text, kb)
        else:
            await _send(chat_id, text, kb)
        return

    if is_new_user:
        await _credit_pending_referral(user_id)

    host = _safe_host()
    sub_url = f"https://{host}/sub/{uid}"
    limit_txt = "∞" if not d.get("limit_bytes") else fmt_bytes(d["limit_bytes"])
    exp_txt = "بدون انقضا"
    if d.get("expires_at"):
        try:
            exp_txt = datetime.fromisoformat(d["expires_at"]).strftime("%Y-%m-%d %H:%M")
        except Exception:
            exp_txt = str(d["expires_at"])

    text = (
        "🎉 <b>خوش اومدی به تیم آزادی!</b>\n\n"
        "🔗 <b>لینک ساب اختصاصی:</b>\n"
        f"<code>{sub_url}</code>\n\n"
        f"📦 حجم: {limit_txt}\n"
        f"⏰ انقضا: {exp_txt}\n\n"
        f"📢 کانال:\nhttps://t.me/{_channel_username()}"
    )
    kb = [
        [{"text": "🔗 کپی لینک ساب", "callback_data": f"m:copy:{uid}"}],
        [
            {"text": "🎁 دعوت دوستان", "callback_data": "ref:me"},
            {"text": "🏆 برترین‌ها", "callback_data": "ref:board"},
        ],
        [{"text": "📩 پیام به پشتیبانی", "callback_data": "sup:start"}],
        [{"text": "🔄 بروزرسانی", "callback_data": "j:check"}],
    ]
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


# ── پشتیبانی ──────────────────────────────────────────────────────────────
SUPPORT_MSG_COOLDOWN = 60
_last_support_msg: dict[str, float] = {}


async def _handle_support_message(chat_id, text):
    _wizard.pop(str(chat_id), None)
    user_id = str(chat_id)
    msg = (text or "").strip()
    if not msg:
        await _send(chat_id, "پیام خالی بود.")
        return

    now = time.time()
    last = _last_support_msg.get(user_id, 0)
    if now - last < SUPPORT_MSG_COOLDOWN:
        wait = int(SUPPORT_MSG_COOLDOWN - (now - last))
        await _send(chat_id, f"⏳ {wait} ثانیه صبر کن.")
        return
    _last_support_msg[user_id] = now

    admins = _allowed_chats()
    if not admins:
        await _send(chat_id, "⚠️ پشتیبانی فعلاً در دسترس نیست.")
        return

    uid = USER_LINKS.get(user_id)
    label = html.escape(str(LINKS.get(uid, {}).get("label", "?"))) if uid else "بدون کانفیگ"
    safe_msg = html.escape(msg[:3500])

    for admin_chat in admins:
        await _send(
            admin_chat,
            f"📩 <b>پیام پشتیبانی</b>\n"
            f"از: <code>{user_id}</code> (کانفیگ: {label})\n\n{safe_msg}",
            [[{"text": "↩️ پاسخ", "callback_data": f"sup:reply:{user_id}"}]],
        )
    await _send(chat_id, "✅ پیامت ارسال شد.")
    log_activity("system", f"پیام پشتیبانی از {user_id}", "info")


# ══════════════════════════════════════════════════════════════════════════════
# هندلر متن
# ══════════════════════════════════════════════════════════════════════════════
async def _handle_text(
    chat_id, text, is_admin: bool = False, from_user: dict | None = None,
):
    w = _wizard.get(str(chat_id))
    text = (text or "").strip()
    from_user = from_user or {}
    _remember_display_name(chat_id, from_user)

    if text.startswith("/start"):
        parts = text.split(maxsplit=1)
        payload = parts[1].strip() if len(parts) > 1 else ""

        if not is_admin and payload.startswith("ref_"):
            referrer_id = payload[4:].strip()
            user_id = str(chat_id)
            already = user_id in USER_LINKS and USER_LINKS[user_id] in LINKS
            if referrer_id and referrer_id != user_id and not already:
                _pending_referrer[user_id] = referrer_id

        if is_admin:
            await _show_main_menu(chat_id)
        else:
            await _handle_join_start(chat_id)
        return

    if text.startswith("/menu"):
        if is_admin:
            await _show_main_menu(chat_id)
        else:
            await _handle_join_start(chat_id)
        return

    if text.startswith("/broadcast") and is_admin:
        _wizard[str(chat_id)] = {"step": "broadcast_wait", "data": {}}
        await _send(chat_id, "📢 متن پیام همگانی رو بفرست:\n\n❌ انصراف: /menu")
        return

    if not is_admin:
        if w and w.get("step") == "support_wait":
            await _handle_support_message(chat_id, text)
            return
        _wizard.pop(str(chat_id), None)
        await _handle_join_start(chat_id)
        return

    if not w:
        await _send(chat_id, "برای شروع /menu رو بزن.")
        return

    step = w["step"]

    if step == "label":
        w["data"]["label"] = text[:60] or "کانفیگ جدید"
        w["step"] = "quota"
        await _wizard_ask_quota(chat_id)

    elif step == "quota_custom":
        try:
            w["data"]["quota_gb"] = max(0.0, float(text.replace(",", ".")))
        except ValueError:
            await _send(chat_id, "عدد معتبر نبود؛ دوباره بفرست:")
            return
        w["step"] = "expiry"
        await _wizard_ask_expiry(chat_id)

    elif step == "expiry_custom":
        try:
            w["data"]["expiry_days"] = max(0.0, float(text.replace(",", ".")))
        except ValueError:
            await _send(chat_id, "عدد معتبر نبود؛ دوباره بفرست:")
            return
        await _wizard_finish(chat_id)

    elif step == "support_reply_wait":
        _wizard.pop(str(chat_id), None)
        target = w["data"].get("target")
        msg = text[:3500]
        if not target or not msg:
            await _send(chat_id, "لغو شد.")
            return
        res = await _send(target, f"💬 <b>پاسخ پشتیبانی:</b>\n\n{msg}")
        if res is not None:
            await _send(chat_id, "✅ پاسخ ارسال شد.")
            log_activity("system", f"ادمین {chat_id} به {target} پاسخ داد", "ok")
        else:
            await _send(chat_id, "❌ ارسال ناموفق (شاید بات رو بلاک کرده).")

    elif step == "broadcast_wait":
        _wizard.pop(str(chat_id), None)
        msg = text[:3500]
        if not msg:
            await _send(chat_id, "متن خالی بود، لغو شد.")
            return
        async with LINKS_LOCK:
            targets = sorted({
                d.get("join_user") for d in LINKS.values() if d.get("join_user")
            })
        await _send(chat_id, f"⏳ ارسال برای {len(targets)} کاربر...")
        sent, failed = 0, 0
        for user_id in targets:
            res = await _send(user_id, msg)
            if res is not None:
                sent += 1
            else:
                failed += 1
            await asyncio.sleep(0.05)
        await _send(chat_id, f"✅ تموم شد. موفق: {sent} | ناموفق: {failed}")
        log_activity("system", f"پیام همگانی: {sent} موفق از {len(targets)}", "ok")

    elif step == "ref_bonus_wait":
        _wizard.pop(str(chat_id), None)
        try:
            gb = max(0.0, float(text.replace(",", ".")))
        except ValueError:
            await _send(chat_id, "عدد معتبر نبود، لغو شد.")
            return
        REFERRAL_SETTINGS["bonus_gb"] = gb
        await save_state()
        await _send(chat_id, f"✅ هدیه‌ی رفرال: {gb} گیگ")
        log_activity("system", f"هدیه رفرال تغییر به {gb}GB", "ok")

    elif step == "ref_daily_wait":
        _wizard.pop(str(chat_id), None)
        try:
            cap = int(float(text.replace(",", ".")))
        except ValueError:
            await _send(chat_id, "عدد معتبر نبود، لغو شد.")
            return
        cap = max(0, cap)
        REFERRAL_SETTINGS["max_daily_credits"] = cap
        await save_state()
        cap_txt = "بدون سقف" if cap == 0 else f"{cap} در روز"
        await _send(chat_id, f"✅ سقف روزانه: «{cap_txt}»")

    elif step == "ref_points_uid_wait":
        target = text.strip()
        if not target.lstrip("-").isdigit():
            await _send(chat_id, "آیدی عددی معتبر نیست.")
            return
        _wizard[str(chat_id)] = {"step": "ref_points_amount_wait", "data": {"target": target}}
        cur = REFERRALS.get(target, {}).get("points", 0)
        await _send(chat_id, f"امتیاز فعلی: {cur}\n\nچند امتیاز بدم؟ (منفی برای کم‌کردن):")

    elif step == "ref_points_amount_wait":
        _wizard.pop(str(chat_id), None)
        target = w["data"].get("target")
        try:
            delta = int(float(text.replace(",", ".")))
        except ValueError:
            await _send(chat_id, "عدد معتبر نبود، لغو شد.")
            return
        disp = _display_names.get(target, {})
        new_total = adjust_points(target, delta, disp.get("name", ""), disp.get("username", ""))
        await save_state()
        await _send(chat_id, f"✅ امتیاز <code>{target}</code>: {new_total}")
        if delta > 0:
            await _send(target, f"🎖 ادمین {delta} امتیاز بهت داد. مجموع: {new_total}")
        elif delta < 0:
            await _send(target, f"⚠️ {abs(delta)} امتیاز کم شد. مجموع: {new_total}")

    elif step == "filter_addcustom_cat_wait":
        cat = text.strip().lower()
        if cat not in ("ads", "adult"):
            await _send(chat_id, "فقط <code>ads</code> یا <code>adult</code> معتبره.")
            return
        _wizard[str(chat_id)] = {"step": "filter_addcustom_domain_wait", "data": {"cat": cat}}
        await _send(chat_id, "دامنه رو بفرست (مثلاً example.com):")

    elif step == "filter_addcustom_domain_wait":
        _wizard.pop(str(chat_id), None)
        cat = w["data"].get("cat", "ads")
        ok = add_custom_blocked_domain(text, cat)
        if not ok:
            await _send(chat_id, "دامنه معتبر نبود.")
            return
        await save_state()
        cat_fa = "تبلیغات" if cat == "ads" else "بزرگسال"
        await _send(chat_id, f"✅ دامنه به لیست {cat_fa} اضافه شد.")

    elif step == "ref_template_wait":
        _wizard.pop(str(chat_id), None)
        new_template = text[:2000]
        if not new_template:
            await _send(chat_id, "متن خالی بود.")
            return
        REFERRAL_SETTINGS["message_template"] = new_template
        await save_state()
        await _send(chat_id, "✅ متن پیام رفرال بروزرسانی شد.")

    elif step == "search":
        _wizard.pop(str(chat_id), None)
        q = text.lower()
        async with LINKS_LOCK:
            hits = [(uid, d) for uid, d in LINKS.items() if q in d.get("label", "").lower()][:20]
        if not hits:
            await _send(
                chat_id, "چیزی پیدا نشد.",
                [[{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}]],
            )
            return
        kb = [[{"text": _link_line(uid, d), "callback_data": f"l:{uid}"}] for uid, d in hits]
        kb.append([{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}])
        await _send(chat_id, f"🔍 {len(hits)} نتیجه:", kb)

    elif step == "increase_quota":
        uid = w["data"]["uid"]
        try:
            extra_gb = max(0.0, float(text.replace(",", ".")))
        except ValueError:
            await _send(chat_id, "عدد معتبر نبود:")
            return
        _wizard.pop(str(chat_id), None)
        async with LINKS_LOCK:
            link = LINKS.get(uid)
            if link:
                if link.get("limit_bytes", 0) == 0:
                    await _send(chat_id, "این کانفیگ نامحدود است.")
                    return
                link["limit_bytes"] += parse_size_to_bytes(extra_gb, "GB")
                link["quota_notified"] = False
        from main import schedule_save
        await schedule_save()
        await _send(
            chat_id, f"✅ {extra_gb}GB اضافه شد.",
            [[{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}]],
        )


# ══════════════════════════════════════════════════════════════════════════════
# هندلر callback
# ══════════════════════════════════════════════════════════════════════════════
async def _handle_callback(
    chat_id, message_id, cb_id, data, is_admin: bool = False,
):
    await _answer_cb(cb_id)
    if data == "noop":
        return

    if _is_admin_only_action(data) and not is_admin:
        await _edit(
            chat_id, message_id,
            "⛔️ این بخش فقط برای مدیر است.",
            [[{"text": "🔄 بروزرسانی کانفیگ من", "callback_data": "j:check"}]],
        )
        return

    if data == "j:check":
        await _handle_join_start(chat_id, message_id)
        return

    if data == "sup:start":
        _wizard[str(chat_id)] = {"step": "support_wait", "data": {}}
        await _send(chat_id, "✍️ پیامت رو بنویس:\n\n❌ انصراف: /menu")
        return

    if data == "ref:me":
        user_id = str(chat_id)
        if not USER_LINKS.get(user_id):
            await _send(chat_id, "اول یک کانفیگ بگیر. /menu")
            return
        bot_username = await _get_bot_username()
        if not bot_username:
            await _send(chat_id, "⚠️ فعلاً در دسترس نیست.")
            return
        ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
        ref_count = REFERRALS.get(user_id, {}).get("count", 0)
        template = REFERRAL_SETTINGS.get("message_template", "{ref_link}")
        try:
            text = template.format(
                bonus_gb=REFERRAL_SETTINGS.get("bonus_gb", 5),
                ref_link=ref_link, ref_count=ref_count,
            )
        except Exception:
            text = (
                f"🔗 لینک رفرال:\n<code>{ref_link}</code>\n\n"
                f"✅ رفرال موفق: {ref_count}"
            )
        if not REFERRAL_SETTINGS.get("enabled", True):
            text += "\n\n⚠️ سیستم رفرال موقتاً غیرفعاله."
        await _send(chat_id, text)
        return

    if data == "ref:board":
        await _send_leaderboard(chat_id)
        return

    if data.startswith("sup:reply:"):
        target = data.split(":", 2)[2]
        _wizard[str(chat_id)] = {"step": "support_reply_wait", "data": {"target": target}}
        await _send(chat_id, f"✍️ پاسخ به <code>{target}</code>:")
        return

    if data == "m:broadcast":
        _wizard[str(chat_id)] = {"step": "broadcast_wait", "data": {}}
        await _send(chat_id, "📢 متن پیام همگانی رو بفرست:\n\n❌ انصراف: /menu")
        return

    if data == "m:main":
        _wizard.pop(str(chat_id), None)
        if is_admin:
            await _show_main_menu(chat_id, message_id)
        else:
            await _handle_join_start(chat_id, message_id)

    elif data == "m:new":
        await _wizard_start(chat_id, message_id)

    elif data.startswith("m:list:"):
        await _show_list(chat_id, message_id, int(data.split(":")[2]))

    elif data == "m:stats":
        await _show_stats(chat_id, message_id)

    elif data == "m:search":
        _wizard[str(chat_id)] = {"step": "search", "data": {}}
        await _edit(
            chat_id, message_id, "🔍 بخشی از اسم کانفیگ رو بفرست:",
            [[{"text": "❌ انصراف", "callback_data": "m:main"}]],
        )

    elif data.startswith("m:subs:"):
        await _show_subs(chat_id, message_id, int(data.split(":")[2]))

    elif data.startswith("m:copy:"):
        uid = data.split(":", 2)[2]
        if not is_admin and USER_LINKS.get(str(chat_id)) != uid:
            await _answer_cb(cb_id, "⛔️ اجازه دسترسی نداری.")
            return
        host = _safe_host()
        await _send(chat_id, f"✅ لینک ساب:\n\n<code>https://{host}/sub/{uid}</code>")

    elif data.startswith("q:"):
        val = data[2:]
        w = _wizard.get(str(chat_id))
        if not w:
            return
        if val == "custom":
            w["step"] = "quota_custom"
            await _edit(
                chat_id, message_id, "✏️ مقدار حجم (گیگابایت):",
                [[{"text": "❌ انصراف", "callback_data": "m:main"}]],
            )
        else:
            w["data"]["quota_gb"] = float(val)
            w["step"] = "expiry"
            await _wizard_ask_expiry(chat_id, message_id)

    elif data.startswith("e:"):
        val = data[2:]
        w = _wizard.get(str(chat_id))
        if not w:
            return
        if val == "custom":
            w["step"] = "expiry_custom"
            await _edit(
                chat_id, message_id, "✏️ تعداد روز:",
                [[{"text": "❌ انصراف", "callback_data": "m:main"}]],
            )
        else:
            w["data"]["expiry_days"] = float(val) if val != "0" else None
            await _wizard_finish(chat_id, message_id)

    elif data.startswith("l:"):
        await _show_link_detail(chat_id, message_id, data[2:])

    elif data.startswith("lt:"):
        uid = data[3:]
        async with LINKS_LOCK:
            link = LINKS.get(uid)
            if link:
                link["active"] = not link.get("active", True)
        from main import schedule_save
        await schedule_save()
        await _show_link_detail(chat_id, message_id, uid)

    elif data.startswith("lr:"):
        uid = data[3:]
        async with LINKS_LOCK:
            link = LINKS.get(uid)
            if link:
                link["used_bytes"] = 0
                link["quota_notified"] = False
        from main import schedule_save
        await schedule_save()
        await _answer_cb(cb_id, "مصرف ریست شد ✓")
        await _show_link_detail(chat_id, message_id, uid)

    elif data.startswith("li:"):
        uid = data[3:]
        _wizard[str(chat_id)] = {"step": "increase_quota", "data": {"uid": uid}}
        await _edit(
            chat_id, message_id, "✏️ چند گیگابایت اضافه شود؟",
            [[{"text": "❌ انصراف", "callback_data": "m:main"}]],
        )

    elif data.startswith("lg:"):
        await _send_link_and_qr(chat_id, data[3:])

    elif data.startswith("ldc:"):
        uid = data[4:]
        async with LINKS_LOCK:
            label = LINKS.get(uid, {}).get("label", uid)
            LINKS.pop(uid, None)
        from main import schedule_save
        await schedule_save()
        log_activity("link", f"«{label}» حذف شد", "warn")
        await _edit(
            chat_id, message_id, f"🗑 «{html.escape(label)}» حذف شد.",
            [[{"text": "⬅️ لیست", "callback_data": "m:list:0"}]],
        )

    elif data.startswith("ldn:"):
        await _show_link_detail(chat_id, message_id, data[4:])

    elif data.startswith("ld:"):
        uid = data[3:]
        await _edit(
            chat_id, message_id, "⚠️ مطمئنی حذف شود؟",
            [
                [{"text": "✅ بله", "callback_data": f"ldc:{uid}"},
                 {"text": "❌ نه", "callback_data": f"ldn:{uid}"}],
            ],
        )

    elif data.startswith("st:"):
        await _toggle_sub_lock(chat_id, message_id, data[3:])

    elif data == "m:ref":
        await _show_referral_admin(chat_id, message_id)

    elif data == "ref:toggle":
        REFERRAL_SETTINGS["enabled"] = not REFERRAL_SETTINGS.get("enabled", True)
        await save_state()
        await _show_referral_admin(chat_id, message_id)

    elif data == "ref:setbonus":
        _wizard[str(chat_id)] = {"step": "ref_bonus_wait", "data": {}}
        await _send(chat_id, f"مقدار فعلی: {REFERRAL_SETTINGS.get('bonus_gb', 5)} گیگ\nمقدار جدید:")

    elif data == "ref:setdaily":
        _wizard[str(chat_id)] = {"step": "ref_daily_wait", "data": {}}
        cur = REFERRAL_SETTINGS.get("max_daily_credits", 0)
        cur_txt = "بدون سقف" if cur <= 0 else str(cur)
        await _send(chat_id, f"سقف فعلی: {cur_txt}\nعدد جدید (۰=نامحدود):")

    elif data == "ref:settemplate":
        _wizard[str(chat_id)] = {"step": "ref_template_wait", "data": {}}
        await _send(
            chat_id,
            "متن جدید رو بفرست. متغیرها:\n"
            "<code>{bonus_gb}</code> <code>{ref_link}</code> <code>{ref_count}</code>\n\n"
            f"متن فعلی:\n{REFERRAL_SETTINGS.get('message_template', '')}",
        )

    elif data == "ref:givepoints":
        _wizard[str(chat_id)] = {"step": "ref_points_uid_wait", "data": {}}
        await _send(chat_id, "آیدی عددی کاربر (chat_id):")

    elif data == "m:filter":
        await _show_filter_admin(chat_id, message_id)

    elif data == "filter:toggle:ads":
        FILTER_SETTINGS["block_ads"] = not FILTER_SETTINGS.get("block_ads", False)
        await save_state()
        await _show_filter_admin(chat_id, message_id)

    elif data == "filter:toggle:adult":
        FILTER_SETTINGS["block_adult"] = not FILTER_SETTINGS.get("block_adult", False)
        await save_state()
        await _show_filter_admin(chat_id, message_id)

    elif data == "filter:refreshadult":
        await _answer_cb(cb_id, "در حال دانلود لیست...")
        count = await refresh_adult_blocklist()
        if count < 0:
            await _send(chat_id, "❌ دانلود لیست ناموفق بود. لیست قبلی دست‌نخورده مونده.")
        else:
            await _send(chat_id, f"✅ لیست بزرگسال بروزرسانی شد: {count} دامنه.")
            log_activity("system", f"لیست بزرگسال بروزرسانی شد ({count} دامنه)", "ok")
        await _show_filter_admin(chat_id, message_id)

    elif data == "filter:addcustom":
        _wizard[str(chat_id)] = {"step": "filter_addcustom_cat_wait", "data": {}}
        await _send(chat_id, "دسته رو بنویس: <code>ads</code> یا <code>adult</code>")


# ══════════════════════════════════════════════════════════════════════════════
# گروه‌های ساب
# ══════════════════════════════════════════════════════════════════════════════
async def _show_subs(chat_id, message_id, page: int):
    async with SUBS_LOCK:
        items = sorted(
            SUBS.items(),
            key=lambda kv: kv[1].get("created_at", ""),
            reverse=True,
        )
    total = len(items)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, pages - 1))
    chunk = items[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]

    kb = []
    for sid, s in chunk:
        locked = s.get("locked", False)
        kb.append([
            {
                "text": f"{'🔒' if locked else '📂'} {html.escape(s.get('name', '?'))} ({len(s.get('link_ids', []))})",
                "callback_data": "noop",
            },
            {
                "text": f"{'🔓 باز کن' if locked else '🔒 قفل کن'}",
                "callback_data": f"st:{sid}",
            },
        ])

    nav = []
    if page > 0:
        nav.append({"text": "◀️ قبلی", "callback_data": f"m:subs:{page - 1}"})
    nav.append({"text": f"{page + 1}/{pages}", "callback_data": "noop"})
    if page < pages - 1:
        nav.append({"text": "بعدی ▶️", "callback_data": f"m:subs:{page + 1}"})
    kb.append(nav)
    kb.append([{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}])

    text = f"📂 <b>گروه‌های ساب</b> ({total} گروه)" if total else "هنوز گروه سابی ساخته نشده."
    await _edit(chat_id, message_id, text, kb)


async def _toggle_sub_lock(chat_id, message_id, sub_id):
    name = ""
    locked = False
    async with SUBS_LOCK:
        s = SUBS.get(sub_id)
        if s:
            s["locked"] = not s.get("locked", False)
            name = s.get("name", "")
            locked = s["locked"]
    from main import schedule_save
    await schedule_save()
    if name:
        log_activity("sub", f"گروه «{name}» {'قفل' if locked else 'باز'} شد", "warn" if locked else "ok")
    await _show_subs(chat_id, message_id, 0)


# ══════════════════════════════════════════════════════════════════════════════
# پردازش آپدیت‌های تلگرام
# ══════════════════════════════════════════════════════════════════════════════
async def _process_update(update: dict):
    try:
        if "callback_query" in update:
            cq = update["callback_query"]
            chat_id = cq["message"]["chat"]["id"]
            _remember_display_name(chat_id, cq.get("from") or {})
            await _handle_callback(
                chat_id,
                cq["message"]["message_id"],
                cq["id"],
                cq.get("data", ""),
                _is_admin(chat_id),
            )
        elif "message" in update:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            await _handle_text(
                chat_id, msg.get("text", ""),
                _is_admin(chat_id), msg.get("from") or {},
            )
    except Exception as e:
        logger.warning("telegram_bot: process_update error: %s", e)


# ══════════════════════════════════════════════════════════════════════════════
# حلقه Polling اصلی
# ══════════════════════════════════════════════════════════════════════════════
async def polling_loop():
    global _offset, _running
    _running = True
    logger.info("telegram_bot: polling loop started")
    
    await _get_bot_username()

    # دور ریختن آپدیت‌های قدیمی
    try:
        pending = await _api("getUpdates", {"offset": -1, "timeout": 0})
        if pending:
            _offset = pending[-1]["update_id"] + 1
    except Exception:
        pass

    consecutive_errors = 0
    while True:
        try:
            if not (TELEGRAM_SETTINGS.get("enabled") and TELEGRAM_SETTINGS.get("bot_token")):
                await asyncio.sleep(5)
                continue
            
            result = await _api("getUpdates", {
                "offset": _offset,
                "timeout": 25,
                "allowed_updates": ["message", "callback_query"],
            })
            
            if result is None:
                consecutive_errors += 1
                await asyncio.sleep(min(60, 5 * (2 ** min(consecutive_errors, 4))))
                continue
                
            consecutive_errors = 0
            for update in result:
                _offset = update["update_id"] + 1
                await _process_update(update)
                
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.warning("telegram_bot: polling_loop error: %s", e)
            consecutive_errors += 1
            await asyncio.sleep(min(60, 5 * (2 ** min(consecutive_errors, 4))))
            
    _running = False
    logger.info("telegram_bot: polling loop stopped")


# ══════════════════════════════════════════════════════════════════════════════
# نظارت خودکار عضویت کانال (قفل/بازکردن کانفیگ بر اساس عضویت)
# ══════════════════════════════════════════════════════════════════════════════
CHANNEL_WATCH_INTERVAL = 600   # هر ۱۰ دقیقه
CHANNEL_WATCH_STAGGER = 0.35   # فاصله بین هر چک (ثانیه)

async def channel_watch_loop():
    logger.info("telegram_bot: channel watch loop started")
    while True:
        try:
            if not (TELEGRAM_SETTINGS.get("enabled") and 
                    TELEGRAM_SETTINGS.get("bot_token") and 
                    JOIN_SETTINGS.get("channel_required")):
                await asyncio.sleep(60)
                continue

            # گرفتن اسنپشات برای رها کردن قفل سریعاً
            async with LINKS_LOCK:
                to_check = [
                    (uid, d["join_user"]) 
                    for uid, d in LINKS.items() if d.get("join_user")
                ]

            for uid, user_id in to_check:
                # بررسی وضعیت عضویت (سه‌حالته)
                status = await check_channel_membership_status(user_id)
                
                # اگر نامعلوم بود (خطای شبکه و...) کانفیگ را دست نزن
                if status is None:
                    await asyncio.sleep(CHANNEL_WATCH_STAGGER)
                    continue

                async with LINKS_LOCK:
                    link = LINKS.get(uid)
                    if not link or not link.get("join_user"):
                        continue

                    # اگر رفته و هنوز فعال است → غیرفعال کن
                    if not status and link.get("active") and not link.get("disabled_by_leave"):
                        link["active"] = False
                        link["disabled_by_leave"] = True
                        label = html.escape(link.get("label", "?"))
                        log_activity("system", f"کانفیگ {uid} به‌خاطر ترک کانال غیرفعال شد ({user_id})", "warn")
                        asyncio.create_task(
                            _send(user_id, f"⚠️ کانفیگ «{label}» غیرفعال شد چون عضویتت در کانال قطع شده.\nبرای فعال‌سازی دوباره عضو شو و /menu رو بزن.")
                        )

                    # اگر برگشته و قبلاً توسط همین سیستم غیرفعال شده → فعال کن
                    elif status and link.get("disabled_by_leave"):
                        link["active"] = True
                        link["disabled_by_leave"] = False
                        label = html.escape(link.get("label", "?"))
                        log_activity("system", f"کانفیگ {uid} به‌خاطر بازگشت به کانال فعال شد ({user_id})", "ok")
                        asyncio.create_task(
                            _send(user_id, f"✅ کانفیگ «{label}» دوباره فعال شد. خوش امدی!")
                        )

                await asyncio.sleep(CHANNEL_WATCH_STAGGER)

        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.warning("channel_watch_loop error: %s", e)

        await asyncio.sleep(CHANNEL_WATCH_INTERVAL)
