# assets.py - لوگو و assets های تیم آزادی Gateway
# ══════════════════════════════════════════════════════════════════════════════
# شامل لوگوهای SVG به صورت base64 برای استفاده در صفحات مختلف
# ══════════════════════════════════════════════════════════════════════════════

# ── لوگوی اصلی تیم آزادی (SVG) ──────────────────────────────────────────────
LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#8B5CF6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#EC4899;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="logoGrad2" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1E40AF;stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:#7C3AED;stop-opacity:0.3" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  
  <!-- پس‌زمینه -->
  <rect width="100" height="100" rx="22" fill="url(#logoGrad)"/>
  <rect width="100" height="100" rx="22" fill="url(#logoGrad2)"/>
  
  <!-- حلقه‌های تزئینی -->
  <circle cx="50" cy="50" r="38" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
  <circle cx="50" cy="50" r="28" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  
  <!-- نماد اصلی - حرف "ت" به صورت خلاقانه -->
  <g filter="url(#glow)">
    <text x="50" y="68" font-family="'Vazirmatn', 'Arial', sans-serif" 
          font-size="52" font-weight="900" text-anchor="middle" 
          fill="white" letter-spacing="-2">
      ت
    </text>
  </g>
  
  <!-- نقطه‌ی تزئینی زیر حرف -->
  <circle cx="50" cy="82" r="3" fill="rgba(255,255,255,0.6)"/>
  
  <!-- خط‌های موج‌دار تزئینی -->
  <path d="M15 88 Q30 82 45 88 Q60 94 75 88 Q85 84 90 88" 
        fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
</svg>"""

# ── لوگوی کوچک (برای favicon و هدر) ──────────────────────────────────────
LOGO_SVG_SMALL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">
  <defs>
    <linearGradient id="logoSmall" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3B82F6" />
      <stop offset="100%" style="stop-color:#8B5CF6" />
    </linearGradient>
  </defs>
  <rect width="40" height="40" rx="10" fill="url(#logoSmall)"/>
  <text x="20" y="28" font-family="'Arial', sans-serif" font-size="22" font-weight="bold" text-anchor="middle" fill="white">ت</text>
</svg>"""

# ── لوگوی سفید (برای تم تاریک) ─────────────────────────────────────────────
LOGO_SVG_WHITE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="logoWhite" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#60A5FA" />
      <stop offset="100%" style="stop-color:#A78BFA" />
    </linearGradient>
  </defs>
  <rect width="100" height="100" rx="22" fill="#0a1628" stroke="rgba(96,165,250,0.2)" stroke-width="1.5"/>
  <rect width="94" height="94" x="3" y="3" rx="19" fill="none" stroke="rgba(96,165,250,0.08)" stroke-width="1"/>
  <text x="50" y="68" font-family="'Vazirmatn', 'Arial', sans-serif" font-size="52" font-weight="900" text-anchor="middle" fill="url(#logoWhite)">ت</text>
</svg>"""

# ── لوگوی برند (برای صفحات سفید-برند) ──────────────────────────────────────
LOGO_SVG_BRANDLESS = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="brandless" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6B7280" />
      <stop offset="100%" style="stop-color:#9CA3AF" />
    </linearGradient>
  </defs>
  <rect width="100" height="100" rx="22" fill="#1F2937" stroke="rgba(107,114,128,0.2)" stroke-width="1"/>
  <circle cx="50" cy="40" r="16" fill="none" stroke="url(#brandless)" stroke-width="2"/>
  <path d="M50 56 L50 80" stroke="url(#brandless)" stroke-width="2" stroke-linecap="round"/>
  <path d="M35 70 L65 70" stroke="url(#brandless)" stroke-width="2" stroke-linecap="round"/>
</svg>"""

# ── تبدیل به Data URI ──────────────────────────────────────────────────────
import base64
from urllib.parse import quote

def svg_to_data_uri(svg: str) -> str:
    """تبدیل SVG به Data URI"""
    # حذف فاصله‌های اضافی و فشرده‌سازی
    svg_min = svg.replace('\n', '').replace('  ', ' ').replace('> <', '><')
    encoded = quote(svg_min, safe='')
    return f"data:image/svg+xml,{encoded}"

LOGO_DATA_URI = svg_to_data_uri(LOGO_SVG)
LOGO_SMALL_URI = svg_to_data_uri(LOGO_SVG_SMALL)
LOGO_WHITE_URI = svg_to_data_uri(LOGO_SVG_WHITE)
LOGO_BRANDLESS_URI = svg_to_data_uri(LOGO_SVG_BRANDLESS)

# ── Favicon (Base64) ──────────────────────────────────────────────────────
FAVICON_BASE64 = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Cdefs%3E%3ClinearGradient id='f' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%233B82F6'/%3E%3Cstop offset='100%25' style='stop-color:%238B5CF6'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='40' height='40' rx='8' fill='url(%23f)'/%3E%3Ctext x='20' y='28' font-family='Arial' font-size='22' font-weight='bold' text-anchor='middle' fill='white'%3Eت%3C/text%3E%3C/svg%3E"

# ── رنگ‌های برند ──────────────────────────────────────────────────────────
BRAND_COLORS = {
    "primary": "#3B82F6",
    "primary_dark": "#2563EB",
    "primary_light": "#60A5FA",
    "secondary": "#8B5CF6",
    "secondary_dark": "#7C3AED",
    "secondary_light": "#A78BFA",
    "accent": "#EC4899",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "dark_bg": "#060f1d",
    "card_bg": "#0d1b2e",
}

# ── فونت‌ها ────────────────────────────────────────────────────────────────
FONTS = {
    "primary": "'Vazirmatn', sans-serif",
    "mono": "ui-monospace, 'JetBrains Mono', monospace",
}

# ── متادیتا ─────────────────────────────────────────────────────────────────
META = {
    "name": "تیم آزادی Gateway",
    "version": "10.0",
    "description": "پنل مدیریت VPN با قابلیت‌های پیشرفته",
    "author": "تیم آزادی",
    "telegram": "https://t.me/TimAzadi",
    "github": "https://github.com/timazadi/gateway",
}

# ── استایل‌های مشترک (CSS) ────────────────────────────────────────────────
COMMON_STYLES = """
:root {
  --bg-primary: #060f1d;
  --bg-secondary: #0a1628;
  --bg-card: #0d1b2e;
  --bg-card-hover: #12243f;
  --text-primary: #E8F4FF;
  --text-secondary: #7BAED4;
  --text-muted: #3D6B8E;
  --accent: #3B82F6;
  --accent-hover: #2563EB;
  --accent-light: #60A5FA;
  --accent-dark: #1D4ED8;
  --accent-glow: rgba(59,130,246,0.3);
  --border-color: rgba(59,130,246,0.12);
  --border-hover: rgba(59,130,246,0.25);
  --shadow: 0 4px 24px rgba(0,0,0,0.35);
  --radius: 16px;
  --transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
"""

# ── استایل‌های Glassmorphism ──────────────────────────────────────────────
GLASS_STYLES = """
.glass {
  background: rgba(13, 27, 46, 0.7);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(59, 130, 246, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
.glass-light {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.glass-dark {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.05);
}
"""

# ── استایل‌های انیمیشن ──────────────────────────────────────────────────
ANIMATION_STYLES = """
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
@keyframes breathe {
  0%, 100% { transform: scale(1); opacity: 0.6; }
  50% { transform: scale(1.05); opacity: 1; }
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
"""
