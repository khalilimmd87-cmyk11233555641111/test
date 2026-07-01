# pages.py – تیم آزادی · RVG Gateway v9.0

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · تیم آزادی</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg-base:#0B1220;
  --bg-elevated:#111827;
  --glass-bg:rgba(17,24,39,0.7);
  --accent:#3B82F6;
  --accent-soft:#60A5FA;
  --accent-glow:rgba(59,130,246,0.35);
  --border:rgba(59,130,246,0.15);
  --text-primary:#F1F5F9;
  --text-secondary:#94A3B8;
  --text-muted:#64748B;
  --error:#EF4444;
  --error-bg:rgba(239,68,68,0.1);
  --radius:16px;
  --transition:0.25s cubic-bezier(0.4,0,0.2,1);
}
html,body{height:100%;overflow:hidden}
body{
  font-family:'Vazirmatn',sans-serif;
  background:var(--bg-base);
  display:flex;
  align-items:center;
  justify-content:center;
  padding:20px;
  position:relative;
}
.bg-layer{
  position:fixed;inset:0;z-index:0;
  background:
    radial-gradient(ellipse 70% 50% at 50% 0%,rgba(59,130,246,0.08),transparent 60%),
    var(--bg-base);
}
.grid-overlay{
  position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:
    linear-gradient(rgba(59,130,246,0.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(59,130,246,0.03) 1px,transparent 1px);
  background-size:44px 44px;
}
.particles{
  position:fixed;inset:0;z-index:0;pointer-events:none;
  overflow:hidden;
}
.particle{
  position:absolute;
  border-radius:50%;
  background:rgba(96,165,250,0.2);
  filter:blur(60px);
  animation:float 12s ease-in-out infinite;
}
.particle:nth-child(1){width:320px;height:320px;top:-100px;right:-80px;animation-delay:0s}
.particle:nth-child(2){width:220px;height:220px;bottom:-80px;left:-60px;animation-delay:4s}
.particle:nth-child(3){width:180px;height:180px;top:40%;left:-90px;animation-delay:8s}
@keyframes float{
  0%,100%{transform:translateY(0) scale(1)}
  50%{transform:translateY(-20px) scale(1.05)}
}
.wrapper{
  position:relative;z-index:10;
  width:100%;max-width:420px;
  animation:fadeInUp 0.6s cubic-bezier(0.2,0.8,0.2,1);
}
@keyframes fadeInUp{
  from{opacity:0;transform:translateY(24px)}
  to{opacity:1;transform:none}
}
.glass-card{
  background:var(--glass-bg);
  backdrop-filter:blur(32px);
  -webkit-backdrop-filter:blur(32px);
  border:1px solid var(--border);
  border-radius:24px;
  padding:40px 36px;
  box-shadow:
    0 20px 60px rgba(0,0,0,0.5),
    0 0 80px var(--accent-glow);
  transition:box-shadow var(--transition);
}
.glass-card:hover{
  box-shadow:
    0 25px 70px rgba(0,0,0,0.55),
    0 0 100px var(--accent-glow);
}
.brand-row{
  display:flex;align-items:center;gap:14px;margin-bottom:32px;
}
.brand-logo{
  width:48px;height:48px;
  border-radius:14px;
  overflow:hidden;
  border:1px solid var(--border);
  box-shadow:0 0 24px var(--accent-glow);
  flex-shrink:0;
}
.brand-logo img{width:100%;height:100%;object-fit:cover}
.brand-name{font-size:18px;font-weight:700;color:var(--text-primary);letter-spacing:-0.02em}
.brand-ver{font-size:11px;color:var(--text-muted);margin-top:2px}
h1{
  font-size:22px;font-weight:700;
  color:var(--text-primary);
  margin-bottom:6px;
  letter-spacing:-0.03em;
}
.subtitle{
  font-size:13px;color:var(--text-secondary);
  margin-bottom:28px;line-height:1.6;
}
.hint-box{
  display:flex;align-items:center;gap:12px;
  background:rgba(59,130,246,0.06);
  border:1px solid rgba(59,130,246,0.2);
  border-radius:12px;
  padding:12px 16px;
  margin-bottom:24px;
}
.hint-label{font-size:12px;color:var(--text-muted)}
.hint-value{
  font-family:ui-monospace,monospace;
  font-size:15px;font-weight:700;
  color:var(--accent);
  background:rgba(59,130,246,0.15);
  border:1px solid rgba(59,130,246,0.3);
  padding:4px 12px;
  border-radius:8px;
  cursor:pointer;
  transition:all 0.15s;
  letter-spacing:0.06em;
}
.hint-value:hover{
  background:rgba(59,130,246,0.25);
  transform:scale(1.03);
}
.error-msg{
  display:none;
  align-items:center;gap:10px;
  background:var(--error-bg);
  border:1px solid rgba(239,68,68,0.25);
  border-radius:12px;
  padding:12px 16px;
  margin-bottom:20px;
  font-size:13px;color:#FCA5A5;
  animation:shake 0.4s ease;
}
.error-msg.show{display:flex}
@keyframes shake{
  0%,100%{transform:translateX(0)}
  25%{transform:translateX(-6px)}
  50%{transform:translateX(6px)}
  75%{transform:translateX(-3px)}
}
.field{margin-bottom:22px}
.field label{
  display:block;
  font-size:11px;font-weight:600;
  color:var(--text-secondary);
  margin-bottom:8px;
  text-transform:uppercase;
  letter-spacing:0.08em;
}
.input-wrap{position:relative}
.input-wrap input[type=password]{
  width:100%;
  padding:14px 44px 14px 16px;
  border-radius:14px;
  border:1px solid var(--border);
  background:rgba(15,23,42,0.6);
  color:var(--text-primary);
  font-family:inherit;
  font-size:15px;
  outline:none;
  transition:all var(--transition);
}
.input-wrap input:focus{
  border-color:var(--accent);
  background:rgba(15,23,42,0.8);
  box-shadow:0 0 0 4px rgba(59,130,246,0.15);
}
.input-icon{
  position:absolute;left:14px;top:50%;
  transform:translateY(-50%);
  color:var(--text-muted);
  font-size:20px;
  pointer-events:none;
  transition:color var(--transition);
}
.input-wrap input:focus ~ .input-icon{color:var(--accent)}
.login-btn{
  width:100%;
  padding:15px;
  border-radius:14px;
  border:none;
  cursor:pointer;
  background:linear-gradient(135deg,#2563EB,#1D4ED8);
  color:#fff;
  font-family:inherit;
  font-size:15px;
  font-weight:600;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:10px;
  box-shadow:0 6px 24px rgba(37,99,235,0.4);
  transition:all 0.2s;
  position:relative;
  overflow:hidden;
}
.login-btn::after{
  content:'';
  position:absolute;
  inset:0;
  background:rgba(255,255,255,0.1);
  opacity:0;
  transition:opacity 0.2s;
}
.login-btn:hover::after{opacity:1}
.login-btn:hover{
  transform:translateY(-2px);
  box-shadow:0 10px 30px rgba(37,99,235,0.5);
}
.login-btn:active{transform:translateY(0)}
.login-btn:disabled{opacity:0.6;cursor:not-allowed;transform:none}
.footer-row{
  margin-top:28px;
  padding-top:20px;
  border-top:1px solid var(--border);
  display:flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  font-size:12px;
  color:var(--text-muted);
}
.footer-row a{
  color:var(--accent-soft);
  font-weight:600;
  text-decoration:none;
  display:flex;
  align-items:center;
  gap:4px;
  transition:color 0.15s;
}
.footer-row a:hover{color:#93C5FD}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="bg-layer"></div>
<div class="grid-overlay"></div>
<div class="particles">
  <div class="particle"></div>
  <div class="particle"></div>
  <div class="particle"></div>
</div>
<div class="wrapper">
  <div class="glass-card">
    <div class="brand-row">
      <div class="brand-logo"><img src="https://sftaq.ir/photo_2026-06-11_23-01-59.jpg" alt="تیم آزادی"></div>
      <div>
        <div class="brand-name">تیم آزادی</div>
        <div class="brand-ver">RVG Gateway · v9.0</div>
      </div>
    </div>
    <h1>ورود به پنل مدیریت</h1>
    <p class="subtitle">لطفاً رمز عبور امن خود را وارد کنید</p>
    <div class="error-msg" id="err"><i class="ti ti-alert-circle" style="font-size:18px"></i><span id="err-text"></span></div>
    <div class="hint-box">
      <span class="hint-label">رمز پیش‌فرض سیستم</span>
      <span class="hint-value" onclick="document.getElementById('pw').value='@TimAzadi';document.getElementById('pw').focus()">@TimAzadi</span>
    </div>
    <form id="form">
      <div class="field">
        <label>رمز عبور</label>
        <div class="input-wrap">
          <input type="password" id="pw" placeholder="••••••••" autofocus required>
          <i class="ti ti-lock input-icon"></i>
        </div>
      </div>
      <button class="login-btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود به داشبورد</button>
    </form>
    <div class="footer-row">
      کانال رسمی
      <a href="https://t.me/TimAzadi" target="_blank"><i class="ti ti-brand-telegram"></i> @TimAzadi</a>
    </div>
  </div>
</div>
<script>
document.getElementById('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('btn'),err=document.getElementById('err'),et=document.getElementById('err-text');
  err.classList.remove('show');btn.disabled=true;
  btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال ورود...';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:document.getElementById('pw').value})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'خطا');}
    location.href='/panel';
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.innerHTML='<i class="ti ti-login-2"></i> ورود به داشبورد';
  }
});
</script>
</body></html>"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>داشبورد · تیم آزادی</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
/* ── Design System ── */
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg-root:#0B1220;
  --bg-surface:#111827;
  --bg-elevated:#1E293B;
  --glass-bg:rgba(17,24,39,0.75);
  --glass-border:rgba(59,130,246,0.12);
  --accent:#3B82F6;
  --accent-soft:#60A5FA;
  --accent-glow:rgba(59,130,246,0.4);
  --green:#10B981;--green-bg:rgba(16,185,129,0.12);
  --red:#EF4444;--red-bg:rgba(239,68,68,0.12);
  --amber:#F59E0B;--amber-bg:rgba(245,158,11,0.12);
  --purple:#8B5CF6;--purple-bg:rgba(139,92,246,0.12);
  --text-primary:#F1F5F9;
  --text-secondary:#94A3B8;
  --text-muted:#64748B;
  --radius-sm:10px;
  --radius-md:14px;
  --radius-lg:20px;
  --shadow-card:0 8px 32px rgba(0,0,0,0.3);
  --shadow-glow:0 0 40px var(--accent-glow);
  --transition:0.25s cubic-bezier(0.4,0,0.2,1);
}
[data-theme="light"]{
  --bg-root:#F8FAFC;
  --bg-surface:#FFFFFF;
  --bg-elevated:#F1F5F9;
  --glass-bg:rgba(255,255,255,0.8);
  --glass-border:rgba(59,130,246,0.15);
  --accent:#2563EB;
  --accent-soft:#1D4ED8;
  --accent-glow:rgba(37,99,235,0.2);
  --text-primary:#0F172A;
  --text-secondary:#334155;
  --text-muted:#64748B;
  --shadow-card:0 8px 24px rgba(0,0,0,0.06);
}

html,body{height:100%}
body{
  font-family:'Vazirmatn',sans-serif;
  background:var(--bg-root);
  color:var(--text-primary);
  display:flex;
  font-size:14px;
  transition:background 0.3s,color 0.3s;
}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--text-muted);border-radius:3px}

/* ── Sidebar ── */
.sidebar{
  width:260px;
  min-height:100vh;
  background:var(--glass-bg);
  backdrop-filter:blur(32px);
  -webkit-backdrop-filter:blur(32px);
  border-left:1px solid var(--glass-border);
  display:flex;
  flex-direction:column;
  flex-shrink:0;
  position:fixed;
  right:0;top:0;bottom:0;
  z-index:200;
  transition:transform 0.3s cubic-bezier(0.4,0,0.2,1),background 0.3s,border-color 0.3s;
  border-radius:0 20px 20px 0;
  box-shadow:var(--shadow-card);
}
.logo-block{
  display:flex;align-items:center;gap:12px;
  padding:24px 20px 18px;
  border-bottom:1px solid var(--glass-border);
}
.logo-img{
  width:40px;height:40px;
  border-radius:12px;
  overflow:hidden;
  border:1px solid var(--glass-border);
  box-shadow:0 0 18px var(--accent-glow);
}
.logo-img img{width:100%;height:100%;object-fit:cover}
.logo-name{font-size:15px;font-weight:700;color:var(--text-primary)}
.logo-sub{font-size:10px;color:var(--text-muted);margin-top:2px}

.sb-close{
  display:none;
  position:absolute;left:14px;top:22px;
  background:rgba(59,130,246,0.1);
  border:1px solid var(--glass-border);
  color:var(--text-secondary);
  width:32px;height:32px;
  border-radius:10px;
  font-size:18px;
  align-items:center;justify-content:center;
  cursor:pointer;
  transition:background 0.15s;
}
.sb-close:hover{background:rgba(59,130,246,0.2)}

.nav-wrap{flex:1;overflow-y:auto;padding:8px 0}
.nav-section{
  padding:16px 18px 6px;
  font-size:10px;font-weight:700;
  text-transform:uppercase;
  letter-spacing:0.14em;
  color:var(--text-muted);
}
.nav-item{
  display:flex;align-items:center;gap:10px;
  padding:11px 18px;
  margin:2px 10px;
  border-radius:var(--radius-sm);
  color:var(--text-secondary);
  font-size:13px;
  cursor:pointer;
  transition:all 0.15s;
  position:relative;
}
.nav-item i{font-size:18px;width:20px;text-align:center;flex-shrink:0}
.nav-item:hover{
  background:rgba(59,130,246,0.08);
  color:var(--text-primary);
}
.nav-item.on{
  background:rgba(59,130,246,0.15);
  color:var(--accent-soft);
  font-weight:600;
}
.nav-item.on::before{
  content:'';
  position:absolute;
  right:0;top:12px;bottom:12px;
  width:3px;
  background:var(--accent);
  border-radius:3px;
}
.nav-badge{
  margin-right:auto;
  background:rgba(59,130,246,0.15);
  color:var(--accent-soft);
  font-size:10px;
  padding:2px 8px;
  border-radius:20px;
  font-weight:700;
}

.sb-foot{
  padding:16px 18px;
  border-top:1px solid var(--glass-border);
  display:flex;
  flex-direction:column;
  gap:8px;
}
.btn-telegram{
  display:flex;align-items:center;justify-content:center;gap:8px;
  background:linear-gradient(135deg,#0098e6,#0077bb);
  color:#fff;
  border-radius:10px;
  padding:10px;
  font-size:13px;font-weight:600;
  border:none;cursor:pointer;
  transition:filter 0.15s;
}
.btn-telegram:hover{filter:brightness(1.1)}
.btn-theme{
  display:flex;align-items:center;justify-content:center;gap:6px;
  background:rgba(59,130,246,0.08);
  color:var(--text-secondary);
  border:1px solid var(--glass-border);
  border-radius:10px;
  padding:8px;
  font-size:12px;
  cursor:pointer;
  transition:all 0.15s;
}
.btn-theme:hover{background:rgba(59,130,246,0.15);color:var(--text-primary)}
.btn-logout{
  display:flex;align-items:center;justify-content:center;gap:6px;
  background:var(--red-bg);
  color:#FCA5A5;
  border:1px solid rgba(239,68,68,0.2);
  border-radius:10px;
  padding:8px;
  font-size:12px;
  cursor:pointer;
  transition:all 0.15s;
}
.btn-logout:hover{background:rgba(239,68,68,0.25)}

/* ── Mobile top bar ── */
.mob-top{
  display:none;
  position:fixed;top:0;right:0;left:0;height:56px;
  background:var(--glass-bg);
  backdrop-filter:blur(24px);
  border-bottom:1px solid var(--glass-border);
  z-index:150;
  align-items:center;
  justify-content:space-between;
  padding:0 16px;
}
.mob-logo{width:32px;height:32px;border-radius:10px;overflow:hidden}
.mob-logo img{width:100%;height:100%}
.mob-title{font-size:14px;font-weight:700;color:var(--text-primary)}
.mob-actions{display:flex;gap:8px}
.menu-btn,.theme-mob{
  width:36px;height:36px;
  border-radius:10px;
  background:rgba(59,130,246,0.08);
  border:1px solid var(--glass-border);
  color:var(--text-secondary);
  font-size:18px;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;
}
.overlay{
  display:none;
  position:fixed;inset:0;
  background:rgba(0,0,0,0.6);
  backdrop-filter:blur(6px);
  z-index:190;
}
.overlay.show{display:block}

/* ── Main ── */
.main{
  margin-right:260px;
  flex:1;
  padding:32px 32px 80px;
  min-width:0;
  transition:margin 0.3s;
}
.page{
  display:none;
  animation:fadeSlide 0.25s ease;
}
.page.on{display:block}
@keyframes fadeSlide{
  from{opacity:0;transform:translateY(12px)}
  to{opacity:1;transform:none}
}

/* ── Top bar ── */
.topbar{
  display:flex;align-items:flex-start;justify-content:space-between;
  margin-bottom:28px;
  flex-wrap:wrap;gap:16px;
}
.tb-title{
  font-size:20px;font-weight:700;
  color:var(--text-primary);
  display:flex;align-items:center;gap:10px;
  letter-spacing:-0.03em;
}
.tb-title i{color:var(--accent);font-size:22px}
.tb-sub{font-size:12px;color:var(--text-muted);margin-top:6px}

.status-badge{
  font-size:10px;padding:4px 12px;
  border-radius:20px;
  font-weight:700;
  display:inline-flex;align-items:center;gap:6px;
  white-space:nowrap;
}
.bg-green{background:var(--green-bg);color:#34D399}
.bg-blue{background:rgba(59,130,246,0.12);color:var(--accent-soft)}
.bg-amber{background:var(--amber-bg);color:#FCD34D}
.bg-red{background:var(--red-bg);color:#FCA5A5}
.dot{width:6px;height:6px;border-radius:50%;display:inline-block}
.dg{background:var(--green)}.dr{background:var(--red)}
.da{background:var(--amber)}.db{background:var(--accent)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}

/* ── Metrics cards ── */
.metrics-grid{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:16px;
  margin-bottom:24px;
}
.metric-card{
  background:var(--glass-bg);
  backdrop-filter:blur(20px);
  border:1px solid var(--glass-border);
  border-radius:var(--radius-md);
  padding:20px;
  transition:all 0.25s;
  cursor:default;
}
.metric-card:hover{
  transform:translateY(-4px);
  box-shadow:var(--shadow-card),0 0 30px var(--accent-glow);
  border-color:rgba(59,130,246,0.25);
}
.metric-icon{
  width:36px;height:36px;
  border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  margin-bottom:14px;
  font-size:18px;
}
.metric-icon.blue{background:rgba(59,130,246,0.12);color:var(--accent-soft)}
.metric-icon.green{background:var(--green-bg);color:#34D399}
.metric-icon.purple{background:var(--purple-bg);color:#C084FC}
.metric-label{
  font-size:11px;font-weight:600;
  text-transform:uppercase;
  letter-spacing:0.06em;
  color:var(--text-muted);
  margin-bottom:6px;
}
.metric-value{
  font-size:26px;font-weight:700;
  color:var(--text-primary);
  line-height:1;
}
.metric-unit{font-size:14px;color:var(--text-muted);margin-right:4px}
.metric-sub{
  font-size:11px;color:var(--text-muted);
  margin-top:8px;
  display:flex;align-items:center;gap:4px;
}

/* ── Default link box ── */
.vless-hero{
  background:linear-gradient(135deg,var(--bg-elevated),var(--bg-surface));
  border:1px solid var(--glass-border);
  border-radius:var(--radius-lg);
  padding:24px 28px;
  margin-bottom:24px;
  position:relative;
  overflow:hidden;
}
.vless-hero::before{
  content:'';
  position:absolute;
  top:-60px;left:-60px;
  width:200px;height:200px;
  background:radial-gradient(circle,var(--accent-glow),transparent 70%);
  pointer-events:none;
}
.vl-header{
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:12px;
  margin-bottom:16px;
}
.vl-title{
  font-size:12px;font-weight:700;
  color:var(--text-secondary);
  text-transform:uppercase;
  letter-spacing:0.07em;
  display:flex;align-items:center;gap:8px;
}
.vl-title i{color:var(--accent);font-size:16px}
.vl-code{
  background:rgba(0,0,0,0.2);
  border:1px solid var(--glass-border);
  border-radius:12px;
  padding:14px 16px;
  font-family:ui-monospace,monospace;
  font-size:11px;
  color:var(--accent-soft);
  word-break:break-all;
  line-height:1.9;
}
.vl-actions{
  display:flex;gap:10px;
  margin-top:18px;
  flex-wrap:wrap;
}

/* ── Buttons ── */
.btn{
  font-family:inherit;font-size:12px;font-weight:600;
  border-radius:10px;
  padding:10px 16px;
  cursor:pointer;
  display:inline-flex;align-items:center;gap:6px;
  border:none;
  transition:all 0.15s;
  white-space:nowrap;
}
.btn i{font-size:14px}
.btn:disabled{opacity:0.5;cursor:not-allowed}
.btn-primary{
  background:linear-gradient(135deg,#2563EB,#1D4ED8);
  color:#fff;
  box-shadow:0 4px 16px rgba(37,99,235,0.3);
}
.btn-primary:hover{
  background:linear-gradient(135deg,#1D4ED8,#1E40AF);
  box-shadow:0 6px 20px rgba(37,99,235,0.4);
  transform:translateY(-1px);
}
.btn-ghost{
  background:transparent;
  border:1px solid var(--glass-border);
  color:var(--text-secondary);
}
.btn-ghost:hover{
  background:rgba(59,130,246,0.08);
  color:var(--text-primary);
}
.btn-subtle{
  background:rgba(59,130,246,0.08);
  color:var(--accent-soft);
  border:1px solid rgba(59,130,246,0.15);
}
.btn-subtle:hover{background:rgba(59,130,246,0.15)}
.btn-danger{
  background:var(--red-bg);
  color:#FCA5A5;
  border:1px solid rgba(239,68,68,0.2);
}
.btn-danger:hover{background:rgba(239,68,68,0.25)}
.btn-sm{padding:6px 10px;font-size:11px;border-radius:8px}

/* ── Cards ── */
.card{
  background:var(--glass-bg);
  backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:var(--radius-md);
  padding:20px 22px;
  transition:border-color 0.2s,box-shadow 0.2s;
}
.card:hover{
  border-color:rgba(59,130,246,0.2);
  box-shadow:0 4px 24px rgba(0,0,0,0.2);
}
.card-title{
  font-size:13px;font-weight:700;
  color:var(--text-primary);
  margin-bottom:16px;
  display:flex;align-items:center;gap:8px;
}
.card-title i{font-size:17px;color:var(--accent)}
.ml-auto{margin-right:auto}

/* ── Grid layouts ── */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:20px}
.mb20{margin-bottom:20px}

/* ── Service rows ── */
.service-row{
  display:flex;align-items:center;justify-content:space-between;
  padding:10px 0;
  border-bottom:1px solid rgba(59,130,246,0.05);
}
.service-row:last-child{border-bottom:none}
.sr-key{color:var(--text-secondary);display:flex;align-items:center;gap:6px;font-size:12px}
.sr-val{font-size:12px;font-weight:600;color:var(--text-primary)}

/* ── Progress bar ── */
.progress-bar{
  height:6px;
  border-radius:3px;
  background:rgba(59,130,246,0.1);
  overflow:hidden;
  margin-top:6px;
}
.progress-fill{
  height:100%;
  border-radius:3px;
  background:linear-gradient(90deg,var(--accent),var(--accent-soft));
  transition:width 0.8s;
}

/* ── Charts ── */
.chart-wrap{position:relative;height:220px}
.chart-wrap-lg{height:340px}
.chart-wrap-sm{height:180px}

/* ── Table ── */
.data-table{
  width:100%;border-collapse:collapse;
}
.data-table th{
  text-align:right;
  font-size:10px;font-weight:700;
  color:var(--text-muted);
  padding:10px 10px;
  border-bottom:1px solid var(--glass-border);
  text-transform:uppercase;
  letter-spacing:0.07em;
  white-space:nowrap;
}
.data-table td{
  padding:12px 10px;
  border-bottom:1px solid rgba(59,130,246,0.04);
  font-size:12px;
  vertical-align:middle;
}
.data-table tbody tr{transition:background 0.15s}
.data-table tbody tr:hover td{background:rgba(59,130,246,0.05)}

.uuid-chip{
  font-family:ui-monospace,monospace;
  font-size:10px;
  color:var(--accent-soft);
  background:rgba(59,130,246,0.1);
  padding:3px 8px;
  border-radius:6px;
  cursor:pointer;
}
.uuid-chip:hover{background:rgba(59,130,246,0.2)}
.usage-bar{height:6px;border-radius:3px;background:rgba(59,130,246,0.1);overflow:hidden;margin-bottom:4px}
.usage-fill{height:100%;border-radius:3px;transition:width 0.3s}
.exp-chip{
  font-size:10px;padding:3px 8px;
  border-radius:6px;
  font-weight:700;
  display:inline-flex;align-items:center;gap:4px;
}
.ec-ok{background:var(--green-bg);color:#34D399}
.ec-warn{background:var(--amber-bg);color:#FCD34D}
.ec-exp{background:var(--red-bg);color:#FCA5A5}
.ec-inf{background:rgba(59,130,246,0.12);color:var(--accent-soft)}

.toggle{
  width:34px;height:20px;
  border-radius:20px;
  background:rgba(100,116,139,0.3);
  position:relative;
  cursor:pointer;
  border:none;
  transition:background 0.2s;
}
.toggle::after{
  content:'';
  position:absolute;
  width:14px;height:14px;
  border-radius:50%;
  background:#fff;
  top:3px;right:3px;
  transition:right 0.2s;
}
.toggle.on{background:var(--green)}
.toggle.on::after{right:17px}

/* ── Form elements ── */
.form-row{display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end}
.fg{display:flex;flex-direction:column;gap:5px}
.fg label{
  font-size:10px;font-weight:700;
  color:var(--text-muted);
  text-transform:uppercase;
  letter-spacing:0.06em;
}
.input,.select{
  padding:9px 12px;
  border-radius:10px;
  border:1px solid var(--glass-border);
  background:rgba(0,0,0,0.2);
  color:var(--text-primary);
  font-family:inherit;
  font-size:12px;
  outline:none;
  transition:all 0.15s;
}
.input:focus,.select:focus{
  border-color:var(--accent);
  background:rgba(0,0,0,0.3);
  box-shadow:0 0 0 3px rgba(59,130,246,0.15);
}
[data-theme="light"] .input,[data-theme="light"] .select{
  background:rgba(0,0,0,0.03);
}

/* ── Info box ── */
.info-box{
  background:rgba(59,130,246,0.06);
  border:1px solid rgba(59,130,246,0.15);
  border-radius:10px;
  padding:12px 14px;
  font-size:11px;
  color:var(--text-secondary);
  display:flex;gap:8px;
  align-items:flex-start;
  line-height:1.8;
  margin-top:12px;
}
.info-box i{color:var(--accent);font-size:15px;margin-top:1px}
.info-box.amber{
  background:var(--amber-bg);
  border-color:rgba(245,158,11,0.25);
  color:#FCD34D;
}
.info-box.amber i{color:var(--amber)}

/* ── Subscription section ── */
.sub-grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(320px,1fr));
  gap:16px;
  margin-bottom:20px;
}
.sub-card{
  background:var(--glass-bg);
  backdrop-filter:blur(16px);
  border:1px solid var(--glass-border);
  border-radius:var(--radius-lg);
  padding:20px;
  transition:all 0.25s;
  position:relative;
  overflow:hidden;
}
.sub-card::before{
  content:'';
  position:absolute;
  top:0;right:0;
  width:4px;height:100%;
  background:var(--purple);
  opacity:0.6;
}
.sub-card:hover{
  transform:translateY(-3px);
  box-shadow:var(--shadow-card);
  border-color:rgba(139,92,246,0.3);
}
.sub-card-header{
  display:flex;align-items:flex-start;justify-content:space-between;
  gap:10px;margin-bottom:12px;
}
.sub-card-name{font-size:15px;font-weight:700}
.sub-card-desc{font-size:11px;color:var(--text-muted);margin-top:4px;line-height:1.6}
.public-url-box{
  background:rgba(139,92,246,0.08);
  border:1px solid rgba(139,92,246,0.2);
  border-radius:10px;
  padding:10px 14px;
  display:flex;align-items:center;gap:8px;
  flex-wrap:wrap;
  margin-bottom:12px;
}
.public-url-text{
  font-family:ui-monospace,monospace;
  font-size:11px;
  color:#C084FC;
  word-break:break-all;
  flex:1;
}
.sub-card-footer{
  display:flex;gap:6px;
  flex-wrap:wrap;
  padding-top:14px;
  border-top:1px solid var(--glass-border);
}

/* ── Modal ── */
.modal-bg{
  display:none;
  position:fixed;inset:0;
  background:rgba(0,0,0,0.65);
  backdrop-filter:blur(8px);
  z-index:500;
  align-items:center;justify-content:center;
}
.modal-bg.open{display:flex}
.modal{
  background:var(--bg-surface);
  border:1px solid var(--glass-border);
  border-radius:var(--radius-lg);
  padding:28px 28px;
  max-width:520px;
  width:calc(100% - 32px);
  max-height:90vh;
  overflow-y:auto;
  position:relative;
  animation:fadeSlide 0.2s ease;
  box-shadow:0 20px 60px rgba(0,0,0,0.5);
}
.modal-close{
  position:absolute;top:14px;left:14px;
  background:rgba(59,130,246,0.08);
  border:1px solid var(--glass-border);
  color:var(--text-secondary);
  width:30px;height:30px;
  border-radius:8px;
  cursor:pointer;
}
.modal-title{
  font-size:16px;font-weight:700;
  margin-bottom:20px;
  display:flex;align-items:center;gap:8px;
}
.modal-title i{color:var(--accent)}
.lrow{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(59,130,246,0.05)}
.lrow-check{width:16px;height:16px;accent-color:var(--accent)}

/* ── Toast ── */
.toast{
  position:fixed;bottom:24px;left:50%;
  transform:translateX(-50%) translateY(60px);
  background:var(--bg-surface);
  border:1px solid var(--glass-border);
  color:var(--text-primary);
  border-radius:12px;
  padding:12px 20px;
  font-size:13px;
  opacity:0;
  transition:all 0.25s;
  z-index:999;
  pointer-events:none;
  display:flex;align-items:center;gap:8px;
  box-shadow:var(--shadow-card);
}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,0.3);background:var(--green-bg);color:#34D399}
.toast.err{border-color:rgba(239,68,68,0.3);background:var(--red-bg);color:#FCA5A5}

/* ── Footer ── */
.dash-footer{
  border-top:1px solid var(--glass-border);
  margin-top:20px;
  padding-top:16px;
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:10px;
  font-size:10px;color:var(--text-muted);
}
.df-link{
  color:var(--accent-soft);
  font-weight:600;
  display:flex;align-items:center;gap:4px;
}

/* ── Empty state ── */
.empty-state{
  text-align:center;padding:48px 20px;
  color:var(--text-muted);
}
.empty-state i{font-size:36px;opacity:0.3;margin-bottom:12px;display:block}
.empty-state p{font-size:12px}

/* ── Responsive ── */
@media(max-width:1050px){
  .sidebar{
    transform:translateX(100%);
    border-radius:0;
  }
  .sidebar.open{transform:translateX(0);box-shadow:-20px 0 50px rgba(0,0,0,0.4)}
  .sb-close{display:flex}
  .main{margin-right:0;padding-top:72px}
  .mob-top{display:flex}
  .metrics-grid{grid-template-columns:1fr 1fr}
  .g2,.g3{grid-template-columns:1fr}
}
@media(max-width:500px){
  .metrics-grid{grid-template-columns:1fr}
  .main{padding:68px 12px 50px}
  .sub-grid{grid-template-columns:1fr}
}

@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>

<!-- Toast -->
<div class="toast" id="toast"></div>

<!-- Modal: مدیریت لینک‌های گروه -->
<div class="modal-bg" id="modal-links">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-links')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-link-plus"></i> مدیریت کانفیگ‌های <span id="modal-sub-name" style="color:var(--accent)">—</span></div>
    <div id="modal-links-body">در حال بارگذاری...</div>
    <div style="margin-top:20px;display:flex;gap:8px;justify-content:flex-end">
      <button class="btn btn-ghost" onclick="closeModal('modal-links')">بستن</button>
      <button class="btn btn-primary" id="modal-save-btn" onclick="saveSubLinks()"><i class="ti ti-check"></i> ذخیره</button>
    </div>
  </div>
</div>

<!-- Modal: ساخت گروه -->
<div class="modal-bg" id="modal-create-sub">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-create-sub')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-folder-plus"></i> ساخت گروه جدید</div>
    <div class="fg" style="margin-bottom:14px"><label>نام گروه</label><input class="input" id="ns-name" placeholder="مثلاً: کانال تلگرام" style="width:100%"></div>
    <div class="fg" style="margin-bottom:14px"><label>توضیحات (اختیاری)</label><input class="input" id="ns-desc" placeholder="توضیح کوتاه" style="width:100%"></div>
    <div class="fg" style="margin-bottom:18px"><label>رمز صفحه پابلیک (اختیاری)</label><input class="input" type="password" id="ns-pw" placeholder="خالی = بدون رمز" style="width:100%"></div>
    <div class="info-box"><i class="ti ti-info-circle"></i><span>صفحه پابلیک با لینک UUID-based در اینترنت قابل دسترس خواهد بود.</span></div>
    <div style="margin-top:18px;display:flex;gap:8px;justify-content:flex-end">
      <button class="btn btn-ghost" onclick="closeModal('modal-create-sub')">انصراف</button>
      <button class="btn btn-primary" onclick="createSub()"><i class="ti ti-folder-plus"></i> ساخت</button>
    </div>
  </div>
</div>

<!-- Mobile top bar -->
<div class="mob-top">
  <div style="display:flex;align-items:center;gap:10px">
    <div class="mob-logo"><img src="https://sftaq.ir/photo_2026-06-11_23-01-59.jpg" alt="تیم آزادی"></div>
    <span class="mob-title">تیم آزادی</span>
  </div>
  <div class="mob-actions">
    <button class="theme-mob" id="theme-mob-btn" onclick="toggleTheme()"><i class="ti ti-sun" id="theme-mob-icon"></i></button>
    <button class="menu-btn" id="open-sb"><i class="ti ti-menu-2"></i></button>
  </div>
</div>

<!-- Overlay -->
<div class="overlay" id="overlay"></div>

<!-- Sidebar -->
<aside class="sidebar" id="sb">
  <button class="sb-close" id="close-sb"><i class="ti ti-x"></i></button>
  <div class="logo-block">
    <div class="logo-img"><img src="https://sftaq.ir/photo_2026-06-11_23-01-59.jpg" alt="تیم آزادی"></div>
    <div>
      <div class="logo-name">تیم آزادی</div>
      <div class="logo-sub">RVG Gateway · v9.0</div>
    </div>
  </div>

  <div class="nav-wrap">
    <div class="nav-section">پنل</div>
    <div class="nav-item on" data-pg="overview"><i class="ti ti-layout-dashboard"></i> داشبورد</div>
    <div class="nav-item" data-pg="links"><i class="ti ti-link-plus"></i> کانفیگ‌ها <span class="nav-badge" id="links-nb">0</span></div>
    <div class="nav-item" data-pg="subgroups"><i class="ti ti-folders"></i> گروه‌های ساب <span class="nav-badge" id="subs-nb">0</span></div>
    <div class="nav-item" data-pg="subscriptions"><i class="ti ti-rss"></i> سابسکریپشن</div>
    <div class="nav-item" data-pg="traffic"><i class="ti ti-chart-area"></i> ترافیک</div>
    <div class="nav-item" data-pg="connections"><i class="ti ti-plug-connected"></i> اتصالات <span class="nav-badge" id="conns-nb">0</span></div>
    <div class="nav-section">سیستم</div>
    <div class="nav-item" data-pg="security"><i class="ti ti-shield-lock"></i> امنیت</div>
    <div class="nav-item" data-pg="errors"><i class="ti ti-alert-triangle"></i> خطاها</div>
    <div class="nav-item" data-pg="testws"><i class="ti ti-wifi"></i> تست WebSocket</div>
    <div class="nav-item" data-pg="settings"><i class="ti ti-settings"></i> تنظیمات</div>
  </div>

  <div class="sb-foot">
    <button class="btn-theme" onclick="toggleTheme()">
      <i class="ti ti-moon" id="theme-icon"></i> <span id="theme-label">تم روشن</span>
    </button>
    <a class="btn-telegram" href="https://t.me/TimAzadi" target="_blank">
      <i class="ti ti-brand-telegram"></i> @TimAzadi
    </a>
    <button class="btn-logout" id="logout-btn"><i class="ti ti-logout"></i> خروج</button>
  </div>
</aside>

<!-- Main Content -->
<main class="main">

  <!-- ─── صفحه داشبورد ─── -->
  <section class="page on" id="pg-overview">
    <div class="topbar">
      <div>
        <div class="tb-title"><i class="ti ti-layout-dashboard"></i> داشبورد</div>
        <div class="tb-sub" id="last-upd">در حال بارگذاری...</div>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        <span class="status-badge bg-green"><span class="dot dg pulse"></span> فعال</span>
        <span class="status-badge bg-blue" id="uptime-badge">—</span>
        <button class="btn btn-primary btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button>
      </div>
    </div>

    <div class="metrics-grid">
      <div class="metric-card">
        <div class="metric-icon blue"><i class="ti ti-plug-connected"></i></div>
        <div class="metric-label">اتصالات فعال</div>
        <div class="metric-value" id="m-conns">—</div>
        <div class="metric-sub"><span class="dot dg pulse"></span> WebSocket زنده</div>
      </div>
      <div class="metric-card">
        <div class="metric-icon blue"><i class="ti ti-transfer"></i></div>
        <div class="metric-label">کل ترافیک</div>
        <div class="metric-value" id="m-traffic">—<span class="metric-unit">MB</span></div>
        <div class="metric-sub">از راه‌اندازی</div>
      </div>
      <div class="metric-card">
        <div class="metric-icon green"><i class="ti ti-link"></i></div>
        <div class="metric-label">کانفیگ فعال</div>
        <div class="metric-value" id="m-alinks">—</div>
        <div class="metric-sub" id="m-lsub">از کل</div>
      </div>
      <div class="metric-card">
        <div class="metric-icon purple"><i class="ti ti-folders"></i></div>
        <div class="metric-label">گروه‌های ساب</div>
        <div class="metric-value" id="m-subs">—</div>
        <div class="metric-sub">فعال</div>
      </div>
    </div>

    <div class="vless-hero">
      <div class="vl-header">
        <div class="vl-title"><i class="ti ti-link"></i> لینک پیش‌فرض (بدون محدودیت)</div>
        <span class="status-badge bg-blue"><span class="dot db"></span> TLS 443 · WS</span>
      </div>
      <div class="vl-code" id="vless-main">در حال دریافت...</div>
      <div class="vl-actions">
        <button class="btn btn-primary" onclick="cpText('vless-main')"><i class="ti ti-copy"></i> کپی</button>
        <button class="btn btn-subtle" onclick="qrFor('vless-main')"><i class="ti ti-qrcode"></i> QR</button>
        <button class="btn btn-ghost" onclick="navTo('links')"><i class="ti ti-link-plus"></i> کانفیگ محدود</button>
        <button class="btn btn-ghost" onclick="navTo('subgroups')"><i class="ti ti-folders"></i> گروه‌های ساب</button>
      </div>
    </div>

    <div class="g3">
      <div class="card">
        <div class="card-title"><i class="ti ti-chart-area"></i> ترافیک ساعتی (MB)</div>
        <div class="chart-wrap"><canvas id="ch1"></canvas></div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-chart-donut"></i> توزیع</div>
        <div class="chart-wrap-sm"><canvas id="ch2"></canvas></div>
      </div>
    </div>

    <div class="g2">
      <div class="card">
        <div class="card-title"><i class="ti ti-activity"></i> وضعیت سرویس</div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-shield-check"></i> UUID Auth</span><span class="sr-val" style="color:#34D399">● فعال · سخت‌گیرانه</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-circle-check"></i> VLESS / WS Tunnel</span><span class="sr-val" style="color:#34D399">● فعال</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-folders"></i> Sub Groups</span><span class="sr-val" style="color:#34D399">● فعال v9</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-rss"></i> Subscription API</span><span class="sr-val" style="color:#34D399">● فعال</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-clock"></i> آپتایم</span><span class="sr-val" id="uptime-inline">—</span></div>
        <div style="margin-top:10px">
          <div style="display:flex;justify-content:space-between;font-size:12px;color:var(--text-secondary)">
            <span><i class="ti ti-gauge"></i> بار نسبی</span>
            <span id="bw-pct">—%</span>
          </div>
          <div class="progress-bar"><div class="progress-fill" id="bw-bar" style="width:0%"></div></div>
        </div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-list"></i> خلاصه کانفیگ‌ها <span class="ml-auto status-badge bg-blue" id="lsummary-badge">۰</span></div>
        <div id="lsummary">—</div>
      </div>
    </div>

    <div class="dash-footer">
      <span>تیم آزادی · RVG Gateway v9.0 · Railway · 2025</span>
      <a class="df-link" href="https://t.me/TimAzadi" target="_blank"><i class="ti ti-brand-telegram"></i> t.me/TimAzadi</a>
    </div>
  </section>

  <!-- ─── صفحه کانفیگ‌ها ─── -->
  <section class="page" id="pg-links">
    <div class="topbar">
      <div>
        <div class="tb-title"><i class="ti ti-link-plus"></i> کانفیگ‌ها</div>
        <div class="tb-sub">ساخت و مدیریت کانفیگ با سهمیه، انقضا و گروه‌بندی</div>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        <span class="status-badge bg-blue" id="links-pg-cnt">۰ کانفیگ</span>
      </div>
    </div>

    <div class="card mb20">
      <div class="card-title"><i class="ti ti-plus"></i> ساخت کانفیگ جدید</div>
      <div class="form-row">
        <div class="fg" style="flex:1;min-width:140px"><label>عنوان</label><input class="input" id="nl-label" placeholder="مثلاً: کاربر علی" style="width:100%"></div>
        <div class="fg"><label>سهمیه</label><input class="input" id="nl-val" type="number" min="0" step="0.1" placeholder="0=∞" style="width:110px"></div>
        <div class="fg"><label>واحد</label><select class="select" id="nl-unit"><option value="GB">GB</option><option value="MB" selected>MB</option></select></div>
        <div class="fg"><label>انقضا (روز)</label><input class="input" id="nl-exp" type="number" min="0" step="1" placeholder="0=∞" style="width:100px"></div>
        <div class="fg"><label>گروه ساب</label><select class="select" id="nl-sub"><option value="">— بدون گروه —</option></select></div>
        <div class="fg" style="flex:1;min-width:120px"><label>یادداشت</label><input class="input" id="nl-note" placeholder="اختیاری" style="width:100%"></div>
        <button class="btn btn-primary" onclick="createLink()"><i class="ti ti-link-plus"></i> ساخت</button>
      </div>
      <div class="info-box"><i class="ti ti-info-circle"></i><span>UUID کاملاً رندوم · فقط UUID‌های ثبت‌شده می‌توانند اتصال برقرار کنند · می‌توانید بعداً گروه را تغییر دهید.</span></div>
    </div>

    <div class="card">
      <div class="card-title"><i class="ti ti-list"></i> لیست کانفیگ‌ها</div>
      <div style="overflow-x:auto">
        <table class="data-table">
          <thead><tr><th>عنوان / یادداشت</th><th>UUID</th><th>مصرف / سهمیه</th><th>گروه</th><th>انقضا</th><th>وضعیت</th><th>عملیات</th></tr></thead>
          <tbody id="links-tb"></tbody>
        </table>
      </div>
      <div class="empty-state" id="links-empty" style="display:none"><i class="ti ti-link-off"></i><p>هنوز کانفیگی وجود ندارد</p></div>
    </div>
  </section>

  <!-- ─── صفحه گروه‌های ساب ─── -->
  <section class="page" id="pg-subgroups">
    <div class="topbar">
      <div>
        <div class="tb-title"><i class="ti ti-folders"></i> گروه‌های ساب</div>
        <div class="tb-sub">هر گروه یک صفحه پابلیک دارد</div>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        <span class="status-badge bg-purple" style="background:var(--purple-bg);color:#C084FC" id="subs-pg-cnt">۰ گروه</span>
        <button class="btn btn-subtle" onclick="openModal('modal-create-sub')"><i class="ti ti-folder-plus"></i> گروه جدید</button>
      </div>
    </div>
    <div class="sub-grid" id="subs-grid">
      <div class="empty-state" style="grid-column:1/-1"><i class="ti ti-folders"></i><p>هنوز گروهی وجود ندارد</p></div>
    </div>
  </section>

  <!-- ─── صفحه سابسکریپشن ─── -->
  <section class="page" id="pg-subscriptions">
    <div class="topbar"><div><div class="tb-title"><i class="ti ti-rss"></i> سابسکریپشن</div><div class="tb-sub">لینک‌های اشتراک برای اپ‌های v2ray</div></div></div>
    <div class="g2">
      <div class="card">
        <div class="card-title"><i class="ti ti-rss"></i> سابسکریپشن تکی (هر کانفیگ)</div>
        <p style="font-size:12px;color:var(--text-muted);line-height:1.8;margin-bottom:12px">هر کانفیگ URL سابسکریپشن مخصوص دارد. از جدول کانفیگ‌ها روی آیکون <i class="ti ti-rss"></i> کلیک کنید.</p>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-database"></i> سابسکریپشن کامل (ادمین)</div>
        <p style="font-size:12px;color:var(--text-muted);line-height:1.8;margin-bottom:4px">شامل تمام کانفیگ‌های فعال.</p>
        <div class="public-url-box" style="margin-top:12px">
          <span class="public-url-text" id="sub-all-url">در حال دریافت...</span>
          <div style="display:flex;gap:6px">
            <button class="btn btn-sm btn-subtle" onclick="cpSubAll()"><i class="ti ti-copy"></i></button>
            <button class="btn btn-sm btn-subtle" onclick="window.open(location.protocol+'//'+location.host+'/sub-all')"><i class="ti ti-external-link"></i></button>
          </div>
        </div>
        <div class="info-box amber" style="margin-top:12px"><i class="ti ti-alert-triangle"></i><span>این آدرس فقط در مرورگری که به پنل وارد شده کار می‌کند (نیاز به کوکی سشن).</span></div>
      </div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-folders"></i> لینک سابسکریپشن گروه‌ها</div>
      <div id="sub-groups-list">در حال بارگذاری...</div>
    </div>
  </section>

  <!-- ─── صفحه ترافیک ─── -->
  <section class="page" id="pg-traffic">
    <div class="topbar"><div><div class="tb-title"><i class="ti ti-chart-area"></i> ترافیک</div></div><div style="display:flex;align-items:center;gap:10px"><button class="btn btn-primary btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
    <div class="metrics-grid" style="grid-template-columns:repeat(3,1fr)">
      <div class="metric-card">
        <div class="metric-icon blue"><i class="ti ti-database"></i></div>
        <div class="metric-label">کل</div>
        <div class="metric-value" id="t-traffic">—<span class="metric-unit">MB</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-icon blue"><i class="ti ti-arrow-up"></i></div>
        <div class="metric-label">میانگین ساعتی</div>
        <div class="metric-value" id="t-avg">—<span class="metric-unit">MB</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-icon blue"><i class="ti ti-chart-bar"></i></div>
        <div class="metric-label">پیک ساعتی</div>
        <div class="metric-value" id="t-peak">—<span class="metric-unit">MB</span></div>
      </div>
    </div>
    <div class="card"><div class="card-title"><i class="ti ti-chart-area"></i> نمودار ترافیک ساعتی</div><div class="chart-wrap-lg"><canvas id="ch3"></canvas></div></div>
  </section>

  <!-- ─── صفحه اتصالات ─── -->
  <section class="page" id="pg-connections">
    <div class="topbar"><div><div class="tb-title"><i class="ti ti-plug-connected"></i> اتصالات</div></div><div style="display:flex;align-items:center;gap:10px"><span class="status-badge bg-green" id="conns-live">—</span><button class="btn btn-primary btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
    <div class="card"><div class="card-title"><i class="ti ti-list"></i> جزئیات</div><div id="conns-list"></div><div class="empty-state" id="conns-empty" style="display:none"><i class="ti ti-plug-off"></i><p>هیچ اتصال فعالی نیست</p></div></div>
  </section>

  <!-- ─── صفحه امنیت ─── -->
  <section class="page" id="pg-security">
    <div class="topbar"><div><div class="tb-title"><i class="ti ti-shield-lock"></i> امنیت</div></div></div>
    <div class="g2">
      <div class="card">
        <div class="card-title"><i class="ti ti-lock"></i> رمزنگاری</div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-certificate"></i> TLS/HTTPS</span><span class="sr-val" style="color:#34D399">● فعال (443)</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-fingerprint"></i> Fingerprint</span><span class="sr-val">Chrome Spoof</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-network"></i> پروتکل</span><span class="sr-val">VLESS/WS</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-key"></i> هش رمز</span><span class="sr-val">SHA-256+Salt</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-cookie"></i> سشن</span><span class="sr-val">HttpOnly · 7 روز</span></div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-shield-check"></i> کنترل دسترسی</div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-id-badge"></i> UUID Auth سخت‌گیرانه</span><span class="sr-val" style="color:#34D399">● فعال v9</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-toggle-right"></i> فعال/غیرفعال کانفیگ</span><span class="sr-val" style="color:#34D399">● فعال</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-gauge"></i> سهمیه ترافیک</span><span class="sr-val" style="color:#34D399">● فعال</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-calendar-x"></i> تاریخ انقضا</span><span class="sr-val" style="color:#34D399">● فعال</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-lock"></i> رمز صفحه پابلیک ساب</span><span class="sr-val" style="color:#34D399">● اختیاری · SHA-256</span></div>
      </div>
    </div>
  </section>

  <!-- ─── صفحه خطاها ─── -->
  <section class="page" id="pg-errors">
    <div class="topbar"><div><div class="tb-title"><i class="ti ti-alert-triangle"></i> خطاها</div></div><div style="display:flex;align-items:center;gap:10px"><span class="status-badge bg-red" id="errs-badge">۰</span><button class="btn btn-primary btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
    <div class="card"><div class="card-title"><i class="ti ti-bug"></i> لاگ خطاها</div><div id="errs-full">—</div></div>
  </section>

  <!-- ─── صفحه تست WebSocket ─── -->
  <section class="page" id="pg-testws">
    <div class="topbar"><div><div class="tb-title"><i class="ti ti-wifi"></i> تست WebSocket</div></div></div>
    <div class="card" style="max-width:660px">
      <div class="info-box amber" style="margin-top:0;margin-bottom:12px"><i class="ti ti-alert-triangle"></i><span>فقط UUID‌های ثبت‌شده و فعال اتصال برقرار می‌کنند.</span></div>
      <div class="form-row" style="margin-bottom:12px">
        <div class="fg" style="flex:1"><label>UUID (باید در کانفیگ‌ها وجود داشته باشد)</label><input class="input" id="ws-uuid" placeholder="UUID یک کانفیگ فعال" style="width:100%"></div>
        <button class="btn btn-primary" onclick="wsConn()"><i class="ti ti-plug-connected"></i> اتصال</button>
        <button class="btn btn-danger" onclick="wsDisc()"><i class="ti ti-plug-x"></i> قطع</button>
      </div>
      <div class="form-row" style="margin-bottom:12px">
        <input class="input" id="ws-msg" placeholder="پیام تست..." style="flex:1">
        <button class="btn btn-ghost" onclick="wsSend()"><i class="ti ti-send"></i> ارسال</button>
      </div>
      <div style="background:rgba(0,0,0,0.2);border:1px solid var(--glass-border);border-radius:12px;padding:16px;height:250px;overflow-y:auto;font-family:ui-monospace,monospace;font-size:11px;line-height:1.9" id="ws-log">
        <p style="color:var(--text-muted)">منتظر اتصال...</p>
      </div>
    </div>
  </section>

  <!-- ─── صفحه تنظیمات ─── -->
  <section class="page" id="pg-settings">
    <div class="topbar"><div><div class="tb-title"><i class="ti ti-settings"></i> تنظیمات</div></div></div>
    <div class="g2">
      <div class="card">
        <div class="card-title"><i class="ti ti-server"></i> اطلاعات سرور</div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-world"></i> دامنه</span><span class="sr-val" id="set-host">—</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-route"></i> پورت</span><span class="sr-val">443 (TLS)</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-versions"></i> نسخه</span><span class="sr-val">v9.0</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-brand-fastapi"></i> فریم‌ورک</span><span class="sr-val">FastAPI + Uvicorn</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-cloud"></i> پلتفرم</span><span class="sr-val">Railway</span></div>
        <div class="service-row"><span class="sr-key"><i class="ti ti-device-floppy"></i> ذخیره‌سازی</span><span class="sr-val">JSON File (/data)</span></div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-key"></i> تغییر رمز عبور</div>
        <div class="fg" style="margin-bottom:12px"><label>رمز فعلی</label><input class="input" type="password" id="cp-cur" placeholder="رمز فعلی" style="width:100%"></div>
        <div class="fg" style="margin-bottom:12px"><label>رمز جدید</label><input class="input" type="password" id="cp-new" placeholder="حداقل ۴ کاراکتر" style="width:100%"></div>
        <div class="fg" style="margin-bottom:16px"><label>تکرار رمز جدید</label><input class="input" type="password" id="cp-cf" placeholder="تکرار رمز جدید" style="width:100%"></div>
        <button class="btn btn-primary" onclick="changePw()" style="width:100%;justify-content:center"><i class="ti ti-key"></i> تغییر رمز</button>
      </div>
    </div>
  </section>

</main>

<script>
/* ── تمام اسکریپت‌ها بدون تغییر در منطق، فقط Selectorهای کلاس جدید ── */
let isDark=localStorage.getItem('rvg-theme')!=='light';
function applyTheme(dark){
  document.documentElement.setAttribute('data-theme',dark?'dark':'light');
  const icon=dark?'ti-sun':'ti-moon',label=dark?'تم روشن':'تم تاریک';
  document.getElementById('theme-icon').className='ti '+icon;
  document.getElementById('theme-label').textContent=label;
  const mobI=document.getElementById('theme-mob-icon');if(mobI)mobI.className='ti '+icon;
}
function toggleTheme(){isDark=!isDark;localStorage.setItem('rvg-theme',isDark?'dark':'light');applyTheme(isDark)}
applyTheme(isDark);
function toast(msg,type=''){
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2400);
}
function fmtB(b){if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}
function toFa(n){return String(n).replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d])}
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function daysLeft(exp){if(!exp)return null;return Math.ceil((new Date(exp)-Date.now())/(864e5))}
function expChip(exp,expired){
  if(expired)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if(!exp)return '<span class="exp-chip ec-inf"><i class="ti ti-infinity"></i> ∞</span>';
  const d=daysLeft(exp);
  if(d<=0)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if(d<=3)return `<span class="exp-chip ec-warn"><i class="ti ti-alert-triangle"></i> ${toFa(d)}ر</span>`;
  return `<span class="exp-chip ec-ok"><i class="ti ti-calendar-check"></i> ${toFa(d)}ر</span>`;
}
async function checkAuth(){try{const r=await fetch('/api/me');const d=await r.json();if(!d.authenticated)location.href='/login';}catch(e){location.href='/login'}}
async function logout(){try{await fetch('/api/logout',{method:'POST'})}catch(e){}location.href='/login'}
document.getElementById('logout-btn').addEventListener('click',logout);
async function authF(url,opts={}){
  const r=await fetch(url,opts);
  if(r.status===401){location.href='/login';throw new Error('unauthorized')}
  return r;
}
const sb=document.getElementById('sb'),overlay=document.getElementById('overlay');
function openSb(){sb.classList.add('open');overlay.classList.add('show')}
function closeSb(){sb.classList.remove('open');overlay.classList.remove('show')}
document.getElementById('open-sb').addEventListener('click',openSb);
document.getElementById('close-sb').addEventListener('click',closeSb);
overlay.addEventListener('click',closeSb);
function navTo(name){
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.toggle('on',n.dataset.pg===name));
  document.querySelectorAll('.page').forEach(p=>p.classList.toggle('on',p.id==='pg-'+name));
  const loaders={links:loadLinks,connections:loadConns,errors:loadErrs,subscriptions:loadSubsPage,subgroups:loadSubs};
  if(loaders[name])loaders[name]();
  closeSb();window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.nav-item').forEach(el=>el.addEventListener('click',()=>navTo(el.dataset.pg)));
function openModal(id){document.getElementById(id).classList.add('open')}
function closeModal(id){document.getElementById(id).classList.remove('open')}
let prevTraf=0,ch1,ch2,ch3;
async function fetchStats(){
  try{
    const r=await authF('/stats'),d=await r.json();
    document.getElementById('m-conns').textContent=d.active_connections;
    document.getElementById('conns-nb').textContent=d.active_connections;
    document.getElementById('m-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="metric-unit">MB</span>';
    document.getElementById('m-alinks').textContent=d.active_links??'—';
    document.getElementById('m-lsub').textContent='از '+d.links_count+' کانفیگ';
    document.getElementById('m-subs').textContent=d.subs_count??'—';
    document.getElementById('errs-badge').textContent=d.total_errors+' خطا';
    document.getElementById('uptime-inline').textContent=d.uptime;
    document.getElementById('uptime-badge').textContent='Railway · '+d.uptime;
    document.getElementById('last-upd').textContent='آخرین بروزرسانی: '+new Date().toLocaleTimeString('fa-IR');
    document.getElementById('conns-live').innerHTML='<span class="dot dg pulse"></span> '+d.active_connections+' اتصال';
    document.getElementById('t-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="metric-unit">MB</span>';
    const delta=d.total_traffic_mb-prevTraf,pct=Math.min(100,Math.round((delta/50)*100));
    document.getElementById('bw-pct').textContent=pct+'%';
    document.getElementById('bw-bar').style.width=pct+'%';
    prevTraf=d.total_traffic_mb;
    if(d.hourly){
      const labels=Object.keys(d.hourly).sort(),vals=labels.map(k=>+(d.hourly[k]/1024**2).toFixed(2));
      [ch1,ch3].forEach(c=>{if(!c)return;c.data.labels=labels;c.data.datasets[0].data=vals;c.update()});
      if(vals.length){const avg=vals.reduce((a,b)=>a+b,0)/vals.length,peak=Math.max(...vals);document.getElementById('t-avg').innerHTML=avg.toFixed(2)+'<span class="metric-unit">MB</span>';document.getElementById('t-peak').innerHTML=peak.toFixed(2)+'<span class="metric-unit">MB</span>';}
    }
    renderErrs(d.recent_errors||[]);
  }catch(e){console.error(e)}
}
function renderErrs(errs){
  const el=document.getElementById('errs-full');if(!el)return;
  if(!errs.length){el.innerHTML='<div style="color:#34D399;padding:10px;font-size:12px;display:flex;align-items:center;gap:5px"><i class="ti ti-circle-check"></i> هیچ خطایی نیست</div>';return}
  el.innerHTML=errs.slice().reverse().map(e=>`<div class="service-row"><div class="sr-key"><i class="ti ti-clock"></i>${new Date(e.time).toLocaleString('fa-IR')}</div><div class="sr-val" style="color:#FCA5A5;font-family:ui-monospace,monospace">${esc(e.error)}${e.url?' — '+esc(e.url):''}</div></div>`).join('');
}
let allSubsList=[];
async function loadLinks(){
  try{
    const [lr,sr]=await Promise.all([authF('/api/links'),authF('/api/subs')]);
    const {links=[]}=await lr.json();
    const {subs=[]}=await sr.json();
    allSubsList=subs;
    const nlSub=document.getElementById('nl-sub');
    nlSub.innerHTML='<option value="">— بدون گروه —</option>'+subs.map(s=>`<option value="${esc(s.sub_id)}">${esc(s.name)}</option>`).join('');
    document.getElementById('links-nb').textContent=links.length;
    document.getElementById('links-pg-cnt').textContent=toFa(links.length)+' کانفیگ';
    document.getElementById('lsummary-badge').textContent=toFa(links.length);
    const tb=document.getElementById('links-tb'),empty=document.getElementById('links-empty');
    if(!links.length){tb.innerHTML='';empty.style.display='block';document.getElementById('lsummary').innerHTML='<div class="empty-state"><i class="ti ti-link-off"></i><p>کانفیگی وجود ندارد</p></div>';return}
    empty.style.display='none';
    const subMap=Object.fromEntries(subs.map(s=>[s.sub_id,s.name]));
    tb.innerHTML=links.map(l=>{
      const lim=l.limit_bytes===0?'∞':fmtB(l.limit_bytes);
      const pct=l.limit_bytes===0?0:Math.min(100,l.used_bytes/l.limit_bytes*100);
      const bc=pct>90?'var(--red)':pct>70?'var(--amber)':'var(--accent)';
      const allowed=l.active&&!l.expired;
      const subOpts='<option value="">— بدون گروه —</option>'+subs.map(s=>`<option value="${esc(s.sub_id)}"${l.sub_id===s.sub_id?' selected':''}>${esc(s.name)}</option>`).join('');
      return `<tr>
        <td><div style="font-weight:600;color:var(--text-primary);font-size:13px">${esc(l.label)}</div><div style="font-size:10px;color:var(--text-muted);margin-top:2px">${new Date(l.created_at).toLocaleDateString('fa-IR')}${l.note?` · <span title="${esc(l.note)}">${esc(l.note.slice(0,20))}${l.note.length>20?'…':''}</span>`:''}</div></td>
        <td><span class="uuid-chip" onclick="navigator.clipboard.writeText('${l.uuid}').then(()=>toast('UUID کپی شد','ok'))" title="${l.uuid}">${l.uuid.slice(0,13)}…</span></td>
        <td><div style="width:115px"><div class="usage-bar"><div class="usage-fill" style="width:${pct}%;background:${bc}"></div></div><div style="font-size:10px;color:var(--text-muted)">${fmtB(l.used_bytes)} / ${lim}</div></div></td>
        <td><select class="select" style="font-size:10px;padding:4px 8px;min-width:90px" onchange="moveLinkSub('${l.uuid}',this.value)">${subOpts}</select></td>
        <td>${expChip(l.expires_at,l.expired)}</td>
        <td><button class="toggle${allowed?' on':''}" onclick="toggleActive('${l.uuid}',${!l.active})"></button></td>
        <td><div style="display:flex;gap:4px;flex-wrap:nowrap">
          <button class="btn btn-sm btn-subtle" onclick="navigator.clipboard.writeText('${esc(l.vless_link)}').then(()=>toast('VLESS کپی شد','ok'))" title="کپی VLESS"><i class="ti ti-copy"></i></button>
          <button class="btn btn-sm btn-subtle" onclick="navigator.clipboard.writeText('${esc(l.sub_url)}').then(()=>toast('Sub کپی شد','ok'))" title="Sub URL"><i class="ti ti-rss"></i></button>
          <button class="btn btn-sm btn-subtle" onclick="showQR('${esc(l.vless_link)}')" title="QR"><i class="ti ti-qrcode"></i></button>
          <button class="btn btn-sm btn-subtle" onclick="resetUsage('${l.uuid}')" title="ریست مصرف"><i class="ti ti-rotate"></i></button>
          <button class="btn btn-sm btn-danger" onclick="deleteLink('${l.uuid}')" title="حذف"><i class="ti ti-trash"></i></button>
        </div></td>
      </tr>`;
    }).join('');
    document.getElementById('lsummary').innerHTML=links.slice(0,6).map(l=>`<div class="service-row"><span class="sr-key" style="gap:5px"><i class="ti ${l.expired?'ti-calendar-x':l.active?'ti-circle-check':'ti-circle-x'}" style="color:${l.expired?'var(--amber)':l.active?'var(--green)':'var(--red)'}"></i>${esc(l.label)}</span><span class="sr-val" style="font-size:10px">${fmtB(l.used_bytes)} / ${l.limit_bytes===0?'∞':fmtB(l.limit_bytes)}</span></div>`).join('');
  }catch(e){console.error(e)}
}
async function createLink(){
  const label=document.getElementById('nl-label').value.trim()||'کانفیگ جدید';
  const val=document.getElementById('nl-val').value;
  const unit=document.getElementById('nl-unit').value;
  const exp=document.getElementById('nl-exp').value;
  const note=document.getElementById('nl-note').value.trim();
  const sub_id=document.getElementById('nl-sub').value||null;
  try{
    const r=await authF('/api/links',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({label,limit_value:val||0,limit_unit:unit,expires_days:exp||0,note,sub_id})});
    if(!r.ok)throw new Error('failed');
    ['nl-label','nl-val','nl-exp','nl-note'].forEach(id=>document.getElementById(id).value='');
    toast('کانفیگ ساخته شد ✓','ok');loadLinks();
  }catch(e){toast('خطا در ساخت','err')}
}
async function moveLinkSub(uuid,newSubId){
  try{
    const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({sub_id:newSubId||null})});
    if(!r.ok)throw new Error();
    toast('گروه تغییر کرد ✓','ok');loadLinks();
  }catch(e){toast('خطا','err')}
}
async function toggleActive(uuid,newState){
  try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({active:newState})});if(!r.ok)throw new Error();toast(newState?'فعال شد ✓':'غیرفعال شد','ok');loadLinks();}catch(e){toast('خطا','err')}
}
async function resetUsage(uuid){
  try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({reset_usage:true})});if(!r.ok)throw new Error();toast('مصرف ریست شد ✓','ok');loadLinks();}catch(e){toast('خطا','err')}
}
async function deleteLink(uuid){
  if(!confirm('حذف این کانفیگ؟'))return;
  try{const r=await authF('/api/links/'+uuid,{method:'DELETE'});if(!r.ok)throw new Error();toast('حذف شد ✓','ok');loadLinks();}catch(e){toast('خطا','err')}
}
function showQR(link){window.open('https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+encodeURIComponent(link),'_blank')}
let currentSubId=null;
async function loadSubs(){
  try{
    const r=await authF('/api/subs'),d=await r.json();
    const subs=d.subs||[];
    document.getElementById('subs-nb').textContent=subs.length;
    document.getElementById('subs-pg-cnt').textContent=toFa(subs.length)+' گروه';
    const grid=document.getElementById('subs-grid');
    if(!subs.length){grid.innerHTML='<div class="empty-state" style="grid-column:1/-1"><i class="ti ti-folders"></i><p>هنوز گروهی وجود ندارد</p></div>';return}
    grid.innerHTML=subs.map(s=>`
      <div class="sub-card">
        <div class="sub-card-header">
          <div><div class="sub-card-name">${esc(s.name)}</div>${s.desc?`<div class="sub-card-desc">${esc(s.desc)}</div>`:''}</div>
          <div style="display:flex;gap:5px;flex-shrink:0">${s.has_password?'<span class="status-badge bg-amber"><i class="ti ti-lock"></i> رمز</span>':'<span class="status-badge bg-green"><i class="ti ti-globe"></i> پابلیک</span>'}</div>
        </div>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px;font-size:10px;color:var(--text-muted)">
          <span><i class="ti ti-link"></i> ${toFa(s.links_count)} کانفیگ</span>
          <span><i class="ti ti-circle-check" style="color:var(--green)"></i> ${toFa(s.active_count)} فعال</span>
          <span><i class="ti ti-database"></i> ${esc(s.total_used_fmt)} مصرف</span>
          <span><i class="ti ti-calendar"></i> ${new Date(s.created_at).toLocaleDateString('fa-IR')}</span>
        </div>
        <div class="public-url-box">
          <span class="public-url-text">${esc(s.public_url)}</span>
          <button class="btn btn-sm btn-subtle" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('لینک پابلیک کپی شد','ok'))"><i class="ti ti-copy"></i></button>
          <button class="btn btn-sm btn-subtle" onclick="window.open('${esc(s.public_url)}','_blank')"><i class="ti ti-external-link"></i></button>
          <button class="btn btn-sm btn-subtle" onclick="showQR('${esc(s.sub_url)}')" title="QR کل گروه"><i class="ti ti-qrcode"></i></button>
        </div>
        <div class="sub-card-footer">
          <button class="btn btn-sm btn-subtle" onclick="openSubLinks('${esc(s.sub_id)}','${esc(s.name)}')"><i class="ti ti-link-plus"></i> مدیریت کانفیگ‌ها</button>
          <button class="btn btn-sm btn-ghost" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('لینک ساب کپی شد','ok'))"><i class="ti ti-rss"></i> کپی ساب</button>
          <button class="btn btn-sm btn-danger" onclick="deleteSub('${esc(s.sub_id)}')"><i class="ti ti-trash"></i></button>
        </div>
      </div>
    `).join('');
  }catch(e){console.error(e)}
}
async function createSub(){
  const name=document.getElementById('ns-name').value.trim()||'گروه جدید';
  const desc=document.getElementById('ns-desc').value.trim();
  const pw=document.getElementById('ns-pw').value;
  try{
    const r=await authF('/api/subs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,desc,password:pw})});
    if(!r.ok)throw new Error('failed');
    ['ns-name','ns-desc','ns-pw'].forEach(id=>document.getElementById(id).value='');
    closeModal('modal-create-sub');
    toast('گروه ساخته شد ✓','ok');loadSubs();
  }catch(e){toast('خطا در ساخت گروه','err')}
}
async function deleteSub(sub_id){
  if(!confirm('حذف این گروه؟ کانفیگ‌ها حذف نمی‌شوند.'))return;
  try{const r=await authF('/api/subs/'+sub_id,{method:'DELETE'});if(!r.ok)throw new Error();toast('گروه حذف شد ✓','ok');loadSubs();loadLinks();}catch(e){toast('خطا','err')}
}
async function openSubLinks(sub_id,name){
  currentSubId=sub_id;
  document.getElementById('modal-sub-name').textContent=name;
  document.getElementById('modal-links-body').innerHTML='<div style="color:var(--text-muted);font-size:12px;padding:10px">در حال بارگذاری...</div>';
  openModal('modal-links');
  try{
    const [lr,sr]=await Promise.all([authF('/api/links'),authF('/api/subs')]);
    const {links=[]}=await lr.json();
    const {subs=[]}=await sr.json();
    const thisSub=subs.find(s=>s.sub_id===sub_id);
    const inSub=new Set(thisSub?.link_ids||[]);
    if(!links.length){document.getElementById('modal-links-body').innerHTML='<div class="empty-state"><i class="ti ti-link-off"></i><p>هنوز کانفیگی وجود ندارد</p></div>';return}
    document.getElementById('modal-links-body').innerHTML=links.map(l=>`
      <div class="lrow">
        <input type="checkbox" class="lrow-check" id="lc-${l.uuid}" ${inSub.has(l.uuid)?'checked':''} value="${l.uuid}">
        <label for="lc-${l.uuid}" style="font-size:12px;color:var(--text-primary)">${esc(l.label)}</label>
        ${l.active&&!l.expired?'<span class="status-badge bg-green" style="font-size:9px">فعال</span>':'<span class="status-badge bg-red" style="font-size:9px">غیرفعال</span>'}
        <span style="font-size:10px;color:var(--text-muted)">${fmtB(l.used_bytes)}</span>
      </div>
    `).join('');
  }catch(e){toast('خطا در بارگذاری','err')}
}
async function saveSubLinks(){
  if(!currentSubId)return;
  const checks=document.querySelectorAll('#modal-links-body .lrow-check');
  const link_ids=[...checks].filter(c=>c.checked).map(c=>c.value);
  try{
    const r=await authF('/api/subs/'+currentSubId,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({link_ids})});
    if(!r.ok)throw new Error();
    const allChecks=[...checks].map(c=>({uuid:c.value,inSub:c.checked}));
    await Promise.all(allChecks.map(({uuid,inSub})=>
      authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({sub_id:inSub?currentSubId:null})})
    ));
    closeModal('modal-links');
    toast('کانفیگ‌های گروه ذخیره شدند ✓','ok');
    loadSubs();loadLinks();
  }catch(e){toast('خطا در ذخیره','err')}
}
async function loadSubsPage(){
  document.getElementById('sub-all-url').textContent=location.protocol+'//'+location.host+'/sub-all';
  try{
    const r=await authF('/api/subs'),d=await r.json();
    const subs=d.subs||[];
    const el=document.getElementById('sub-groups-list');
    if(!subs.length){el.innerHTML='<div class="empty-state"><i class="ti ti-rss-off"></i><p>هنوز گروهی ندارید</p></div>';return}
    el.innerHTML=subs.map(s=>`
      <div style="padding:14px 16px;background:rgba(59,130,246,0.06);border:1px solid var(--glass-border);border-radius:12px;margin-bottom:10px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap">
        <div>
          <div style="font-weight:700;font-size:13px;margin-bottom:4px">${esc(s.name)}</div>
          <div style="font-family:ui-monospace,monospace;font-size:11px;color:#C084FC">${esc(s.sub_url)}</div>
          <div style="font-size:10px;color:var(--text-muted);margin-top:4px">${toFa(s.links_count)} کانفیگ · ${esc(s.total_used_fmt)} مصرف ${s.has_password?'· 🔒 رمزدار':''}</div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap">
          <button class="btn btn-sm btn-subtle" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-copy"></i> ساب</button>
          <button class="btn btn-sm btn-subtle" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-globe"></i> پابلیک</button>
          <button class="btn btn-sm btn-subtle" onclick="showQR('${esc(s.sub_url)}')"><i class="ti ti-qrcode"></i></button>
        </div>
      </div>
    `).join('');
  }catch(e){}
}
function cpSubAll(){navigator.clipboard.writeText(location.protocol+'//'+location.host+'/sub-all').then(()=>toast('کپی شد ✓','ok'))}
async function loadConns(){
  try{const r=await authF('/stats'),d=await r.json();const cl=document.getElementById('conns-list'),ce=document.getElementById('conns-empty');if(d.active_connections===0){cl.innerHTML='';ce.style.display='block';return}ce.style.display='none';cl.innerHTML=`<div style="padding:14px;background:var(--green-bg);border:1px solid rgba(16,185,129,0.15);border-radius:10px;display:flex;align-items:center;gap:10px;font-size:12px;color:#34D399"><span class="dot dg pulse"></span>${d.active_connections} اتصال فعال · کل ${d.total_traffic_mb.toFixed(1)} MB</div>`;}catch(e){}
}
async function loadErrs(){try{const r=await authF('/stats'),d=await r.json();renderErrs(d.recent_errors||[]);}catch(e){}}
async function fetchDefaultVless(){
  try{const r=await authF('/api/links'),d=await r.json();const links=d.links||[];const def=links.find(l=>l.limit_bytes===0&&l.active&&!l.expired)||links.find(l=>l.active&&!l.expired)||links[0];document.getElementById('vless-main').textContent=def?def.vless_link:'هنوز کانفیگی وجود ندارد';}catch(e){}
}
function cpText(id){navigator.clipboard.writeText(document.getElementById(id).textContent).then(()=>toast('کپی شد ✓','ok'))}
function qrFor(id){showQR(document.getElementById(id).textContent)}
function refreshAll(){fetchStats();fetchDefaultVless();loadLinks();if(document.getElementById('pg-subgroups').classList.contains('on'))loadSubs();if(document.getElementById('pg-subscriptions').classList.contains('on'))loadSubsPage();toast('رفرش شد','ok')}
async function changePw(){
  const cur=document.getElementById('cp-cur').value,nw=document.getElementById('cp-new').value,cf=document.getElementById('cp-cf').value;
  if(!cur||!nw||!cf){toast('همه فیلدها را پر کنید','err');return}
  if(nw.length<4){toast('حداقل ۴ کاراکتر','err');return}
  if(nw!==cf){toast('تکرار رمز اشتباه','err');return}
  try{
    const r=await authF('/api/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({current_password:cur,new_password:nw})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok)throw new Error(d.detail||'خطا');
    toast('رمز تغییر کرد ✓','ok');
    ['cp-cur','cp-new','cp-cf'].forEach(id=>document.getElementById(id).value='');
  }catch(e){toast('✗ '+e.message,'err')}
}
function initCharts(){
  const opts={responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:'rgba(15,23,42,0.95)',borderColor:'rgba(59,130,246,0.2)',borderWidth:1,titleColor:'#F1F5F9',bodyColor:'#94A3B8',callbacks:{label:v=>`${v.parsed.y.toFixed(2)} MB`}}},scales:{x:{grid:{color:'rgba(59,130,246,0.06)'},ticks:{color:'#64748B',font:{size:9}}},y:{grid:{color:'rgba(59,130,246,0.06)'},ticks:{color:'#64748B',font:{size:9},callback:v=>v+'MB'}}}};
  const ds={label:'MB',data:[],borderColor:'rgba(59,130,246,0.9)',backgroundColor:'rgba(59,130,246,0.05)',fill:true,tension:.45,pointRadius:3,pointHoverRadius:5,borderWidth:2};
  ch1=new Chart(document.getElementById('ch1'),{type:'line',data:{labels:[],datasets:[{...ds}]},options:opts});
  ch3=new Chart(document.getElementById('ch3'),{type:'line',data:{labels:[],datasets:[{...ds}]},options:opts});
  ch2=new Chart(document.getElementById('ch2'),{type:'doughnut',data:{labels:['VLESS/WS','HTTP Proxy','سایر'],datasets:[{data:[70,25,5],backgroundColor:['rgba(59,130,246,0.9)','rgba(16,185,129,0.8)','rgba(139,92,246,0.8)'],borderColor:'rgba(0,0,0,0)',borderWidth:3,hoverOffset:8}]},options:{responsive:true,maintainAspectRatio:false,cutout:'68%',plugins:{legend:{position:'bottom',labels:{color:'var(--text-secondary)',font:{size:9},padding:10,usePointStyle:true}}}}});
}
let ws;
function wsLog(c,m){const l=document.getElementById('ws-log'),p=document.createElement('p');const colors={ok:'#34D399',err:'#FCA5A5',info:'#94A3B8',sent:'#FCD34D'};p.style.color=colors[c]||'#fff';p.textContent='['+new Date().toLocaleTimeString('fa-IR')+'] '+m;l.appendChild(p);l.scrollTop=l.scrollHeight}
function wsConn(){const u=document.getElementById('ws-uuid').value.trim();if(!u){toast('UUID را وارد کنید','err');return}const url=(location.protocol==='https:'?'wss':'ws')+'://'+location.host+'/ws/'+u;wsLog('info','اتصال: '+url);ws=new WebSocket(url);ws.onopen=()=>wsLog('ok','✓ متصل - UUID معتبر');ws.onerror=()=>wsLog('err','✗ خطا - UUID نامعتبر یا غیرفعال');ws.onmessage=m=>wsLog('info','دریافت '+(m.data.size||m.data.length)+' byte');ws.onclose=e=>wsLog('err','قطع ('+e.code+')'+(e.code===1008?' - دسترسی رد شد':''))}
function wsSend(){const m=document.getElementById('ws-msg').value;if(!m||!ws||ws.readyState!==1)return;ws.send(m);wsLog('sent','ارسال: '+m);document.getElementById('ws-msg').value=''}
function wsDisc(){if(ws)ws.close()}
document.addEventListener('DOMContentLoaded',async()=>{
  await checkAuth();
  initCharts();
  document.getElementById('set-host').textContent=location.host;
  document.getElementById('sub-all-url')&&(document.getElementById('sub-all-url').textContent=location.protocol+'//'+location.host+'/sub-all');
  fetchStats();fetchDefaultVless();loadLinks();loadSubs();
  setInterval(fetchStats,4000);
  setInterval(()=>{
    if(document.getElementById('pg-links').classList.contains('on'))loadLinks();
    if(document.getElementById('pg-subgroups').classList.contains('on'))loadSubs();
    if(document.getElementById('pg-subscriptions').classList.contains('on'))loadSubsPage();
  },5000);
});
</script>
</body></html>"""


def get_public_page_html(uuid_key: str) -> str:
    """صفحه‌ی عمومی یک گروه ساب - طراحی مدرن و حرفه‌ای"""
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ساب · تیم آزادی</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --bg-primary:#0A0E14;
  --bg-secondary:#11181F;
  --bg-card:#181F28;
  --bg-card-hover:#1F2833;
  --text-primary:#E8EDF5;
  --text-secondary:#8FA3B8;
  --text-muted:#5A6F84;
  --accent:#E83C6A;
  --accent-dark:#C72A56;
  --accent-glow:rgba(232,60,106,0.15);
  --border-color:rgba(143,171,202,0.08);
  --border-hover:rgba(232,60,106,0.3);
  --success:#10B981;
  --success-bg:rgba(16,185,129,0.12);
  --warning:#F59E0B;
  --warning-bg:rgba(245,158,11,0.12);
  --danger:#EF4444;
  --danger-bg:rgba(239,68,68,0.12);
  --radius:16px;
  --shadow:0 8px 32px rgba(0,0,0,0.4);
  --transition:0.3s cubic-bezier(0.4,0,0.2,1);
}}
html,body{{
  min-height:100%;
  background:var(--bg-primary);
  font-family:'Vazirmatn',sans-serif;
  color:var(--text-primary);
  font-size:14px;
  line-height:1.6;
}}
::-webkit-scrollbar{{width:6px;height:6px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:var(--accent);border-radius:3px}}

.bg-layer{{
  position:fixed;
  inset:0;
  z-index:0;
  background:
    radial-gradient(ellipse 60% 40% at 50% 0%, rgba(232,60,106,0.06), transparent 60%),
    radial-gradient(ellipse 40% 30% at 80% 80%, rgba(232,60,106,0.04), transparent 50%),
    var(--bg-primary);
  pointer-events:none;
}}
.grid-overlay{{
  position:fixed;
  inset:0;
  z-index:0;
  background-image:
    linear-gradient(rgba(232,60,106,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(232,60,106,0.03) 1px, transparent 1px);
  background-size:48px 48px;
  pointer-events:none;
}}

.wrap{{
  position:relative;
  z-index:10;
  max-width:820px;
  margin:0 auto;
  padding:24px 20px 60px;
}}

/* ── Header ── */
.header{{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:32px;
  padding:12px 20px;
  background:var(--bg-card);
  border:1px solid var(--border-color);
  border-radius:var(--radius);
  backdrop-filter:blur(12px);
}}
.brand{{
  display:flex;
  align-items:center;
  gap:12px;
}}
.brand-icon{{
  width:42px;
  height:42px;
  border-radius:12px;
  background:linear-gradient(135deg,var(--accent),var(--accent-dark));
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:20px;
  font-weight:900;
  color:#fff;
  box-shadow:0 0 24px var(--accent-glow);
}}
.brand-text{{
  font-size:16px;
  font-weight:700;
  color:var(--text-primary);
}}
.brand-sub{{
  font-size:10px;
  color:var(--text-muted);
  letter-spacing:0.06em;
}}
.header-actions{{
  display:flex;
  gap:8px;
  align-items:center;
}}
.channel-link{{
  display:flex;
  align-items:center;
  gap:6px;
  padding:6px 14px;
  border-radius:8px;
  background:rgba(232,60,106,0.1);
  color:var(--accent);
  font-size:12px;
  font-weight:600;
  text-decoration:none;
  transition:var(--transition);
}}
.channel-link:hover{{
  background:rgba(232,60,106,0.2);
  transform:translateY(-1px);
}}

/* ── Sub Info Card ── */
.sub-info{{
  background:var(--bg-card);
  border:1px solid var(--border-color);
  border-radius:var(--radius);
  padding:24px 28px;
  margin-bottom:24px;
  transition:var(--transition);
}}
.sub-info:hover{{
  border-color:var(--border-hover);
  box-shadow:var(--shadow);
}}
.sub-name{{
  font-size:22px;
  font-weight:800;
  background:linear-gradient(135deg,var(--text-primary),var(--text-secondary));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  margin-bottom:4px;
}}
.sub-desc{{
  font-size:13px;
  color:var(--text-secondary);
  margin-bottom:16px;
}}
.sub-meta{{
  display:flex;
  flex-wrap:wrap;
  gap:16px;
  margin-bottom:16px;
  font-size:12px;
  color:var(--text-muted);
}}
.sub-meta span{{
  display:flex;
  align-items:center;
  gap:6px;
}}
.sub-meta i{{color:var(--accent);font-size:14px}}

.url-box{{
  display:flex;
  align-items:center;
  gap:8px;
  padding:10px 14px;
  background:rgba(232,60,106,0.06);
  border:1px solid rgba(232,60,106,0.15);
  border-radius:10px;
  flex-wrap:wrap;
}}
.url-text{{
  flex:1;
  font-family:ui-monospace,monospace;
  font-size:11px;
  color:#C084FC;
  word-break:break-all;
  min-width:120px;
}}
.url-actions{{
  display:flex;
  gap:6px;
}}

/* ── Stats Grid ── */
.stats-grid{{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:14px;
  margin-bottom:28px;
}}
.stat-card{{
  background:var(--bg-card);
  border:1px solid var(--border-color);
  border-radius:var(--radius);
  padding:18px 20px;
  transition:var(--transition);
}}
.stat-card:hover{{
  border-color:var(--border-hover);
  transform:translateY(-2px);
  box-shadow:var(--shadow);
}}
.stat-label{{
  font-size:10px;
  font-weight:700;
  color:var(--text-muted);
  text-transform:uppercase;
  letter-spacing:0.08em;
  margin-bottom:4px;
}}
.stat-value{{
  font-size:26px;
  font-weight:800;
  color:var(--text-primary);
  line-height:1.2;
}}
.stat-sub{{
  font-size:11px;
  color:var(--text-muted);
  margin-top:4px;
}}
.stat-sub .dot{{
  display:inline-block;
  width:6px;
  height:6px;
  border-radius:50%;
  animation:pulse 2s infinite;
}}
.stat-sub .dot.green{{background:var(--success)}}
.stat-sub .dot.accent{{background:var(--accent)}}

/* ── Configs Section ── */
.section-title{{
  font-size:15px;
  font-weight:700;
  color:var(--text-secondary);
  margin-bottom:16px;
  display:flex;
  align-items:center;
  gap:10px;
}}
.section-title i{{color:var(--accent);font-size:18px}}
.section-title .badge{{
  font-size:10px;
  padding:2px 10px;
  border-radius:20px;
  background:var(--accent-glow);
  color:var(--accent);
  font-weight:700;
}}

.cfg-grid{{
  display:grid;
  gap:14px;
}}
.cfg-card{{
  background:var(--bg-card);
  border:1px solid var(--border-color);
  border-radius:var(--radius);
  padding:20px;
  transition:var(--transition);
}}
.cfg-card:hover{{
  border-color:var(--border-hover);
  box-shadow:var(--shadow);
  transform:translateY(-2px);
}}
.cfg-header{{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:12px;
  margin-bottom:12px;
}}
.cfg-label{{
  font-size:15px;
  font-weight:700;
  color:var(--text-primary);
}}
.cfg-status{{
  font-size:10px;
  font-weight:700;
  padding:3px 12px;
  border-radius:20px;
  display:inline-flex;
  align-items:center;
  gap:4px;
  white-space:nowrap;
}}
.cfg-status.active{{
  background:var(--success-bg);
  color:var(--success);
}}
.cfg-status.inactive{{
  background:var(--danger-bg);
  color:var(--danger);
}}
.cfg-status i{{font-size:12px}}

.usage-wrapper{{
  margin-bottom:14px;
}}
.usage-bar{{
  height:6px;
  border-radius:3px;
  background:rgba(255,255,255,0.06);
  overflow:hidden;
  margin-bottom:4px;
}}
.usage-fill{{
  height:100%;
  border-radius:3px;
  transition:width 0.6s ease;
}}
.usage-text{{
  font-size:11px;
  color:var(--text-muted);
  display:flex;
  justify-content:space-between;
}}

.cfg-link{{
  background:rgba(0,0,0,0.3);
  border:1px solid var(--border-color);
  border-radius:10px;
  padding:10px 14px;
  font-family:ui-monospace,monospace;
  font-size:11px;
  color:var(--accent);
  word-break:break-all;
  line-height:1.8;
  margin-bottom:14px;
  transition:var(--transition);
}}
.cfg-link:hover{{
  border-color:var(--border-hover);
}}

.cfg-actions{{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
}}
.btn{{
  font-family:inherit;
  font-size:11px;
  font-weight:600;
  border-radius:8px;
  padding:8px 16px;
  cursor:pointer;
  display:inline-flex;
  align-items:center;
  gap:6px;
  border:none;
  transition:var(--transition);
  text-decoration:none;
}}
.btn i{{font-size:14px}}
.btn-primary{{
  background:linear-gradient(135deg,var(--accent),var(--accent-dark));
  color:#fff;
  box-shadow:0 4px 16px var(--accent-glow);
}}
.btn-primary:hover{{
  transform:translateY(-1px);
  box-shadow:0 6px 24px var(--accent-glow);
  filter:brightness(1.08);
}}
.btn-ghost{{
  background:rgba(232,60,106,0.08);
  color:var(--accent);
  border:1px solid rgba(232,60,106,0.15);
}}
.btn-ghost:hover{{
  background:rgba(232,60,106,0.15);
  transform:translateY(-1px);
}}
.btn-ghost-light{{
  background:rgba(255,255,255,0.04);
  color:var(--text-secondary);
  border:1px solid var(--border-color);
}}
.btn-ghost-light:hover{{
  background:rgba(255,255,255,0.08);
  color:var(--text-primary);
}}

/* ── Lock Screen ── */
.lock-card{{
  max-width:380px;
  margin:80px auto;
  background:var(--bg-card);
  border:1px solid var(--border-color);
  border-radius:24px;
  padding:40px 36px;
  text-align:center;
  box-shadow:var(--shadow);
}}
.lock-icon{{
  font-size:48px;
  color:var(--accent);
  margin-bottom:16px;
  opacity:0.7;
}}
.lock-title{{
  font-size:18px;
  font-weight:700;
  margin-bottom:6px;
}}
.lock-sub{{
  font-size:12px;
  color:var(--text-muted);
  margin-bottom:22px;
}}
.lock-input{{
  width:100%;
  padding:12px 16px;
  border-radius:12px;
  border:1px solid var(--border-color);
  background:rgba(0,0,0,0.3);
  color:var(--text-primary);
  font-family:inherit;
  font-size:14px;
  outline:none;
  margin-bottom:14px;
  text-align:center;
  letter-spacing:0.1em;
  transition:var(--transition);
}}
.lock-input:focus{{
  border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-glow);
}}
.lock-error{{
  color:var(--danger);
  font-size:12px;
  margin-bottom:14px;
  min-height:20px;
}}
.lock-btn{{
  width:100%;
  justify-content:center;
  padding:12px;
  font-size:14px;
}}

/* ── Toast ── */
.toast{{
  position:fixed;
  bottom:24px;
  left:50%;
  transform:translateX(-50%) translateY(60px);
  background:var(--bg-card);
  border:1px solid var(--border-color);
  color:var(--text-primary);
  border-radius:12px;
  padding:12px 20px;
  font-size:13px;
  opacity:0;
  transition:all 0.3s ease;
  z-index:999;
  pointer-events:none;
  display:flex;
  align-items:center;
  gap:8px;
  box-shadow:var(--shadow);
}}
.toast.show{{
  opacity:1;
  transform:translateX(-50%) translateY(0);
}}
.toast.ok{{
  border-color:rgba(16,185,129,0.3);
  background:var(--success-bg);
  color:var(--success);
}}
.toast.err{{
  border-color:rgba(239,68,68,0.3);
  background:var(--danger-bg);
  color:var(--danger);
}}

/* ── QR Modal ── */
.qr-modal{{
  display:none;
  position:fixed;
  inset:0;
  background:rgba(0,0,0,0.75);
  backdrop-filter:blur(8px);
  z-index:600;
  align-items:center;
  justify-content:center;
}}
.qr-modal.open{{
  display:flex;
}}
.qr-box{{
  background:var(--bg-card);
  border:1px solid var(--border-color);
  border-radius:20px;
  padding:24px;
  text-align:center;
  max-width:340px;
  width:calc(100% - 32px);
  animation:fadeSlide 0.25s ease;
}}
.qr-title{{
  font-size:15px;
  font-weight:700;
  margin-bottom:16px;
}}
.qr-img{{
  border-radius:14px;
  overflow:hidden;
  margin-bottom:16px;
  background:#fff;
  padding:12px;
}}
.qr-img img{{
  width:100%;
  display:block;
}}

/* ── Footer ── */
.footer{{
  text-align:center;
  padding-top:32px;
  font-size:11px;
  color:var(--text-muted);
  border-top:1px solid var(--border-color);
  margin-top:24px;
}}
.footer a{{
  color:var(--accent);
  font-weight:600;
  text-decoration:none;
}}
.footer a:hover{{text-decoration:underline}}

/* ── Animations ── */
@keyframes pulse{{
  0%,100%{{opacity:1}}
  50%{{opacity:0.3}}
}}
@keyframes fadeSlide{{
  from{{opacity:0;transform:translateY(12px)}}
  to{{opacity:1;transform:none}}
}}
@keyframes spin{{
  to{{transform:rotate(360deg)}}
}}

/* ── Responsive ── */
@media(max-width:768px){{
  .header{{
    flex-wrap:wrap;
    gap:10px;
  }}
  .stats-grid{{
    grid-template-columns:1fr 1fr;
  }}
  .wrap{{
    padding:16px 12px 40px;
  }}
  .sub-info{{
    padding:18px 16px;
  }}
  .cfg-card{{
    padding:16px;
  }}
  .url-box{{
    flex-direction:column;
    align-items:stretch;
  }}
  .url-actions{{
    justify-content:center;
  }}
}}
@media(max-width:480px){{
  .stats-grid{{
    grid-template-columns:1fr;
  }}
  .header{{
    flex-direction:column;
    align-items:stretch;
    text-align:center;
  }}
  .brand{{
    justify-content:center;
  }}
  .header-actions{{
    justify-content:center;
  }}
  .cfg-header{{
    flex-direction:column;
    align-items:flex-start;
  }}
  .cfg-actions{{
    justify-content:center;
  }}
}}
</style>
</head>
<body>
<div class="bg-layer"></div>
<div class="grid-overlay"></div>

<div class="toast" id="toast"></div>

<div class="qr-modal" id="qr-modal" onclick="this.classList.remove('open')">
  <div class="qr-box" onclick="event.stopPropagation()">
    <div class="qr-title" id="qr-label">QR Code</div>
    <div class="qr-img"><img id="qr-img" src="" alt="QR"></div>
    <button class="btn btn-ghost" style="width:100%;justify-content:center" onclick="document.getElementById('qr-modal').classList.remove('open')">
      <i class="ti ti-x"></i> بستن
    </button>
  </div>
</div>

<div class="wrap">
  <!-- Header -->
  <div class="header">
    <div class="brand">
      <div class="brand-icon">آ</div>
      <div>
        <div class="brand-text">تیم آزادی</div>
        <div class="brand-sub">RVG Gateway · v9.0</div>
      </div>
    </div>
    <div class="header-actions">
      <a class="channel-link" href="https://t.me/TimAzadi" target="_blank">
        <i class="ti ti-brand-telegram"></i> @TimAzadi
      </a>
    </div>
  </div>

  <!-- Main Content -->
  <div id="root">
    <div style="text-align:center;padding:80px 20px;color:var(--text-muted)">
      <i class="ti ti-loader-2" style="font-size:38px;display:block;margin-bottom:14px;animation:spin 1s linear infinite"></i>
      در حال بارگذاری...
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    کانال رسمی: <a href="https://t.me/TimAzadi" target="_blank">@TimAzadi</a>
    ·
    تیم آزادی · RVG Gateway v9.0
  </div>
</div>

<script>
const UUID_KEY='{uuid_key}';
let savedPw='';

function toast(msg,type){{
  const t=document.getElementById('toast');
  t.textContent=msg;
  t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2600);
}}

function esc(s){{
  return String(s||'').replace(/[&<>"']/g,c=>({{
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }}));
}}

function fmtB(b){{
  if(!b||b===0)return '0 B';
  if(b<1024)return b+' B';
  if(b<1024**2)return (b/1024).toFixed(1)+' KB';
  if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';
  return (b/1024**3).toFixed(2)+' GB';
}}

function toFa(n){{
  return String(n).replace(/\\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d]);
}}

function showQR(label,link){{
  document.getElementById('qr-label').textContent=label;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(link);
  document.getElementById('qr-modal').classList.add('open');
}}

async function loadData(pw){{
  const url='/api/public/sub/'+UUID_KEY+(pw?'?pw='+encodeURIComponent(pw):'');
  const r=await fetch(url);
  return r.json();
}}

function renderLock(name,errMsg){{
  document.getElementById('root').innerHTML=`
    <div class="lock-card">
      <div class="lock-icon"><i class="ti ti-lock"></i></div>
      <div class="lock-title">${{esc(name)}}</div>
      <div class="lock-sub">این گروه رمزدار است. رمز را وارد کنید.</div>
      <div class="lock-error" id="lock-err">${{esc(errMsg||'')}}</div>
      <input class="lock-input" type="password" id="lock-pw" placeholder="رمز عبور" autofocus>
      <button class="btn btn-primary lock-btn" onclick="submitLock()">
        <i class="ti ti-lock-open"></i> ورود
      </button>
    </div>
  `;
  document.getElementById('lock-pw').addEventListener('keydown',e=>{{
    if(e.key==='Enter') submitLock();
  }});
  document.getElementById('lock-pw').focus();
}}

async function submitLock(){{
  const pw=document.getElementById('lock-pw').value;
  const data=await loadData(pw);
  if(data.locked){{
    renderLock(data.name,'رمز اشتباه است');
    return;
  }}
  savedPw=pw;
  renderContent(data);
}}

function renderContent(d){{
  const activeCount = d.links.filter(l=>l.active).length;
  const baseSubUrl = d.sub_url || (window.location.protocol + '//' + window.location.host + '/sub-group/' + UUID_KEY);
  const subUrl = baseSubUrl + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : '');
  
  window._rvgSubUrl  = subUrl;
  window._rvgSubName = d.name;
  window._rvgLinks   = d.links.map(l => ({{
    vless : l.vless_link,
    sub   : l.sub_url + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : ''),
    label : l.label,
  }}));

  var html = '';
  html += `<div class="sub-info">
    <div class="sub-name">${{esc(d.name)}}</div>`;
  if(d.desc) html += `<div class="sub-desc">${{esc(d.desc)}}</div>`;
  html += `
    <div class="sub-meta">
      <span><i class="ti ti-clock"></i> آخرین بروزرسانی: ${{new Date().toLocaleTimeString('fa-IR')}}</span>
      <span><i class="ti ti-link"></i> ${{toFa(d.links.length)}} کانفیگ</span>
      <span><i class="ti ti-circle-check" style="color:var(--success)"></i> ${{toFa(activeCount)}} فعال</span>
    </div>
    <div class="url-box">
      <span class="url-text">${{esc(subUrl)}}</span>
      <div class="url-actions">
        <button class="btn btn-ghost btn-sm" onclick="navigator.clipboard.writeText(window._rvgSubUrl).then(()=>toast('لینک ساب کپی شد ✓','ok'))">
          <i class="ti ti-copy"></i> کپی
        </button>
        <button class="btn btn-ghost btn-sm" onclick="showQR(window._rvgSubName + ' — کل گروه', window._rvgSubUrl)">
          <i class="ti ti-qrcode"></i> QR
        </button>
      </div>
    </div>
  </div>

  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-label">کانفیگ‌های فعال</div>
      <div class="stat-value">${{toFa(activeCount)}}</div>
      <div class="stat-sub">از ${{toFa(d.links.length)}} کانفیگ</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">اتصالات زنده</div>
      <div class="stat-value">${{toFa(d.active_connections)}}</div>
      <div class="stat-sub"><span class="dot green"></span> آنلاین</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">کل مصرف</div>
      <div class="stat-value" style="font-size:18px">${{esc(d.total_used_fmt)}}</div>
      <div class="stat-sub">همه کانفیگ‌ها</div>
    </div>
  </div>

  <div class="section-title">
    <i class="ti ti-link"></i> کانفیگ‌ها
    <span class="badge">${{toFa(d.links.length)}} عدد</span>
  </div>
  <div class="cfg-grid">`;

  d.links.forEach(function(l, i) {{
    var pct = l.limit_bytes === 0 ? 0 : Math.min(100, l.used_bytes / l.limit_bytes * 100);
    var bc = pct > 90 ? 'var(--danger)' : pct > 70 ? 'var(--warning)' : 'var(--success)';
    var lim = l.limit_bytes === 0 ? '∞' : fmtB(l.limit_bytes);
    var isActive = l.active;
    var statusClass = isActive ? 'active' : 'inactive';
    var statusIcon = isActive ? 'circle-check' : 'circle-x';
    var statusText = isActive ? 'فعال' : 'غیرفعال';
    
    html += `
    <div class="cfg-card">
      <div class="cfg-header">
        <div>
          <div class="cfg-label">${{esc(l.label)}}</div>`;
    if(l.connections > 0) {{
      html += `<span style="display:inline-flex;align-items:center;gap:4px;margin-top:4px;font-size:10px;background:var(--success-bg);color:var(--success);padding:2px 10px;border-radius:20px;font-weight:700"><span style="width:5px;height:5px;border-radius:50%;background:var(--success);animation:pulse 2s infinite;display:inline-block"></span> ${{toFa(l.connections)}} اتصال</span>`;
    }}
    html += `
        </div>
        <span class="cfg-status ${{statusClass}}">
          <i class="ti ti-${{statusIcon}}"></i>
          ${{statusText}}
        </span>
      </div>
      <div class="usage-wrapper">
        <div class="usage-bar"><div class="usage-fill" style="width:${{pct}}%;background:${{bc}}"></div></div>
        <div class="usage-text">
          <span>مصرف: ${{esc(l.used_fmt)}}</span>
          <span>سهمیه: ${{lim}}</span>
        </div>
      </div>
      <div class="cfg-link">${{esc(l.vless_link)}}</div>
      <div class="cfg-actions">
        <button class="btn btn-primary btn-sm" onclick="navigator.clipboard.writeText(window._rvgLinks[${{i}}].vless).then(()=>toast('لینک کپی شد ✓','ok'))">
          <i class="ti ti-copy"></i> کپی
        </button>
        <button class="btn btn-ghost btn-sm" onclick="showQR(window._rvgLinks[${{i}}].label, window._rvgLinks[${{i}}].vless)">
          <i class="ti ti-qrcode"></i> QR
        </button>
        <button class="btn btn-ghost-light btn-sm" onclick="navigator.clipboard.writeText(window._rvgLinks[${{i}}].sub).then(()=>toast('لینک ساب کپی شد ✓','ok'))">
          <i class="ti ti-rss"></i> ساب
        </button>
      </div>
    </div>`;
  }});

  html += `</div>`;
  document.getElementById('root').innerHTML = html;
  
  setTimeout(function() {{
    try{{
      const data = loadData(savedPw);
      if (!data.locked) renderContent(data);
    }} catch(e) {{}}
  }}, 30000);
}}

async function init(){{
  try{{
    const data = await loadData('');
    if (data.locked) {{
      renderLock(data.name);
      return;
    }}
    renderContent(data);
  }} catch(e) {{
    document.getElementById('root').innerHTML = `
      <div style="text-align:center;padding:80px 20px;color:var(--danger)">
        <i class="ti ti-alert-circle" style="font-size:38px;display:block;margin-bottom:14px"></i>
        خطا در بارگذاری اطلاعات
      </div>
    `;
  }}
}}

init();
</script>
</body></html>"""


def get_single_link_page_html(uuid: str, link_data: dict) -> str:
    """صفحه‌ی عمومی یک کانفیگ تکی – UI حرفه‌ای"""
    label = link_data.get("label", "بدون نام")
    vless_link = link_data.get("vless_link", "")
    sub_url = link_data.get("sub_url", "")
    used_fmt = link_data.get("used_fmt", "0 B")
    limit_fmt = link_data.get("limit_fmt", "∞")
    limit_bytes = link_data.get("limit_bytes", 0)
    used_bytes = link_data.get("used_bytes", 0)
    active = link_data.get("active", True)
    expired = link_data.get("expired", False)
    created_at = link_data.get("created_at", "")
    
    pct = 0 if limit_bytes == 0 else min(100, used_bytes / limit_bytes * 100)
    bar_color = "var(--danger)" if pct > 90 else ("var(--warning)" if pct > 70 else "var(--success)")
    status_class = "active" if active and not expired else "inactive"
    status_icon = "circle-check" if active and not expired else "circle-x"
    status_text = "فعال" if active and not expired else "غیرفعال"

    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{label} · تیم آزادی</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --bg-primary:#0A0E14;
  --bg-secondary:#11181F;
  --bg-card:#181F28;
  --bg-card-hover:#1F2833;
  --text-primary:#E8EDF5;
  --text-secondary:#8FA3B8;
  --text-muted:#5A6F84;
  --accent:#E83C6A;
  --accent-dark:#C72A56;
  --accent-glow:rgba(232,60,106,0.15);
  --border-color:rgba(143,171,202,0.08);
  --border-hover:rgba(232,60,106,0.3);
  --success:#10B981;
  --success-bg:rgba(16,185,129,0.12);
  --warning:#F59E0B;
  --warning-bg:rgba(245,158,11,0.12);
  --danger:#EF4444;
  --danger-bg:rgba(239,68,68,0.12);
  --radius:16px;
  --shadow:0 8px 32px rgba(0,0,0,0.4);
  --transition:0.3s cubic-bezier(0.4,0,0.2,1);
}}
html,body{{
  min-height:100%;
  background:var(--bg-primary);
  font-family:'Vazirmatn',sans-serif;
  color:var(--text-primary);
  font-size:14px;
  line-height:1.6;
}}
::-webkit-scrollbar{{width:6px;height:6px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:var(--accent);border-radius:3px}}

.bg-layer{{
  position:fixed;
  inset:0;
  z-index:0;
  background:
    radial-gradient(ellipse 60% 40% at 50% 0%, rgba(232,60,106,0.06), transparent 60%),
    radial-gradient(ellipse 40% 30% at 80% 80%, rgba(232,60,106,0.04), transparent 50%),
    var(--bg-primary);
  pointer-events:none;
}}
.grid-overlay{{
  position:fixed;
  inset:0;
  z-index:0;
  background-image:
    linear-gradient(rgba(232,60,106,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(232,60,106,0.03) 1px, transparent 1px);
  background-size:48px 48px;
  pointer-events:none;
}}

.wrap{{
  position:relative;
  z-index:10;
  max-width:680px;
  margin:0 auto;
  padding:24px 20px 60px;
}}

.header{{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:32px;
  padding:12px 20px;
  background:var(--bg-card);
  border:1px solid var(--border-color);
  border-radius:var(--radius);
  backdrop-filter:blur(12px);
}}
.brand{{
  display:flex;
  align-items:center;
  gap:12px;
}}
.brand-icon{{
  width:42px;
  height:42px;
  border-radius:12px;
  background:linear-gradient(135deg,var(--accent),var(--accent-dark));
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:20px;
  font-weight:900;
  color:#fff;
  box-shadow:0 0 24px var(--accent-glow);
}}
.brand-text{{
  font-size:16px;
  font-weight:700;
  color:var(--text-primary);
}}
.brand-sub{{
  font-size:10px;
  color:var(--text-muted);
  letter-spacing:0.06em;
}}
.header-actions{{
  display:flex;
  gap:8px;
  align-items:center;
}}
.channel-link{{
  display:flex;
  align-items:center;
  gap:6px;
  padding:6px 14px;
  border-radius:8px;
  background:rgba(232,60,106,0.1);
  color:var(--accent);
  font-size:12px;
  font-weight:600;
  text-decoration:none;
  transition:var(--transition);
}}
.channel-link:hover{{
  background:rgba(232,60,106,0.2);
  transform:translateY(-1px);
}}

.hero-card{{
  background:var(--bg-card);
  border:1px solid var(--border-color);
  border-radius:var(--radius);
  padding:28px;
  margin-bottom:20px;
  transition:var(--transition);
}}
.hero-card:hover{{
  border-color:var(--border-hover);
  box-shadow:var(--shadow);
}}
.hero-title{{
  font-size:24px;
  font-weight:800;
  background:linear-gradient(135deg,var(--text-primary),var(--text-secondary));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  margin-bottom:4px;
}}
.hero-meta{{
  display:flex;
  flex-wrap:wrap;
  gap:12px;
  margin-bottom:16px;
  font-size:12px;
  color:var(--text-muted);
}}
.hero-meta span{{
  display:flex;
  align-items:center;
  gap:6px;
}}
.hero-meta i{{color:var(--accent)}}

.status-badge{{
  font-size:10px;
  font-weight:700;
  padding:3px 12px;
  border-radius:20px;
  display:inline-flex;
  align-items:center;
  gap:4px;
  white-space:nowrap;
}}
.status-badge.active{{
  background:var(--success-bg);
  color:var(--success);
}}
.status-badge.inactive{{
  background:var(--danger-bg);
  color:var(--danger);
}}

.usage-section{{
  margin-bottom:18px;
}}
.usage-bar{{
  height:6px;
  border-radius:3px;
  background:rgba(255,255,255,0.06);
  overflow:hidden;
  margin-bottom:4px;
}}
.usage-fill{{
  height:100%;
  border-radius:3px;
  transition:width 0.6s ease;
}}
.usage-text{{
  font-size:12px;
  color:var(--text-muted);
  display:flex;
  justify-content:space-between;
}}

.vless-box{{
  background:rgba(0,0,0,0.3);
  border:1px solid var(--border-color);
  border-radius:10px;
  padding:12px 16px;
  font-family:ui-monospace,monospace;
  font-size:11px;
  color:var(--accent);
  word-break:break-all;
  line-height:1.8;
  margin-bottom:18px;
  transition:var(--transition);
}}
.vless-box:hover{{
  border-color:var(--border-hover);
}}

.actions{{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
}}
.btn{{
  font-family:inherit;
  font-size:12px;
  font-weight:600;
  border-radius:8px;
  padding:10px 18px;
  cursor:pointer;
  display:inline-flex;
  align-items:center;
  gap:6px;
  border:none;
  transition:var(--transition);
  text-decoration:none;
}}
.btn i{{font-size:14px}}
.btn-primary{{
  background:linear-gradient(135deg,var(--accent),var(--accent-dark));
  color:#fff;
  box-shadow:0 4px 16px var(--accent-glow);
}}
.btn-primary:hover{{
  transform:translateY(-1px);
  box-shadow:0 6px 24px var(--accent-glow);
  filter:brightness(1.08);
}}
.btn-ghost{{
  background:rgba(232,60,106,0.08);
  color:var(--accent);
  border:1px solid rgba(232,60,106,0.15);
}}
.btn-ghost:hover{{
  background:rgba(232,60,106,0.15);
  transform:translateY(-1px);
}}
.btn-ghost-light{{
  background:rgba(255,255,255,0.04);
  color:var(--text-secondary);
  border:1px solid var(--border-color);
}}
.btn-ghost-light:hover{{
  background:rgba(255,255,255,0.08);
  color:var(--text-primary);
}}

.toast{{
  position:fixed;
  bottom:24px;
  left:50%;
  transform:translateX(-50%) translateY(60px);
  background:var(--bg-card);
  border:1px solid var(--border-color);
  color:var(--text-primary);
  border-radius:12px;
  padding:12px 20px;
  font-size:13px;
  opacity:0;
  transition:all 0.3s ease;
  z-index:999;
  pointer-events:none;
  display:flex;
  align-items:center;
  gap:8px;
  box-shadow:var(--shadow);
}}
.toast.show{{
  opacity:1;
  transform:translateX(-50%) translateY(0);
}}
.toast.ok{{
  border-color:rgba(16,185,129,0.3);
  background:var(--success-bg);
  color:var(--success);
}}
.toast.err{{
  border-color:rgba(239,68,68,0.3);
  background:var(--danger-bg);
  color:var(--danger);
}}

.qr-modal{{
  display:none;
  position:fixed;
  inset:0;
  background:rgba(0,0,0,0.75);
  backdrop-filter:blur(8px);
  z-index:600;
  align-items:center;
  justify-content:center;
}}
.qr-modal.open{{
  display:flex;
}}
.qr-box{{
  background:var(--bg-card);
  border:1px solid var(--border-color);
  border-radius:20px;
  padding:24px;
  text-align:center;
  max-width:340px;
  width:calc(100% - 32px);
  animation:fadeSlide 0.25s ease;
}}
.qr-title{{
  font-size:15px;
  font-weight:700;
  margin-bottom:16px;
}}
.qr-img{{
  border-radius:14px;
  overflow:hidden;
  margin-bottom:16px;
  background:#fff;
  padding:12px;
}}
.qr-img img{{
  width:100%;
  display:block;
}}

.footer{{
  text-align:center;
  padding-top:32px;
  font-size:11px;
  color:var(--text-muted);
  border-top:1px solid var(--border-color);
  margin-top:24px;
}}
.footer a{{
  color:var(--accent);
  font-weight:600;
  text-decoration:none;
}}
.footer a:hover{{text-decoration:underline}}

@keyframes pulse{{
  0%,100%{{opacity:1}}
  50%{{opacity:0.3}}
}}
@keyframes fadeSlide{{
  from{{opacity:0;transform:translateY(12px)}}
  to{{opacity:1;transform:none}}
}}
@keyframes spin{{
  to{{transform:rotate(360deg)}}
}}

@media(max-width:640px){{
  .wrap{{
    padding:16px 12px 40px;
  }}
  .hero-card{{
    padding:18px 16px;
  }}
  .header{{
    flex-wrap:wrap;
    gap:10px;
    justify-content:center;
  }}
  .brand{{
    flex:1;
  }}
  .header-actions{{
    flex:1;
    justify-content:flex-end;
  }}
  .actions{{
    justify-content:center;
  }}
  .vless-box{{
    font-size:10px;
    padding:10px 12px;
  }}
}}
</style>
</head>
<body>
<div class="bg-layer"></div>
<div class="grid-overlay"></div>

<div class="toast" id="toast"></div>

<div class="qr-modal" id="qr-modal" onclick="this.classList.remove('open')">
  <div class="qr-box" onclick="event.stopPropagation()">
    <div class="qr-title" id="qr-label">QR Code</div>
    <div class="qr-img"><img id="qr-img" src="" alt="QR"></div>
    <button class="btn btn-ghost" style="width:100%;justify-content:center" onclick="document.getElementById('qr-modal').classList.remove('open')">
      <i class="ti ti-x"></i> بستن
    </button>
  </div>
</div>

<div class="wrap">
  <div class="header">
    <div class="brand">
      <div class="brand-icon">آ</div>
      <div>
        <div class="brand-text">تیم آزادی</div>
        <div class="brand-sub">RVG Gateway · v9.0</div>
      </div>
    </div>
    <div class="header-actions">
      <a class="channel-link" href="https://t.me/TimAzadi" target="_blank">
        <i class="ti ti-brand-telegram"></i> @TimAzadi
      </a>
    </div>
  </div>

  <div class="hero-card">
    <div class="hero-title">{label}</div>
    <div class="hero-meta">
      <span><i class="ti ti-calendar"></i> {created_at[:10] if created_at else "—"}</span>
      <span class="status-badge {status_class}">
        <i class="ti ti-{status_icon}"></i>
        {status_text}
      </span>
    </div>

    <div class="usage-section">
      <div class="usage-bar"><div class="usage-fill" style="width:{pct}%;background:{bar_color}"></div></div>
      <div class="usage-text">
        <span>مصرف: {used_fmt}</span>
        <span>سهمیه: {limit_fmt}</span>
      </div>
    </div>

    <div class="vless-box">{vless_link}</div>

    <div class="actions">
      <button class="btn btn-primary" onclick="copyToClipboard('{vless_link}')">
        <i class="ti ti-copy"></i> کپی لینک VLESS
      </button>
      <button class="btn btn-ghost" onclick="showQR('{label}', '{vless_link}')">
        <i class="ti ti-qrcode"></i> QR Code
      </button>
      <button class="btn btn-ghost-light" onclick="copyToClipboard('{sub_url}')">
        <i class="ti ti-rss"></i> کپی لینک ساب
      </button>
    </div>
  </div>

  <div class="footer">
    کانال رسمی: <a href="https://t.me/TimAzadi" target="_blank">@TimAzadi</a>
    ·
    تیم آزادی · RVG Gateway v9.0
  </div>
</div>

<script>
function toast(msg,type){{
  const t=document.getElementById('toast');
  t.textContent=msg;
  t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2600);
}}

function copyToClipboard(text){{
  navigator.clipboard.writeText(text).then(()=>toast('کپی شد ✓','ok'));
}}

function showQR(label,link){{
  document.getElementById('qr-label').textContent=label;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(link);
  document.getElementById('qr-modal').classList.add('open');
}}
</script>
</body></html>"""
