async def _send_link_and_qr(chat_id, uid: str):
    """ارسال لینک‌های کانفیگ و QR کد با مدیریت خطا"""
    logger.info(f"telegram_bot: _send_link_and_qr called for uid={uid}")
    try:
        async with LINKS_LOCK:
            d = LINKS.get(uid)
        if not d:
            logger.warning(f"telegram_bot: link not found for uid={uid}")
            await _send(chat_id, "❌ این کانفیگ دیگر وجود ندارد.")
            return
        
        host = get_host()
        logger.info(f"telegram_bot: host={host}")
        if not host or host == "localhost":
            await _send(chat_id, "❌ آدرس سرور تنظیم نشده است. لطفاً متغیر محیطی RAILWAY_PUBLIC_DOMAIN را در Railway تنظیم کنید.")
            return
        
        label = d.get("label", "کانفیگ")
        used_bytes = d.get("used_bytes", 0)
        limit_bytes = d.get("limit_bytes", 0)
        flag = d.get("flag", "")
        
        logger.info(f"telegram_bot: generating links for label={label}, host={host}")
        
        # تولید لینک‌ها با try/except جداگانه
        try:
            bundle = generate_all_vless_links(uid, host, label, used_bytes, limit_bytes, flag=flag)
            if not bundle or len(bundle) == 0:
                logger.error(f"telegram_bot: bundle empty for uid={uid}")
                await _send(chat_id, "❌ خطا در تولید لینک. لطفاً دوباره تلاش کنید.")
                return
            logger.info(f"telegram_bot: bundle generated with {len(bundle)} protocols")
        except Exception as e:
            logger.error(f"telegram_bot: generate_all_vless_links error: {e}", exc_info=True)
            await _send(chat_id, f"❌ خطا در تولید لینک: {str(e)[:100]}")
            return
        
        primary = bundle[0]["vless_link"]
        all_text = "\n".join(b["vless_link"] for b in bundle)
        sub_url = f"https://{host}/sub/{uid}"
        
        text = f"🔗 <b>{label}</b>\n\n<code>{all_text}</code>\n\n📡 لینک ساب:\n{sub_url}"
        
        # ساخت QR با try/except جداگانه
        try:
            qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=" + _urlquote(primary, safe="")
            logger.info(f"telegram_bot: sending photo to chat_id={chat_id}")
            await _send(chat_id, text, photo=qr_url)
            logger.info(f"telegram_bot: photo sent successfully")
        except Exception as e:
            logger.warning(f"telegram_bot: QR send error: {e}", exc_info=True)
            # اگر QR خطا داد، حداقل لینک رو بفرست
            kb = [[{"text": "⬅️ منوی اصلی", "callback_data": "m:main"}]]
            await _send(chat_id, text + "\n\n⚠️ QR code قابل ارسال نبود، لینک‌ها بالا ارسال شدند.", kb)
            
    except Exception as e:
        logger.error(f"telegram_bot: _send_link_and_qr error: {e}", exc_info=True)
        await _send(chat_id, f"❌ خطای غیرمنتظره: {str(e)[:200]}")
