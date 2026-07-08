# rate_limiter.py
# ============================================================
# 🛡️ Rate Limiting - جلوگیری از اسپم درخواست
# ============================================================
from collections import defaultdict
import time
import asyncio

RATE_LIMIT = 20
RATE_WINDOW = 60

_rate_store = defaultdict(list)
_rate_lock = asyncio.Lock()

async def check_rate_limit(ip: str) -> bool:
    now = time.time()
    async with _rate_lock:
        _rate_store[ip] = [t for t in _rate_store[ip] if now - t < RATE_WINDOW]
        if len(_rate_store[ip]) >= RATE_LIMIT:
            return False
        _rate_store[ip].append(now)
        return True
