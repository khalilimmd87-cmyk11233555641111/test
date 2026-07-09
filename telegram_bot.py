# telegram_bot.py
# ══════════════════════════════════════════════════════════════════════════════
# مدیریت پنل از طریق بات تلگرام — دو-طرفه (نه فقط نوتیفیکیشن)
# سیستم رفرال کامل حذف شده. هرکسی وارد بات شود (/start)، پس از تأیید عضویت
# اجباری در کانال، به‌طور خودکار یک کانفیگ اختصاصی با حجم هدیه (پیش‌فرض ۱۰۰GB)
# دریافت می‌کند. پنل مدیریتی فقط برای ادمین (chat_id های تنظیم‌شده) باز است.
# ══════════════════════════════════════════════════════════════════════════════
import asyncio
from datetime import datetime
from urllib.parse import quote as _urlquote

from state import (
    LINKS, LINKS_LOCK, SUBS, SUBS_LOCK,
    TELEGRAM_SETTINGS, connections, stats,
    generate_uuid, generate_all_vless_links,
    is_link_allowed, is_link_expired, fmt_bytes, parse_size_to_bytes,
    parse_expiry_to_timedelta, get_host, log_activity, logger,
    DEFAULT_PROTOCOL, uptime,
    JOIN_SETTINGS, USER_LINKS,
    check_channel_membership, create_join_link,
    save_state,
)

PAGE_SIZE = 6
_offset = 0
_wizard: dict[str, dict] = {}
_running = False


def _allowed_chats() -> set[str]:
    raw = (TELEGRAM_SETTINGS.get("chat_id") or "").strip()
    if not raw:
        return set()
    return {p.strip() for p in raw.replace(";", ",").split(",") if p.strip()}


def _is_admin(chat_id) -> bool:
    """ادمین یعنی chat_id داخل لیست TELEGRAM_SETTINGS.chat_id باشد."""
    return str(chat_id) in _allowed_chats()


# ── یوزرنیم بات: خودکار از API تلگرام (getMe) گرفته می‌شود ─────────────────────
# قبلاً از یک فیلد دستی (TELEGRAM_SETTINGS["bot_username"]) خونده می‌شد که اگر
# خالی می‌ماند، لینک رفرال به‌صورت t.me/bot?start=... یا t.me/?start=... ساخته
# می‌شد که آدرس معتبری نیست و مرورگر آن را به گوگل هدایت می‌کرد. این تابع به‌جای
# آن، یوزرنیم واقعی بات را مستقیماً از تلگرام می‌گیرد و کش می‌کند.
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


# دسته‌بندی‌های callback که فقط مخصوص ادمین است (مدیریت کانفیگ‌ها، آمار، گروه‌های ساب و ...)
ADMIN_ONLY_PREFIXES = (
    "m:new", "m:list:", "m:stats", "m:search", "m:subs:",
    "q:", "e:", "l:", "lt:", "lr:", "li:", "lg:", "ld", "st:",
)


def _is_admin_only_action(data: str) -> bool:
    return any(data == p or data.startswith(p) for p in ADMIN_ONLY_PREFIXES)


def _channel_username() -> str:
    return (JOIN_SETTINGS.get("channel_username", "TimAzadi") or "TimAzadi").strip().lstrip("@")


def _safe_host() -> str:
    """
    get_host() را می‌گیرد؛ قبلاً وقتی RAILWAY_PUBLIC_DOMAIN تنظیم نبود این تابع
    یک دامین هارد-کد شده‌ی متعلق به یک دیپلوی دیگر (mmd-mimi-mikham.up.railway.app)
    برمی‌گرداند که باعث می‌شد لینک‌های کاربران به یک سایت اشتباه/غیرمرتبط اشاره کند.
    حالا در این حالت فقط لاگ هشدار می‌زند و از CONFIG['host'] واقعی استفاده می‌کند.
    """
    host = get_host()
    if not host or host == "localhost":
        logger.warning(
            "RAILWAY_PUBLIC_DOMAIN تنظیم نشده — لینک‌های ساخته‌شده ممکن است نادرست باشند؛ "
            "این متغیر را در Railway تنظیم کن."
        )
    return host


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
            logger.warning(f"telegram_bot: {method} failed: {data}")
            return None
        return data.get("result")
    except Exception as e:
        logger.warning(f"telegram_bot: {method} error: {e}")
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
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML"}
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


def _link_line(uid: str, d: dict) -> str:
    ok = is_link_allowed(d)
    dot = "🟢" if ok else "🔴"
    used = fmt_bytes(d.get("used_bytes", 0))
    limit = "∞" if not d.get("limit_bytes") else fmt_bytes(d["limit_bytes"])
    return f"{dot} {d.get('label','?')} — {used}/{limit}"


def _main_menu_kb():
    return [
        [{"text": "➕ کانفیگ جدید", "callback_data": "m:new"}, {"text": "📋 لیست کانفیگ‌ها", "callback_data": "m:list:0"}],
        [{"text": "📊 آمار سیستم", "callback_data": "m:stats"}, {"text": "🔍 جستجو", "callback_data": "m:search"}],
        [{"text": "📂 گروه‌های ساب", "callback_data": "m:subs:0"}],
    ]


async def _show_main_menu(chat_id, message_id=None):
    text = "🤖 <b>پنل مدیریت تیم آزادی</b>\nیکی از گزینه‌ها رو انتخاب کن:"
    kb = _main_menu_kb()
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


async def _show_list(chat_id, message_id, page: int):
    async with LINKS_LOCK:
        items = sorted(LINKS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(items)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, pages - 1))
    chunk = items[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]
    kb = [[{"text": _link_line(uid, d), "callback_data": f"l:{uid}"}] for uid, d in chunk]
    nav = []
    if page > 0:
        nav.append({"text": "◀️ قبلی", "callback_data": f"m:list:{page-1}"})
    nav.append({"text": f"{page+1}/{pages}", "callback_data": "noop"})
    if page < pages - 1:
        nav.append({"text": "بعدی ▶️", "callback_data": f"m:list:{page+1}"})
    kb.append(nav)
    kb.append([{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}])
    text = f"📋 <b>لیست کانفیگ‌ها</b> ({total} مورد)\nروی هرکدام بزن برای مدیریت:" if total else "هیچ کانفیگی هنوز ساخته نشده."
    await _edit(chat_id, message_id, text, kb)


async def _show_link_detail(chat_id, message_id, uid: str):
    async with LINKS_LOCK:
        d = LINKS.get(uid)
    if not d:
        await _edit(chat_id, message_id, "این کانفیگ دیگر وجود ندارد.", [[{"text": "⬅️ لیست", "callback_data": "m:list:0"}]])
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
            exp_txt = d["expires_at"]
    gift_txt = "\n🎁 این یک کانفیگ هدیه‌داده‌شده است." if d.get("parent_id") else ""
    text = (
        f"🔧 <b>{d.get('label','?')}</b>\n\n"
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
        label = d.get("label", "کانفیگ")
        sub_url = f"https://{host}/sub/{uid}"
        text = f"🔗 <b>{label}</b>\n\n📡 لینک ساب:\n<code>{sub_url}</code>"
        kb = [[{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}]]
        await _send(chat_id, text, kb)
    except Exception:
        await _send(chat_id, "❌ خطا در دریافت لینک. لطفاً دوباره تلاش کنید.")


QUOTA_OPTIONS = [("1GB", 1), ("5GB", 5), ("10GB", 10), ("20GB", 20), ("50GB", 50), ("100GB", 100), ("∞ نامحدود", 0)]
EXPIRY_OPTIONS = [("بدون انقضا", None), ("۱ روز", 1), ("۷ روز", 7), ("۳۰ روز", 30)]


async def _wizard_start(chat_id, message_id):
    _wizard[str(chat_id)] = {"step": "label", "data": {}}
    await _edit(chat_id, message_id, "✏️ اسم این کانفیگ رو بفرست (مثلاً: کاربر علی):", [[{"text": "❌ انصراف", "callback_data": "m:main"}]])


async def _wizard_ask_quota(chat_id, message_id=None):
    kb = [[{"text": t, "callback_data": f"q:{v}"} for t, v in QUOTA_OPTIONS[i:i+2]] for i in range(0, len(QUOTA_OPTIONS), 2)]
    kb.append([{"text": "✏️ مقدار دلخواه (GB)", "callback_data": "q:custom"}])
    kb.append([{"text": "❌ انصراف", "callback_data": "m:main"}])
    text = "📦 چه مقدار حجم بدیم؟"
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


async def _wizard_ask_expiry(chat_id, message_id=None):
    kb = [[{"text": t, "callback_data": f"e:{v if v is not None else 0}"} for t, v in EXPIRY_OPTIONS[i:i+2]] for i in range(0, len(EXPIRY_OPTIONS), 2)]
    kb.append([{"text": "✏️ مقدار دلخواه (روز)", "callback_data": "e:custom"}])
    kb.append([{"text": "❌ انصراف", "callback_data": "m:main"}])
    text = "⏰ تا کِی معتبر باشه؟"
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


async def _wizard_finish(chat_id, message_id=None):
    w = _wizard.pop(str(chat_id), None)
    if not w:
        return
    d = w["data"]
    label = d.get("label", "کانفیگ جدید")[:60]
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
            "label": label, "limit_bytes": limit_bytes, "used_bytes": 0,
            "created_at": datetime.now().isoformat(), "active": True,
            "expires_at": expires_at, "note": "از بات تلگرام ساخته شد",
            "is_default": False, "sub_id": None, "protocol": DEFAULT_PROTOCOL,
            "parent_id": None, "white_label": False, "flag": "🇺🇸",
            "max_devices": 0, "quota_notified": False, "expiry_notified": False,
        }
    from main import schedule_save
    await schedule_save()
    log_activity("link", f"کانفیگ «{label}» از بات تلگرام ساخته شد", "ok")
    limit_txt = "∞" if not limit_bytes else fmt_bytes(limit_bytes)
    exp_txt = "بدون انقضا" if not expires_at else f"{exp_days} روز دیگر"
    text = f"✅ کانفیگ ساخته شد!\n\n<b>{label}</b>\nحجم: {limit_txt}\nانقضا: {exp_txt}"
    kb = [[{"text": "🔗 دریافت لینک/QR", "callback_data": f"lg:{uid}"}], [{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}]]
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


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
    await _edit(chat_id, message_id, text, [[{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}]])


async def _handle_join_start(chat_id, message_id=None):
    """هر کاربر عادی که /start یا /menu بزند از این مسیر عبور می‌کند."""
    user_id = str(chat_id)

    # اگر کاربر قبلاً کانفیگ خودش را گرفته، دیگر لازم نیست دوباره چک عضویت شود؛
    # مستقیم همان لینک قبلی‌اش را نشان بده.
    existing_uid = USER_LINKS.get(user_id)
    if existing_uid and existing_uid in LINKS:
        await _grant_join_link(chat_id, message_id)
        return

    if JOIN_SETTINGS.get("channel_required", True):
        is_member = await check_channel_membership(user_id, TELEGRAM_SETTINGS.get("bot_token"))
        if not is_member:
            channel = _channel_username()
            text = (
                "❌ برای دریافت کانفیگ رایگان، ابتدا باید در کانال تیم آزادی عضو شوید.\n\n"
                "📢 لطفاً عضو کانال شوید:\n"
                f"👉 https://t.me/{channel}\n\n"
                "سپس روی دکمه‌ی زیر بزنید."
            )
            kb = [[{"text": "🔄 بررسی مجدد عضویت", "callback_data": "j:check"}]]
            if message_id:
                await _edit(chat_id, message_id, text, kb)
            else:
                await _send(chat_id, text, kb)
            return

    await _grant_join_link(chat_id, message_id)


async def _grant_join_link(chat_id, message_id=None):
    """کانفیگ اختصاصی کاربر را می‌سازد (اگر قبلاً نساخته) و نشان می‌دهد."""
    user_id = str(chat_id)
    uid = USER_LINKS.get(user_id)
    if not uid or uid not in LINKS:
        uid = await create_join_link(user_id)
    d = LINKS.get(uid) if uid else None
    if not uid or not d:
        text = "❌ خطا در ساخت کانفیگ. لطفاً بعداً دوباره تلاش کنید."
        kb = [[{"text": "🔄 تلاش مجدد", "callback_data": "j:check"}]]
        if message_id:
            await _edit(chat_id, message_id, text, kb)
        else:
            await _send(chat_id, text, kb)
        return

    host = _safe_host()
    sub_url = f"https://{host}/sub/{uid}"
    limit_txt = "∞" if not d.get("limit_bytes") else fmt_bytes(d["limit_bytes"])
    exp_txt = "بدون انقضا"
    if d.get("expires_at"):
        try:
            exp_txt = datetime.fromisoformat(d["expires_at"]).strftime("%Y-%m-%d %H:%M")
        except Exception:
            exp_txt = d["expires_at"]
    text = (
        "🎉 <b>خوش اومدی به تیم آزادی!</b>\n\n"
        "🔗 <b>لینک ساب اختصاصی شما:</b>\n"
        f"<code>{sub_url}</code>\n\n"
        f"📦 حجم اختصاصی: {limit_txt}\n"
        f"⏰ انقضا: {exp_txt}\n\n"
        f"📢 کانال تیم آزادی:\nhttps://t.me/{_channel_username()}"
    )
    kb = [
        [{"text": "🔗 کپی لینک ساب", "callback_data": f"m:copy:{uid}"}],
        [{"text": "🔄 بروزرسانی وضعیت", "callback_data": "j:check"}],
    ]
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


async def _handle_text(chat_id, text, is_admin: bool = False):
    w = _wizard.get(str(chat_id))
    text = (text or "").strip()

    if text.startswith("/start"):
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

    if not is_admin:
        # مراحل ویزارد ساخت کانفیگ فقط برای ادمین است؛ کاربر عادی همیشه به فلوی دریافت کانفیگ می‌رود
        _wizard.pop(str(chat_id), None)
        await _handle_join_start(chat_id)
        return

    if not w:
        await _send(chat_id, "برای شروع /menu رو بزن یا از دکمه‌های پایین پیام‌های قبلی استفاده کن.")
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
            await _send(chat_id, "عدد معتبر نبود؛ دوباره بفرست (مثلاً 7.5):")
            return
        w["step"] = "expiry"
        await _wizard_ask_expiry(chat_id)
    elif step == "expiry_custom":
        try:
            w["data"]["expiry_days"] = max(0.0, float(text.replace(",", ".")))
        except ValueError:
            await _send(chat_id, "عدد معتبر نبود؛ دوباره بفرست (مثلاً 3):")
            return
        await _wizard_finish(chat_id)
    elif step == "search":
        _wizard.pop(str(chat_id), None)
        q = text.lower()
        async with LINKS_LOCK:
            hits = [(uid, d) for uid, d in LINKS.items() if q in d.get("label", "").lower()][:20]
        if not hits:
            await _send(chat_id, "چیزی پیدا نشد.", [[{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}]])
            return
        kb = [[{"text": _link_line(uid, d), "callback_data": f"l:{uid}"}] for uid, d in hits]
        kb.append([{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}])
        await _send(chat_id, f"🔍 {len(hits)} نتیجه:", kb)
    elif step == "increase_quota":
        uid = w["data"]["uid"]
        try:
            extra_gb = max(0.0, float(text.replace(",", ".")))
        except ValueError:
            await _send(chat_id, "عدد معتبر نبود؛ دوباره بفرست:")
            return
        _wizard.pop(str(chat_id), None)
        async with LINKS_LOCK:
            link = LINKS.get(uid)
            if link:
                if link.get("limit_bytes", 0) == 0:
                    await _send(chat_id, "این کانفیگ نامحدود است؛ افزایش حجم لازم نیست.")
                    return
                link["limit_bytes"] += parse_size_to_bytes(extra_gb, "GB")
                link["quota_notified"] = False
        from main import schedule_save
        await schedule_save()
        await _send(chat_id, f"✅ {extra_gb}GB اضافه شد.", [[{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}]])


async def _handle_callback(chat_id, message_id, cb_id, data, is_admin: bool = False):
    await _answer_cb(cb_id)
    if data == "noop":
        return

    if _is_admin_only_action(data) and not is_admin:
        await _edit(
            chat_id, message_id, "⛔️ این بخش فقط برای مدیر پنل در دسترس است.",
            [[{"text": "🔄 بروزرسانی وضعیت کانفیگ من", "callback_data": "j:check"}]]
        )
        return

    if data == "j:check":
        await _handle_join_start(chat_id, message_id)
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
        await _edit(chat_id, message_id, "🔍 بخشی از اسم کانفیگ رو بفرست:", [[{"text": "❌ انصراف", "callback_data": "m:main"}]])
    elif data.startswith("m:subs:"):
        await _show_subs(chat_id, message_id, int(data.split(":")[2]))
    elif data.startswith("m:copy:"):
        uid = data.split(":", 2)[2]
        # قبلاً این هندلر بدون هیچ چک مالکیتی، لینک ساب هر uuid ارسالی در callback_data را
        # برمی‌گرداند؛ حالا فقط ادمین یا خودِ صاحب آن کانفیگ می‌تواند لینکش را از این مسیر بگیرد.
        if not is_admin and USER_LINKS.get(str(chat_id)) != uid:
            await _answer_cb(cb_id, "⛔️ اجازه دسترسی به این کانفیگ را نداری.")
            return
        host = _safe_host()
        await _send(chat_id, f"✅ لینک ساب کپی شد!\n\n<code>https://{host}/sub/{uid}</code>")
    elif data.startswith("q:"):
        val = data[2:]
        w = _wizard.get(str(chat_id))
        if not w:
            return
        if val == "custom":
            w["step"] = "quota_custom"
            await _edit(chat_id, message_id, "✏️ مقدار حجم رو به گیگابایت بفرست (مثلاً 7.5):", [[{"text": "❌ انصراف", "callback_data": "m:main"}]])
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
            await _edit(chat_id, message_id, "✏️ تعداد روز رو بفرست (مثلاً 3):", [[{"text": "❌ انصراف", "callback_data": "m:main"}]])
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
        await _edit(chat_id, message_id, "✏️ چند گیگابایت اضافه شود؟ (مثلاً 5):", [[{"text": "❌ انصراف", "callback_data": "m:main"}]])
    elif data.startswith("lg:"):
        await _send_link_and_qr(chat_id, data[3:])
    elif data.startswith("ldc:"):
        uid = data[4:]
        async with LINKS_LOCK:
            label = LINKS.get(uid, {}).get("label", uid)
            LINKS.pop(uid, None)
        from main import schedule_save
        await schedule_save()
        log_activity("link", f"کانفیگ «{label}» از بات تلگرام حذف شد", "warn")
        await _edit(chat_id, message_id, f"🗑 «{label}» حذف شد.", [[{"text": "⬅️ لیست", "callback_data": "m:list:0"}]])
    elif data.startswith("ldn:"):
        await _show_link_detail(chat_id, message_id, data[4:])
    elif data.startswith("ld:"):
        uid = data[3:]
        await _edit(chat_id, message_id, "⚠️ مطمئنی این کانفیگ کامل حذف شود؟ این عمل قابل بازگشت نیست.",
                     [[{"text": "✅ بله، حذف شود", "callback_data": f"ldc:{uid}"}, {"text": "❌ نه", "callback_data": f"ldn:{uid}"}]])
    elif data.startswith("st:"):
        sub_id = data[3:]
        await _toggle_sub_lock(chat_id, message_id, sub_id)


async def _show_subs(chat_id, message_id, page: int):
    async with SUBS_LOCK:
        items = sorted(SUBS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(items)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, pages - 1))
    chunk = items[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]
    kb = []
    for sid, s in chunk:
        lock_icon = "🔒" if s.get("locked") else "🔓"
        kb.append([
            {"text": f"{'🔒' if s.get('locked') else '📂'} {s.get('name','?')} ({len(s.get('link_ids', []))})", "callback_data": "noop"},
            {"text": f"{lock_icon} {'باز کن' if s.get('locked') else 'قفل کن'}", "callback_data": f"st:{sid}"},
        ])
    nav = []
    if page > 0:
        nav.append({"text": "◀️ قبلی", "callback_data": f"m:subs:{page-1}"})
    nav.append({"text": f"{page+1}/{pages}", "callback_data": "noop"})
    if page < pages - 1:
        nav.append({"text": "بعدی ▶️", "callback_data": f"m:subs:{page+1}"})
    kb.append(nav)
    kb.append([{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}])
    text = f"📂 <b>گروه‌های ساب</b> ({total} گروه)" if total else "هنوز هیچ گروه سابی ساخته نشده."
    await _edit(chat_id, message_id, text, kb)


async def _toggle_sub_lock(chat_id, message_id, sub_id):
    async with SUBS_LOCK:
        s = SUBS.get(sub_id)
        if s:
            s["locked"] = not s.get("locked")
            name, locked = s["name"], s["locked"]
    from main import schedule_save
    await schedule_save()
    if s:
        log_activity("sub", f"گروه «{name}» از بات تلگرام {'قفل' if locked else 'باز'} شد", "warn" if locked else "ok")
    await _show_subs(chat_id, message_id, 0)


async def _process_update(update: dict):
    try:
        if "callback_query" in update:
            cq = update["callback_query"]
            chat_id = cq["message"]["chat"]["id"]
            await _handle_callback(chat_id, cq["message"]["message_id"], cq["id"], cq.get("data", ""), _is_admin(chat_id))
        elif "message" in update:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            await _handle_text(chat_id, msg.get("text", ""), _is_admin(chat_id))
    except Exception as e:
        logger.warning(f"telegram_bot: process_update error: {e}")


async def polling_loop():
    global _offset, _running
    _running = True
    logger.info("telegram_bot: polling loop started")
    await _get_bot_username()  # پیش‌گرم کردن کش یوزرنیم بات تا لینک رفرال از همون اول درست باشد

    # آپدیت‌های قدیمی/باقی‌مانده از قبل از استارت را فقط یک‌بار در ابتدا دور بریز؛
    # قبلاً drop_pending_updates روی هر تک تک درخواست‌های getUpdates فرستاده می‌شد که
    # اصلاً پارامتر معتبری برای این متد نیست (فقط برای setWebhook/deleteWebhook تعریف شده)
    # و صرفاً نادیده گرفته می‌شد؛ اینجا کار درستش را یک‌بار با offset=-1 انجام می‌دهیم.
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
                # چند بار پشت‌سرهم خطا یعنی احتمالاً توکن غلط است یا تلگرام موقتاً محدودمان کرده؛
                # backoff نمایی می‌زنیم تا به جای اسپم کردن API، فشار را کم کنیم و ریت‌لیمیت/بن نشویم.
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
            logger.warning(f"telegram_bot: polling_loop error: {e}")
            consecutive_errors += 1
            await asyncio.sleep(min(60, 5 * (2 ** min(consecutive_errors, 4))))
    _running = False
    logger.info("telegram_bot: polling loop stopped")


# ══════════════════════════════════════════════════════════════════════════════
# فیچر: قفل/بازکردن خودکار کانفیگ بر اساس عضویت در کانال
# هر چند دقیقه یک‌بار عضویت کاربرانی که کانفیگشان را از مسیر «ورود به بات + عضویت
# در کانال» گرفته‌اند (link["join_user"] ست شده) چک می‌شود:
#   - اگر کانال را ترک کرده و کانفیگش فعال است → غیرفعال می‌شود + پیام هشدار.
#   - اگر دوباره عضو شده و قبلاً همین سیستم غیرفعالش کرده بود → دوباره فعال می‌شود + پیام اطلاع.
# کانفیگ‌هایی که ادمین دستی ساخته (join_user ندارند) هرگز دست‌خورده نمی‌شوند.
# توجه: این پیام از طریق خودِ بات تلگرام فرستاده می‌شود، نه پیامک واقعی — این
# پروژه هیچ سرویس ارسال SMS ندارد.
# ══════════════════════════════════════════════════════════════════════════════
CHANNEL_WATCH_INTERVAL = 600   # هر ۱۰ دقیقه یک دور کامل چک
CHANNEL_WATCH_STAGGER = 0.35   # فاصله بین هر getChatMember تا به API تلگرام فشار نیاریم و ریت‌لیمیت/بن نشیم


async def channel_watch_loop():
    logger.info("telegram_bot: channel_watch_loop started")
    while True:
        await asyncio.sleep(CHANNEL_WATCH_INTERVAL)
        try:
            if not (TELEGRAM_SETTINGS.get("enabled") and TELEGRAM_SETTINGS.get("bot_token")):
                continue
            if not JOIN_SETTINGS.get("channel_required", True):
                continue

            async with LINKS_LOCK:
                # اسنپ‌شات می‌گیریم تا در طول چک عضویت (که چند ثانیه طول می‌کشد) قفل را نگه نداریم
                candidates = [(uid, d.get("join_user")) for uid, d in LINKS.items() if d.get("join_user")]

            changed = False
            for uid, user_id in candidates:
                if not user_id:
                    continue
                try:
                    is_member = await check_channel_membership(user_id, TELEGRAM_SETTINGS.get("bot_token"))
                except Exception:
                    continue
                await asyncio.sleep(CHANNEL_WATCH_STAGGER)

                async with LINKS_LOCK:
                    link = LINKS.get(uid)
                    if link is None:
                        continue
                    was_active = link.get("active", True)
                    disabled_by_leave = link.get("disabled_by_leave", False)

                    if not is_member and was_active:
                        link["active"] = False
                        link["disabled_by_leave"] = True
                        label = link.get("label", "کانفیگ")
                        action = "disabled"
                    elif is_member and (not was_active) and disabled_by_leave:
                        link["active"] = True
                        link["disabled_by_leave"] = False
                        label = link.get("label", "کانفیگ")
                        action = "enabled"
                    else:
                        continue

                changed = True
                channel = (JOIN_SETTINGS.get("channel_username", "TimAzadi") or "TimAzadi").strip().lstrip("@")
                if action == "disabled":
                    log_activity("sub", f"کانفیگ «{label}» به‌خاطر ترک کانال توسط کاربر {user_id} غیرفعال شد", "warn")
                    await _send(
                        user_id,
                        f"⚠️ متوجه شدیم از کانال @{channel} خارج شدید.\n\n"
                        f"طبق قوانین، کانفیگ رایگان «{label}» شما موقتاً <b>غیرفعال</b> شد.\n"
                        f"برای فعال‌سازی دوباره، کافیه دوباره در کانال عضو بشید — خودکار فعال می‌شه.",
                    )
                else:
                    log_activity("sub", f"کانفیگ «{label}» بعد از بازگشت کاربر {user_id} به کانال دوباره فعال شد", "ok")
                    await _send(
                        user_id,
                        f"✅ عضویت شما در @{channel} دوباره تایید شد.\n\n"
                        f"کانفیگ «{label}» شما دوباره <b>فعال</b> شد. لینک ساب همانی است که قبلاً داشتید.",
                    )

            if changed:
                asyncio.create_task(save_state())
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.warning(f"telegram_bot: channel_watch_loop error: {e}")
