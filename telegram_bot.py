# telegram_bot.py
# ══════════════════════════════════════════════════════════════════════════════
# مدیریت پنل از طریق بات تلگرام — دو-طرفه (نه فقط نوتیفیکیشن)
# با سیستم رفرال و عضویت اجباری در کانال
# عمومی‌سازی شده: همه می‌توانند استفاده کنند
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
    REFERRAL_SETTINGS, REFERRALS, REFERRALS_LOCK,
    USER_LINKS, generate_referral_code,
    check_channel_membership, create_link_from_referral,
    BOT_USERS, BOT_STATS, BOT_SETTINGS,
    add_bot_user, user_can_create_link, add_user_link,
    get_user_links, remove_user_link,
)

PAGE_SIZE = 6
_offset = 0
_wizard: dict[str, dict] = {}
_running = False

# ── دکمه‌های شیشه‌ای (Glassmorphism) ─────────────────────────────────────────
def glass_button(text: str, callback_data: str, style: str = "primary") -> dict:
    """ساخت دکمه شیشه‌ای با استایل‌های مختلف"""
    styles = {
        "primary": {"bg": "rgba(59,130,246,0.2)", "border": "rgba(59,130,246,0.3)"},
        "success": {"bg": "rgba(16,185,129,0.2)", "border": "rgba(16,185,129,0.3)"},
        "danger": {"bg": "rgba(239,68,68,0.2)", "border": "rgba(239,68,68,0.3)"},
        "warning": {"bg": "rgba(245,158,11,0.2)", "border": "rgba(245,158,11,0.3)"},
        "purple": {"bg": "rgba(139,92,246,0.2)", "border": "rgba(139,92,246,0.3)"},
        "glass": {"bg": "rgba(255,255,255,0.08)", "border": "rgba(255,255,255,0.15)"},
    }
    s = styles.get(style, styles["primary"])
    return {"text": text, "callback_data": callback_data}


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


# ── منوی اصلی با دکمه‌های شیشه‌ای و میانبر ──────────────────────────────────
def _main_menu_kb() -> list:
    kb = [
        [
            glass_button("⚡ کانفیگ جدید", "m:new", "primary"),
            glass_button("📋 لیست کانفیگ‌ها", "m:list:0", "glass"),
        ],
        [
            glass_button("📊 آمار سیستم", "m:stats", "purple"),
            glass_button("🔍 جستجو", "m:search", "glass"),
        ],
        [
            glass_button("📂 گروه‌های ساب", "m:subs:0", "warning"),
            glass_button("🎁 رفرال", "m:referral", "success"),
        ],
        [
            glass_button("📖 راهنما", "m:help", "glass"),
        ],
    ]
    
    # دکمه‌های میانبر (Quick Actions)
    kb.append([
        glass_button("⚡ 1GB/7 روز", "m:quick:1:7", "primary"),
        glass_button("⚡ 5GB/30 روز", "m:quick:5:30", "success"),
    ])
    
    # دکمه‌ی تنظیمات برای ادمین
    if TELEGRAM_SETTINGS.get("chat_id") and str(chat_id) in str(TELEGRAM_SETTINGS.get("chat_id", "")).split(","):
        kb.append([glass_button("⚙️ تنظیمات بات", "m:bot_settings", "danger")])
    
    return kb


async def _show_main_menu(chat_id, message_id=None):
    text = """🤖 <b>پنل مدیریت تیم آزادی</b>

یکی از گزینه‌ها رو انتخاب کن:

⚡ <b>کانفیگ جدید</b> — با حجم و انقضای دلخواه
📋 <b>لیست کانفیگ‌ها</b> — مدیریت کانفیگ‌های خودت
📊 <b>آمار سیستم</b> — وضعیت سرور
🔍 <b>جستجو</b> — پیدا کردن کانفیگ
📂 <b>گروه‌های ساب</b> — دسته‌بندی کانفیگ‌ها
🎁 <b>رفرال</b> — معرفی دوستان و دریافت کانفیگ رایگان
📖 <b>راهنما</b> — راهنمای کامل استفاده

💡 <i>برای ساخت سریع، از دکمه‌های میانبر استفاده کن.</i>"""
    kb = _main_menu_kb()
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


async def _show_help(chat_id, message_id=None):
    text = """📖 <b>راهنمای کامل استفاده از بات</b>

🔹 <b>ساخت کانفیگ جدید:</b>
روی دکمه <code>⚡ کانفیگ جدید</code> بزن، سپس اسم، حجم و انقضا رو مشخص کن.

🔹 <b>دکمه‌های میانبر:</b>
با یک کلیک کانفیگ با حجم و زمان مشخص بساز:
• <code>1GB/7 روز</code> — ۱ گیگابایت به مدت ۷ روز
• <code>5GB/30 روز</code> — ۵ گیگابایت به مدت ۳۰ روز

🔹 <b>لیست کانفیگ‌ها:</b>
همه کانفیگ‌های خودت رو ببین و مدیریت کن (فعال/غیرفعال، ریست مصرف، افزایش حجم، حذف).

🔹 <b>رفرال:</b>
با معرفی دوستان، کانفیگ رایگان دریافت کن. لینک رفرال خودت رو به دوستانت بده.

🔹 <b>محدودیت‌ها:</b>
• حداکثر {max_links} کانفیگ برای هر کاربر
• حجم پیش‌فرض: {default_quota} GB
• مدت اعتبار پیش‌فرض: {default_expiry} روز

📢 <b>کانال تیم آزادی:</b>
https://t.me/TimAzadi

❓ سوالی داری؟ به ادمین پیام بده."""
    
    max_links = BOT_SETTINGS.get("max_links_per_user", 5)
    default_quota = BOT_SETTINGS.get("default_quota_gb", 1)
    default_expiry = BOT_SETTINGS.get("default_expiry_days", 7)
    
    text = text.format(max_links=max_links, default_quota=default_quota, default_expiry=default_expiry)
    
    kb = [[glass_button("⬅️ منوی اصلی", "m:main", "glass")]]
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


async def _show_list(chat_id, message_id, page: int):
    user_id = str(chat_id)
    user_links = get_user_links(user_id)
    
    async with LINKS_LOCK:
        items = [(uid, LINKS[uid]) for uid in user_links if uid in LINKS]
        items.sort(key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    
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
    kb.append([glass_button("⬅️ منوی اصلی", "m:main", "glass")])

    text = f"📋 <b>لیست کانفیگ‌های شما</b> ({total} مورد)\nروی هرکدام بزن برای مدیریت:" if total else "❌ شما هنوز هیچ کانفیگی ندارید.\n\nبرای ساخت کانفیگ جدید، روی دکمه <code>⚡ کانفیگ جدید</code> بزن."
    await _edit(chat_id, message_id, text, kb)


async def _show_link_detail(chat_id, message_id, uid: str):
    user_id = str(chat_id)
    user_links = get_user_links(user_id)
    
    if uid not in user_links:
        await _edit(chat_id, message_id, "❌ این کانفیگ متعلق به شما نیست یا حذف شده است.", [[glass_button("⬅️ لیست", "m:list:0", "glass")]])
        return
    
    async with LINKS_LOCK:
        d = LINKS.get(uid)
    if not d:
        await _edit(chat_id, message_id, "❌ این کانفیگ دیگر وجود ندارد.", [[glass_button("⬅️ لیست", "m:list:0", "glass")]])
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
    
    host = get_host()
    sub_url = f"https://{host}/sub/{uid}"
    
    text = f"""
🔧 <b>{d.get('label','?')}</b>

📊 وضعیت: {'🟢 فعال' if ok else ('⏰ منقضی' if expired else '🔴 غیرفعال/اتمام حجم')}
📦 مصرف: {used} از {limit}
⏰ انقضا: {exp_txt}
📡 پروتکل: {d.get('protocol', DEFAULT_PROTOCOL)}
🔗 لینک ساب: <code>{sub_url}</code>
    """
    
    kb = [
        [
            {"text": ("🔒 غیرفعال کن" if d.get("active", True) else "🔓 فعال کن"), "callback_data": f"lt:{uid}"},
            {"text": "♻️ ریست مصرف", "callback_data": f"lr:{uid}"},
        ],
        [
            {"text": "➕ افزایش حجم", "callback_data": f"li:{uid}"},
            {"text": "🔗 لینک/QR", "callback_data": f"lg:{uid}"},
        ],
        [{"text": "🗑 حذف کامل", "callback_data": f"ld:{uid}"}],
        [glass_button("⬅️ لیست", "m:list:0", "glass")],
    ]
    await _edit(chat_id, message_id, text, kb)


async def _send_link_and_qr(chat_id, uid: str):
    try:
        async with LINKS_LOCK:
            d = LINKS.get(uid)
        if not d:
            await _send(chat_id, "❌ این کانفیگ دیگر وجود ندارد.")
            return
        
        host = get_host()
        if not host or host == "localhost":
            host = "mmd-mimi-mikham.up.railway.app"
        
        label = d.get("label", "کانفیگ")
        sub_url = f"https://{host}/sub/{uid}"
        
        # ارسال QR Code
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={_urlquote(sub_url)}"
        
        text = f"🔗 <b>{label}</b>\n\n📡 لینک ساب:\n<code>{sub_url}</code>"
        
        kb = [[glass_button("⬅️ منوی اصلی", "m:main", "glass")]]
        await _send(chat_id, text, kb, photo=qr_url)
            
    except Exception as e:
        logger.warning(f"send_link_and_qr error: {e}")
        await _send(chat_id, "❌ خطا در دریافت لینک. لطفاً دوباره تلاش کنید.")


# ── ویزارد ساخت کانفیگ ───────────────────────────────────────────────────────
QUOTA_OPTIONS = [("1GB", 1), ("5GB", 5), ("10GB", 10), ("20GB", 20), ("50GB", 50), ("100GB", 100), ("∞ نامحدود", 0)]
EXPIRY_OPTIONS = [("بدون انقضا", None), ("۱ روز", 1), ("۷ روز", 7), ("۳۰ روز", 30)]


async def _wizard_start(chat_id, message_id):
    user_id = str(chat_id)
    can_create, msg = user_can_create_link(user_id)
    if not can_create:
        await _edit(chat_id, message_id, f"❌ {msg}", [[glass_button("⬅️ منوی اصلی", "m:main", "glass")]])
        return
    
    _wizard[str(chat_id)] = {"step": "label", "data": {}}
    await _edit(chat_id, message_id, "✏️ اسم این کانفیگ رو بفرست (مثلاً: کاربر علی):", [[glass_button("❌ انصراف", "m:main", "danger")]])


async def _wizard_ask_quota(chat_id, message_id=None):
    kb = [[{"text": t, "callback_data": f"q:{v}"} for t, v in QUOTA_OPTIONS[i:i+2]] for i in range(0, len(QUOTA_OPTIONS), 2)]
    kb.append([{"text": "✏️ مقدار دلخواه (GB)", "callback_data": "q:custom"}])
    kb.append([glass_button("❌ انصراف", "m:main", "danger")])
    text = "📦 چه مقدار حجم بدیم؟"
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


async def _wizard_ask_expiry(chat_id, message_id=None):
    kb = [[{"text": t, "callback_data": f"e:{v if v is not None else 0}"} for t, v in EXPIRY_OPTIONS[i:i+2]] for i in range(0, len(EXPIRY_OPTIONS), 2)]
    kb.append([{"text": "✏️ مقدار دلخواه (روز)", "callback_data": "e:custom"}])
    kb.append([glass_button("❌ انصراف", "m:main", "danger")])
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
            "label": label,
            "limit_bytes": limit_bytes,
            "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "expires_at": expires_at,
            "note": f"ساخته‌شده از بات تلگرام توسط کاربر {chat_id}",
            "is_default": False,
            "sub_id": None,
            "protocol": DEFAULT_PROTOCOL,
            "parent_id": None,
            "white_label": False,
            "flag": "🇺🇸",
            "max_devices": 0,
            "quota_notified": False,
            "expiry_notified": False,
        }
    
    # افزودن به کاربر
    await add_user_link(str(chat_id), uid)
    
    from main import schedule_save
    await schedule_save()
    log_activity("link", f"کانفیگ «{label}» از بات تلگرام توسط {chat_id} ساخته شد", "ok")

    limit_txt = "∞" if not limit_bytes else fmt_bytes(limit_bytes)
    exp_txt = "بدون انقضا" if not expires_at else f"{exp_days} روز دیگر"
    host = get_host()
    sub_url = f"https://{host}/sub/{uid}"
    
    text = f"""✅ <b>کانفیگ ساخته شد!</b>

🔧 <b>{label}</b>
📦 حجم: {limit_txt}
⏰ انقضا: {exp_txt}
🔗 لینک ساب: <code>{sub_url}</code>

💡 برای دریافت QR و مدیریت، روی دکمه‌های زیر بزن."""
    
    kb = [
        [{"text": "🔗 دریافت لینک/QR", "callback_data": f"lg:{uid}"}],
        [{"text": "⚡ کانفیگ جدید", "callback_data": "m:new"}],
        [glass_button("⬅️ منوی اصلی", "m:main", "glass")],
    ]
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


async def _show_stats(chat_id, message_id):
    async with LINKS_LOCK:
        total = len(LINKS)
        active = sum(1 for d in LINKS.values() if is_link_allowed(d))
    
    user_id = str(chat_id)
    user_links = get_user_links(user_id)
    user_active = sum(1 for uid in user_links if uid in LINKS and is_link_allowed(LINKS[uid]))
    
    text = f"""📊 <b>آمار سیستم</b>

🔹 <b>سرور:</b>
• کل کانفیگ‌ها: {total}
• کانفیگ‌های فعال: {active}
• اتصالات زنده: {len(connections)}
• کل ترافیک: {fmt_bytes(stats.get('total_bytes', 0))}
• آپ‌تایم: {uptime()}

👤 <b>شما:</b>
• کانفیگ‌های شما: {len(user_links)}
• کانفیگ‌های فعال شما: {user_active}
"""
    kb = [[glass_button("⬅️ منوی اصلی", "m:main", "glass")]]
    await _edit(chat_id, message_id, text, kb)


async def _show_referral_menu(chat_id, message_id=None):
    user_id = str(chat_id)
    
    if REFERRAL_SETTINGS.get("channel_required", True):
        is_member = await check_channel_membership(user_id)
        if not is_member:
            channel = REFERRAL_SETTINGS.get("channel_username", "TimAzadi")
            text = f"""❌ برای دریافت کانفیگ رفرال، ابتدا باید در کانال تیم آزادی عضو شوید.

📢 لطفاً ابتدا عضو کانال شوید:
👉 https://t.me/{channel}

سپس دوباره روی دکمه کلیک کنید."""
            kb = [[glass_button("🔄 بررسی مجدد", "m:referral_check", "success")]]
            if message_id:
                await _edit(chat_id, message_id, text, kb)
            else:
                await _send(chat_id, text, kb)
            return
    
    user_links = get_user_links(user_id)
    max_links = BOT_SETTINGS.get("max_links_per_user", 5)
    remaining = max(0, max_links - len(user_links))
    
    if remaining <= 0:
        text = f"""❌ شما به حداکثر تعداد کانفیگ مجاز رسیده‌اید.

حداکثر تعداد کانفیگ برای هر کاربر: {max_links}
تعداد کانفیگ‌های شما: {len(user_links)}

برای دریافت کانفیگ جدید، باید یکی از کانفیگ‌های قبلی خود را حذف کنید."""
        kb = [[glass_button("⬅️ منوی اصلی", "m:main", "glass")]]
        if message_id:
            await _edit(chat_id, message_id, text, kb)
        else:
            await _send(chat_id, text, kb)
        return
    
    async with REFERRALS_LOCK:
        existing_code = None
        for code, data in REFERRALS.items():
            if data.get("user_id") == user_id:
                existing_code = code
                break
        
        if not existing_code:
            existing_code = generate_referral_code(user_id)
            REFERRALS[existing_code] = {
                "user_id": user_id,
                "used_by": [],
                "created_at": datetime.now().isoformat()
            }
            from main import schedule_save
            await schedule_save()
    
    used_count = len(REFERRALS.get(existing_code, {}).get("used_by", []))
    referral_limit = REFERRAL_SETTINGS.get("referral_limit", 5)
    
    bot_username = TELEGRAM_SETTINGS.get("bot_username", "bot")
    
    text = f"""🎁 <b>سیستم رفرال تیم آزادی</b>

👤 شناسه شما: <code>{user_id}</code>

🔗 <b>لینک رفرال شما:</b>
<code>https://t.me/{bot_username}?start=ref_{existing_code}</code>

📊 <b>آمار شما:</b>
• تعداد رفرال‌های استفاده‌شده: {used_count} از {referral_limit}
• کانفیگ‌های باقی‌مانده: {remaining} از {max_links}
• حجم هر کانفیگ: {REFERRAL_SETTINGS.get('referral_reward_gb', 1)} GB
• مدت اعتبار: {REFERRAL_SETTINGS.get('referral_reward_days', 7)} روز

📌 <b>نحوه استفاده:</b>
1. لینک رفرال خود را برای دوستان خود ارسال کنید
2. هر کاربر جدید با لینک شما وارد شود، یک رفرال برای شما ثبت می‌شود
3. به ازای هر {REFERRAL_SETTINGS.get('referral_reward_gb', 1)} رفرال، یک کانفیگ جدید دریافت می‌کنید

💡 <b>سقف رفرال:</b> {referral_limit} نفر"""
    
    kb = [
        [{"text": "🔗 کپی لینک رفرال", "callback_data": f"m:referral_copy:{existing_code}"}],
        [glass_button("🔄 بررسی مجدد عضویت", "m:referral_check", "success")],
        [glass_button("⬅️ منوی اصلی", "m:main", "glass")],
    ]
    
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


async def _handle_referral_start(chat_id, ref_code: str):
    user_id = str(chat_id)
    
    async with REFERRALS_LOCK:
        ref_data = REFERRALS.get(ref_code)
        if not ref_data:
            await _send(chat_id, "❌ لینک رفرال نامعتبر است.")
            await _show_main_menu(chat_id)
            return
        
        if user_id in ref_data.get("used_by", []):
            await _send(chat_id, "⚠️ شما قبلاً با این لینک رفرال ثبت‌نام کرده‌اید.")
            await _show_main_menu(chat_id)
            return
        
        if len(ref_data.get("used_by", [])) >= REFERRAL_SETTINGS.get("referral_limit", 5):
            await _send(chat_id, "❌ این لینک رفرال به حداکثر تعداد خود رسیده است.")
            await _show_main_menu(chat_id)
            return
        
        ref_data.setdefault("used_by", []).append(user_id)
        from main import schedule_save
        await schedule_save()
    
    if REFERRAL_SETTINGS.get("channel_required", True):
        is_member = await check_channel_membership(user_id)
        if not is_member:
            channel = REFERRAL_SETTINGS.get("channel_username", "TimAzadi")
            text = f"""🎉 <b>تبریک! رفرال شما ثبت شد!</b>

✅ شما با موفقیت از لینک رفرال استفاده کردید.

⚠️ اما برای دریافت کانفیگ، ابتدا باید در کانال تیم آزادی عضو شوید:

📢 لطفاً عضو کانال شوید:
👉 https://t.me/{channel}

سپس روی دکمه زیر کلیک کنید."""
            kb = [[glass_button("🔄 بررسی عضویت و دریافت کانفیگ", f"m:referral_claim:{ref_code}", "success")]]
            await _send(chat_id, text, kb)
            return
    
    uid = await create_link_from_referral(user_id)
    if uid:
        # افزودن به کاربر
        await add_user_link(user_id, uid)
        
        host = get_host()
        if not host or host == "localhost":
            host = "mmd-mimi-mikham.up.railway.app"
        
        sub_url = f"https://{host}/sub/{uid}"
        text = f"""🎉 <b>تبریک! کانفیگ شما آماده شد!</b>

✅ رفرال شما با موفقیت ثبت شد.
🔗 لینک ساب شما:
<code>{sub_url}</code>

📌 نکات:
• حجم: {REFERRAL_SETTINGS.get('referral_reward_gb', 1)} GB
• مدت اعتبار: {REFERRAL_SETTINGS.get('referral_reward_days', 7)} روز
• حداکثر تعداد دستگاه: ۱

📢 کانال تیم آزادی:
https://t.me/{REFERRAL_SETTINGS.get('channel_username', 'TimAzadi')}"""
        
        kb = [
            [{"text": "🔗 کپی لینک ساب", "callback_data": f"m:copy:{uid}"}],
            [{"text": "🎁 دریافت کانفیگ رفرال", "callback_data": "m:referral"}],
            [glass_button("⬅️ منوی اصلی", "m:main", "glass")],
        ]
        await _send(chat_id, text, kb)
    else:
        await _send(chat_id, "❌ خطا در ساخت کانفیگ. لطفاً دوباره تلاش کنید.")


# ── منوی تنظیمات بات (فقط ادمین) ────────────────────────────────────────────
async def _show_bot_settings(chat_id, message_id=None):
    bot_stats = BOT_STATS
    settings = BOT_SETTINGS
    
    text = f"""⚙️ <b>تنظیمات و آمار بات</b>

📊 <b>آمار:</b>
• کاربران کل: {bot_stats.get('total_users', 0)}
• کانفیگ‌های ساخته‌شده: {bot_stats.get('total_links_created', 0)}
• پیام‌های ارسال‌شده: {bot_stats.get('total_messages', 0)}
• آپ‌تایم: {int((time.time() - bot_stats.get('started_at', time.time())) // 3600)} ساعت

⚙️ <b>تنظیمات:</b>
• وضعیت: {'🟢 فعال' if settings.get('enabled', True) else '🔴 غیرفعال'}
• دسترسی عمومی: {'✅ باز' if settings.get('allow_public', True) else '❌ بسته'}
• حداکثر کانفیگ برای هر کاربر: {settings.get('max_links_per_user', 5)}
• حجم پیش‌فرض: {settings.get('default_quota_gb', 1)} GB
• انقضای پیش‌فرض: {settings.get('default_expiry_days', 7)} روز

📨 <b>ارسال پیام گروهی:</b>
برای ارسال پیام به همه‌ی کاربران، دستور زیر رو بفرست:
<code>/broadcast پیام شما</code>"""
    
    kb = [
        [
            {"text": "🔓 باز کردن عمومی", "callback_data": "bs:public:true"},
            {"text": "🔒 بستن عمومی", "callback_data": "bs:public:false"},
        ],
        [
            {"text": "📈 افزایش سقف", "callback_data": "bs:max:10"},
            {"text": "📉 کاهش سقف", "callback_data": "bs:max:3"},
        ],
        [glass_button("⬅️ منوی اصلی", "m:main", "glass")],
    ]
    
    if message_id:
        await _edit(chat_id, message_id, text, kb)
    else:
        await _send(chat_id, text, kb)


async def _handle_text(chat_id, text):
    w = _wizard.get(str(chat_id))
    text = (text or "").strip()
    
    # ── دستورات ──────────────────────────────────────────────────────────────
    if text.startswith("/start"):
        parts = text.split()
        if len(parts) > 1:
            ref_code = parts[1]
            if ref_code.startswith("ref_"):
                await _handle_referral_start(chat_id, ref_code)
                return
        
        # ثبت کاربر جدید
        try:
            from main import send_telegram_message
            chat_info = await _api("getChat", {"chat_id": chat_id})
            if chat_info:
                first_name = chat_info.get("first_name", "")
                username = chat_info.get("username", "")
                await add_bot_user(str(chat_id), first_name, username)
        except Exception:
            pass
        
        await _show_main_menu(chat_id)
        return
    
    if text.startswith("/broadcast"):
        # فقط ادمین
        admin_chat_ids = str(TELEGRAM_SETTINGS.get("chat_id", "")).split(",")
        if str(chat_id) not in admin_chat_ids:
            await _send(chat_id, "❌ شما دسترسی ارسال پیام گروهی ندارید.")
            return
        
        msg = text.replace("/broadcast", "").strip()
        if not msg:
            await _send(chat_id, "⚠️ لطفاً پیام خود را بعد از دستور وارد کنید.\nمثال: <code>/broadcast سلام به همه</code>")
            return
        
        await _send(chat_id, f"📨 در حال ارسال پیام به {len(BOT_USERS)} کاربر...")
        
        from state import send_broadcast
        ok, sent, failed = await send_broadcast(msg)
        
        if ok:
            await _send(chat_id, f"✅ پیام به {sent} کاربر ارسال شد.\n❌ {failed} کاربر دریافت نکردند.")
        else:
            await _send(chat_id, "❌ خطا در ارسال پیام گروهی.")
        return
    
    if text.startswith("/help"):
        await _show_help(chat_id)
        return
    
    if text.startswith("/stats"):
        try:
            from main import send_telegram_message
            if str(chat_id) in str(TELEGRAM_SETTINGS.get("chat_id", "")).split(","):
                await _send(chat_id, f"📊 {get_bot_stats()}")
            else:
                await _send(chat_id, f"📊 {BOT_STATS}")
        except Exception:
            await _send(chat_id, "❌ خطا در دریافت آمار")
        return
    
    if text.startswith("/menu"):
        await _show_main_menu(chat_id)
        return
    
    # ── ویزارد ──────────────────────────────────────────────────────────────
    if not w:
        await _send(chat_id, "❓ برای شروع /menu رو بزن یا از دکمه‌های پایین پیام‌های قبلی استفاده کن.")
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
            await _send(chat_id, "❌ عدد معتبر نبود؛ دوباره بفرست (مثلاً 7.5):")
            return
        w["step"] = "expiry"
        await _wizard_ask_expiry(chat_id)
    elif step == "expiry_custom":
        try:
            w["data"]["expiry_days"] = max(0.0, float(text.replace(",", ".")))
        except ValueError:
            await _send(chat_id, "❌ عدد معتبر نبود؛ دوباره بفرست (مثلاً 3):")
            return
        await _wizard_finish(chat_id)
    elif step == "search":
        _wizard.pop(str(chat_id), None)
        q = text.lower()
        
        # جستجو در کانفیگ‌های کاربر
        user_links = get_user_links(str(chat_id))
        async with LINKS_LOCK:
            hits = [(uid, LINKS[uid]) for uid in user_links if uid in LINKS and q in LINKS[uid].get("label", "").lower()]
            hits = hits[:20]
        
        if not hits:
            await _send(chat_id, "❌ چیزی پیدا نشد.", [[glass_button("⬅️ منوی اصلی", "m:main", "glass")]])
            return
        kb = [[{"text": _link_line(uid, d), "callback_data": f"l:{uid}"}] for uid, d in hits]
        kb.append([glass_button("⬅️ منوی اصلی", "m:main", "glass")])
        await _send(chat_id, f"🔍 {len(hits)} نتیجه:", kb)
    elif step == "increase_quota":
        uid = w["data"]["uid"]
        try:
            extra_gb = max(0.0, float(text.replace(",", ".")))
        except ValueError:
            await _send(chat_id, "❌ عدد معتبر نبود؛ دوباره بفرست:")
            return
        _wizard.pop(str(chat_id), None)
        async with LINKS_LOCK:
            link = LINKS.get(uid)
            if link:
                if link.get("limit_bytes", 0) == 0:
                    await _send(chat_id, "ℹ️ این کانفیگ نامحدود است؛ افزایش حجم لازم نیست.")
                    return
                link["limit_bytes"] += parse_size_to_bytes(extra_gb, "GB")
                link["quota_notified"] = False
        from main import schedule_save
        await schedule_save()
        await _send(chat_id, f"✅ {extra_gb}GB اضافه شد.", [[glass_button("⬅️ منوی اصلی", "m:main", "glass")]])


# ── مدیریت Callback ──────────────────────────────────────────────────────────
async def _handle_callback(chat_id, message_id, cb_id, data):
    await _answer_cb(cb_id)
    if data == "noop":
        return

    if data == "m:main":
        _wizard.pop(str(chat_id), None)
        await _show_main_menu(chat_id, message_id)
    
    elif data == "m:help":
        await _show_help(chat_id, message_id)
    
    elif data == "m:new":
        await _wizard_start(chat_id, message_id)
    
    elif data.startswith("m:list:"):
        await _show_list(chat_id, message_id, int(data.split(":")[2]))
    
    elif data == "m:stats":
        await _show_stats(chat_id, message_id)
    
    elif data == "m:search":
        _wizard[str(chat_id)] = {"step": "search", "data": {}}
        await _edit(chat_id, message_id, "🔍 بخشی از اسم کانفیگ رو بفرست:", [[glass_button("❌ انصراف", "m:main", "danger")]])
    
    elif data.startswith("m:subs:"):
        await _show_subs(chat_id, message_id, int(data.split(":")[2]))
    
    elif data == "m:referral":
        await _show_referral_menu(chat_id, message_id)
    
    elif data == "m:referral_check":
        user_id = str(chat_id)
        is_member = await check_channel_membership(user_id)
        if is_member:
            await _edit(chat_id, message_id, "✅ عضویت شما در کانال تأیید شد. لطفاً دوباره روی دکمه دریافت کانفیگ کلیک کنید.", [[glass_button("🎁 دریافت کانفیگ رفرال", "m:referral", "success")]])
        else:
            channel = REFERRAL_SETTINGS.get("channel_username", "TimAzadi")
            await _edit(chat_id, message_id, f"❌ شما هنوز در کانال تیم آزادی عضو نشده‌اید.\n\n📢 لطفاً عضو شوید:\nhttps://t.me/{channel}", [[glass_button("🔄 بررسی مجدد", "m:referral_check", "success")]])
    
    elif data.startswith("m:referral_copy:"):
        code = data.split(":", 2)[2]
        bot_username = TELEGRAM_SETTINGS.get("bot_username", "bot")
        await _send(chat_id, f"🔗 لینک رفرال شما کپی شد!\n\n<code>https://t.me/{bot_username}?start=ref_{code}</code>")
        await _show_referral_menu(chat_id, message_id)
    
    elif data.startswith("m:referral_claim:"):
        ref_code = data.split(":", 2)[2]
        user_id = str(chat_id)
        
        if REFERRAL_SETTINGS.get("channel_required", True):
            is_member = await check_channel_membership(user_id)
            if not is_member:
                channel = REFERRAL_SETTINGS.get("channel_username", "TimAzadi")
                await _edit(chat_id, message_id, f"❌ شما هنوز در کانال عضو نشده‌اید.\n\n📢 لطفاً عضو شوید:\nhttps://t.me/{channel}", [[glass_button("🔄 بررسی مجدد", f"m:referral_claim:{ref_code}", "success")]])
                return
        
        uid = await create_link_from_referral(user_id)
        if uid:
            await add_user_link(user_id, uid)
            host = get_host()
            if not host or host == "localhost":
                host = "mmd-mimi-mikham.up.railway.app"
            
            sub_url = f"https://{host}/sub/{uid}"
            text = f"""🎉 <b>تبریک! کانفیگ شما آماده شد!</b>

🔗 لینک ساب شما:
<code>{sub_url}</code>

📌 نکات:
• حجم: {REFERRAL_SETTINGS.get('referral_reward_gb', 1)} GB
• مدت اعتبار: {REFERRAL_SETTINGS.get('referral_reward_days', 7)} روز
• حداکثر تعداد دستگاه: ۱"""
            
            kb = [
                [{"text": "🔗 کپی لینک ساب", "callback_data": f"m:copy:{uid}"}],
                [{"text": "🎁 دریافت کانفیگ رفرال", "callback_data": "m:referral"}],
                [glass_button("⬅️ منوی اصلی", "m:main", "glass")],
            ]
            await _edit(chat_id, message_id, text, kb)
        else:
            await _edit(chat_id, message_id, "❌ خطا در ساخت کانفیگ. لطفاً دوباره تلاش کنید.", [[glass_button("⬅️ منوی اصلی", "m:main", "glass")]])
    
    elif data.startswith("m:copy:"):
        uid = data.split(":", 2)[2]
        host = get_host()
        if not host or host == "localhost":
            host = "mmd-mimi-mikham.up.railway.app"
        await _send(chat_id, f"✅ لینک ساب کپی شد!\n\n<code>https://{host}/sub/{uid}</code>")
    
    # ── دکمه‌های میانبر (Quick Actions) ──────────────────────────────────
    elif data.startswith("m:quick:"):
        parts = data.split(":")
        if len(parts) >= 4:
            quota_gb = float(parts[2])
            expiry_days = int(parts[3])
            
            user_id = str(chat_id)
            can_create, msg = user_can_create_link(user_id)
            if not can_create:
                await _edit(chat_id, message_id, f"❌ {msg}", [[glass_button("⬅️ منوی اصلی", "m:main", "glass")]])
                return
            
            label = f"کانفیگ {quota_gb}GB/{expiry_days}روز"
            uid = generate_uuid()
            limit_bytes = parse_size_to_bytes(quota_gb, "GB")
            expires_at = (datetime.now() + timedelta(days=expiry_days)).isoformat()
            
            async with LINKS_LOCK:
                LINKS[uid] = {
                    "label": label,
                    "limit_bytes": limit_bytes,
                    "used_bytes": 0,
                    "created_at": datetime.now().isoformat(),
                    "active": True,
                    "expires_at": expires_at,
                    "note": f"ساخته‌شده از طریق میانبر بات توسط {chat_id}",
                    "is_default": False,
                    "sub_id": None,
                    "protocol": DEFAULT_PROTOCOL,
                    "parent_id": None,
                    "white_label": False,
                    "flag": "🇺🇸",
                    "max_devices": 0,
                    "quota_notified": False,
                    "expiry_notified": False,
                }
            
            await add_user_link(user_id, uid)
            from main import schedule_save
            await schedule_save()
            
            host = get_host()
            sub_url = f"https://{host}/sub/{uid}"
            
            text = f"""✅ <b>کانفیگ میانبر ساخته شد!</b>

🔧 <b>{label}</b>
📦 حجم: {quota_gb} GB
⏰ انقضا: {expiry_days} روز
🔗 لینک ساب: <code>{sub_url}</code>"""
            
            kb = [
                [{"text": "🔗 دریافت لینک/QR", "callback_data": f"lg:{uid}"}],
                [glass_button("⬅️ منوی اصلی", "m:main", "glass")],
            ]
            await _edit(chat_id, message_id, text, kb)
    
    # ── مدیریت کانفیگ ──────────────────────────────────────────────────────
    elif data.startswith("q:"):
        val = data[2:]
        w = _wizard.get(str(chat_id))
        if not w:
            return
        if val == "custom":
            w["step"] = "quota_custom"
            await _edit(chat_id, message_id, "✏️ مقدار حجم رو به گیگابایت بفرست (مثلاً 7.5):", [[glass_button("❌ انصراف", "m:main", "danger")]])
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
            await _edit(chat_id, message_id, "✏️ تعداد روز رو بفرست (مثلاً 3):", [[glass_button("❌ انصراف", "m:main", "danger")]])
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
        await _edit(chat_id, message_id, "✏️ چند گیگابایت اضافه شود؟ (مثلاً 5):", [[glass_button("❌ انصراف", "m:main", "danger")]])
    
    elif data.startswith("lg:"):
        await _send_link_and_qr(chat_id, data[3:])
    
    elif data.startswith("ldc:"):
        uid = data[4:]
        async with LINKS_LOCK:
            label = LINKS.get(uid, {}).get("label", uid)
            LINKS.pop(uid, None)
        await remove_user_link(str(chat_id), uid)
        from main import schedule_save
        await schedule_save()
        log_activity("link", f"کانفیگ «{label}» از بات تلگرام توسط {chat_id} حذف شد", "warn")
        await _edit(chat_id, message_id, f"🗑 «{label}» حذف شد.", [[glass_button("⬅️ لیست", "m:list:0", "glass")]])
    
    elif data.startswith("ldn:"):
        await _show_link_detail(chat_id, message_id, data[4:])
    
    elif data.startswith("ld:"):
        uid = data[3:]
        await _edit(chat_id, message_id, "⚠️ مطمئنی این کانفیگ کامل حذف شود؟ این عمل قابل بازگشت نیست.",
                    [[{"text": "✅ بله، حذف شود", "callback_data": f"ldc:{uid}"}, {"text": "❌ نه", "callback_data": f"ldn:{uid}"}]])
    
    elif data.startswith("st:"):
        sub_id = data[3:]
        await _toggle_sub_lock(chat_id, message_id, sub_id)
    
    # ── تنظیمات بات ────────────────────────────────────────────────────────
    elif data == "m:bot_settings":
        await _show_bot_settings(chat_id, message_id)
    
    elif data.startswith("bs:"):
        parts = data.split(":")
        if len(parts) >= 3:
            key = parts[1]
            value = parts[2]
            
            if key == "public":
                BOT_SETTINGS["allow_public"] = value == "true"
            elif key == "max":
                BOT_SETTINGS["max_links_per_user"] = int(value)
            
            from main import schedule_save
            await schedule_save()
            await _show_bot_settings(chat_id, message_id)


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
    kb.append([glass_button("⬅️ منوی اصلی", "m:main", "glass")])

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
    log_activity("sub", f"گروه «{name}» از بات تلگرام توسط {chat_id} {'قفل' if locked else 'باز'} شد", "warn" if locked else "ok")
    await _show_subs(chat_id, message_id, 0)


async def _process_update(update: dict):
    try:
        if "callback_query" in update:
            cq = update["callback_query"]
            chat_id = cq["message"]["chat"]["id"]
            await _handle_callback(chat_id, cq["message"]["message_id"], cq["id"], cq.get("data", ""))
        elif "message" in update:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            await _handle_text(chat_id, msg.get("text", ""))
    except Exception as e:
        logger.warning(f"telegram_bot: process_update error: {e}")


# ── حلقه‌ی Polling ──────────────────────────────────────────────────────────
async def polling_loop():
    global _offset, _running
    _running = True
    logger.info("telegram_bot: polling loop started")
    while True:
        try:
            if not (TELEGRAM_SETTINGS.get("enabled") and TELEGRAM_SETTINGS.get("bot_token")):
                await asyncio.sleep(5)
                continue
            
            result = await _api("getUpdates", {
                "offset": _offset,
                "timeout": 25,
                "allowed_updates": ["message", "callback_query"],
                "drop_pending_updates": True
            })
            
            if result is None:
                await asyncio.sleep(5)
                continue
                
            for update in result:
                _offset = update["update_id"] + 1
                await _process_update(update)
                
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.warning(f"telegram_bot: polling_loop error: {e}")
            await asyncio.sleep(5)
    _running = False
    logger.info("telegram_bot: polling loop stopped")
