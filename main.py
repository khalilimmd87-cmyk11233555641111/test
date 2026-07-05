import asyncio
import secrets
import time
from datetime import datetime, timedelta
from urllib.parse import quote

from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import Response, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx

import os

from state import (
    logger, CONFIG,
    connections, stats, error_logs, activity_logs, hourly_traffic,
    LINKS, LINKS_LOCK, SUBS, SUBS_LOCK,
    PROTOCOLS, DEFAULT_PROTOCOL, log_activity,
    SESSION_COOKIE, SESSION_TTL, hash_password, verify_password, is_legacy_hash, AUTH,
    SESSIONS, SESSIONS_LOCK,
    create_session, is_valid_session, destroy_session, require_auth,
    load_state, save_state,
    get_host, generate_uuid, now_ir, generate_vless_link, generate_all_vless_links, uptime,
    parse_size_to_bytes, is_link_expired, is_link_allowed, fmt_bytes, client_ip,
    ensure_default_link,
    check_login_rate_limit, record_login_attempt,
    is_blocked_proxy_target,
)

# ✅ امنیت: به‌جای CORS باز (allow_origins=["*"] + allow_credentials=True که
# ترکیب خطرناکی‌ست و می‌تواند کوکی سشن را در معرض هر سایتی بگذارد)، فقط
# دامنه‌ی واقعی سرویس (و هر چیزی که صریحاً در ALLOWED_ORIGINS ست شود) مجاز است.
_public_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
_extra_origins = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "").split(",") if o.strip()]
ALLOWED_ORIGINS = list({
    *( [f"https://{_public_domain}"] if _public_domain else [] ),
    *_extra_origins,
}) or ["http://localhost:8000"]  # دست‌کم یک مقدار امن برای اجرای لوکال

# کوکی سشن روی HTTPS واقعی (Railway) باید secure باشد؛ فقط برای اجرای لوکال
# روی http://localhost می‌توان با متغیر محیطی خاموشش کرد.
SECURE_COOKIES = os.environ.get("DISABLE_SECURE_COOKIE", "0") != "1"

# ── متغیر سراسری برای مدیریت تسک ذخیره‌سازی ──
_save_task = None

async def schedule_save():
    """ذخیره‌سازی state رو با اولویت پایین و بدون تداخل انجام بده"""
    global _save_task
    # اگر تسک قبلی هنوز در حال اجراست، اون رو کنسل کن
    if _save_task and not _save_task.done():
        _save_task.cancel()
        try:
            await _save_task
        except asyncio.CancelledError:
            pass
    # تسک جدید رو شروع کن
    _save_task = asyncio.create_task(save_state())

app = FastAPI(title="تیم آزادی Gateway", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

http_client: httpx.AsyncClient | None = None

# ✅ ضد-پروبینگ/سخت‌سازی: uvicorn به‌صورت پیش‌فرض هدر "server: uvicorn" را روی
# هر پاسخ می‌گذارد که یک نشانه‌ی رایگان برای شناسایی این‌که پشت این دامنه یک
# اپ پایتونی/uvicorn است (به‌جای مثلاً یک وب‌سرور معمولی) به هر پروب فعال
# می‌دهد. این middleware آن را حذف/جایگزین می‌کند و چند هدر امنیتی استاندارد
# هم اضافه می‌کند که تفاوتش با یک سایت معمولی را کمتر می‌کند.
@app.middleware("http")
async def _harden_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["server"] = "nginx"
    response.headers.setdefault("x-content-type-options", "nosniff")
    response.headers.setdefault("referrer-policy", "no-referrer")
    response.headers.setdefault("x-frame-options", "SAMEORIGIN")
    return response

# ── Startup / Shutdown ────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    global http_client
    limits = httpx.Limits(max_connections=500, max_keepalive_connections=100)
    timeout = httpx.Timeout(30.0, connect=10.0)
    http_client = httpx.AsyncClient(
        limits=limits, timeout=timeout, follow_redirects=True,
    )
    await load_state()
    if os.environ.get("ADMIN_PASSWORD") is None:
        logger.warning("⚠️  ADMIN_PASSWORD در env تنظیم نشده؛ رمز پیش‌فرض در حال استفاده است. برای امنیت، آن را در متغیرهای محیطی ست کنید و/یا از پنل تغییر بدهید.")
    log_activity("system", "سرور راه‌اندازی شد", "ok")
    logger.info(f"تیم آزادی Gateway v10.0 started on port {CONFIG['port']}")

@app.on_event("shutdown")
async def shutdown():
    await save_state()
    if http_client:
        await http_client.aclose()

# ── Basic endpoints ───────────────────────────────────────────────────────────
# 🐛 باگ امنیتی/ضد-پروبینگ رفع‌شده: قبلاً "/" و "/health" بدون هیچ احراز
# هویتی، هویت این سرویس (نام پروژه، ورژن) و حتی تعداد اتصالات زنده را به هر
# بازدیدکننده‌ی ناشناس (از جمله ابزارهای اسکن/پروبینگ سانسور) اعلام می‌کردند —
# دقیقاً برخلاف هدف «ضد-پروبینگ»ی که بقیه‌ی پروژه (حذف پیام‌های خطای
# اختصاصی و...) دنبالش بود. الان این دو مسیر مثل یک وب‌سرویس معمولی و
# بی‌اهمیت به نظر می‌رسند؛ آمار زنده‌ی واقعی فقط برای ادمین لاگین‌شده
# در دسترس است.
@app.get("/")
async def root():
    return JSONResponse({"status": "ok"})

@app.get("/health")
async def health():
    return JSONResponse({"status": "ok"})

@app.get("/api/health")
async def health_admin(_=Depends(require_auth)):
    """آمار سلامت واقعی (اتصالات زنده، uptime) — فقط برای ادمین لاگین‌شده."""
    return {"status": "ok", "connections": len(connections), "uptime": uptime()}

# ── Subscription (single link) ────────────────────────────────────────────────
@app.get("/sub/{uuid}")
async def subscription_single(uuid: str, request: Request):
    import base64
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not link or not is_link_allowed(link):
        raise HTTPException(status_code=404, detail="not found or inactive")

    host = get_host()
    proto = link.get("protocol", DEFAULT_PROTOCOL)
    used_bytes = link.get("used_bytes", 0)
    limit_bytes = link.get("limit_bytes", 0)
    # ✅ سفید-برند: اگر این کانفیگ متعلق به یک ساب سفید-برند (تقسیم/هدیه‌شده)
    # باشد، هیچ اسمی از تیم‌آزادی حتی داخل remark (اسمی که در اپ کلاینت
    # دیده می‌شود) نمی‌آید.
    owning_sub = SUBS.get(link.get("sub_id")) if link.get("sub_id") else None
    white_label = bool(link.get("white_label")) or bool(owning_sub and owning_sub.get("white_label"))
    # ✅ فیچر: به‌جای یک کانفیگ تک‌پروتکلی، ساب حالا هر سه پروتکل کارکردی
    # (WS + دو مد XHTTP) را با هم می‌دهد — اگر یکی فیلتر شد، بقیه در کلاینت
    # موجودند؛ هر سه روی همان uuid/سهمیه کار می‌کنند.
    bundle = generate_all_vless_links(uuid, host, link["label"], used_bytes, limit_bytes, brand=not white_label)
    vless = next((b["vless_link"] for b in bundle if b["protocol"] == proto), bundle[0]["vless_link"])
    sub_url = f"https://{host}/sub/{uuid}"

    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        from pages import get_single_link_page_html
        link_data = {
            "uuid": uuid,
            **link,
            "expired": is_link_expired(link),
            "vless_link": vless,
            "vless_links": bundle,
            "sub_url": sub_url,
            "used_fmt": fmt_bytes(used_bytes),
            "limit_fmt": "∞" if limit_bytes == 0 else fmt_bytes(limit_bytes),
            "protocol": proto,
            "white_label": white_label,
        }
        return HTMLResponse(content=get_single_link_page_html(uuid, link_data))

    content = base64.b64encode("\n".join(b["vless_link"] for b in bundle).encode()).decode()
    headers = {"profile-title": quote(link["label"])}
    if not white_label:
        headers["support-url"] = "https://t.me/TimAzadi"
    return Response(content=content, media_type="text/plain", headers=headers)

@app.get("/sub-all")
async def subscription_all(_=Depends(require_auth)):
    import base64
    host = get_host()
    async with LINKS_LOCK:
        lines = []
        for uid, d in LINKS.items():
            if is_link_allowed(d):
                bundle = generate_all_vless_links(uid, host, d["label"], d.get("used_bytes", 0), d.get("limit_bytes", 0))
                lines.extend(b["vless_link"] for b in bundle)
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain")

# ══════════════════════════════════════════════════════════════════════════════
# QUOTA SPLIT — خودِ کاربرِ یک ساب (بدون نیاز به لاگین ادمین؛ uuid خودش توکن
# دسترسی است، مثل بقیه‌ی مسیرهای /sub/{uuid}) می‌تواند بخشی از سهمیه‌ی باقی‌مانده‌ی
# خودش را به‌صورت یک ساب کاملاً مستقل و بدون‌برند جدا کند و به یک دوست بدهد.
# ══════════════════════════════════════════════════════════════════════════════

MAX_CHILDREN_PER_LINK = 50
MIN_SPLIT_BYTES = 1 * 1024 * 1024  # حداقل ۱ مگابایت، برای جلوگیری از هرزنامه/ساب‌های صفر-حجمی

def _child_view(uid: str, d: dict, host: str) -> dict:
    return {
        "uuid": uid,
        "label": d["label"],
        "used_bytes": d.get("used_bytes", 0),
        "used_fmt": fmt_bytes(d.get("used_bytes", 0)),
        "limit_bytes": d.get("limit_bytes", 0),
        "limit_fmt": "∞" if not d.get("limit_bytes") else fmt_bytes(d["limit_bytes"]),
        "active": d.get("active", True),
        "expired": is_link_expired(d),
        "created_at": d.get("created_at"),
        "sub_url": f"https://{host}/sub/{uid}",
    }

@app.post("/api/public/split/{uuid}")
async def create_split_child(uuid: str, request: Request):
    body = await request.json()
    amount = float(body.get("amount") or 0)
    unit = body.get("unit") or "GB"
    label = (body.get("label") or "اشتراکی").strip()[:60]
    if amount <= 0:
        raise HTTPException(status_code=400, detail="مقدار حجم نامعتبر است")
    amount_bytes = parse_size_to_bytes(amount, unit)
    if amount_bytes < MIN_SPLIT_BYTES:
        raise HTTPException(status_code=400, detail="حداقل حجم قابل‌جداسازی ۱ مگابایت است")

    host = get_host()
    async with LINKS_LOCK:
        parent = LINKS.get(uuid)
        if not parent or not is_link_allowed(parent):
            raise HTTPException(status_code=404, detail="not found or inactive")
        n_children = sum(1 for d in LINKS.values() if d.get("parent_id") == uuid)
        if n_children >= MAX_CHILDREN_PER_LINK:
            raise HTTPException(status_code=400, detail="سقف تعداد ساب‌های ساخته‌شده از این لینک پر شده")

        parent_limit = parent.get("limit_bytes", 0)
        if parent_limit > 0:
            remaining = parent_limit - parent.get("used_bytes", 0)
            if amount_bytes > remaining:
                raise HTTPException(status_code=400, detail="این مقدار بیشتر از سهمیه‌ی باقی‌مانده‌ی توست")
            parent["limit_bytes"] = parent_limit - amount_bytes
        # اگه سهمیه‌ی خودِ parent نامحدود باشه (limit_bytes==0)، جداسازی یک
        # سهمیه‌ی مستقل و محدود می‌سازه بدون اینکه چیزی از parent کم بشه.

        child_uid = generate_uuid()
        LINKS[child_uid] = {
            "label": label,
            "limit_bytes": amount_bytes,
            "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "expires_at": None,
            "note": "",
            "is_default": False,
            "sub_id": None,
            "protocol": parent.get("protocol", DEFAULT_PROTOCOL),
            "parent_id": uuid,
            "white_label": True,
        }
        parent_view = _child_view(uuid, parent, host)
        child_view = _child_view(child_uid, LINKS[child_uid], host)

    await schedule_save()
    log_activity("link", f"سهمیه‌ی «{fmt_bytes(amount_bytes)}» از «{parent['label']}» جدا و ساب جدید «{label}» ساخته شد", "ok")
    return {"child": child_view, "parent": parent_view}

@app.get("/api/public/children/{uuid}")
async def list_split_children(uuid: str):
    host = get_host()
    async with LINKS_LOCK:
        if uuid not in LINKS:
            raise HTTPException(status_code=404, detail="not found")
        children = [_child_view(uid, d, host) for uid, d in LINKS.items() if d.get("parent_id") == uuid]
    children.sort(key=lambda x: x["created_at"] or "", reverse=True)
    return {"children": children}

@app.delete("/api/public/split/{uuid}/{child_uuid}")
async def revoke_split_child(uuid: str, child_uuid: str):
    host = get_host()
    async with LINKS_LOCK:
        parent = LINKS.get(uuid)
        child = LINKS.get(child_uuid)
        if not parent or not child or child.get("parent_id") != uuid:
            raise HTTPException(status_code=404, detail="not found")
        # سهمیه‌ی مصرف‌نشده‌ی ساب لغو‌شده، به سهمیه‌ی خودِ کاربر برمی‌گردد
        # (فقط اگر سهمیه‌ی parent محدود باشد؛ برای نامحدود چیزی برای برگرداندن نیست).
        if parent.get("limit_bytes", 0) > 0:
            unused = max(0, child.get("limit_bytes", 0) - child.get("used_bytes", 0))
            parent["limit_bytes"] += unused
        del LINKS[child_uuid]
        connections.pop(child_uuid, None)
        parent_view = _child_view(uuid, parent, host)

    await schedule_save()
    log_activity("link", f"ساب «{child['label']}» لغو شد و سهمیه‌ی باقی‌مانده به «{parent['label']}» برگشت", "warn")
    return {"parent": parent_view}

# ══════════════════════════════════════════════════════════════════════════════
# SUB GROUP endpoints
# ══════════════════════════════════════════════════════════════════════════════

@app.post("/api/subs")
async def create_sub(request: Request, _=Depends(require_auth)):
    body = await request.json()
    name = (body.get("name") or "گروه جدید").strip()[:60]
    desc = (body.get("desc") or "").strip()[:200]
    password = (body.get("password") or "").strip()
    # ✅ فیچر: «استخر تقسیم‌پذیر» — اگر ادمین یک سقف حجم (pool) برای این گروه
    # تعیین کند، صاحب همین ساب می‌تواند بعداً از داخل صفحه‌ی عمومی خودش
    # بخشی از این سقف را جدا کند و به‌عنوان یک ساب-فرزند مستقل به کس دیگری
    # بدهد (بدون نیاز به پنل ادمین).
    pool_value = float(body.get("pool_value") or 0)
    pool_unit = str(body.get("pool_unit") or "GB")
    pool_limit_bytes = parse_size_to_bytes(pool_value, pool_unit) if pool_value > 0 else 0
    sub_id = generate_uuid()
    uuid_key = secrets.token_urlsafe(16)
    async with SUBS_LOCK:
        SUBS[sub_id] = {
            "name": name,
            "desc": desc,
            "password_hash": hash_password(password) if password else None,
            "uuid_key": uuid_key,
            "created_at": datetime.now().isoformat(),
            "link_ids": [],
            "pool_limit_bytes": pool_limit_bytes,
            "pool_allocated_bytes": 0,
            "parent_sub_id": None,
            "child_sub_ids": [],
            "white_label": False,
        }
    await schedule_save()
    log_activity("sub", f"گروه «{name}» ساخته شد", "ok")
    host = get_host()
    return {
        "sub_id": sub_id,
        **SUBS[sub_id],
        "public_url": f"https://{host}/p/{uuid_key}",
        "sub_url": f"https://{host}/sub-group/{uuid_key}",
    }

@app.get("/api/subs")
async def list_subs(_=Depends(require_auth)):
    host = get_host()
    async with SUBS_LOCK:
        snap_subs = dict(SUBS)
    async with LINKS_LOCK:
        snap_links = dict(LINKS)
    result = []
    for sid, s in snap_subs.items():
        link_ids = s.get("link_ids", [])
        active_count = sum(1 for lid in link_ids if is_link_allowed(snap_links.get(lid)))
        total_used = sum(snap_links[lid].get("used_bytes", 0) for lid in link_ids if lid in snap_links)
        pool_limit = s.get("pool_limit_bytes", 0)
        pool_alloc = s.get("pool_allocated_bytes", 0)
        result.append({
            "sub_id": sid,
            **s,
            "password_hash": None,
            "has_password": s.get("password_hash") is not None,
            "links_count": len(link_ids),
            "active_count": active_count,
            "total_used_bytes": total_used,
            "total_used_fmt": fmt_bytes(total_used),
            "pool_limit_bytes": pool_limit,
            "pool_allocated_bytes": pool_alloc,
            "pool_available_bytes": max(0, pool_limit - pool_alloc) if pool_limit else 0,
            "pool_limit_fmt": fmt_bytes(pool_limit) if pool_limit else "—",
            "pool_available_fmt": fmt_bytes(max(0, pool_limit - pool_alloc)) if pool_limit else "—",
            "public_url": f"https://{host}/p/{s['uuid_key']}",
            "sub_url": f"https://{host}/sub-group/{s['uuid_key']}",
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"subs": result}

@app.patch("/api/subs/{sub_id}")
async def update_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        s = SUBS[sub_id]
        if "name" in body:
            s["name"] = str(body["name"])[:60]
        if "desc" in body:
            s["desc"] = str(body["desc"])[:200]
        if "password" in body:
            pw = str(body["password"]).strip()
            s["password_hash"] = hash_password(pw) if pw else None
        if "link_ids" in body:
            s["link_ids"] = list(body["link_ids"])
        if "pool_value" in body:
            pool_value = float(body.get("pool_value") or 0)
            pool_unit = str(body.get("pool_unit") or "GB")
            s["pool_limit_bytes"] = parse_size_to_bytes(pool_value, pool_unit) if pool_value > 0 else 0
            s.setdefault("pool_allocated_bytes", 0)
    await schedule_save()
    return {"ok": True}

@app.delete("/api/subs/{sub_id}")
async def delete_sub(sub_id: str, _=Depends(require_auth)):
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        name = SUBS[sub_id].get("name", sub_id)
        del SUBS[sub_id]
    async with LINKS_LOCK:
        for link in LINKS.values():
            if link.get("sub_id") == sub_id:
                link["sub_id"] = None
    await schedule_save()
    log_activity("sub", f"گروه «{name}» حذف شد", "warn")
    return {"ok": True, "deleted": sub_id}

@app.post("/api/subs/{sub_id}/links")
async def assign_link_to_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    link_id = str(body.get("link_id", ""))
    action = str(body.get("action", "add"))
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        s = SUBS[sub_id]
        ids = s.setdefault("link_ids", [])
        if action == "add":
            if link_id not in ids:
                ids.append(link_id)
        else:
            if link_id in ids:
                ids.remove(link_id)
    async with LINKS_LOCK:
        if link_id in LINKS:
            LINKS[link_id]["sub_id"] = sub_id if action == "add" else None
    await schedule_save()
    return {"ok": True}

# ── Public sub-group subscription file ───────────────────────────────────────
@app.get("/sub-group/{uuid_key}")
async def sub_group_subscription(uuid_key: str, request: Request):
    import base64
    async with SUBS_LOCK:
        sub = next((s for s in SUBS.values() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        raise HTTPException(status_code=404, detail="not found")

    if sub.get("password_hash"):
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            raise HTTPException(status_code=403, detail="wrong password")

    host = get_host()
    link_ids = sub.get("link_ids", [])
    white_label = bool(sub.get("white_label"))
    async with LINKS_LOCK:
        lines = []
        for lid in link_ids:
            link = LINKS.get(lid)
            if link and is_link_allowed(link):
                bundle = generate_all_vless_links(lid, host, link["label"], link.get("used_bytes", 0), link.get("limit_bytes", 0), brand=not white_label)
                lines.extend(b["vless_link"] for b in bundle)

    content = base64.b64encode("\n".join(lines).encode()).decode()
    headers = {"profile-title": quote(sub["name"]), "profile-update-interval": "12"}
    if not white_label:
        headers["support-url"] = "https://t.me/TimAzadi"
    return Response(content=content, media_type="text/plain", headers=headers)

# ── Auth endpoints ────────────────────────────────────────────────────────────
@app.post("/api/login")
async def api_login(request: Request):
    ip = client_ip(request)

    # ✅ امنیت: rate-limit روی تلاش‌های ورود برای مقابله با brute-force
    if not await check_login_rate_limit(ip):
        log_activity("auth", f"مسدود شدن موقت تلاش‌های ورود از {ip} (بیش از حد مجاز)", "err")
        raise HTTPException(status_code=429, detail="تعداد تلاش‌ها بیش از حد است، چند دقیقه بعد دوباره تلاش کنید")

    body = await request.json()
    password = str(body.get("password", ""))

    if not verify_password(password, AUTH["password_hash"]):
        await record_login_attempt(ip)
        log_activity("auth", f"تلاش ورود ناموفق از {ip}", "err")
        raise HTTPException(status_code=401, detail="رمز عبور اشتباه است")

    # ✅ ارتقای خودکار هش قدیمی (sha256 ساده) به PBKDF2 بعد از اولین ورود موفق
    if is_legacy_hash(AUTH["password_hash"]):
        AUTH["password_hash"] = hash_password(password)
        await schedule_save()

    token = await create_session()
    log_activity("auth", f"ورود موفق به پنل از {ip}", "ok")
    resp = JSONResponse({"ok": True})
    resp.set_cookie(
        SESSION_COOKIE, token, max_age=SESSION_TTL,
        httponly=True, samesite="lax", secure=SECURE_COOKIES, path="/",
    )
    return resp

@app.post("/api/logout")
async def api_logout(request: Request):
    await destroy_session(request.cookies.get(SESSION_COOKIE))
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp

@app.get("/api/me")
async def api_me(request: Request):
    return {"authenticated": await is_valid_session(request.cookies.get(SESSION_COOKIE))}

@app.post("/api/change-password")
async def api_change_password(request: Request, token=Depends(require_auth)):
    body = await request.json()
    if not verify_password(str(body.get("current_password", "")), AUTH["password_hash"]):
        raise HTTPException(status_code=400, detail="رمز فعلی اشتباه است")
    new = str(body.get("new_password", ""))
    if len(new) < 4:
        raise HTTPException(status_code=400, detail="رمز جدید باید حداقل ۴ کاراکتر باشد")
    AUTH["password_hash"] = hash_password(new)
    async with SESSIONS_LOCK:
        SESSIONS.clear()
        SESSIONS[token] = time.time() + SESSION_TTL
    await schedule_save()
    log_activity("auth", "رمز عبور پنل تغییر کرد", "ok")
    return {"ok": True}

# ── Stats ─────────────────────────────────────────────────────────────────────
@app.get("/stats")
async def get_stats(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)
    return {
        "active_connections": len(connections),
        "total_traffic_mb": round(stats["total_bytes"] / (1024 ** 2), 2),
        "total_requests": stats["total_requests"],
        "total_errors": stats["total_errors"],
        "uptime": uptime(),
        "timestamp": datetime.now().isoformat(),
        "hourly": dict(hourly_traffic),
        "recent_errors": list(error_logs)[-10:],
        "links_count": len(snap),
        "active_links": sum(1 for l in snap.values() if is_link_allowed(l)),
        "expired_links": sum(1 for l in snap.values() if is_link_expired(l)),
        "subs_count": len(SUBS),
    }

# ── Activity Logs ─────────────────────────────────────────────────────────────
@app.get("/api/activity")
async def get_activity(_=Depends(require_auth)):
    return {"logs": list(activity_logs)[-150:]}

# ── Live connections (with IP) ────────────────────────────────────────────────
@app.get("/api/connections")
async def get_connections(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)

    grouped: dict[str, dict] = {}
    for conn_id, c in connections.items():
        ip = c.get("ip", "نامشخص")
        link = snap.get(c.get("uuid"))
        label = link.get("label") if link else "نامشخص"
        g = grouped.get(ip)
        if g is None:
            g = {
                "ip": ip,
                "sessions": 0,
                "bytes": 0,
                "labels": set(),
                "transports": set(),
                "first_connected_at": c.get("connected_at"),
                "last_connected_at": c.get("connected_at"),
            }
            grouped[ip] = g
        g["sessions"] += 1
        g["bytes"] += c.get("bytes", 0)
        g["labels"].add(label)
        g["transports"].add(c.get("transport", "vless-ws"))
        ca = c.get("connected_at")
        if ca:
            if not g["first_connected_at"] or ca < g["first_connected_at"]:
                g["first_connected_at"] = ca
            if not g["last_connected_at"] or ca > g["last_connected_at"]:
                g["last_connected_at"] = ca

    result = []
    for ip, g in grouped.items():
        result.append({
            "ip": ip,
            "sessions": g["sessions"],
            "labels": sorted(g["labels"]),
            "label": " · ".join(sorted(g["labels"])) if g["labels"] else "نامشخص",
            "transports": sorted(g["transports"]),
            "bytes": g["bytes"],
            "bytes_fmt": fmt_bytes(g["bytes"]),
            "connected_at": g["first_connected_at"],
            "last_connected_at": g["last_connected_at"],
        })
    result.sort(key=lambda x: x.get("last_connected_at") or "", reverse=True)

    return {
        "connections": result,
        "count": len(result),
        "raw_count": len(connections),
    }

# ── Link Management ───────────────────────────────────────────────────────────
@app.post("/api/links")
async def create_link(request: Request, _=Depends(require_auth)):
    body = await request.json()
    label = (body.get("label") or "لینک جدید").strip()[:60]
    lv = float(body.get("limit_value") or 0)
    lu = body.get("limit_unit") or "GB"
    limit_bytes = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
    exp_days = int(body.get("expires_days") or 0)
    expires_at = (datetime.now() + timedelta(days=exp_days)).isoformat() if exp_days > 0 else None
    note = (body.get("note") or "").strip()[:200]
    sub_id = body.get("sub_id") or None
    protocol = body.get("protocol") or DEFAULT_PROTOCOL
    if protocol not in PROTOCOLS:
        protocol = DEFAULT_PROTOCOL

    uid = generate_uuid()
    async with LINKS_LOCK:
        LINKS[uid] = {
            "label": label,
            "limit_bytes": limit_bytes,
            "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "expires_at": expires_at,
            "note": note,
            "is_default": False,
            "sub_id": sub_id,
            "protocol": protocol,
            "parent_id": None,
            "white_label": False,
        }

    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].setdefault("link_ids", [])
                if uid not in ids:
                    ids.append(uid)

    await schedule_save()
    log_activity("link", f"کانفیگ «{label}» ساخته شد", "ok")
    host = get_host()
    return {
        "uuid": uid,
        **LINKS[uid],
        "expired": False,
        "vless_link": generate_vless_link(uid, host, remark=f"تیم‌آزادی-{label}", protocol=protocol),
        "sub_url": f"https://{host}/sub/{uid}",
    }

@app.get("/api/links")
async def list_links(_=Depends(require_auth)):
    host = get_host()
    async with LINKS_LOCK:
        snap = dict(LINKS)
    result = []
    for uid, d in snap.items():
        proto = d.get("protocol", DEFAULT_PROTOCOL)
        used_bytes = d.get("used_bytes", 0)
        limit_bytes = d.get("limit_bytes", 0)
        # ✅ فیچر: بسته‌ی هر ۳ پروتکل (WS + دو مد XHTTP) اینجا هم اضافه شد؛
        # قبلاً فقط generate_vless_link (تک‌پروتکلی) صدا زده می‌شد و پنل هیچ
        # دسترسی‌ای به بسته‌ی کامل نداشت، برای همین دکمه‌ی کپی/QR توی خودِ
        # پنل هم فقط یک پروتکل را نشان می‌داد.
        bundle = generate_all_vless_links(uid, host, d["label"], used_bytes, limit_bytes)
        result.append({
            "uuid": uid,
            **d,
            "protocol": proto,
            "expired": is_link_expired(d),
            "vless_link": next((b["vless_link"] for b in bundle if b["protocol"] == proto), bundle[0]["vless_link"]),
            "vless_links": bundle,
            "sub_url": f"https://{host}/sub/{uid}",
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"links": result}

@app.patch("/api/links/{uid}")
async def update_link(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        link = LINKS[uid]
        old_sub = link.get("sub_id")
        label = link.get("label")
        if "active" in body:
            link["active"] = bool(body["active"])
            log_activity("link", f"کانفیگ «{label}» {'فعال' if link['active'] else 'غیرفعال'} شد", "ok" if link["active"] else "warn")
        if "label" in body:
            link["label"] = str(body["label"])[:60]
        if "note" in body:
            link["note"] = str(body["note"])[:200]
        if "reset_usage" in body and body["reset_usage"]:
            link["used_bytes"] = 0
            log_activity("link", f"مصرف کانفیگ «{label}» ریست شد", "info")
        if "limit_value" in body:
            lv = float(body.get("limit_value") or 0)
            lu = body.get("limit_unit") or "GB"
            link["limit_bytes"] = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
        if "expires_days" in body:
            ed = int(body["expires_days"] or 0)
            link["expires_at"] = (datetime.now() + timedelta(days=ed)).isoformat() if ed > 0 else None
        if any(k in body for k in ("label", "note", "limit_value", "expires_days")):
            log_activity("link", f"کانفیگ «{link['label']}» ویرایش شد", "info")
        new_sub = body.get("sub_id", "UNCHANGED")
        if new_sub != "UNCHANGED":
            link["sub_id"] = new_sub or None

    if new_sub != "UNCHANGED":
        async with SUBS_LOCK:
            if old_sub and old_sub in SUBS:
                ids = SUBS[old_sub].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)
            if new_sub and new_sub in SUBS:
                ids = SUBS[new_sub].setdefault("link_ids", [])
                if uid not in ids:
                    ids.append(uid)

    await schedule_save()
    return {"ok": True}

@app.delete("/api/links/{uid}")
async def delete_link(uid: str, _=Depends(require_auth)):
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        label = LINKS[uid].get("label", uid)
        sub_id = LINKS[uid].get("sub_id")
        del LINKS[uid]
    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)
    await schedule_save()
    log_activity("link", f"کانفیگ «{label}» حذف شد", "err")
    return {"ok": True, "deleted": uid}

# ══════════════════════════════════════════════════════════════════════════════
# VLESS Relay
# ══════════════════════════════════════════════════════════════════════════════

from relay_vless import (
    RELAY_BUF,
    parse_vless_header,
    check_and_use,
    relay_ws_to_tcp,
    relay_tcp_to_ws,
    websocket_tunnel,
)

app.add_api_websocket_route("/ws/{uuid}", websocket_tunnel)

# ══════════════════════════════════════════════════════════════════════════════
# XHTTP
# ══════════════════════════════════════════════════════════════════════════════
from xhttp_siz10 import router as xhttp_router
app.include_router(xhttp_router)

# ── HTTP Proxy ────────────────────────────────────────────────────────────────
_HOP = {"connection","keep-alive","proxy-authenticate","proxy-authorization",
        "te","trailers","transfer-encoding","upgrade","content-encoding","content-length"}

@app.api_route("/proxy/{target_url:path}", methods=["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS"])
async def http_proxy(target_url: str, request: Request, _=Depends(require_auth)):
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    # ✅ امنیت: قبلاً این پراکسی به هر URL دلخواه (از جمله IPهای داخلی شبکه یا
    # سرویس متادیتای کلود مثل 169.254.169.254) وصل می‌شد که یک ریسک SSRF
    # واقعی بود. الان آی‌پی خصوصی/لوکال/متادیتا (چه literal و چه بعد از resolve
    # نام دامنه) مسدود می‌شود.
    #
    # 🐛 باگ امنیتی رفع‌شده: این چک فقط روی URL اولیه انجام می‌شد، اما
    # http_client با follow_redirects=True ساخته شده بود؛ یعنی یک سرور مجاز و
    # عمومی می‌توانست با یک 3xx به یک آدرس داخلی/متادیتا ریدایرکت کند و httpx
    # بدون عبور از چک SSRF آن را دنبال می‌کرد (SSRF-via-redirect، دور زدن کامل
    # محافظت بالا). الان هر hop ریدایرکت هم به‌طور جداگانه اعتبارسنجی می‌شود و
    # ریدایرکت خودکار httpx خاموش شده است.
    if await is_blocked_proxy_target(target_url):
        raise HTTPException(status_code=400, detail="این آدرس مجاز نیست")

    MAX_REDIRECTS = 5
    try:
        body = await request.body()
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _HOP and k.lower() != "host"}
        method = request.method
        url = target_url
        for _hop in range(MAX_REDIRECTS + 1):
            resp = await http_client.request(
                method=method, url=url, headers=headers, content=body, follow_redirects=False,
            )
            if resp.status_code in (301, 302, 303, 307, 308) and "location" in resp.headers:
                next_url = str(httpx.URL(url).join(resp.headers["location"]))
                if await is_blocked_proxy_target(next_url):
                    raise HTTPException(status_code=400, detail="این آدرس مجاز نیست")
                url = next_url
                if resp.status_code == 303:
                    method = "GET"
                    body = b""
                continue
            break
        stats["total_bytes"] += len(resp.content)
        stats["total_requests"] += 1
        hourly_traffic[now_ir().strftime("%H:00")] += len(resp.content)
        return Response(content=resp.content, status_code=resp.status_code,
                        headers={k: v for k, v in resp.headers.items() if k.lower() not in _HOP})
    except HTTPException:
        raise
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "url": target_url, "time": datetime.now().isoformat()})
        raise HTTPException(status_code=502, detail=f"Proxy error: {exc}")

# ── Public sub page ───────────────────────────────────────────────────────────
@app.get("/p/{uuid_key}", response_class=HTMLResponse)
async def public_sub_page(uuid_key: str, request: Request):
    from pages import get_public_page_html
    async with SUBS_LOCK:
        sub = next(({"sub_id": sid, **s} for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        return HTMLResponse("<h2 style='font-family:sans-serif;padding:40px'>گروه پیدا نشد</h2>", status_code=404)
    return HTMLResponse(content=get_public_page_html(uuid_key, white_label=bool(sub.get("white_label"))))

@app.get("/api/public/sub/{uuid_key}")
async def public_sub_data(uuid_key: str, request: Request):
    async with SUBS_LOCK:
        sub_entry = next(((sid, s) for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
    if not sub_entry:
        raise HTTPException(status_code=404, detail="not found")
    sub_id, sub = sub_entry

    has_pw = sub.get("password_hash") is not None
    if has_pw:
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            return JSONResponse({"locked": True, "name": sub["name"]})

    host = get_host()
    link_ids = sub.get("link_ids", [])
    white_label = bool(sub.get("white_label"))
    async with LINKS_LOCK:
        snap = dict(LINKS)

    links_out = []
    active_conns = 0
    for lid in link_ids:
        link = snap.get(lid)
        if not link:
            continue
        allowed = is_link_allowed(link)
        conn_count = sum(1 for c in connections.values() if c.get("uuid") == lid)
        active_conns += conn_count
        proto = link.get("protocol", DEFAULT_PROTOCOL)
        used_bytes = link.get("used_bytes", 0)
        limit_bytes = link.get("limit_bytes", 0)
        bundle = generate_all_vless_links(lid, host, link["label"], used_bytes, limit_bytes, brand=not white_label)
        links_out.append({
            "uuid": lid,
            "label": link["label"],
            "active": allowed,
            "protocol": proto,
            "used_bytes": used_bytes,
            "used_fmt": fmt_bytes(used_bytes),
            "limit_bytes": limit_bytes,
            "limit_fmt": "∞" if limit_bytes == 0 else fmt_bytes(limit_bytes),
            "expires_at": link.get("expires_at"),
            "vless_link": next((b["vless_link"] for b in bundle if b["protocol"] == proto), bundle[0]["vless_link"]),
            "vless_links": bundle,
            "sub_url": f"https://{host}/sub/{lid}",
            "connections": conn_count,
        })

    total_used = sum(l["used_bytes"] for l in links_out)
    pool_limit = sub.get("pool_limit_bytes", 0)
    pool_alloc = sub.get("pool_allocated_bytes", 0)
    pool_available = max(0, pool_limit - pool_alloc) if pool_limit else 0
    return {
        "locked": False,
        "name": sub["name"],
        "desc": sub.get("desc", ""),
        "sub_url": f"https://{host}/sub-group/{uuid_key}",
        "active_connections": active_conns,
        "total_used_fmt": fmt_bytes(total_used),
        "links": links_out,
        "white_label": white_label,
        # ✅ فیچر «تقسیم سهمیه»: اگر ادمین برای این ساب یک سقف (pool) تعیین
        # کرده باشد، صاحب ساب می‌تواند از همین صفحه بخشی از باقی‌مانده‌ی
        # سقف را جدا کند و به‌عنوان یک ساب مستقل و کاملاً سفید-برند (بدون
        # هیچ نام/لوگویی) به کس دیگری بدهد.
        "pool_enabled": pool_limit > 0,
        "pool_limit_bytes": pool_limit,
        "pool_allocated_bytes": pool_alloc,
        "pool_available_bytes": pool_available,
        "pool_limit_fmt": fmt_bytes(pool_limit) if pool_limit else "—",
        "pool_available_fmt": fmt_bytes(pool_available) if pool_limit else "—",
    }

@app.post("/api/public/sub/{uuid_key}/split")
async def split_sub_quota(uuid_key: str, request: Request):
    """صاحب یک ساب استخردار (pool-managed) بخشی از سهمیه‌ی باقی‌مانده‌ی خودش را
    جدا می‌کند و یک ساب-فرزند کاملاً مستقل و سفید-برند (بدون هیچ نام/لوگویی)
    می‌سازد که می‌تواند به کس دیگری بدهد. سهمیه‌ی جداشده از سقف ساب خودش کم
    می‌شود (رزرو می‌شود) تا امکان دوباره‌فروشی بیش از حجم واقعی وجود نداشته
    باشد."""
    body = await request.json()
    pw = str(body.get("pw", ""))
    amount_value = float(body.get("amount_value") or 0)
    amount_unit = str(body.get("amount_unit") or "GB")
    child_label = str(body.get("label") or "کانفیگ هدیه").strip()[:60]
    child_name = str(body.get("name") or "ساب هدیه").strip()[:60]

    async with SUBS_LOCK:
        sub_entry = next(((sid, s) for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
        if not sub_entry:
            raise HTTPException(status_code=404, detail="not found")
        sub_id, sub = sub_entry
        if sub.get("password_hash") and hash_password(pw) != sub["password_hash"]:
            raise HTTPException(status_code=403, detail="رمز اشتباه است")

        pool_limit = sub.get("pool_limit_bytes", 0)
        if pool_limit <= 0:
            raise HTTPException(status_code=400, detail="این ساب قابلیت تقسیم حجم ندارد")
        pool_alloc = sub.get("pool_allocated_bytes", 0)
        available = max(0, pool_limit - pool_alloc)

        amount_bytes = parse_size_to_bytes(amount_value, amount_unit) if amount_value > 0 else 0
        if amount_bytes <= 0:
            raise HTTPException(status_code=400, detail="حجم نامعتبر است")
        if amount_bytes > available:
            raise HTTPException(status_code=400, detail=f"فقط {fmt_bytes(available)} از این ساب باقی مانده است")

        host = get_host()
        child_uuid = generate_uuid()
        child_sub_id = generate_uuid()
        child_uuid_key = secrets.token_urlsafe(16)

        # سهمیه از استخر والد رزرو می‌شود — چه دوستش همین الان مصرف کند چه نه
        sub["pool_allocated_bytes"] = pool_alloc + amount_bytes
        sub.setdefault("child_sub_ids", []).append(child_sub_id)

        SUBS[child_sub_id] = {
            "name": child_name,
            "desc": "",
            "password_hash": None,
            "uuid_key": child_uuid_key,
            "created_at": datetime.now().isoformat(),
            "link_ids": [child_uuid],
            # سهمیه‌ی فرزند همان مقدار جداشده است و همان‌جا کامل رزرو شده،
            # پس این ساب دیگر خودش قابل تقسیم مجدد نیست (available=0)
            "pool_limit_bytes": amount_bytes,
            "pool_allocated_bytes": amount_bytes,
            "parent_sub_id": sub_id,
            "child_sub_ids": [],
            "white_label": True,
        }

    async with LINKS_LOCK:
        LINKS[child_uuid] = {
            "label": child_label,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "used_bytes": 0,
            "limit_bytes": amount_bytes,
            "expires_at": None,
            "note": "",
            "protocol": DEFAULT_PROTOCOL,
            "sub_id": child_sub_id,
        }

    await schedule_save()
    log_activity("sub", f"«{sub['name']}» مقدار {fmt_bytes(amount_bytes)} را به یک ساب هدیه‌ی جدید تقسیم کرد", "ok")

    return {
        "ok": True,
        "public_url": f"https://{host}/p/{child_uuid_key}",
        "sub_url": f"https://{host}/sub-group/{child_uuid_key}",
        "amount_fmt": fmt_bytes(amount_bytes),
        "pool_available_fmt": fmt_bytes(max(0, pool_limit - sub['pool_allocated_bytes'])),
    }

# ── HTML Pages (login + dashboard) ───────────────────────────────────────────
from pages import LOGIN_HTML, DASHBOARD_HTML

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(url="/timazadi")
    return HTMLResponse(content=LOGIN_HTML)

@app.get("/timazadi", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(url="/login")
    await ensure_default_link()
    return HTMLResponse(content=DASHBOARD_HTML)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_redirect(request: Request):
    return RedirectResponse(url="/timazadi")

@app.get("/test-ws", response_class=HTMLResponse)
async def test_ws_redirect():
    return HTMLResponse(content="<script>location.href='/timazadi'</script>")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=CONFIG["port"], log_level="info", workers=1)
