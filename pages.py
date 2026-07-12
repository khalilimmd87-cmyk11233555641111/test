# pages.py  -  تیم آزادی Gateway v10.0
# شامل: LOGIN_HTML, DASHBOARD_HTML, get_public_page_html(), get_single_link_page_html()

from assets import LOGO_DATA_URI

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · تیم آزادی Gateway</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#060f1d;--card:rgba(10,22,40,0.9);--accent:#3B82F6;--text:#E8F4FF;--dim:#3D6B8E;--mid:#7BAED4;--border:rgba(59,130,246,0.2)}
html,body{height:100%;overflow:hidden}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);display:flex;align-items:center;justify-content:center;padding:20px}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(59,130,246,0.1),transparent 70%),var(--bg);z-index:0}
.grid{position:fixed;inset:0;background-image:linear-gradient(rgba(59,130,246,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(59,130,246,0.04) 1px,transparent 1px);background-size:44px 44px;z-index:0}
.orb{position:fixed;border-radius:50%;filter:blur(90px);z-index:0;animation:fl 9s ease-in-out infinite}
.o1{width:380px;height:380px;background:rgba(59,130,246,0.07);top:-100px;right:-80px}
.o2{width:280px;height:280px;background:rgba(16,185,129,0.04);bottom:-60px;left:-60px;animation-delay:4s}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}
.wrap{position:relative;z-index:10;width:100%;max-width:400px}
.card{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:38px 34px 34px;backdrop-filter:blur(24px);box-shadow:0 0 80px rgba(59,130,246,0.07),0 20px 60px rgba(0,0,0,.5)}
.brand{display:flex;align-items:center;gap:14px;margin-bottom:28px}
.brand-img{width:48px;height:48px;border-radius:13px;overflow:hidden;border:1px solid var(--border);box-shadow:0 0 20px rgba(59,130,246,0.3);flex-shrink:0}
.brand-img img{width:100%;height:100%;object-fit:cover}
.brand-name{font-size:16px;font-weight:700;color:var(--text)}
.brand-sub{font-size:11px;color:var(--dim);margin-top:2px}
h1{font-size:21px;font-weight:700;color:var(--text);margin-bottom:5px;letter-spacing:-.02em}
.sub{font-size:12px;color:var(--mid);margin-bottom:24px;line-height:1.6}
.hint{display:flex;align-items:center;gap:10px;background:rgba(59,130,246,0.07);border:1px solid rgba(59,130,246,0.15);border-radius:10px;padding:10px 14px;margin-bottom:20px}
.hint-label{font-size:11px;color:var(--dim);flex:1}
.hint-val{font-family:ui-monospace,monospace;font-size:14px;font-weight:700;color:var(--accent);background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.25);padding:3px 11px;border-radius:7px;cursor:pointer;transition:.15s;letter-spacing:.08em}
.hint-val:hover{background:rgba(59,130,246,0.22)}
.field{margin-bottom:18px}
.field label{display:block;font-size:10.5px;font-weight:600;color:var(--mid);margin-bottom:7px;text-transform:uppercase;letter-spacing:.06em}
.inp-wrap{position:relative}
input[type=password]{width:100%;padding:13px 44px 13px 16px;border-radius:11px;border:1px solid var(--border);background:rgba(0,0,0,.3);color:var(--text);font-family:inherit;font-size:14px;outline:none;transition:.2s}
input[type=password]:focus{border-color:rgba(59,130,246,.55);background:rgba(0,0,0,.4);box-shadow:0 0 0 3px rgba(59,130,246,.1)}
.ic{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--dim);font-size:18px;pointer-events:none;transition:.2s}
input:focus+.ic{color:var(--accent)}
.err{display:none;background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:12px;color:#F87171;align-items:center;gap:8px}
.err.show{display:flex}
.btn{width:100%;padding:13px;border-radius:11px;border:none;cursor:pointer;background:linear-gradient(135deg,#2563EB,#1D4ED8);color:#fff;font-family:inherit;font-size:14px;font-weight:600;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 20px rgba(37,99,235,.4);transition:.2s;position:relative;overflow:hidden}
.btn::before{content:'';position:absolute;inset:0;background:rgba(255,255,255,.08);opacity:0;transition:.2s}
.btn:hover::before{opacity:1}
.btn:disabled{opacity:.5;cursor:not-allowed}
.footer{margin-top:22px;padding-top:18px;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:center;gap:8px;font-size:11px;color:var(--dim)}
.footer a{color:var(--accent);font-weight:600;text-decoration:none;display:flex;align-items:center;gap:4px}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="bg"></div><div class="grid"></div>
<div class="orb o1"></div><div class="orb o2"></div>
<div class="wrap">
  <div class="card">
    <div class="brand">
      <div class="brand-img"><img src="{{LOGO}}" alt="تیم آزادی"></div>
      <div><div class="brand-name">تیم آزادی</div><div class="brand-sub">تیم آزادی Gateway · v10.0</div></div>
    </div>
    <h1>ورود به پنل</h1>
    <p class="sub">رمز عبور را برای دسترسی به داشبورد وارد کنید</p>
    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
    <form id="form">
      <div class="field">
        <label>رمز عبور</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus required>
          <i class="ti ti-lock ic"></i>
        </div>
      </div>
      <button class="btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود به داشبورد</button>
    </form>
    <div class="footer">کانال رسمی<a href="https://t.me/TimAzadi" target="_blank"><i class="ti ti-brand-telegram"></i>@TimAzadi</a></div>
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
    location.href='/timazadi';
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.innerHTML='<i class="ti ti-login-2"></i> ورود به داشبورد';
  }
});
</script>
</body></html>""".replace("{{LOGO}}", LOGO_DATA_URI)


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تیم آزادی Gateway</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#060f1d;--bg2:#0a1628;--bg3:#0e1e35;
  --card:#0d1b2e;--card-b:rgba(59,130,246,0.13);--card-bh:rgba(59,130,246,0.28);
  --accent:#3B82F6;--accent2:#60A5FA;--accent-d:rgba(59,130,246,0.12);
  --green:#10B981;--green-bg:rgba(16,185,129,0.1);--green-t:#34D399;
  --red:#EF4444;--red-bg:rgba(239,68,68,0.1);--red-t:#F87171;
  --amber:#F59E0B;--amber-bg:rgba(245,158,11,0.1);--amber-t:#FCD34D;
  --purple:#8B5CF6;--purple-bg:rgba(139,92,246,0.1);
  --t1:#E8F4FF;--t2:#7BAED4;--t3:#3D6B8E;
  --sidebar-w:248px;--radius:16px;
  --shadow:0 4px 24px rgba(0,0,0,0.35);
}
[data-theme="light"]{
  --bg:#F0F4FA;--bg2:#E4EDF9;--bg3:#D5E3F5;
  --card:#FFFFFF;--card-b:rgba(59,130,246,0.15);--card-bh:rgba(59,130,246,0.35);
  --accent:#2563EB;--accent2:#1D4ED8;--accent-d:rgba(37,99,235,0.08);
  --green:#059669;--green-bg:rgba(5,150,105,0.08);--green-t:#065F46;
  --red:#DC2626;--red-bg:rgba(220,38,38,0.08);--red-t:#991B1B;
  --amber:#D97706;--amber-bg:rgba(217,119,6,0.08);--amber-t:#92400E;
  --purple:#7C3AED;--purple-bg:rgba(124,58,237,0.08);
  --t1:#0F172A;--t2:#334155;--t3:#64748B;
  --shadow:0 4px 20px rgba(0,0,0,0.1);
}
html,body{height:100%}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--t1);min-height:100vh;display:flex;font-size:14px;transition:background .3s,color .3s}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:3px}
a{color:inherit;text-decoration:none}
.sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--bg2);border-left:1px solid var(--card-b);display:flex;flex-direction:column;flex-shrink:0;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform .25s cubic-bezier(.4,0,.2,1),background .3s,border-color .3s}
.logo{display:flex;align-items:center;gap:12px;padding:20px 16px 16px;border-bottom:1px solid var(--card-b)}
.logo-img{width:38px;height:38px;border-radius:10px;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 14px var(--accent-d);flex-shrink:0}
.logo-img img{width:100%;height:100%;object-fit:cover}
.logo-name{font-size:13.5px;font-weight:700;color:var(--t1)}
.logo-sub{font-size:10px;color:var(--t3);margin-top:1px}
.sb-close{display:none;position:absolute;left:12px;top:20px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;align-items:center;justify-content:center;cursor:pointer}
.nav-wrap{flex:1;overflow-y:auto;padding:6px 0 8px}
.nav-sec{padding:14px 14px 4px;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--t3);font-weight:700}
.nav-it{display:flex;align-items:center;gap:9px;padding:9px 14px;color:var(--t3);font-size:12.5px;cursor:pointer;border-right:2px solid transparent;transition:all .15s;margin:1px 6px}
.nav-it i{font-size:16px;width:18px;text-align:center;flex-shrink:0}
.nav-it:hover{background:var(--accent-d);color:var(--t2)}
.nav-it.on{background:var(--accent-d);color:var(--t1);border-right-color:var(--accent);font-weight:600}
.nav-badge{margin-right:auto;background:rgba(59,130,246,0.15);color:var(--accent2);font-size:9px;padding:1px 6px;border-radius:20px;font-weight:700}
.sb-foot{padding:12px 14px;border-top:1px solid var(--card-b)}
.tg-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:linear-gradient(135deg,#0098e6,#0077bb);color:#fff;border-radius:9px;padding:10px;font-size:12.5px;font-weight:600;font-family:inherit;border:none;cursor:pointer;width:100%;transition:.15s}
.tg-btn:hover{filter:brightness(1.1)}
.theme-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--accent-d);color:var(--t2);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid var(--card-b);cursor:pointer;width:100%;transition:.15s;margin-bottom:7px}
.theme-btn:hover{background:var(--card-b);color:var(--t1)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--red-bg);color:var(--red-t);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid rgba(239,68,68,0.2);cursor:pointer;width:100%;transition:.15s;margin-top:6px}
.logout-btn:hover{background:rgba(239,68,68,0.2)}
.mob-top{display:none;position:fixed;top:0;right:0;left:0;height:52px;background:var(--bg2);border-bottom:1px solid var(--card-b);z-index:150;align-items:center;justify-content:space-between;padding:0 14px;transition:background .3s}
.mob-top .ml{display:flex;align-items:center;gap:9px}
.mob-logo{width:28px;height:28px;border-radius:7px;overflow:hidden}
.mob-logo img{width:100%;height:100%;object-fit:cover}
.mob-title{color:var(--t1);font-size:13px;font-weight:700}
.mob-right{display:flex;gap:6px}
.menu-btn,.theme-mob{background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:34px;height:34px;border-radius:8px;font-size:17px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:.15s}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:190;backdrop-filter:blur(3px)}
.overlay.show{display:block}
.main{margin-right:var(--sidebar-w);flex:1;padding:28px 28px 60px;min-width:0;transition:margin .25s}
.pg{display:none}
.pg.on{display:block;animation:fi .2s ease}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:22px;flex-wrap:wrap;gap:12px}
.tb-title{font-size:18px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:8px;letter-spacing:-.02em}
.tb-title i{color:var(--accent);font-size:20px}
.tb-sub{font-size:11px;color:var(--t3);margin-top:4px}
.tb-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.badge{font-size:10px;padding:3px 10px;border-radius:20px;font-weight:700;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.bg-green{background:var(--green-bg);color:var(--green-t)}
.bg-blue{background:var(--accent-d);color:var(--accent2)}
.bg-amber{background:var(--amber-bg);color:var(--amber-t)}
.bg-red{background:var(--red-bg);color:var(--red-t)}
.bg-purple{background:var(--purple-bg);color:#A78BFA}
.dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;display:inline-block}
.dg{background:var(--green)}.dr{background:var(--red)}.da{background:var(--amber)}.db{background:var(--accent)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:18px}
.metric{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:17px 17px 14px;transition:all .2s;position:relative;overflow:hidden;cursor:default}
.metric::after{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--accent);opacity:0;transition:.2s}
.metric:hover{border-color:var(--card-bh);transform:translateY(-2px);box-shadow:var(--shadow)}
.metric:hover::after{opacity:1}
.metric.suc::after{background:var(--green)}
.metric.dan::after{background:var(--red)}
.traf-hero{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:13px;margin-bottom:18px}
.traf-main-stat{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 60%);border:1px solid var(--card-b);border-radius:20px;padding:22px 24px;position:relative;overflow:hidden}
.traf-main-stat::before{content:'';position:absolute;top:-50px;left:-50px;width:200px;height:200px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.traf-main-label{font-size:10.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center;gap:6px;margin-bottom:10px;position:relative;z-index:1}
.traf-main-val{font-size:34px;font-weight:800;color:var(--t1);line-height:1;letter-spacing:-.02em;display:flex;align-items:baseline;gap:6px;position:relative;z-index:1}
.traf-main-val span{font-size:14px;font-weight:500;color:var(--t3)}
.traf-trend{display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:700;padding:4px 10px;border-radius:20px;margin-top:12px;position:relative;z-index:1}
.traf-trend.up{background:var(--green-bg);color:var(--green-t)}
.traf-trend.down{background:var(--red-bg);color:var(--red-t)}
.traf-mini{background:var(--card);border:1px solid var(--card-b);border-radius:20px;padding:18px 19px;display:flex;flex-direction:column;justify-content:space-between;transition:.2s}
.traf-mini:hover{border-color:var(--card-bh);transform:translateY(-2px)}
.traf-mini-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.traf-mini-icon{width:32px;height:32px;border-radius:9px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:15px}
.traf-mini-icon.pk{background:var(--amber-bg);color:var(--amber)}
.traf-mini-icon.lo{background:var(--purple-bg);color:var(--purple)}
.traf-mini-label{font-size:9.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.traf-mini-val{font-size:21px;font-weight:800;color:var(--t1);letter-spacing:-.01em}
.traf-mini-sub{font-size:9.5px;color:var(--t3);margin-top:3px}
.traf-chart-card{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:22px 24px 18px;box-shadow:var(--shadow);margin-bottom:16px}
.traf-chart-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;flex-wrap:wrap;gap:10px}
.traf-chart-title{font-size:14px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:8px}
.traf-chart-title i{color:var(--accent);font-size:18px}
.traf-chart-sub{font-size:10.5px;color:var(--t3);margin-top:3px}
.traf-legend{display:flex;gap:14px;align-items:center}
.traf-legend-item{display:flex;align-items:center;gap:6px;font-size:10.5px;color:var(--t2);font-weight:600}
.traf-legend-dot{width:8px;height:8px;border-radius:3px}
.traf-range-tabs{display:flex;gap:4px;background:var(--accent-d);padding:3px;border-radius:10px;border:1px solid var(--card-b)}
.traf-range-tab{padding:6px 13px;border-radius:8px;font-size:10.5px;font-weight:700;color:var(--t3);cursor:pointer;transition:.15s;border:none;background:transparent;font-family:inherit}
.traf-range-tab.on{background:var(--accent);color:#fff;box-shadow:0 2px 8px rgba(59,130,246,.35)}
.traf-chart-body{height:320px;margin-top:14px;position:relative}
@media(max-width:900px){.traf-hero{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.traf-hero{grid-template-columns:1fr}.traf-chart-body{height:260px}}
.m-icon{width:34px;height:34px;border-radius:8px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;margin-bottom:11px;color:var(--accent);font-size:17px}
.m-icon.suc{background:var(--green-bg);color:var(--green)}
.m-icon.dan{background:var(--red-bg);color:var(--red)}
.m-icon.pur{background:var(--purple-bg);color:var(--purple)}
.m-label{font-size:10px;color:var(--t3);margin-bottom:4px;font-weight:600;text-transform:uppercase;letter-spacing:.05em}
.m-val{font-size:25px;font-weight:700;color:var(--t1);line-height:1;letter-spacing:-.02em}
.m-unit{font-size:12px;font-weight:400;color:var(--t3)}
.m-sub{font-size:10px;color:var(--t3);margin-top:6px;display:flex;align-items:center;gap:3px}
.vless-box{background:linear-gradient(135deg,var(--bg3) 0%,var(--bg2) 100%);border:1px solid var(--card-b);border-radius:18px;padding:20px 22px;margin-bottom:18px;box-shadow:var(--shadow);position:relative;overflow:hidden;transition:background .3s}
.vless-box::before{content:'';position:absolute;top:-50px;left:-50px;width:180px;height:180px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.vl-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:13px;flex-wrap:wrap;gap:8px}
.vl-title{color:var(--t2);font-size:11px;display:flex;align-items:center;gap:6px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.vl-title i{color:var(--accent);font-size:15px}
.vl-code{background:rgba(0,0,0,.18);border:1px solid var(--card-b);border-radius:9px;padding:13px 15px;font-size:11px;font-family:ui-monospace,monospace;color:var(--accent2);word-break:break-all;line-height:1.8;letter-spacing:.01em}
[data-theme="light"] .vl-code{background:rgba(0,0,0,.04)}
.vl-actions{display:flex;gap:8px;margin-top:13px;flex-wrap:wrap}
.btn{font-family:inherit;font-size:12px;font-weight:500;border-radius:9px;padding:8px 14px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s;white-space:nowrap}
.btn i{font-size:13px}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-p{background:var(--accent);color:#fff;box-shadow:0 2px 12px rgba(59,130,246,.3)}
.btn-p:hover{background:#2563EB;box-shadow:0 4px 18px rgba(59,130,246,.4)}
.btn-o{background:transparent;border:1px solid var(--card-b);color:var(--t2)}
.btn-o:hover{background:var(--accent-d);border-color:rgba(59,130,246,.3)}
.btn-g{background:var(--accent-d);color:var(--accent2);border:1px solid rgba(59,130,246,.15)}
.btn-g:hover{background:rgba(59,130,246,.22)}
.btn-d{background:var(--red-bg);color:var(--red-t);border:1px solid rgba(239,68,68,.2)}
.btn-d:hover{background:rgba(239,68,68,.2)}
.btn-pur{background:var(--purple-bg);color:#A78BFA;border:1px solid rgba(139,92,246,.2)}
.btn-pur:hover{background:rgba(139,92,246,.22)}
.btn-amber{background:var(--amber-bg);color:var(--amber-t);border:1px solid rgba(245,158,11,.2)}
.btn-amber:hover{background:rgba(245,158,11,.22)}
.btn-sm{padding:5px 9px;font-size:10.5px;border-radius:7px}
.btn-icon{width:30px;height:30px;padding:0;justify-content:center;border-radius:5px}
.card{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:18px 20px;transition:border-color .2s,background .3s}
.card:hover{border-color:var(--card-bh)}
.card-title{font-size:12.5px;font-weight:700;color:var(--t1);margin-bottom:15px;display:flex;align-items:center;gap:7px}
.card-title i{font-size:16px;color:var(--accent)}
.ml-auto{margin-right:auto}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:16px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:13px;margin-bottom:16px}
.mb16{margin-bottom:16px}
.sr{display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid rgba(59,130,246,0.05);font-size:12px}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--t2);display:flex;align-items:center;gap:6px}
.sr-k i{font-size:13px;color:var(--t3)}
.sr-v{color:var(--t1);font-weight:600;font-size:11.5px}
.ch{position:relative;height:230px}
.ch-lg{position:relative;height:330px}
.ch-sm{position:relative;height:185px}
.exp-chip{font-size:9px;padding:3px 8px;border-radius:6px;font-weight:700;display:inline-flex;align-items:center;gap:3px}
.ec-ok{background:var(--green-bg);color:var(--green-t)}
.ec-warn{background:var(--amber-bg);color:var(--amber-t)}
.ec-exp{background:var(--red-bg);color:var(--red-t)}
.ec-inf{background:var(--accent-d);color:var(--accent2)}
.tog{width:19px;height:34px;border-radius:19px;background:rgba(100,116,139,0.25);position:relative;cursor:pointer;transition:.2s;flex-shrink:0;border:none}
.tog::after{content:'';position:absolute;width:13px;height:13px;border-radius:50%;background:#fff;left:3px;bottom:3px;transition:.2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.tog.on{background:var(--green)}
.tog.on::after{bottom:18px}
.form-row{display:flex;gap:9px;flex-wrap:wrap;align-items:flex-end}
.fg{display:flex;flex-direction:column;gap:5px}
.fg label{font-size:10px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.fi,.fs{padding:9px 12px;border-radius:9px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12px;outline:none;transition:.15s;min-width:100px}
[data-theme="light"] .fi,[data-theme="light"] .fs{background:rgba(0,0,0,.04)}
.fi::placeholder{color:var(--t3)}
.fi:focus,.fs:focus{border-color:rgba(59,130,246,.45);background:rgba(0,0,0,.25);box-shadow:0 0 0 3px rgba(59,130,246,.08)}
.fs option{background:var(--bg2)}
[data-theme="light"] .fs option{background:#fff}
.cl{background:var(--accent-d);border:1px solid rgba(59,130,246,.15);border-radius:10px;padding:11px 13px;font-size:11px;color:var(--t2);display:flex;gap:9px;align-items:flex-start;line-height:1.8;margin-top:12px}
.cl i{font-size:15px;color:var(--accent);margin-top:1px;flex-shrink:0}
.cl.amber{background:var(--amber-bg);border-color:rgba(245,158,11,.2);color:var(--amber-t)}
.create-panel{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 55%);border:1px solid var(--card-b);border-radius:22px;padding:0;overflow:hidden;box-shadow:var(--shadow);margin-bottom:16px;position:relative}
.create-panel::before{content:'';position:absolute;top:-60px;left:-60px;width:220px;height:220px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.cp-head{display:flex;align-items:center;gap:13px;padding:22px 24px 18px;position:relative;z-index:1}
.cp-head-icon{width:44px;height:44px;border-radius:13px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;flex-shrink:0;box-shadow:0 6px 18px rgba(59,130,246,.35)}
.cp-head-text{flex:1;min-width:0}
.cp-head-title{font-size:15px;font-weight:800;color:var(--t1);letter-spacing:-.01em}
.cp-head-sub{font-size:11px;color:var(--t3);margin-top:2px}
.cp-body{padding:2px 24px 22px;position:relative;z-index:1}
.cp-row{display:grid;grid-template-columns:1.3fr 1fr;gap:14px;margin-bottom:16px}
.cp-block{background:rgba(0,0,0,.14);border:1px solid var(--card-b);border-radius:14px;padding:14px 16px}
[data-theme="light"] .cp-block{background:rgba(37,99,235,.03)}
.cp-block-label{font-size:10px;font-weight:800;color:var(--t2);text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center;gap:6px;margin-bottom:11px}
.cp-block-label i{color:var(--accent);font-size:14px}
.cp-input-full{width:100%;padding:10px 13px;border-radius:10px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.15s}
[data-theme="light"] .cp-input-full{background:#fff}
.cp-input-full:focus{border-color:rgba(59,130,246,.5);box-shadow:0 0 0 3px rgba(59,130,246,.1)}
.cp-input-full::placeholder{color:var(--t3)}
.cp-mini-row{display:flex;gap:8px;margin-top:9px}
.cp-quota-inputs{display:flex;gap:8px}
.cp-quota-inputs .cp-input-full{flex:1}
.cp-quota-inputs select.cp-input-full{flex:0 0 76px}
.chip-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}
.chip{font-size:10.5px;font-weight:700;padding:5px 12px;border-radius:8px;background:var(--accent-d);color:var(--t2);border:1px solid var(--card-b);cursor:pointer;transition:.15s;white-space:nowrap}
.chip:hover{background:rgba(59,130,246,.18);color:var(--accent2)}
.chip.active{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 3px 10px rgba(59,130,246,.35)}
.proto-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}
.proto-card{border:1.5px solid var(--card-b);border-radius:13px;padding:13px 12px;cursor:pointer;transition:.18s;text-align:center;position:relative;background:rgba(0,0,0,.1)}
[data-theme="light"] .proto-card{background:#fff}
.proto-card:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.proto-card.active{border-color:var(--accent);background:var(--accent-d);box-shadow:0 0 0 3px rgba(59,130,246,.1)}
.proto-card.active .proto-card-check{opacity:1;transform:scale(1)}
.proto-card-check{position:absolute;top:7px;left:7px;width:16px;height:16px;border-radius:50%;background:var(--accent);color:#fff;font-size:10px;display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.5);transition:.18s}
.proto-card-icon{width:32px;height:32px;border-radius:9px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:16px;margin:0 auto 8px}
.proto-card.active .proto-card-icon{background:var(--accent);color:#fff}
.proto-card-title{font-size:11px;font-weight:800;color:var(--t1)}
.proto-card-desc{font-size:9px;color:var(--t3);margin-top:3px;line-height:1.5}
.cp-footer{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-top:16px;border-top:1px solid var(--card-b);flex-wrap:wrap}
.cp-footer-note{display:flex;align-items:center;gap:8px;font-size:10.5px;color:var(--t3);line-height:1.7;flex:1;min-width:220px}
.cp-footer-note i{color:var(--accent);font-size:15px;flex-shrink:0}
.cp-submit-btn{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;border-radius:13px;padding:13px 26px;font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:8px;box-shadow:0 6px 20px rgba(59,130,246,.35);transition:.18s;white-space:nowrap}
.cp-submit-btn:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(59,130,246,.45)}
.cp-submit-btn:active{transform:translateY(0) scale(.98)}
@media(max-width:760px){
  .cp-row{grid-template-columns:1fr}
  .proto-cards{grid-template-columns:1fr}
  .cp-footer{flex-direction:column;align-items:stretch}
  .cp-submit-btn{justify-content:center}
}
.srv-panel{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 60%);border:1px solid var(--card-b);border-radius:22px;overflow:hidden;box-shadow:var(--shadow);position:relative}
.srv-panel::before{content:'';position:absolute;top:-60px;left:-60px;width:200px;height:200px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.srv-hero{display:flex;align-items:center;gap:14px;padding:22px 24px;position:relative;z-index:1;border-bottom:1px solid var(--card-b)}
.srv-hero-icon{width:50px;height:50px;border-radius:14px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;flex-shrink:0;box-shadow:0 6px 18px rgba(59,130,246,.35)}
.srv-hero-text{flex:1;min-width:0}
.srv-hero-domain{font-size:15px;font-weight:800;color:var(--t1);word-break:break-all}
.srv-hero-sub{font-size:10.5px;color:var(--t3);margin-top:4px;display:flex;align-items:center;gap:6px}
.srv-tiles{display:grid;grid-template-columns:1fr 1fr;gap:11px;padding:20px 22px 22px;position:relative;z-index:1}
.srv-tile{display:flex;align-items:center;gap:11px;background:rgba(0,0,0,.14);border:1px solid var(--card-b);border-radius:13px;padding:12px 14px;transition:.18s}
[data-theme="light"] .srv-tile{background:rgba(37,99,235,.03)}
.srv-tile:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.srv-tile-icon{width:34px;height:34px;border-radius:10px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.srv-tile-text{min-width:0}
.srv-tile-label{font-size:9.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:3px}
.srv-tile-val{font-size:12px;font-weight:700;color:var(--t1);word-break:break-word}
.pw-panel{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 60%);border:1px solid var(--card-b);border-radius:22px;overflow:hidden;box-shadow:var(--shadow);position:relative}
.pw-panel::before{content:'';position:absolute;top:-60px;right:-60px;width:200px;height:200px;background:radial-gradient(circle,var(--purple-bg),transparent 70%);pointer-events:none}
.pw-hero{display:flex;align-items:center;gap:14px;padding:22px 24px 18px;position:relative;z-index:1}
.pw-hero-icon{width:50px;height:50px;border-radius:14px;background:linear-gradient(135deg,var(--purple),#6D48D6);display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;flex-shrink:0;box-shadow:0 6px 18px rgba(139,92,246,.35)}
.pw-hero-text{flex:1;min-width:0}
.pw-hero-title{font-size:15px;font-weight:800;color:var(--t1)}
.pw-hero-sub{font-size:10.5px;color:var(--t3);margin-top:3px}
.pw-body{padding:2px 24px 22px;position:relative;z-index:1}
.pw-field{position:relative;margin-bottom:13px}
.pw-field label{display:block;font-size:10px;font-weight:700;color:var(--t2);text-transform:uppercase;letter-spacing:.06em;margin-bottom:7px}
.pw-input{width:100%;padding:11px 42px 11px 14px;border-radius:11px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.15s}
[data-theme="light"] .pw-input{background:#fff}
.pw-input:focus{border-color:rgba(139,92,246,.5);box-shadow:0 0 0 3px rgba(139,92,246,.1)}
.pw-eye{position:absolute;left:12px;top:34px;background:none;border:none;color:var(--t3);cursor:pointer;font-size:16px;padding:4px;display:flex}
.pw-eye:hover{color:var(--purple)}
.pw-strength{height:4px;border-radius:3px;background:var(--accent-d);margin-top:8px;overflow:hidden;display:flex;gap:3px}
.pw-strength-seg{flex:1;height:100%;border-radius:3px;background:rgba(100,116,139,.2);transition:.25s}
.pw-strength-label{font-size:9.5px;color:var(--t3);margin-top:5px;display:flex;align-items:center;gap:5px}
.pw-reqs{display:flex;flex-wrap:wrap;gap:6px;margin-top:11px;margin-bottom:16px}
.pw-req{font-size:9.5px;padding:4px 10px;border-radius:7px;background:var(--accent-d);color:var(--t3);font-weight:600;display:flex;align-items:center;gap:4px;transition:.18s}
.pw-req.met{background:var(--green-bg);color:var(--green-t)}
.pw-submit{width:100%;justify-content:center;background:linear-gradient(135deg,var(--purple),#6D48D6);color:#fff;border:none;border-radius:12px;padding:12px;font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:8px;box-shadow:0 6px 18px rgba(139,92,246,.32);transition:.18s}
.pw-submit:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(139,92,246,.42)}
.pw-submit:active{transform:translateY(0) scale(.98)}
.conn-hero{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}
.conn-hero-tile{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:16px 18px;position:relative;overflow:hidden;transition:.2s}
.conn-hero-tile:hover{border-color:var(--card-bh);transform:translateY(-2px);box-shadow:var(--shadow)}
.conn-hero-tile::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--green),transparent)}
.conn-hero-icon{width:32px;height:32px;border-radius:9px;background:var(--green-bg);color:var(--green-t);display:flex;align-items:center;justify-content:center;font-size:15px;margin-bottom:10px}
.conn-hero-tile:nth-child(2) .conn-hero-icon{background:var(--accent-d);color:var(--accent)}
.conn-hero-tile:nth-child(3) .conn-hero-icon{background:var(--purple-bg);color:var(--purple)}
.conn-hero-tile:nth-child(4) .conn-hero-icon{background:var(--amber-bg);color:var(--amber)}
.conn-hero-label{font-size:9.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.conn-hero-val{font-size:21px;font-weight:800;color:var(--t1);line-height:1;letter-spacing:-.02em}
.conn-hero-unit{font-size:11px;color:var(--t3);font-weight:500}
.conn-toolbar{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.conn-toolbar-title{font-size:12px;font-weight:800;color:var(--t2);display:flex;align-items:center;gap:7px;text-transform:uppercase;letter-spacing:.06em}
.conn-toolbar-title i{color:var(--green);font-size:15px}
.conn-live-badge{display:flex;align-items:center;gap:6px;font-size:10.5px;font-weight:700;color:var(--green-t);background:var(--green-bg);padding:5px 12px;border-radius:20px;border:1px solid rgba(16,185,129,.2)}
.conn-live-dot{width:6px;height:6px;border-radius:50%;background:var(--green);animation:pulse 1.6s infinite}
.conn-grid-v2{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.conn-card-v2{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:0;overflow:hidden;transition:all .22s cubic-bezier(.4,0,.2,1);position:relative}
.conn-card-v2:hover{border-color:var(--card-bh);transform:translateY(-3px);box-shadow:0 14px 32px rgba(0,0,0,.22)}
.conn-card-v2-glow{position:absolute;top:-40px;left:-40px;width:140px;height:140px;background:radial-gradient(circle,rgba(16,185,129,.1),transparent 70%);pointer-events:none}
.conn-card-v2-top{display:flex;align-items:center;gap:12px;padding:16px 17px 13px;position:relative;z-index:1}
.conn-avatar{width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,var(--green),#0D9668);display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;flex-shrink:0;position:relative;box-shadow:0 4px 14px rgba(16,185,129,.3)}
.conn-avatar::after{content:'';position:absolute;inset:-4px;border-radius:16px;border:1.5px solid var(--green);opacity:.4;animation:breathe2 2.4s ease-in-out infinite}
@keyframes breathe2{0%,100%{transform:scale(1);opacity:.4}50%{transform:scale(1.12);opacity:0}}
.conn-card-v2-id{flex:1;min-width:0}
.conn-ip-v2{font-family:ui-monospace,monospace;font-size:14px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:6px}
.conn-ip-copy{background:none;border:none;color:var(--t3);cursor:pointer;font-size:12px;padding:2px;display:flex;transition:.15s}
.conn-ip-copy:hover{color:var(--accent)}
.conn-label-v2{font-size:10.5px;color:var(--t3);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.conn-status-pill{font-size:9px;font-weight:800;padding:4px 9px;border-radius:20px;background:var(--green-bg);color:var(--green-t);display:flex;align-items:center;gap:4px;white-space:nowrap;flex-shrink:0}
.conn-card-v2-divider{height:1px;background:linear-gradient(90deg,transparent,var(--card-b) 15%,var(--card-b) 85%,transparent);margin:0 17px}
.conn-card-v2-body{padding:14px 17px 16px}
.conn-proto-row{margin-bottom:12px}
.conn-stat-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}
.conn-stat-box{display:flex;align-items:center;gap:8px}
.conn-stat-icon{width:26px;height:26px;border-radius:8px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0}
.conn-stat-icon.time{background:var(--purple-bg);color:var(--purple)}
.conn-stat-text-label{font-size:8.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.conn-stat-text-val{font-size:11.5px;font-weight:700;color:var(--t1);margin-top:1px}
.conn-duration-track{height:5px;border-radius:4px;background:var(--accent-d);overflow:hidden;position:relative}
.conn-duration-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--green),#3FD79C);position:relative;overflow:hidden}
.conn-duration-fill::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent);width:40%;animation:shimmer 1.8s linear infinite}
@keyframes shimmer{0%{transform:translateX(-120%)}100%{transform:translateX(280%)}}
.conn-empty-v2{text-align:center;padding:70px 20px;background:var(--card);border:1px dashed var(--card-b);border-radius:20px}
.conn-empty-v2-icon{width:64px;height:64px;border-radius:18px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;font-size:28px;color:var(--t3);margin:0 auto 16px}
.conn-empty-v2-title{font-size:13.5px;font-weight:700;color:var(--t2);margin-bottom:5px}
.conn-empty-v2-sub{font-size:11px;color:var(--t3)}
@media(max-width:760px){.conn-hero{grid-template-columns:1fr 1fr}}
@media(max-width:500px){.conn-grid-v2{grid-template-columns:1fr}}
@media(max-width:560px){.srv-tiles{grid-template-columns:1fr}}
.cl.amber i{color:var(--amber)}
.sub-box{background:rgba(139,92,246,.07);border:1px solid rgba(139,92,246,.2);border-radius:10px;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:11px}
.sub-url{font-family:ui-monospace,monospace;font-size:10.5px;color:#A78BFA;word-break:break-all;flex:1}
.spbar{height:4px;border-radius:3px;background:var(--accent-d);margin-top:5px;overflow:hidden}
.spfill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width 1s}
.empty{text-align:center;padding:50px 20px;color:var(--t3)}
.empty i{font-size:40px;opacity:.3;margin-bottom:12px;display:block}
.empty p{font-size:12.5px;margin-top:4px}
.subs-toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.subs-search{flex:1;min-width:200px;position:relative}
.subs-search input{width:100%;padding:11px 40px 11px 15px;border-radius:12px;border:1px solid var(--card-b);background:var(--card);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.15s}
.subs-search input:focus{border-color:rgba(139,92,246,.5);box-shadow:0 0 0 3px rgba(139,92,246,.1)}
.subs-search i{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:15px}
.sub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px;margin-bottom:18px}
.sub-card{background:var(--card);border:1px solid var(--card-b);border-radius:20px;padding:0;overflow:hidden;transition:all .25s cubic-bezier(.4,0,.2,1);position:relative}
.sub-card:hover{border-color:var(--card-bh);transform:translateY(-4px);box-shadow:0 16px 36px rgba(0,0,0,.24)}
.sub-card-locked{border-color:rgba(239,68,68,.4);opacity:.86}
.sub-card-locked-banner{background:rgba(239,68,68,.12);color:var(--red-t,#FCA5A5);font-size:11px;font-weight:700;padding:8px 14px;display:flex;align-items:center;gap:6px}
.sub-card-perms{display:flex;flex-direction:column;gap:6px;margin-top:12px;padding-top:12px;border-top:1px dashed var(--card-b)}
.perm-toggle{display:flex;align-items:center;gap:6px;font-size:10.5px;color:var(--t2);font-weight:600;cursor:pointer;user-select:none}
.perm-toggle input{width:14px;height:14px;accent-color:#8b5cf6;cursor:pointer}
.switch{position:relative;display:inline-block;width:42px;height:24px;flex-shrink:0}
.switch input{opacity:0;width:0;height:0}
.switch .slider{position:absolute;cursor:pointer;inset:0;background:var(--card-b);border-radius:24px;transition:.2s}
.switch .slider:before{position:absolute;content:"";height:18px;width:18px;left:3px;bottom:3px;background:#fff;border-radius:50%;transition:.2s}
.switch input:checked+.slider{background:var(--accent)}
.switch input:checked+.slider:before{transform:translateX(18px)}
.sub-card-top{background:linear-gradient(155deg,var(--purple-bg) 0%,transparent 65%);padding:20px 20px 16px;position:relative}
.sub-card-top::before{content:'';position:absolute;top:-30px;left:-30px;width:130px;height:130px;background:radial-gradient(circle,rgba(139,92,246,.14),transparent 70%);pointer-events:none}
.sub-card-head-v2{display:flex;align-items:flex-start;gap:13px;position:relative;z-index:1}
.sub-card-icon{width:46px;height:46px;border-radius:14px;background:linear-gradient(135deg,var(--purple),#6D48D6);display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;flex-shrink:0;box-shadow:0 6px 16px rgba(139,92,246,.35)}
.sub-card-titles{flex:1;min-width:0}
.sub-card-name-v2{font-size:15.5px;font-weight:800;color:var(--t1);letter-spacing:-.01em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sub-card-desc-v2{font-size:11px;color:var(--t3);margin-top:3px;line-height:1.6;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.sub-card-lock-badge{flex-shrink:0;width:26px;height:26px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:12px}
.sub-card-lock-badge.locked{background:var(--amber-bg);color:var(--amber-t)}
.sub-card-lock-badge.open{background:var(--green-bg);color:var(--green-t)}
.sub-card-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:0;position:relative;z-index:1;margin-top:16px;background:rgba(0,0,0,.14);border:1px solid var(--card-b);border-radius:13px;overflow:hidden}
[data-theme="light"] .sub-card-stats{background:rgba(124,58,237,.03)}
.sub-card-stat{padding:11px 8px;text-align:center;border-left:1px solid var(--card-b)}
.sub-card-stat:last-child{border-left:none}
.sub-card-stat-val{font-size:15px;font-weight:800;color:var(--t1);line-height:1.2}
.sub-card-stat-label{font-size:8.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-top:4px}
.sub-card-url-row{margin:14px 20px 0;background:rgba(139,92,246,.08);border:1px dashed rgba(139,92,246,.25);border-radius:11px;padding:9px 12px;display:flex;align-items:center;gap:8px}
.sub-card-url-text{font-family:ui-monospace,monospace;font-size:9.5px;color:#A78BFA;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sub-card-url-copy{background:none;border:none;color:var(--purple);cursor:pointer;font-size:13px;padding:3px;display:flex;flex-shrink:0;transition:.15s}
.sub-card-url-copy:hover{color:#A78BFA;transform:scale(1.1)}
.sub-card-bottom{padding:14px 20px 18px;display:flex;gap:7px;flex-wrap:wrap}
.sub-card-bottom .btn{flex:1;justify-content:center;min-width:fit-content}
.subs-empty-v2{text-align:center;padding:70px 20px;background:var(--card);border:1px dashed var(--card-b);border-radius:20px;grid-column:1/-1}
.subs-empty-v2-icon{width:64px;height:64px;border-radius:18px;background:var(--purple-bg);display:flex;align-items:center;justify-content:center;font-size:28px;color:var(--purple);margin:0 auto 16px}
.subs-empty-v2-title{font-size:13.5px;font-weight:700;color:var(--t2);margin-bottom:5px}
.subs-empty-v2-sub{font-size:11px;color:var(--t3)}
.modal-v2{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:0;max-width:430px;width:calc(100% - 32px);max-height:92vh;overflow-y:auto;position:relative;animation:fi .2s ease;box-shadow:0 24px 70px rgba(0,0,0,.5)}
.modal-v2-head{background:linear-gradient(155deg,rgba(139,92,246,.14) 0%,transparent 65%);padding:18px 22px 14px;position:relative;overflow:hidden}
.modal-v2-head::before{content:'';position:absolute;top:-50px;left:-50px;width:160px;height:160px;background:radial-gradient(circle,rgba(139,92,246,.2),transparent 70%);pointer-events:none}
.modal-v2-close{position:absolute;top:14px;left:14px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:9px;font-size:15px;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:2;transition:.15s}
.modal-v2-close:hover{background:var(--red-bg);color:var(--red-t);border-color:rgba(239,68,68,.25)}
.modal-v2-icon{width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,var(--purple),#6D48D6);display:flex;align-items:center;justify-content:center;color:#fff;font-size:19px;margin-bottom:10px;position:relative;z-index:1;box-shadow:0 8px 18px rgba(139,92,246,.4)}
.modal-v2-title{font-size:15.5px;font-weight:800;color:var(--t1);position:relative;z-index:1;letter-spacing:-.01em}
.modal-v2-sub{font-size:10.5px;color:var(--t3);margin-top:3px;position:relative;z-index:1;line-height:1.6}
.modal-v2-body{padding:16px 22px 20px;border-top:1px solid var(--card-b)}
.modal-v2-field{margin-bottom:11px}
.modal-v2-field label{display:flex;align-items:center;gap:5px;font-size:9.5px;font-weight:800;color:var(--t2);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
.modal-v2-field label i{color:var(--purple);font-size:13px}
.modal-v2-input-wrap{position:relative}
.modal-v2-input-wrap>i{position:absolute;right:13px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:14px;pointer-events:none;transition:.15s;z-index:1}
.modal-v2-input{width:100%;padding:9px 38px 9px 13px;border-radius:11px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.18s}
[data-theme="light"] .modal-v2-input{background:rgba(124,58,237,.04)}
.modal-v2-input::placeholder{color:var(--t3)}
.modal-v2-input:focus{border-color:rgba(139,92,246,.55);box-shadow:0 0 0 3px rgba(139,92,246,.12);background:rgba(0,0,0,.28)}
[data-theme="light"] .modal-v2-input:focus{background:#fff}
.modal-v2-input:focus~i{color:var(--purple)}
.modal-v2-hint{background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.18);border-radius:11px;padding:9px 12px;font-size:10px;color:var(--t2);display:flex;gap:7px;align-items:flex-start;line-height:1.6}
.modal-v2-hint i{font-size:14px;color:var(--accent);margin-top:1px;flex-shrink:0}
.modal-v2-footer{display:flex;gap:8px;margin-top:15px}
.modal-v2-btn-cancel{flex:.75;justify-content:center;padding:10px;border-radius:11px;background:transparent;border:1px solid var(--card-b);color:var(--t2);font-family:inherit;font-size:12px;font-weight:700;cursor:pointer;transition:.15s;display:flex;align-items:center}
.modal-v2-btn-cancel:hover{background:var(--accent-d);color:var(--t1)}
.modal-v2-btn-submit{flex:1;justify-content:center;padding:10px;border-radius:11px;background:linear-gradient(135deg,var(--purple),#6D48D6);color:#fff;border:none;font-family:inherit;font-size:12px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:6px;box-shadow:0 6px 18px rgba(139,92,246,.4);transition:.18s}
.modal-v2-btn-submit:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(139,92,246,.5)}
.modal-v2-btn-submit:active{transform:translateY(0) scale(.98)}
.lmodal-head{background:linear-gradient(155deg,var(--accent-d) 0%,transparent 70%);padding:22px 24px 18px;position:relative;border-bottom:1px solid var(--card-b)}
.lmodal-icon-row{display:flex;align-items:center;gap:12px;position:relative;z-index:1}
.lmodal-icon{width:44px;height:44px;border-radius:13px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:19px;flex-shrink:0;box-shadow:0 6px 16px rgba(59,130,246,.35)}
.lmodal-title-v2{font-size:14.5px;font-weight:800;color:var(--t1)}
.lmodal-sub-v2{font-size:10.5px;color:var(--t3);margin-top:2px}
.lmodal-search{margin-top:14px;position:relative}
.lmodal-search input{width:100%;padding:10px 38px 10px 13px;border-radius:11px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:12px;outline:none}
[data-theme="light"] .lmodal-search input{background:#fff}
.lmodal-search input:focus{border-color:rgba(59,130,246,.5);box-shadow:0 0 0 3px rgba(59,130,246,.1)}
.lmodal-search i{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:14px}
.lmodal-quickbar{display:flex;gap:8px;margin-top:11px;position:relative;z-index:1}
.lmodal-qbtn{font-size:10px;font-weight:700;padding:5px 11px;border-radius:8px;background:var(--accent-d);color:var(--accent2);border:1px solid var(--card-b);cursor:pointer;transition:.15s;font-family:inherit}
.lmodal-qbtn:hover{background:rgba(59,130,246,.2)}
.lmodal-count{margin-right:auto;font-size:10.5px;color:var(--t3);display:flex;align-items:center}
.lmodal-list{padding:10px 14px;max-height:360px;overflow-y:auto}
.lrow-v2{display:flex;align-items:center;gap:11px;padding:11px 12px;border-radius:13px;cursor:pointer;transition:.15s;margin-bottom:4px;border:1px solid transparent}
.lrow-v2:hover{background:var(--accent-d)}
.lrow-v2.checked{background:rgba(59,130,246,.1);border-color:rgba(59,130,246,.25)}
.lrow-v2-check{width:20px;height:20px;border-radius:7px;border:2px solid var(--card-b);flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:.15s;background:rgba(0,0,0,.14)}
.lrow-v2.checked .lrow-v2-check{background:var(--accent);border-color:var(--accent)}
.lrow-v2-check i{font-size:12px;color:#fff;opacity:0;transform:scale(.5);transition:.15s}
.lrow-v2.checked .lrow-v2-check i{opacity:1;transform:scale(1)}
.lrow-v2-avatar{width:34px;height:34px;border-radius:10px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.lrow-v2.checked .lrow-v2-avatar{background:var(--accent);color:#fff}
.lrow-v2-info{flex:1;min-width:0}
.lrow-v2-name{font-size:12.5px;font-weight:700;color:var(--t1);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lrow-v2-meta{font-size:9.5px;color:var(--t3);margin-top:2px;display:flex;align-items:center;gap:6px}
.lrow-v2-status{font-size:9px;font-weight:800;padding:3px 9px;border-radius:20px;flex-shrink:0;white-space:nowrap}
.lrow-v2-status.on{background:var(--green-bg);color:var(--green-t)}
.lrow-v2-status.off{background:var(--red-bg);color:var(--red-t)}
.lmodal-footer{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:16px 24px;border-top:1px solid var(--card-b)}
.lmodal-footer-info{font-size:10.5px;color:var(--t3);display:flex;align-items:center;gap:6px}
.lmodal-footer-info i{color:var(--accent)}
.lmodal-footer-btns{display:flex;gap:8px}
@media(max-width:500px){.sub-grid{grid-template-columns:1fr}.sub-card-stats{grid-template-columns:repeat(3,1fr)}}
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(4px)}
.modal-bg.open{display:flex}
.modal{background:var(--card);border:1px solid var(--card-b);border-radius:20px;padding:28px 26px;max-width:520px;width:calc(100% - 32px);max-height:90vh;overflow-y:auto;position:relative;animation:fi .2s ease}
.modal-close{position:absolute;top:14px;left:14px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;display:flex;align-items:center;justify-content:center;cursor:pointer;border:none}
.modal-title{font-size:16px;font-weight:700;color:var(--t1);margin-bottom:18px;display:flex;align-items:center;gap:8px}
.modal-title i{color:var(--accent)}
.lrow{display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid rgba(59,130,246,.05)}
.lrow:last-child{border-bottom:none}
.lrow-check{width:16px;height:16px;border-radius:4px;cursor:pointer;accent-color:var(--accent)}
.lrow-label{flex:1;font-size:12px;color:var(--t1)}
.lrow-badge{font-size:9px;padding:2px 7px;border-radius:5px;background:var(--green-bg);color:var(--green-t);font-weight:700}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:10px;padding:10px 18px;font-size:12.5px;opacity:0;transition:all .25s;z-index:999;pointer-events:none;display:flex;align-items:center;gap:8px;box-shadow:var(--shadow);white-space:nowrap}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,.3);background:var(--green-bg);color:var(--green-t)}
.toast.err{border-color:rgba(239,68,68,.3);background:var(--red-bg);color:var(--red-t)}
.dash-footer{border-top:1px solid var(--card-b);margin-top:14px;padding-top:14px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.df-text{font-size:10px;color:var(--t3)}
.df-link{font-size:11.5px;color:var(--accent2);display:flex;align-items:center;gap:5px;font-weight:600}
.cfg-grid{display:flex;flex-direction:column;gap:10px}
.cfg-card{background:var(--card);border:1px solid var(--card-b);border-radius:14px;padding:0;transition:all .2s cubic-bezier(.4,0,.2,1);position:relative;overflow:hidden}
.cfg-card:hover{border-color:var(--card-bh);box-shadow:0 6px 24px rgba(0,0,0,.18)}
.cfg-card.is-off{opacity:.6}
.cfg-card.is-exp{opacity:.78}
.cfg-row{display:flex;align-items:center;gap:16px;padding:14px 18px}
.cfg-status-dot{width:9px;height:9px;border-radius:50%;background:var(--green);flex-shrink:0;box-shadow:0 0 0 3px var(--green-bg)}
.cfg-card.is-off .cfg-status-dot{background:var(--red);box-shadow:0 0 0 3px var(--red-bg)}
.cfg-card.is-exp .cfg-status-dot{background:var(--amber);box-shadow:0 0 0 3px var(--amber-bg)}
.cfg-identity{display:flex;flex-direction:column;gap:3px;min-width:150px;flex-shrink:0}
.cfg-label{font-size:13.5px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:7px}
.cfg-sub-meta{display:flex;align-items:center;gap:8px;font-size:10px;color:var(--t3)}
.cfg-uuid-mini{font-family:ui-monospace,monospace;font-size:9.5px;color:var(--accent2);background:var(--accent-d);padding:2px 7px;border-radius:5px;cursor:pointer;transition:.15s}
.cfg-uuid-mini:hover{background:rgba(59,130,246,.2)}
.cfg-divider-v{width:1px;align-self:stretch;background:var(--card-b);flex-shrink:0}
.cfg-usage-col{flex:1;min-width:160px;display:flex;flex-direction:column;gap:5px}
.ubar{height:5px;border-radius:4px;background:rgba(59,130,246,0.1);overflow:hidden}
.ubar-f{height:100%;border-radius:4px;transition:width .4s ease}
.utxt{font-size:10px;color:var(--t3);display:flex;justify-content:space-between}
.cfg-exp-col{flex-shrink:0;min-width:110px}
.cfg-badges-col{display:flex;flex-direction:column;gap:5px;flex-shrink:0;align-items:flex-end}
.cfg-actions{display:flex;gap:5px;flex-shrink:0}
.proto-chip{font-size:9px;padding:3px 8px;border-radius:6px;font-weight:700;white-space:nowrap}
.pc-ws{background:var(--accent-d);color:var(--accent2)}
.pc-xhttp{background:var(--purple-bg);color:#A78BFA}
.pc-ultra{background:var(--green-bg);color:var(--green-t)}
.pc-trojan{background:rgba(239,68,68,.14);color:#f87171}
.cfg-sub-tag{font-size:9.5px;color:var(--t3);display:flex;align-items:center;gap:4px;white-space:nowrap}
.cfg-sub-tag i{color:var(--purple);font-size:11px}
.tog{width:19px;height:30px;border-radius:19px;background:rgba(100,116,139,0.25);position:relative;cursor:pointer;transition:.2s;flex-shrink:0;border:none}
.tog::after{content:'';position:absolute;width:13px;height:13px;border-radius:50%;background:#fff;left:3px;top:3px;transition:.2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.tog.on::after{top:14px}
.tog.on{background:var(--green)}
@media(max-width:880px){
  .cfg-row{flex-wrap:wrap}
  .cfg-divider-v{display:none}
  .cfg-usage-col{min-width:100%;order:5}
}
@media(max-width:768px){
  .cfg-grid{display:grid;grid-template-columns:1fr;gap:13px}
  .cfg-card{border-radius:16px}
  .cfg-row{flex-direction:column;align-items:stretch;gap:12px;padding:16px}
  .cfg-row-top{display:flex;align-items:center;justify-content:space-between;gap:10px}
  .cfg-identity{min-width:0;flex:1}
  .cfg-usage-col{min-width:0}
  .cfg-exp-col{min-width:0}
  .cfg-badges-col{flex-direction:row;align-items:center;flex-wrap:wrap}
  .cfg-actions{flex-wrap:wrap;border-top:1px solid var(--card-b);padding-top:10px;margin-top:2px;width:100%}
}
.conn-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.conn-card{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:15px 17px;transition:.2s;position:relative;overflow:hidden}
.conn-card:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.conn-card::before{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--green)}
.conn-ip-row{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.conn-ip-icon{width:32px;height:32px;border-radius:9px;background:var(--green-bg);color:var(--green-t);display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0}
.conn-ip{font-family:ui-monospace,monospace;font-size:13px;font-weight:700;color:var(--t1)}
.conn-label{font-size:10.5px;color:var(--t3);margin-top:1px}
.conn-meta{display:flex;justify-content:space-between;align-items:center;font-size:10px;color:var(--t3);padding-top:10px;border-top:1px solid var(--card-b)}
.log-timeline{display:flex;flex-direction:column}
.log-item{display:flex;gap:12px;padding:11px 0;border-bottom:1px solid rgba(59,130,246,.05);position:relative}
.log-item:last-child{border-bottom:none}
.log-ic{width:30px;height:30px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.log-ic.ok{background:var(--green-bg);color:var(--green-t)}
.log-ic.err{background:var(--red-bg);color:var(--red-t)}
.log-ic.warn{background:var(--amber-bg);color:var(--amber-t)}
.log-ic.info{background:var(--accent-d);color:var(--accent2)}
.log-body{flex:1;min-width:0}
.log-msg{font-size:12.5px;color:var(--t1);line-height:1.6}
.log-time{font-size:9.5px;color:var(--t3);margin-top:2px;display:flex;align-items:center;gap:5px}
.log-kind{font-size:8.5px;padding:1px 7px;border-radius:10px;background:var(--accent-d);color:var(--accent2);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.erow{padding:9px 0;border-bottom:1px solid rgba(59,130,246,.05)}
.erow:last-child{border-bottom:none}
.etime{color:var(--t3);font-size:9.5px;margin-bottom:3px;display:flex;align-items:center;gap:4px}
.emsg{color:var(--red-t);font-family:ui-monospace,monospace;background:var(--red-bg);padding:6px 9px;border-radius:6px;word-break:break-all;font-size:10.5px}
@media(max-width:1050px){
  .sidebar{transform:translateX(100%)}
  .sidebar.open{transform:translateX(0);box-shadow:-10px 0 40px rgba(0,0,0,.4)}
  .sb-close{display:flex}
  .main{margin-right:0;padding-top:70px}
  .mob-top{display:flex}
  .metrics{grid-template-columns:1fr 1fr}
  .g2,.g3{grid-template-columns:1fr}
}
@media(max-width:500px){
  .metrics{grid-template-columns:1fr}
  .main{padding:62px 12px 50px}
  .sub-grid,.cfg-grid,.conn-grid{grid-template-columns:1fr}
}
.qr-modal-v2{display:none;position:fixed;inset:0;background:rgba(0,0,0,.72);z-index:900;align-items:center;justify-content:center;backdrop-filter:blur(6px);padding:20px}
.qr-modal-v2.open{display:flex}
.qr-box-v2{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:22px;width:100%;max-width:340px;text-align:center}
.qr-box-v2 .qr-title{font-weight:800;font-size:15px;margin-bottom:12px}
.qr-box-v2 .qr-img-wrap{background:#fff;border-radius:14px;padding:10px;margin-bottom:12px}
.qr-box-v2 .qr-img-wrap img{width:100%;display:block;border-radius:6px}
.qr-proto-tabs{display:flex;gap:6px;margin-bottom:12px}
.qr-proto-tab{flex:1;padding:7px 4px;border-radius:9px;background:var(--bg2);border:1px solid var(--border);font-size:11px;font-weight:700;cursor:pointer;color:var(--text2)}
.qr-proto-tab.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.qr-usage-line{font-size:12px;color:var(--text2);margin-bottom:14px;display:flex;align-items:center;justify-content:center;gap:6px}
.qr-box-v2 .btnrow{display:flex;gap:8px}
</style>
</head>
<body>
<div class="toast" id="toast"></div>
<div class="qr-modal-v2" id="qr-modal-v2" onclick="this.classList.remove('open')">
  <div class="qr-box-v2" onclick="event.stopPropagation()">
    <div class="qr-title" id="qrv2-label">QR Code</div>
    <div class="qr-proto-tabs" id="qrv2-tabs"></div>
    <div class="qr-img-wrap"><img id="qrv2-img" src="" alt="QR"></div>
    <div class="qr-usage-line" id="qrv2-usage"></div>
    <div class="btnrow">
      <button class="btn btn-g" style="flex:1;justify-content:center" onclick="copyCurrentQrLink()"><i class="ti ti-copy"></i> کپی این پروتکل</button>
      <button class="btn btn-g" style="flex:1;justify-content:center" onclick="document.getElementById('qr-modal-v2').classList.remove('open')"><i class="ti ti-x"></i> بستن</button>
    </div>
  </div>
</div>
<div class="modal-bg" id="modal-links">
  <div class="modal-v2" style="max-width:500px">
    <div class="lmodal-head">
      <button class="modal-v2-close" onclick="closeModal('modal-links')"><i class="ti ti-x"></i></button>
      <div class="lmodal-icon-row">
        <div class="lmodal-icon"><i class="ti ti-link-plus"></i></div>
        <div>
          <div class="lmodal-title-v2">مدیریت کانفیگ‌های <span id="modal-sub-name" style="color:var(--accent2)">—</span></div>
          <div class="lmodal-sub-v2">کانفیگ‌هایی که می‌خواهید در این گروه باشند را انتخاب کنید</div>
        </div>
      </div>
      <div class="lmodal-search">
        <i class="ti ti-search"></i>
        <input type="text" id="lmodal-search-inp" placeholder="جستجوی کانفیگ..." oninput="filterLmodal(this.value)">
      </div>
      <div class="lmodal-quickbar">
        <button class="lmodal-qbtn" onclick="lmodalSelectAll(true)"><i class="ti ti-checks"></i> انتخاب همه</button>
        <button class="lmodal-qbtn" onclick="lmodalSelectAll(false)"><i class="ti ti-x"></i> لغو همه</button>
        <span class="lmodal-count" id="lmodal-count">۰ انتخاب شده</span>
      </div>
    </div>
    <div class="lmodal-list" id="modal-links-body">در حال بارگذاری...</div>
    <div class="lmodal-footer">
      <div class="lmodal-footer-info"><i class="ti ti-info-circle"></i> تغییرات بلافاصله اعمال می‌شود</div>
      <div class="lmodal-footer-btns">
        <button class="btn btn-o" onclick="closeModal('modal-links')">بستن</button>
        <button class="btn btn-p" id="modal-save-btn" onclick="saveSubLinks()"><i class="ti ti-check"></i> ذخیره</button>
      </div>
    </div>
  </div>
</div>
<div class="modal-bg" id="modal-create-sub">
  <div class="modal-v2">
    <div class="modal-v2-head">
      <button class="modal-v2-close" onclick="closeModal('modal-create-sub')"><i class="ti ti-x"></i></button>
      <div class="modal-v2-icon"><i class="ti ti-folder-plus"></i></div>
      <div class="modal-v2-title">ساخت گروه جدید</div>
      <div class="modal-v2-sub">یک صفحه پابلیک مجزا برای مدیریت کانفیگ‌ها بسازید</div>
    </div>
    <div class="modal-v2-body">
      <div class="modal-v2-field">
        <label><i class="ti ti-tag"></i> نام گروه</label>
        <input class="modal-v2-input" id="ns-name" placeholder="مثلاً: کانال تلگرام">
      </div>
      <div class="modal-v2-field">
        <label><i class="ti ti-align-left"></i> توضیحات (اختیاری)</label>
        <input class="modal-v2-input" id="ns-desc" placeholder="توضیح کوتاه درباره این گروه">
      </div>
      <div class="modal-v2-field" style="margin-bottom:0">
        <label><i class="ti ti-lock"></i> رمز صفحه پابلیک (اختیاری)</label>
        <input class="modal-v2-input" id="ns-pw" type="password" placeholder="خالی بگذارید = بدون رمز">
      </div>
      <div class="modal-v2-field" style="margin-top:14px;margin-bottom:0">
        <label><i class="ti ti-chart-pie"></i> سقف حجم قابل‌تقسیم (اختیاری)</label>
        <div style="display:flex;gap:8px">
          <input class="modal-v2-input" id="ns-pool-val" type="number" min="0" placeholder="مثلاً 10" style="flex:1">
          <select class="modal-v2-input" id="ns-pool-unit" style="flex:.6">
            <option value="GB">GB</option><option value="MB">MB</option>
          </select>
        </div>
        <div class="cl" style="margin-top:8px"><i class="ti ti-info-circle"></i><span>اگر پر شود، صاحب این ساب می‌تواند خودش از داخل صفحه‌ی عمومی‌اش بخشی از این سقف را جدا کند و به‌عنوان یک ساب مستقل و بدون برند به کس دیگری بدهد.</span></div>
      </div>
      <div class="modal-v2-field" style="margin-top:14px;margin-bottom:0">
        <label><i class="ti ti-shield-lock"></i> کنترل کانفیگ‌های هدیه‌ای مشتری</label>
        <div style="display:flex;flex-direction:column;gap:8px;margin-top:4px">
          <label style="display:flex;align-items:center;gap:8px;font-size:12px;color:var(--t2);cursor:pointer;font-weight:600">
            <input type="checkbox" id="ns-can-delete" checked style="width:16px;height:16px;accent-color:var(--accent, #7c5cff)"> مشتری اجازه دارد کانفیگ‌های هدیه‌ای‌اش را حذف کند
          </label>
          <label style="display:flex;align-items:center;gap:8px;font-size:12px;color:var(--t2);cursor:pointer;font-weight:600">
            <input type="checkbox" id="ns-can-disable" checked style="width:16px;height:16px;accent-color:var(--accent, #7c5cff)"> مشتری اجازه دارد کانفیگ‌های هدیه‌ای‌اش را غیرفعال کند
          </label>
        </div>
        <div class="cl" style="margin-top:8px"><i class="ti ti-info-circle"></i><span>اگر خاموش کنید، فقط خودِ مدیر می‌تواند این کانفیگ‌ها را حذف/غیرفعال کند؛ بعداً هم از داخل کارت گروه قابل تغییر است.</span></div>
      </div>
      <div class="cl" style="margin-top:14px"><i class="ti ti-info-circle"></i><span>صفحه پابلیک این گروه با یک لینک منحصر‌به‌فرد در اینترنت در دسترس خواهد بود.</span></div>
      <div class="modal-v2-footer">
        <button class="btn btn-o" onclick="closeModal('modal-create-sub')" style="flex:.6">انصراف</button>
        <button class="btn btn-pur" onclick="createSub()"><i class="ti ti-folder-plus"></i> ساخت گروه</button>
      </div>
    </div>
  </div>
</div>
<div class="modal-bg" id="modal-edit-link">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-edit-link')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-edit"></i> ویرایش کانفیگ</div>
    <input type="hidden" id="el-uuid">
    <div class="fg" style="margin-bottom:13px"><label>عنوان</label><input class="fi" id="el-label" style="width:100%"></div>
    <div class="form-row" style="margin-bottom:13px">
      <div class="fg" style="flex:1"><label>سهمیه (0 = نامحدود)</label><input class="fi" id="el-val" type="number" min="0" step="0.1" style="width:100%"></div>
      <div class="fg"><label>واحد</label><select class="fs" id="el-unit"><option value="GB">GB</option><option value="MB">MB</option></select></div>
    </div>
    <div class="form-row" style="margin-bottom:13px">
      <div class="fg" style="flex:1"><label>انقضا از الان (0 = بدون تغییر)</label><input class="fi" id="el-exp" type="number" min="0" step="1" style="width:100%"></div>
      <div class="fg"><label>واحد</label><select class="fs" id="el-exp-unit"><option value="hours">ساعت</option><option value="days" selected>روز</option></select></div>
    </div>
    <div class="fg" style="margin-bottom:13px"><label>حداکثر تعداد دستگاه/IP هم‌زمان (0 = نامحدود)</label><input class="fi" id="el-devices" type="number" min="0" step="1" style="width:100%"></div>
    <div class="fg" style="margin-bottom:16px"><label>یادداشت</label><input class="fi" id="el-note" style="width:100%"></div>
    <div class="cl"><i class="ti ti-info-circle"></i><span>برای حفظ انقضای فعلی، فیلد انقضا را صفر بگذارید.</span></div>
    <div style="margin-top:16px;display:flex;gap:8px;justify-content:flex-end">
      <button class="btn btn-o" onclick="closeModal('modal-edit-link')">انصراف</button>
      <button class="btn btn-p" onclick="saveEditLink()"><i class="ti ti-check"></i> ذخیره تغییرات</button>
    </div>
  </div>
</div>
<div class="modal-bg" id="modal-daily-chart">
  <div class="modal" style="max-width:560px">
    <button class="modal-close" onclick="closeModal('modal-daily-chart')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-chart-histogram"></i> مصرف روزانه — <span id="dc-title"></span></div>
    <div style="height:260px;margin-top:10px"><canvas id="dc-canvas"></canvas></div>
  </div>
</div>
<div class="mob-top">
  <div class="ml">
    <div class="mob-logo"><img src="{{LOGO}}" alt="تیم آزادی"></div>
    <span class="mob-title">تیم آزادی Gateway</span>
  </div>
  <div class="mob-right">
    <button class="theme-mob" id="theme-mob-btn" onclick="toggleTheme()"><i class="ti ti-sun" id="theme-mob-icon"></i></button>
    <button class="menu-btn" id="open-sb"><i class="ti ti-menu-2"></i></button>
  </div>
</div>
<div class="overlay" id="overlay"></div>
<aside class="sidebar" id="sb">
  <button class="sb-close" id="close-sb"><i class="ti ti-x"></i></button>
  <div class="logo">
    <div class="logo-img"><img src="{{LOGO}}" alt="تیم آزادی"></div>
    <div><div class="logo-name">تیم آزادی</div><div class="logo-sub">تیم آزادی Gateway · v10.0</div></div>
  </div>
  <div class="nav-wrap">
    <div class="nav-sec">پنل</div>
    <div class="nav-it on" data-pg="overview"><i class="ti ti-layout-dashboard"></i> داشبورد</div>
    <div class="nav-it" data-pg="links"><i class="ti ti-link-plus"></i> کانفیگ‌ها <span class="nav-badge" id="links-nb">0</span></div>
    <div class="nav-it" data-pg="subgroups"><i class="ti ti-folders"></i> گروه‌های ساب <span class="nav-badge" id="subs-nb">0</span></div>
    <div class="nav-it" data-pg="subscriptions"><i class="ti ti-rss"></i> سابسکریپشن</div>
    <div class="nav-it" data-pg="traffic"><i class="ti ti-chart-area"></i> ترافیک</div>
    <div class="nav-it" data-pg="connections"><i class="ti ti-plug-connected"></i> اتصالات <span class="nav-badge" id="conns-nb">0</span></div>
    <div class="nav-sec">سیستم</div>
    <div class="nav-it" data-pg="security"><i class="ti ti-shield-lock"></i> امنیت</div>
    <div class="nav-it" data-pg="logs"><i class="ti ti-history"></i> لاگ فعالیت‌ها</div>
    <div class="nav-it" data-pg="errors"><i class="ti ti-alert-triangle"></i> خطاها</div>
    <div class="nav-it" data-pg="testws"><i class="ti ti-wifi"></i> تست WebSocket</div>
    <div class="nav-it" data-pg="settings"><i class="ti ti-settings"></i> تنظیمات</div>
  </div>
  <div class="sb-foot">
    <button class="theme-btn" onclick="toggleTheme()"><i class="ti ti-moon" id="theme-icon"></i> <span id="theme-label">تم روشن</span></button>
    <a class="tg-btn" href="https://t.me/TimAzadi" target="_blank" rel="noopener"><i class="ti ti-brand-telegram"></i> @TimAzadi</a>
    <button class="logout-btn" id="logout-btn"><i class="ti ti-logout"></i> خروج</button>
  </div>
</aside>
<main class="main">
<section class="pg on" id="pg-overview">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-layout-dashboard"></i> داشبورد</div><div class="tb-sub" id="last-upd">در حال بارگذاری...</div></div>
    <div class="tb-right">
      <span class="badge bg-green"><span class="dot dg pulse"></span> فعال</span>
      <span class="badge bg-blue" id="uptime-badge">—</span>
      <button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button>
    </div>
  </div>
  <div class="metrics">
    <div class="metric"><div class="m-icon"><i class="ti ti-plug-connected"></i></div><div class="m-label">اتصالات فعال</div><div class="m-val" id="m-conns">—</div><div class="m-sub"><span class="dot dg pulse"></span> WebSocket / XHTTP زنده</div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-transfer"></i></div><div class="m-label">کل ترافیک</div><div class="m-val" id="m-traffic">—<span class="m-unit">MB</span></div><div class="m-sub">از راه‌اندازی</div></div>
    <div class="metric suc"><div class="m-icon suc"><i class="ti ti-link"></i></div><div class="m-label">کانفیگ فعال</div><div class="m-val" id="m-alinks">—</div><div class="m-sub" id="m-lsub">از کل</div></div>
    <div class="metric pur"><div class="m-icon pur"><i class="ti ti-folders"></i></div><div class="m-label">گروه‌های ساب</div><div class="m-val" id="m-subs">—</div><div class="m-sub">فعال</div></div>
  </div>
  <div class="vless-box">
    <div class="vl-header">
      <div class="vl-title"><i class="ti ti-link"></i> لینک پیش‌فرض (بدون محدودیت)</div>
      <span class="badge bg-blue"><span class="dot db"></span> TLS 443 · WS</span>
    </div>
    <div class="vl-code" id="vless-main">در حال دریافت...</div>
    <div class="vl-actions">
      <button class="btn btn-p" onclick="cpText('vless-main')"><i class="ti ti-copy"></i> کپی</button>
      <button class="btn btn-g" onclick="qrFor('vless-main')"><i class="ti ti-qrcode"></i> QR</button>
      <button class="btn btn-o" onclick="navTo('links')"><i class="ti ti-link-plus"></i> کانفیگ محدود</button>
      <button class="btn btn-pur" onclick="navTo('subgroups')"><i class="ti ti-folders"></i> گروه‌های ساب</button>
    </div>
  </div>
  <div class="g3">
    <div class="card"><div class="card-title"><i class="ti ti-chart-area"></i> ترافیک ساعتی (MB)</div><div class="ch"><canvas id="ch1"></canvas></div></div>
    <div class="card"><div class="card-title"><i class="ti ti-chart-donut"></i> توزیع</div><div class="ch-sm"><canvas id="ch2"></canvas></div></div>
  </div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-activity"></i> وضعیت سرویس</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-shield-check"></i> UUID Auth</span><span class="sr-v" style="color:var(--green-t)">● فعال · سخت‌گیرانه</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-circle-check"></i> VLESS / WS Tunnel</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-bolt"></i> Siz10a XHTTP Ultra</span><span class="sr-v" style="color:var(--green-t)">● فعال · 3 mode</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-folders"></i> Sub Groups</span><span class="sr-v" style="color:var(--green-t)">● فعال v9</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-rss"></i> Subscription API</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-clock"></i> آپتایم</span><span class="sr-v" id="uptime-inline">—</span></div>
      <div class="sr" style="flex-direction:column;align-items:flex-start;gap:4px">
        <div style="width:100%;display:flex;justify-content:space-between"><span class="sr-k"><i class="ti ti-gauge"></i> بار نسبی</span><span class="sr-v" id="bw-pct">—%</span></div>
        <div class="spbar" style="width:100%"><div class="spfill" id="bw-bar" style="width:0%"></div></div>
      </div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-list"></i> خلاصه کانفیگ‌ها <span class="ml-auto badge bg-blue" id="lsummary-badge">۰</span></div>
      <div id="lsummary">—</div>
    </div>
  </div>
  <div class="dash-footer">
    <span class="df-text">تیم آزادی Gateway v10.0 · Railway · 2026</span>
    <a class="df-link" href="https://t.me/TimAzadi" target="_blank"><i class="ti ti-brand-telegram"></i> t.me/TimAzadi</a>
  </div>
</section>
<section class="pg" id="pg-links">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-link-plus"></i> کانفیگ‌ها</div><div class="tb-sub">ساخت و مدیریت کانفیگ با سهمیه، انقضا و گروه‌بندی</div></div>
    <div class="tb-right"><span class="badge bg-blue" id="links-pg-cnt">۰ کانفیگ</span></div>
  </div>
  <div class="create-panel">
    <div class="cp-head">
      <div class="cp-head-icon"><i class="ti ti-square-rounded-plus"></i></div>
      <div class="cp-head-text">
        <div class="cp-head-title">ساخت کانفیگ جدید</div>
        <div class="cp-head-sub">UUID تصادفی · سهمیه، انقضا و پروتکل رو انتخاب کن</div>
      </div>
    </div>
    <div class="cp-body">
      <div class="cp-row">
        <div class="cp-block">
          <div class="cp-block-label"><i class="ti ti-id-badge-2"></i> شناسه کانفیگ</div>
          <input class="cp-input-full" id="nl-label" placeholder="مثلاً: کاربر علی">
          <div class="cp-mini-row">
            <input class="cp-input-full" id="nl-note" placeholder="یادداشت (اختیاری)" style="flex:1">
            <select class="cp-input-full fs" id="nl-flag" style="flex:.5">
              <option value="🇺🇸" selected>🇺🇸 US</option>
              <option value="🇳🇱">🇳🇱 NL</option>
              <option value="🇩🇪">🇩🇪 DE</option>
              <option value="🇬🇧">🇬🇧 GB</option>
              <option value="🇫🇷">🇫🇷 FR</option>
              <option value="🇹🇷">🇹🇷 TR</option>
              <option value="🇸🇬">🇸🇬 SG</option>
              <option value="🇯🇵">🇯🇵 JP</option>
            </select>
          </div>
        </div>
        <div class="cp-block">
          <div class="cp-block-label"><i class="ti ti-folders"></i> گروه ساب و انقضا</div>
          <select class="cp-input-full fs" id="nl-sub"><option value="">— بدون گروه —</option></select>
          <div class="cp-mini-row">
            <input class="cp-input-full" id="nl-exp" type="number" min="0" step="1" placeholder="انقضا · 0 = نامحدود" style="flex:1">
            <select class="cp-input-full fs" id="nl-exp-unit" style="flex:.55"><option value="hours">ساعت</option><option value="days" selected>روز</option></select>
          </div>
          <div class="chip-row" id="exp-chips">
            <span class="chip" onclick="setExpiry(0,'days',this)">نامحدود</span>
            <span class="chip" onclick="setExpiry(6,'hours',this)">۶ ساعت</span>
            <span class="chip" onclick="setExpiry(24,'hours',this)">۲۴ ساعت</span>
            <span class="chip" onclick="setExpiry(7,'days',this)">۷ روز</span>
            <span class="chip active" onclick="setExpiry(30,'days',this)">۳۰ روز</span>
            <span class="chip" onclick="setExpiry(90,'days',this)">۹۰ روز</span>
          </div>
          <div class="cp-mini-row">
            <input class="cp-input-full" id="nl-devices" type="number" min="0" step="1" placeholder="حداکثر تعداد دستگاه/IP هم‌زمان · 0 = نامحدود">
          </div>
        </div>
      </div>
      <div class="cp-block mb16">
        <div class="cp-block-label"><i class="ti ti-gauge"></i> سهمیه ترافیک</div>
        <div class="cp-quota-inputs">
          <input class="cp-input-full" id="nl-val" type="number" min="0" step="0.1" placeholder="0 = نامحدود">
          <select class="cp-input-full fs" id="nl-unit"><option value="GB">GB</option><option value="MB" selected>MB</option></select>
        </div>
        <div class="chip-row" id="quota-chips">
          <span class="chip" onclick="setQuota(0,'GB',this)">نامحدود</span>
          <span class="chip" onclick="setQuota(500,'MB',this)">۵۰۰ MB</span>
          <span class="chip active" onclick="setQuota(1,'GB',this)">۱ GB</span>
          <span class="chip" onclick="setQuota(5,'GB',this)">۵ GB</span>
          <span class="chip" onclick="setQuota(10,'GB',this)">۱۰ GB</span>
          <span class="chip" onclick="setQuota(50,'GB',this)">۵۰ GB</span>
        </div>
      </div>
      <div class="cp-block mb16">
        <div class="cp-block-label"><i class="ti ti-plug-connected"></i> پروتکل انتقال</div>
        <select id="nl-proto" style="display:none">
          <option value="vless-ws">VLESS / WebSocket</option>
          <option value="xhttp-packet-up">XHTTP Ultra · packet-up</option>
          <option value="xhttp-stream-up">XHTTP Ultra · stream-up</option>
        </select>
        <div class="proto-cards">
          <div class="proto-card active" data-val="vless-ws" onclick="selectProto('vless-ws',this)">
            <div class="proto-card-check"><i class="ti ti-check"></i></div>
            <div class="proto-card-icon"><i class="ti ti-link"></i></div>
            <div class="proto-card-title">VLESS / WS</div>
            <div class="proto-card-desc">پایدار و همه‌منظوره</div>
          </div>
          <div class="proto-card" data-val="xhttp-packet-up" onclick="selectProto('xhttp-packet-up',this)">
            <div class="proto-card-check"><i class="ti ti-check"></i></div>
            <div class="proto-card-icon"><i class="ti ti-bolt"></i></div>
            <div class="proto-card-title">XHTTP · packet-up</div>
            <div class="proto-card-desc">سازگار با CDN</div>
          </div>
          <div class="proto-card" data-val="xhttp-stream-up" onclick="selectProto('xhttp-stream-up',this)">
            <div class="proto-card-check"><i class="ti ti-check"></i></div>
            <div class="proto-card-icon"><i class="ti ti-rocket"></i></div>
            <div class="proto-card-title">XHTTP · stream-up</div>
            <div class="proto-card-desc">تاخیر پایین‌تر</div>
          </div>
          <div class="proto-card" data-val="trojan-ws" onclick="selectProto('trojan-ws',this)">
            <div class="proto-card-check"><i class="ti ti-check"></i></div>
            <div class="proto-card-icon"><i class="ti ti-shield-lock"></i></div>
            <div class="proto-card-title">Trojan / WS</div>
            <div class="proto-card-desc">ساده و سریع</div>
          </div>
        </div>
      </div>
      <div class="cp-footer">
        <div class="cp-footer-note"><i class="ti ti-info-circle"></i> UUID کاملاً رندوم تولید می‌شود · فقط UUID‌های ثبت‌شده اجازه اتصال دارند · پروتکل پس از ساخت قابل تغییر نیست.</div>
        <button class="cp-submit-btn" onclick="createLink()"><i class="ti ti-link-plus"></i> ساخت کانفیگ</button>
      </div>
    </div>
  </div>
  <div class="cfg-grid" id="links-grid"></div>
  <div class="empty" id="links-empty" style="display:none"><i class="ti ti-link-off"></i><p>هنوز کانفیگی وجود ندارد</p></div>
</section>
<section class="pg" id="pg-subgroups">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-folders"></i> گروه‌های ساب</div><div class="tb-sub">هر گروه یک صفحه پابلیک مجزا با کانفیگ‌های خودش دارد</div></div>
    <div class="tb-right">
      <span class="badge bg-purple" id="subs-pg-cnt">۰ گروه</span>
      <button class="btn btn-pur" onclick="openModal('modal-create-sub')"><i class="ti ti-folder-plus"></i> گروه جدید</button>
    </div>
  </div>
  <div class="subs-toolbar">
    <div class="subs-search">
      <i class="ti ti-search"></i>
      <input type="text" id="subs-search-inp" placeholder="جستجو در گروه‌ها..." oninput="filterSubs(this.value)">
    </div>
  </div>
  <div class="sub-grid" id="subs-grid">
    <div class="subs-empty-v2"><div class="subs-empty-v2-icon"><i class="ti ti-folders"></i></div><div class="subs-empty-v2-title">هنوز گروهی وجود ندارد</div><div class="subs-empty-v2-sub">یک گروه جدید بسازید تا کانفیگ‌ها را دسته‌بندی کنید</div></div>
  </div>
</section>
<section class="pg" id="pg-subscriptions">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-rss"></i> سابسکریپشن</div><div class="tb-sub">لینک‌های اشتراک برای اپ‌های v2ray</div></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-rss"></i> سابسکریپشن تکی (هر کانفیگ)</div>
      <p style="font-size:11.5px;color:var(--t3);line-height:1.8;margin-bottom:12px">هر کانفیگ URL سابسکریپشن مخصوص دارد. از کارت کانفیگ روی آیکون <i class="ti ti-rss"></i> کلیک کنید.</p>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-database"></i> سابسکریپشن کامل (ادمین)</div>
      <p style="font-size:11.5px;color:var(--t3);line-height:1.8;margin-bottom:4px">شامل تمام کانفیگ‌های فعال.</p>
      <div class="sub-box"><span class="sub-url" id="sub-all-url">در حال دریافت...</span><div style="display:flex;gap:6px"><button class="btn btn-sm btn-g" onclick="cpSubAll()"><i class="ti ti-copy"></i></button><button class="btn btn-sm btn-g" onclick="window.open(location.protocol+'//'+location.host+'/sub-all')"><i class="ti ti-external-link"></i></button></div></div>
      <div class="cl amber" style="margin-top:11px"><i class="ti ti-alert-triangle"></i><span>این آدرس فقط در مرورگری که به پنل وارد شده کار می‌کند (نیاز به کوکی سشن).</span></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title"><i class="ti ti-folders"></i> لینک سابسکریپشن گروه‌ها</div>
    <div id="sub-groups-list">در حال بارگذاری...</div>
  </div>
</section>
<section class="pg" id="pg-traffic">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-chart-area"></i> ترافیک</div><div class="tb-sub">تحلیل و مانیتورینگ مصرف پهنای باند</div></div>
    <div class="tb-right"><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>
  <div class="traf-hero">
    <div class="traf-main-stat">
      <div class="traf-main-label"><i class="ti ti-database"></i> کل ترافیک مصرفی</div>
      <div class="traf-main-val" id="t-traffic">—<span>MB</span></div>
      <div class="traf-trend up" id="t-trend"><i class="ti ti-trending-up"></i> <span id="t-trend-val">—</span></div>
    </div>
    <div class="traf-mini">
      <div class="traf-mini-top"><div class="traf-mini-icon"><i class="ti ti-arrow-up-right"></i></div><span class="traf-mini-label">میانگین ساعتی</span></div>
      <div><div class="traf-mini-val" id="t-avg">—</div><div class="traf-mini-sub">MB در ساعت</div></div>
    </div>
    <div class="traf-mini">
      <div class="traf-mini-top"><div class="traf-mini-icon pk"><i class="ti ti-chart-bar"></i></div><span class="traf-mini-label">پیک مصرف</span></div>
      <div><div class="traf-mini-val" id="t-peak">—</div><div class="traf-mini-sub" id="t-peak-time">بالاترین ساعت</div></div>
    </div>
    <div class="traf-mini">
      <div class="traf-mini-top"><div class="traf-mini-icon lo"><i class="ti ti-clock-hour-4"></i></div><span class="traf-mini-label">کمترین مصرف</span></div>
      <div><div class="traf-mini-val" id="t-low">—</div><div class="traf-mini-sub">MB در ساعت</div></div>
    </div>
  </div>
  <div class="traf-chart-card">
    <div class="traf-chart-head">
      <div>
        <div class="traf-chart-title"><i class="ti ti-activity"></i> روند مصرف ترافیک</div>
        <div class="traf-chart-sub">بر اساس مگابایت در هر ساعت</div>
      </div>
      <div class="traf-legend">
        <div class="traf-legend-item"><span class="traf-legend-dot" style="background:var(--accent)"></span> مصرف</div>
        <div class="traf-legend-item"><span class="traf-legend-dot" style="background:var(--amber)"></span> میانگین</div>
      </div>
    </div>
    <div class="traf-chart-body"><canvas id="ch3"></canvas></div>
  </div>
</section>
<section class="pg" id="pg-connections">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-plug-connected"></i> اتصالات فعال</div><div class="tb-sub">مانیتورینگ زنده‌ی آی‌پی و ترافیک هر اتصال</div></div>
    <div class="tb-right"><span class="badge bg-green" id="conns-live">—</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>
  <div class="conn-hero">
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-plug-connected"></i></div>
      <div class="conn-hero-label">اتصالات زنده</div>
      <div class="conn-hero-val" id="ch-count">—</div>
    </div>
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-transfer"></i></div>
      <div class="conn-hero-label">مجموع ترافیک لحظه‌ای</div>
      <div class="conn-hero-val" id="ch-traffic">—</div>
    </div>
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-clock"></i></div>
      <div class="conn-hero-label">میانگین مدت اتصال</div>
      <div class="conn-hero-val" id="ch-avgdur">—</div>
    </div>
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-map-pin"></i></div>
      <div class="conn-hero-label">آی‌پی‌های یکتا</div>
      <div class="conn-hero-val" id="ch-uniq">—</div>
    </div>
  </div>
  <div class="conn-toolbar">
    <div class="conn-toolbar-title"><i class="ti ti-list-details"></i> لیست اتصالات</div>
    <div class="conn-live-badge"><span class="conn-live-dot"></span> بروزرسانی خودکار هر ۵ ثانیه</div>
  </div>
  <div class="conn-grid-v2" id="conns-grid"></div>
  <div class="conn-empty-v2" id="conns-empty" style="display:none">
    <div class="conn-empty-v2-icon"><i class="ti ti-plug-off"></i></div>
    <div class="conn-empty-v2-title">هیچ اتصال فعالی نیست</div>
    <div class="conn-empty-v2-sub">به محض اتصال کلاینت‌ها، اینجا نمایش داده می‌شوند</div>
  </div>
  <div class="conn-toolbar" style="margin-top:22px">
    <div class="conn-toolbar-title"><i class="ti ti-trophy"></i> پرمصرف‌ترین کانفیگ‌ها</div>
  </div>
  <div class="card" id="top-usage-card">
    <div id="top-usage-list">—</div>
  </div>
</section>
<section class="pg" id="pg-security">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-shield-lock"></i> امنیت</div></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-lock"></i> رمزنگاری</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-certificate"></i> TLS/HTTPS</span><span class="sr-v" style="color:var(--green-t)">● فعال (443)</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-fingerprint"></i> Fingerprint</span><span class="sr-v">Chrome Spoof</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-network"></i> پروتکل‌ها</span><span class="sr-v">VLESS/WS + XHTTP Ultra</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-key"></i> هش رمز</span><span class="sr-v">SHA-256+Salt</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-cookie"></i> سشن</span><span class="sr-v">HttpOnly · 7 روز</span></div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-shield-check"></i> کنترل دسترسی</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-id-badge"></i> UUID Auth سخت‌گیرانه</span><span class="sr-v" style="color:var(--green-t)">● فعال v9</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-toggle-right"></i> فعال/غیرفعال کانفیگ</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-gauge"></i> سهمیه ترافیک</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-calendar-x"></i> تاریخ انقضا</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-lock"></i> رمز صفحه پابلیک ساب</span><span class="sr-v" style="color:var(--green-t)">● اختیاری · SHA-256</span></div>
    </div>
  </div>
</section>
<section class="pg" id="pg-logs">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-history"></i> لاگ فعالیت‌ها</div><div class="tb-sub">تاریخچه‌ی کامل رخدادهای پنل</div></div><div class="tb-right"><button class="btn btn-p btn-sm" onclick="loadActivity()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="card"><div class="log-timeline" id="logs-list">—</div><div class="empty" id="logs-empty" style="display:none"><i class="ti ti-history-toggle"></i><p>هنوز لاگی ثبت نشده</p></div></div>
</section>
<section class="pg" id="pg-errors">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-alert-triangle"></i> خطاها</div></div><div class="tb-right"><span class="badge bg-red" id="errs-badge">۰</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="card"><div class="card-title"><i class="ti ti-bug"></i> لاگ خطاها</div><div id="errs-full">—</div></div>
</section>
<section class="pg" id="pg-testws">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-wifi"></i> تست WebSocket</div></div></div>
  <div class="card" style="max-width:660px">
    <div class="cl amber" style="margin-top:0;margin-bottom:12px"><i class="ti ti-alert-triangle"></i><span>فقط UUID‌های ثبت‌شده و فعال اتصال برقرار می‌کنند (این فقط تست VLESS/WS است؛ تست XHTTP از خود کلاینت انجام می‌شود).</span></div>
    <div class="form-row" style="margin-bottom:12px">
      <div class="fg" style="flex:1"><label>UUID (باید در کانفیگ‌ها وجود داشته باشد)</label><input class="fi" id="ws-uuid" placeholder="UUID یک کانفیگ فعال" style="width:100%"></div>
      <button class="btn btn-p" onclick="wsConn()"><i class="ti ti-plug-connected"></i> اتصال</button>
      <button class="btn btn-d" onclick="wsDisc()"><i class="ti ti-plug-x"></i> قطع</button>
    </div>
    <div class="form-row" style="margin-bottom:12px">
      <input class="fi" id="ws-msg" placeholder="پیام تست..." style="flex:1">
      <button class="btn btn-o" onclick="wsSend()"><i class="ti ti-send"></i> ارسال</button>
    </div>
    <div style="background:rgba(0,0,0,.3);border:1px solid var(--card-b);border-radius:10px;padding:14px;height:250px;overflow-y:auto;font-family:ui-monospace,monospace;font-size:10.5px;line-height:1.9" id="ws-log">
      <p style="color:var(--t3)">منتظر اتصال...</p>
    </div>
  </div>
</section>
<section class="pg" id="pg-settings">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-settings"></i> تنظیمات</div></div></div>
  <div class="g2">
    <div class="srv-panel">
      <div class="srv-hero">
        <div class="srv-hero-icon"><i class="ti ti-server-2"></i></div>
        <div class="srv-hero-text">
          <div class="srv-hero-domain" id="set-host">—</div>
          <div class="srv-hero-sub"><span class="dot dg pulse"></span> آنلاین · Railway</div>
        </div>
      </div>
      <div class="srv-tiles">
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-route"></i></div><div class="srv-tile-text"><div class="srv-tile-label">پورت</div><div class="srv-tile-val">443 (TLS)</div></div></div>
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-versions"></i></div><div class="srv-tile-text"><div class="srv-tile-label">نسخه</div><div class="srv-tile-val">v10.0</div></div></div>
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-brand-fastapi"></i></div><div class="srv-tile-text"><div class="srv-tile-label">فریم‌ورک</div><div class="srv-tile-val">FastAPI + Uvicorn</div></div></div>
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-cloud"></i></div><div class="srv-tile-text"><div class="srv-tile-label">پلتفرم</div><div class="srv-tile-val">Railway</div></div></div>
        <div class="srv-tile" style="grid-column:1/-1"><div class="srv-tile-icon"><i class="ti ti-device-floppy"></i></div><div class="srv-tile-text"><div class="srv-tile-label">ذخیره‌سازی</div><div class="srv-tile-val">JSON File (/data)</div></div></div>
      </div>
    </div>
    <div class="pw-panel">
      <div class="pw-hero">
        <div class="pw-hero-icon"><i class="ti ti-key"></i></div>
        <div class="pw-hero-text">
          <div class="pw-hero-title">تغییر رمز عبور</div>
          <div class="pw-hero-sub">رمز قوی انتخاب کنید و آن را جایی امن نگه دارید</div>
        </div>
      </div>
      <div class="pw-body">
        <div class="pw-field">
          <label>رمز فعلی</label>
          <input class="pw-input" type="password" id="cp-cur" placeholder="رمز فعلی را وارد کنید">
          <button class="pw-eye" type="button" onclick="togglePwField('cp-cur',this)"><i class="ti ti-eye"></i></button>
        </div>
        <div class="pw-field" style="margin-bottom:6px">
          <label>رمز جدید</label>
          <input class="pw-input" type="password" id="cp-new" placeholder="حداقل ۴ کاراکتر" oninput="checkPwStrength(this.value)">
          <button class="pw-eye" type="button" onclick="togglePwField('cp-new',this)"><i class="ti ti-eye"></i></button>
        </div>
        <div class="pw-strength" id="pw-strength-bar">
          <div class="pw-strength-seg"></div><div class="pw-strength-seg"></div><div class="pw-strength-seg"></div><div class="pw-strength-seg"></div>
        </div>
        <div class="pw-strength-label" id="pw-strength-label"><i class="ti ti-shield"></i> قدرت رمز</div>
        <div class="pw-reqs">
          <span class="pw-req" id="req-len"><i class="ti ti-circle-dashed"></i> حداقل ۴ کاراکتر</span>
          <span class="pw-req" id="req-num"><i class="ti ti-circle-dashed"></i> شامل عدد</span>
          <span class="pw-req" id="req-case"><i class="ti ti-circle-dashed"></i> حروف بزرگ/کوچک</span>
        </div>
        <div class="pw-field" style="margin-bottom:18px">
          <label>تکرار رمز جدید</label>
          <input class="pw-input" type="password" id="cp-cf" placeholder="تکرار رمز جدید">
          <button class="pw-eye" type="button" onclick="togglePwField('cp-cf',this)"><i class="ti ti-eye"></i></button>
        </div>
        <button class="pw-submit" onclick="changePw()"><i class="ti ti-shield-check"></i> ذخیره رمز جدید</button>
      </div>
    </div>
    <div class="pw-panel">
      <div class="pw-hero">
        <div class="pw-hero-icon" style="background:rgba(34,158,217,.14);color:#29a9eb"><i class="ti ti-brand-telegram"></i></div>
        <div class="pw-hero-text">
          <div class="pw-hero-title">نوتیفیکیشن تلگرام</div>
          <div class="pw-hero-sub">وقتی حجم/زمان یک کانفیگ داره تموم می‌شه، به مدیر پیام بده</div>
        </div>
      </div>
      <div class="pw-body">
        <div class="pw-field" style="margin-bottom:14px">
          <label style="display:flex;align-items:center;justify-content:space-between">
            <span>فعال‌سازی نوتیفیکیشن</span>
            <label class="switch"><input type="checkbox" id="tg-enabled"><span class="slider"></span></label>
          </label>
        </div>
        <div class="pw-field">
          <label>توکن بات (از @BotFather)</label>
          <input class="pw-input" type="text" id="tg-token" placeholder="123456:ABC-DEF...">
        </div>
        <div class="pw-field" style="margin-bottom:14px">
          <label>چت‌آیدی (خودت یا گروه)</label>
          <input class="pw-input" type="text" id="tg-chatid" placeholder="مثلاً 123456789">
        </div>
        <div class="form-row" style="margin-bottom:14px">
          <div class="fg" style="flex:1"><label>هشدار مصرف در چند درصد؟</label><input class="fi" id="tg-quota-pct" type="number" min="1" max="100" style="width:100%" value="90"></div>
          <div class="fg" style="flex:1"><label>هشدار انقضا چند ساعت قبل؟</label><input class="fi" id="tg-exp-hours" type="number" min="1" style="width:100%" value="24"></div>
        </div>
        <div class="fg" style="margin-bottom:6px">
          <label>IP دستی api.telegram.org (اختیاری — برای دورزدن فیلترینگِ DNS روی همین سرور)</label>
          <div style="display:flex;gap:6px">
            <input class="pw-input" type="text" id="tg-api-ip" placeholder="مثلاً 149.154.167.220 — خالی = استفاده از دامنه">
            <button class="btn btn-o" style="white-space:nowrap" onclick="resolveTelegramIp()"><i class="ti ti-search"></i> پیدا کن</button>
          </div>
        </div>
        <div class="cl amber" style="margin-bottom:14px"><i class="ti ti-alert-triangle"></i><span>این فقط فیلترینگ در سطح DNS را دور می‌زند، نه بلاک در سطح IP. IPهای تلگرام هم گاهی عوض می‌شوند؛ دکمه‌ی «پیدا کن» از خودِ سرور (نه مرورگر شما) IP فعلی را می‌گیرد.</span></div>
        <div style="display:flex;gap:8px">
          <button class="pw-submit" style="flex:1" onclick="saveTelegramSettings()"><i class="ti ti-device-floppy"></i> ذخیره تنظیمات</button>
          <button class="btn btn-g" onclick="testTelegram()"><i class="ti ti-send"></i> تست ارسال</button>
        </div>
        <div class="cl" style="margin-top:12px"><i class="ti ti-info-circle"></i><span>برای ساخت بات، به @BotFather پیام بده و دستور /newbot را بزن؛ برای گرفتن چت‌آیدی خودت، به @userinfobot پیام بده.</span></div>
      </div>
    </div>
    <!-- ============================================================ -->
    <!-- 🌐 تنظیمات عمومی ساب -->
    <!-- ============================================================ -->
    <div class="pw-panel" style="margin-top:16px">
      <div class="pw-hero">
        <div class="pw-hero-icon" style="background:rgba(251,191,36,.14);color:#fbbf24">
          <i class="ti ti-world"></i>
        </div>
        <div class="pw-hero-text">
          <div class="pw-hero-title">🌐 تنظیمات عمومی ساب</div>
          <div class="pw-hero-sub">کنترل اینکه کاربران عادی اجازهی ساخت/حذف کانفیگ دارند یا نه</div>
        </div>
      </div>
      <div class="pw-body">
        <div class="pw-field" style="margin-bottom:12px">
          <label style="display:flex;align-items:center;justify-content:space-between">
            <span><i class="ti ti-plus"></i> ساخت کانفیگ توسط کاربران</span>
            <label class="switch"><input type="checkbox" id="pub-create" checked><span class="slider"></span></label>
          </label>
        </div>
        <div class="pw-field" style="margin-bottom:12px">
          <label style="display:flex;align-items:center;justify-content:space-between">
            <span><i class="ti ti-trash"></i> حذف کانفیگ توسط کاربران</span>
            <label class="switch"><input type="checkbox" id="pub-delete" checked><span class="slider"></span></label>
          </label>
        </div>
        <div class="pw-field" style="margin-bottom:14px">
          <label style="display:flex;align-items:center;justify-content:space-between">
            <span><i class="ti ti-power"></i> تغییر وضعیت (فعال/غیرفعال) توسط کاربران</span>
            <label class="switch"><input type="checkbox" id="pub-toggle" checked><span class="slider"></span></label>
          </label>
        </div>
        <div class="cl amber"><i class="ti ti-alert-triangle"></i>
          <span>اگر این گزینه‌ها را غیرفعال کنید، کاربران فقط <b>کانفیگ‌های موجود</b> را از ساب دریافت می‌کنند و نمی‌توانند کانفیگ جدید بسازند یا کانفیگ خود را حذف کنند. این کار <b>فشار روی سرور را تا ۸۰٪ کاهش</b> می‌دهد.</span>
        </div>
        <button class="pw-submit" style="margin-top:14px;background:linear-gradient(135deg,#fbbf24,#f59e0b)" onclick="savePublicSettings()">
          <i class="ti ti-device-floppy"></i> ذخیره تنظیمات
        </button>
      </div>
    </div>
    <!-- ============================================================ -->
    <!-- ✅ بخش تنظیمات عضویت اجباری در کانال + هدیه‌ی خودکار ورود -->
    <!-- ============================================================ -->
    <div class="pw-panel" style="margin-top:16px">
      <div class="pw-hero">
        <div class="pw-hero-icon" style="background:rgba(251,191,36,.14);color:#fbbf24"><i class="ti ti-gift"></i></div>
        <div class="pw-hero-text">
          <div class="pw-hero-title">🎁 هدیه‌ی ورود به بات</div>
          <div class="pw-hero-sub">هرکسی وارد بات شود، بعد از عضویت در کانال، یک کانفیگ اختصاصی می‌گیرد</div>
        </div>
      </div>
      <div class="pw-body">
        <div class="pw-field" style="margin-bottom:14px">
          <label style="display:flex;align-items:center;justify-content:space-between">
            <span>فعال‌سازی هدیه‌ی خودکار ورود</span>
            <label class="switch"><input type="checkbox" id="join-enabled"><span class="slider"></span></label>
          </label>
        </div>
        <div class="pw-field">
          <label>نام کاربری کانال اجباری (بدون @)</label>
          <input class="pw-input" type="text" id="join-channel" placeholder="TimAzadi" value="TimAzadi">
        </div>
        <div class="pw-field" style="margin-bottom:14px">
          <label style="display:flex;align-items:center;justify-content:space-between">
            <span>عضویت در کانال اجباری باشد؟</span>
            <label class="switch"><input type="checkbox" id="join-channel-required" checked><span class="slider"></span></label>
          </label>
        </div>
        <div class="form-row" style="margin-bottom:14px">
          <div class="fg" style="flex:1"><label>حجم هدیه (GB)</label><input class="fi" id="join-grant-gb" type="number" min="0" step="1" value="100"></div>
          <div class="fg" style="flex:1"><label>مدت اعتبار (روز، ۰ = بدون انقضا)</label><input class="fi" id="join-grant-days" type="number" min="0" value="0"></div>
        </div>
        <div class="pw-field" style="margin-bottom:6px">
          <label>نام کاربری بات (بدون @)</label>
          <input class="pw-input" type="text" id="join-bot-username" placeholder="مثلاً: timazadi_bot">
        </div>
        <div style="display:flex;gap:8px;margin-top:14px">
          <button class="pw-submit" style="flex:1" onclick="saveJoinSettings()"><i class="ti ti-device-floppy"></i> ذخیره تنظیمات</button>
          <button class="btn btn-g" onclick="loadJoinSettings()"><i class="ti ti-refresh"></i></button>
        </div>
        <div class="cl" style="margin-top:12px"><i class="ti ti-info-circle"></i>
          <span>هر کاربری با زدن /start روی بات، بعد از تایید عضویت در کانال بالا، یک کانفیگ اختصاصی با حجم مشخص‌شده می‌گیرد. یادت نره بات باید <b>ادمین</b> کانال باشد تا چک عضویت درست کار کند.</span>
        </div>
      </div>
    </div>
  </div>
</section>
</main>
<script>
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
function daysLeft(exp){if(!exp)return null;return Math.ceil((new Date(exp)-Date.now())/864e5)}
function expChip(exp,expired){
  if(expired)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if(!exp)return '<span class="exp-chip ec-inf"><i class="ti ti-infinity"></i> نامحدود</span>';
  const d=daysLeft(exp);
  if(d<=0)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if(d<=3)return `<span class="exp-chip ec-warn"><i class="ti ti-alert-triangle"></i> ${toFa(d)} روز مانده</span>`;
  return `<span class="exp-chip ec-ok"><i class="ti ti-calendar-check"></i> ${toFa(d)} روز مانده</span>`;
}
function protoBadge(p){
  const m={'vless-ws':['VLESS · WS','pc-ws'],'xhttp-packet-up':['XHTTP · packet-up','pc-xhttp'],'xhttp-stream-up':['XHTTP · stream-up','pc-xhttp'],'xhttp-stream-one':['XHTTP ULTRA','pc-ultra'],'trojan-ws':['Trojan · WS','pc-trojan'],'trojan-xhttp':['Trojan · XHTTP','pc-trojan']};
  const v=m[p]||m['vless-ws'];
  return `<span class="proto-chip ${v[1]}">${v[0]}</span>`;
}
async function checkAuth(){try{const r=await fetch('/api/me');const d=await r.json();if(!d.authenticated)location.href='/login';}catch(e){location.href='/login'}}
async function logout(){try{await fetch('/api/logout',{method:'POST'})}catch(e){}location.href='/login'}
document.getElementById('logout-btn').addEventListener('click',logout);
async function authF(url,opts={}){
  const r=await fetch(url,opts);
  if(r.status===401){location.href='/login';throw new Error('unauthorized')}
  return r;
}
function setQuota(val,unit,el){
  document.getElementById('nl-val').value = val===0?'':val;
  document.getElementById('nl-unit').value = unit;
  document.querySelectorAll('#quota-chips .chip').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
function setExpiry(value,unit,el){
  document.getElementById('nl-exp').value = value===0?'':value;
  document.getElementById('nl-exp-unit').value = unit||'days';
  document.querySelectorAll('#exp-chips .chip').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
function selectProto(val,el){
  document.getElementById('nl-proto').value = val;
  document.querySelectorAll('.proto-card').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
const sb=document.getElementById('sb'),overlay=document.getElementById('overlay');
function openSb(){sb.classList.add('open');overlay.classList.add('show')}
function closeSb(){sb.classList.remove('open');overlay.classList.remove('show')}
document.getElementById('open-sb').addEventListener('click',openSb);
document.getElementById('close-sb').addEventListener('click',closeSb);
overlay.addEventListener('click',closeSb);
function navTo(name){
  document.querySelectorAll('.nav-it').forEach(n=>n.classList.toggle('on',n.dataset.pg===name));
  document.querySelectorAll('.pg').forEach(p=>p.classList.toggle('on',p.id==='pg-'+name));
  const loaders={links:loadLinks,connections:loadConns,errors:loadErrs,subscriptions:loadSubsPage,subgroups:loadSubs,logs:loadActivity};
  if(loaders[name])loaders[name]();
  closeSb();window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.nav-it').forEach(el=>el.addEventListener('click',()=>navTo(el.dataset.pg)));
function openModal(id){document.getElementById(id).classList.add('open')}
function closeModal(id){document.getElementById(id).classList.remove('open')}
let prevTraf=0,ch1,ch2,ch3;
async function fetchStats(){
  try{
    const r=await authF('/stats'),d=await r.json();
    document.getElementById('m-conns').textContent=d.active_connections;
    document.getElementById('conns-nb').textContent=d.active_connections;
    document.getElementById('m-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';
    document.getElementById('m-alinks').textContent=d.active_links??'—';
    document.getElementById('m-lsub').textContent='از '+d.links_count+' کانفیگ';
    document.getElementById('m-subs').textContent=d.subs_count??'—';
    document.getElementById('errs-badge').textContent=d.total_errors+' خطا';
    document.getElementById('uptime-inline').textContent=d.uptime;
    document.getElementById('uptime-badge').textContent='Railway · '+d.uptime;
    document.getElementById('last-upd').textContent='آخرین بروزرسانی: '+new Date().toLocaleTimeString('fa-IR');
    document.getElementById('conns-live').innerHTML='<span class="dot dg pulse"></span> '+d.active_connections+' اتصال';
    document.getElementById('t-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';
    const delta=d.total_traffic_mb-prevTraf,pct=Math.min(100,Math.round((delta/50)*100));
    document.getElementById('bw-pct').textContent=pct+'%';
    document.getElementById('bw-bar').style.width=pct+'%';
    prevTraf=d.total_traffic_mb;
    if(d.hourly){
      const labels=Object.keys(d.hourly).sort(),vals=labels.map(k=>+(d.hourly[k]/1024**2).toFixed(2));
      [ch1,ch3].forEach(c=>{if(!c)return;c.data.labels=labels;c.data.datasets[0].data=vals;c.update()});
      if(vals.length){const avg=vals.reduce((a,b)=>a+b,0)/vals.length,peak=Math.max(...vals);document.getElementById('t-avg').innerHTML=avg.toFixed(2)+'<span class="m-unit">MB</span>';document.getElementById('t-peak').innerHTML=peak.toFixed(2)+'<span class="m-unit">MB</span>';}
    }
    renderErrs(d.recent_errors||[]);
  }catch(e){console.error(e)}
}
function renderErrs(errs){
  const el=document.getElementById('errs-full');if(!el)return;
  if(!errs.length){el.innerHTML='<div style="color:var(--green-t);padding:10px;font-size:12px;display:flex;align-items:center;gap:5px"><i class="ti ti-circle-check"></i> هیچ خطایی نیست</div>';return}
  el.innerHTML=errs.slice().reverse().map(e=>`<div class="erow"><div class="etime"><i class="ti ti-clock"></i>${new Date(e.time).toLocaleString('fa-IR')}</div><div class="emsg">${esc(e.error)}${e.url?' — '+esc(e.url):''}</div></div>`).join('');
}
async function loadActivity(){
  try{
    const r=await authF('/api/activity'),d=await r.json();
    const logs=(d.logs||[]).slice().reverse();
    const el=document.getElementById('logs-list'),em=document.getElementById('logs-empty');
    if(!logs.length){el.innerHTML='';em.style.display='block';return}
    em.style.display='none';
    const icMap={ok:'ti-circle-check',err:'ti-circle-x',warn:'ti-alert-triangle',info:'ti-info-circle'};
    const kindFa={link:'کانفیگ',sub:'گروه',auth:'ورود',connection:'اتصال',system:'سیستم'};
    el.innerHTML=logs.map(l=>`
      <div class="log-item">
        <div class="log-ic ${l.level}"><i class="ti ${icMap[l.level]||'ti-info-circle'}"></i></div>
        <div class="log-body">
          <div class="log-msg">${esc(l.message)}</div>
          <div class="log-time"><i class="ti ti-clock"></i> ${new Date(l.time).toLocaleString('fa-IR')} <span class="log-kind">${kindFa[l.kind]||l.kind}</span></div>
        </div>
      </div>
    `).join('');
  }catch(e){console.error(e)}
}
let allSubsList=[],allLinksList=[];
async function loadLinks(){
  try{
    const [lr,sr]=await Promise.all([authF('/api/links'),authF('/api/subs')]);
    const {links=[]}=await lr.json();
    const {subs=[]}=await sr.json();
    allSubsList=subs;allLinksList=links;
    const nlSub=document.getElementById('nl-sub');
    nlSub.innerHTML='<option value="">— بدون گروه —</option>'+subs.map(s=>`<option value="${esc(s.sub_id)}">${esc(s.name)}</option>`).join('');
    document.getElementById('links-nb').textContent=links.length;
    document.getElementById('links-pg-cnt').textContent=toFa(links.length)+' کانفیگ';
    document.getElementById('lsummary-badge').textContent=toFa(links.length);
    const grid=document.getElementById('links-grid'),empty=document.getElementById('links-empty');
    if(!links.length){grid.innerHTML='';empty.style.display='block';document.getElementById('lsummary').innerHTML='<div class="empty"><i class="ti ti-link-off"></i><p>کانفیگی وجود ندارد</p></div>';return}
    empty.style.display='none';
    const subMap=Object.fromEntries(subs.map(s=>[s.sub_id,s.name]));
    grid.innerHTML=links.map(l=>{
  const lim=l.limit_bytes===0?'∞':fmtB(l.limit_bytes);
  const pct=l.limit_bytes===0?0:Math.min(100,l.used_bytes/l.limit_bytes*100);
  const bc=pct>90?'var(--red)':pct>70?'var(--amber)':'var(--accent)';
  const allowed=l.active&&!l.expired;
  const cardCls=!l.active?'is-off':(l.expired?'is-exp':'');
  return `<div class="cfg-card ${cardCls}">
    <div class="cfg-row">
      <span class="cfg-status-dot ${allowed?'pulse':''}"></span>
      <div class="cfg-identity">
        <div class="cfg-label">${esc(l.label)}</div>
        <div class="cfg-sub-meta">
          <span class="cfg-uuid-mini" onclick="navigator.clipboard.writeText('${l.uuid}').then(()=>toast('UUID کپی شد','ok'))" title="${l.uuid}"><i class="ti ti-fingerprint"></i> ${l.uuid.slice(0,10)}…</span>
          <span>${new Date(l.created_at).toLocaleDateString('fa-IR')}</span>
        </div>
      </div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-usage-col">
        <div class="ubar"><div class="ubar-f" style="width:${pct}%;background:${bc}"></div></div>
        <div class="utxt"><span>${fmtB(l.used_bytes)}</span><span>از ${lim}</span></div>
      </div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-exp-col">${expChip(l.expires_at,l.expired)}</div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-badges-col">
        ${protoBadge(l.protocol)}
        ${l.sub_id&&allSubsList.find(s=>s.sub_id===l.sub_id)?`<span class="cfg-sub-tag"><i class="ti ti-folder"></i> ${esc(allSubsList.find(s=>s.sub_id===l.sub_id).name)}</span>`:''}
        <span class="cfg-sub-tag" style="${l.live_connections>0?'color:var(--green-t);border-color:rgba(34,197,94,.3)':''}" title="اتصال زنده / سقف دستگاه">
          <i class="ti ti-devices"></i> ${toFa(l.live_connections||0)}${l.max_devices?'/'+toFa(l.max_devices):''}
        </span>
      </div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-actions">
        <button class="tog${allowed?' on':''}" onclick="toggleActive('${l.uuid}',${!l.active})" title="فعال/غیرفعال"></button>
        <button class="btn btn-sm btn-g btn-icon" onclick='copyAllProtocols(${JSON.stringify(l.uuid)})' title="کپی هر ۳ کانفیگ باهم"><i class="ti ti-copy"></i></button>
        <button class="btn btn-sm btn-g btn-icon" onclick="navigator.clipboard.writeText('${esc(l.sub_url)}').then(()=>toast('Sub کپی شد','ok'))" title="Sub URL"><i class="ti ti-rss"></i></button>
        <button class="btn btn-sm btn-g btn-icon" onclick='openQrModal(${JSON.stringify(l.uuid)})' title="QR"><i class="ti ti-qrcode"></i></button>
        <button class="btn btn-sm btn-pur btn-icon" onclick="openDailyChart('${l.uuid}','${esc(l.label)}')" title="نمودار مصرف روزانه"><i class="ti ti-chart-histogram"></i></button>
        <button class="btn btn-sm btn-amber btn-icon" onclick="openEditLink('${l.uuid}')" title="ویرایش"><i class="ti ti-edit"></i></button>
        <button class="btn btn-sm btn-g btn-icon" onclick="resetUsage('${l.uuid}')" title="ریست مصرف"><i class="ti ti-rotate"></i></button>
        <button class="btn btn-sm btn-d btn-icon" onclick="deleteLink('${l.uuid}')" title="حذف"><i class="ti ti-trash"></i></button>
      </div>
    </div>
  </div>`;
}).join('');
    document.getElementById('lsummary').innerHTML=links.slice(0,6).map(l=>`<div class="sr"><span class="sr-k" style="gap:5px"><i class="ti ${l.expired?'ti-calendar-x':l.active?'ti-circle-check':'ti-circle-x'}" style="color:${l.expired?'var(--amber)':l.active?'var(--green)':'var(--red)'}"></i>${esc(l.label)}</span><span class="sr-v" style="font-size:10px">${fmtB(l.used_bytes)} / ${l.limit_bytes===0?'∞':fmtB(l.limit_bytes)}</span></div>`).join('');
  }catch(e){console.error(e)}
}
async function createLink(){
  const label=document.getElementById('nl-label').value.trim()||'کانفیگ جدید';
  const val=document.getElementById('nl-val').value;
  const unit=document.getElementById('nl-unit').value;
  const exp=document.getElementById('nl-exp').value;
  const expUnit=document.getElementById('nl-exp-unit').value||'days';
  const note=document.getElementById('nl-note').value.trim();
  const sub_id=document.getElementById('nl-sub').value||null;
  const protocol=document.getElementById('nl-proto').value||'vless-ws';
  const flag=document.getElementById('nl-flag').value||'🇺🇸';
  const max_devices=document.getElementById('nl-devices').value||0;
  try{
    const r=await authF('/api/links',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({label,limit_value:val||0,limit_unit:unit,expires_value:exp||0,expires_unit:expUnit,note,sub_id,protocol,flag,max_devices})});
    if(!r.ok)throw new Error('failed');
    ['nl-label','nl-val','nl-exp','nl-note','nl-devices'].forEach(id=>document.getElementById(id).value='');
    toast('کانفیگ ساخته شد ✓','ok');loadLinks();
  }catch(e){toast('خطا در ساخت','err')}
}
function openEditLink(uuid){
  const l=allLinksList.find(x=>x.uuid===uuid);
  if(!l)return;
  document.getElementById('el-uuid').value=uuid;
  document.getElementById('el-label').value=l.label;
  document.getElementById('el-note').value=l.note||'';
  if(l.limit_bytes===0){document.getElementById('el-val').value='';document.getElementById('el-unit').value='GB';}
  else{document.getElementById('el-val').value=(l.limit_bytes/1024/1024).toFixed(0);document.getElementById('el-unit').value='MB';}
  document.getElementById('el-exp').value='';
  document.getElementById('el-exp-unit').value='days';
  document.getElementById('el-devices').value=l.max_devices||'';
  openModal('modal-edit-link');
}
async function saveEditLink(){
  const uuid=document.getElementById('el-uuid').value;
  const label=document.getElementById('el-label').value.trim();
  const note=document.getElementById('el-note').value.trim();
  const val=document.getElementById('el-val').value;
  const unit=document.getElementById('el-unit').value;
  const exp=document.getElementById('el-exp').value;
  const expUnit=document.getElementById('el-exp-unit').value||'days';
  const max_devices=document.getElementById('el-devices').value;
  const body={label,note,limit_value:val||0,limit_unit:unit,max_devices:max_devices===''?0:Number(max_devices)};
  if(exp&&Number(exp)>0){body.expires_value=Number(exp);body.expires_unit=expUnit;}
  try{
    const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!r.ok)throw new Error();
    closeModal('modal-edit-link');
    toast('کانفیگ ویرایش شد ✓','ok');loadLinks();
  }catch(e){toast('خطا در ویرایش','err')}
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
const PROTO_TAG={'vless-ws':'WS','xhttp-packet-up':'XHTTP-P','xhttp-stream-up':'XHTTP-S','xhttp-stream-one':'ULTRA'};
function copyAllProtocols(uuid){
  const l=allLinksList.find(x=>x.uuid===uuid);
  if(!l)return;
  const bundle=(l.vless_links&&l.vless_links.length)?l.vless_links:[{vless_link:l.vless_link}];
  navigator.clipboard.writeText(bundle.map(b=>b.vless_link).join('\n'))
    .then(()=>toast('هر '+toFa(bundle.length)+' کانفیگ کپی شد ✓','ok'));
}
let qrCurrentBundle=[],qrCurrentIdx=0;
function openQrModal(uuid){
  const l=allLinksList.find(x=>x.uuid===uuid);
  if(!l)return;
  qrCurrentBundle=(l.vless_links&&l.vless_links.length)?l.vless_links:[{protocol:l.protocol,vless_link:l.vless_link}];
  qrCurrentIdx=Math.max(0,qrCurrentBundle.findIndex(b=>b.protocol===l.protocol));
  document.getElementById('qrv2-label').textContent=l.label;
  const lim=l.limit_bytes===0?'∞':fmtB(l.limit_bytes);
  document.getElementById('qrv2-usage').innerHTML='<i class="ti ti-chart-bar"></i> حجم دقیق: '+fmtB(l.used_bytes)+' از '+lim;
  document.getElementById('qrv2-tabs').innerHTML=qrCurrentBundle.map((b,i)=>
    `<button class="qr-proto-tab${i===qrCurrentIdx?' on':''}" onclick="selectQrProto(${i})">${PROTO_TAG[b.protocol]||b.protocol}</button>`).join('');
  renderQrImg();
  document.getElementById('qr-modal-v2').classList.add('open');
}
function selectQrProto(i){qrCurrentIdx=i;document.querySelectorAll('.qr-proto-tab').forEach((el,idx)=>el.classList.toggle('on',idx===i));renderQrImg()}
function renderQrImg(){
  const link=qrCurrentBundle[qrCurrentIdx].vless_link;
  document.getElementById('qrv2-img').src='https://api.qrserver.com/v1/create-qr-code/?size=280x280&data='+encodeURIComponent(link);
}
function copyCurrentQrLink(){
  navigator.clipboard.writeText(qrCurrentBundle[qrCurrentIdx].vless_link).then(()=>toast('لینک این پروتکل کپی شد ✓','ok'));
}
function showQR(link){
  qrCurrentBundle=[{vless_link:link}];qrCurrentIdx=0;
  document.getElementById('qrv2-label').textContent='QR Code';
  document.getElementById('qrv2-usage').innerHTML='';
  document.getElementById('qrv2-tabs').innerHTML='';
  renderQrImg();
  document.getElementById('qr-modal-v2').classList.add('open');
}
let allSubsRaw=[];
async function loadSubs(){
  try{
    const r=await authF('/api/subs'),d=await r.json();
    const subs=d.subs||[];
    allSubsRaw=subs;
    document.getElementById('subs-nb').textContent=subs.length;
    document.getElementById('subs-pg-cnt').textContent=toFa(subs.length)+' گروه';
    renderSubsGrid(subs);
  }catch(e){console.error(e)}
}
function renderSubsGrid(subs){
  const grid=document.getElementById('subs-grid');
  if(!subs.length){
    grid.innerHTML='<div class="subs-empty-v2"><div class="subs-empty-v2-icon"><i class="ti ti-folders"></i></div><div class="subs-empty-v2-title">هنوز گروهی وجود ندارد</div><div class="subs-empty-v2-sub">یک گروه جدید بسازید تا کانفیگ‌ها را دسته‌بندی کنید</div></div>';
    return;
  }
  grid.innerHTML=subs.map(s=>`
    <div class="sub-card${s.locked?' sub-card-locked':''}">
      ${s.locked?'<div class="sub-card-locked-banner"><i class="ti ti-lock"></i> این گروه توسط مدیر قفل شده — همه‌ی کانفیگ‌هایش موقتاً غیرفعالند</div>':''}
      <div class="sub-card-top">
        <div class="sub-card-head-v2">
          <div class="sub-card-icon"><i class="ti ti-folder"></i></div>
          <div class="sub-card-titles">
            <div class="sub-card-name-v2">${esc(s.name)}</div>
            ${s.desc?`<div class="sub-card-desc-v2">${esc(s.desc)}</div>`:'<div class="sub-card-desc-v2" style="opacity:.5">بدون توضیحات</div>'}
          </div>
          <div class="sub-card-lock-badge ${s.has_password?'locked':'open'}" title="${s.has_password?'رمزدار':'پابلیک'}">
            <i class="ti ${s.has_password?'ti-lock':'ti-lock-open'}"></i>
          </div>
        </div>
        <div class="sub-card-stats">
          <div class="sub-card-stat"><div class="sub-card-stat-val">${toFa(s.links_count)}</div><div class="sub-card-stat-label">کانفیگ</div></div>
          <div class="sub-card-stat"><div class="sub-card-stat-val" style="color:var(--green-t)">${toFa(s.active_count)}</div><div class="sub-card-stat-label">فعال</div></div>
          <div class="sub-card-stat"><div class="sub-card-stat-val" style="font-size:12px">${esc(s.total_used_fmt)}</div><div class="sub-card-stat-label">مصرف</div></div>
        </div>
        ${s.pool_limit_bytes?`<div class="cl" style="margin-top:10px;background:rgba(139,92,246,.08);border-color:rgba(139,92,246,.25)"><i class="ti ti-chart-pie" style="color:#a78bfa"></i><span>استخر تقسیم‌پذیر: <b>${esc(s.pool_available_fmt)}</b> باقی از <b>${esc(s.pool_limit_fmt)}</b>${s.child_sub_ids&&s.child_sub_ids.length?' · '+toFa(s.child_sub_ids.length)+' ساب هدیه‌داده‌شده':''}</span></div>`:''}
        ${s.parent_sub_id?`<div class="cl" style="margin-top:10px"><i class="ti ti-gift"></i><span>این یک ساب هدیه‌ست (سفید-برند، بدون لوگو)</span></div>`:''}
        <div class="sub-card-perms">
          <label class="perm-toggle" title="اجازه‌ی حذف کانفیگ هدیه‌ای توسط مشتری">
            <input type="checkbox" ${s.client_can_delete?'checked':''} onchange="setSubPerm('${esc(s.sub_id)}','client_can_delete',this.checked)">
            <i class="ti ti-trash"></i> حذف توسط مشتری
          </label>
          <label class="perm-toggle" title="اجازه‌ی غیرفعال‌کردن کانفیگ هدیه‌ای توسط مشتری">
            <input type="checkbox" ${s.client_can_disable?'checked':''} onchange="setSubPerm('${esc(s.sub_id)}','client_can_disable',this.checked)">
            <i class="ti ti-power"></i> غیرفعال توسط مشتری
          </label>
        </div>
      </div>
      <div class="sub-card-url-row">
        <span class="sub-card-url-text">${esc(s.public_url)}</span>
        <button class="sub-card-url-copy" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('لینک پابلیک کپی شد','ok'))" title="کپی"><i class="ti ti-copy"></i></button>
        <button class="sub-card-url-copy" onclick="window.open('${esc(s.public_url)}','_blank')" title="باز کردن"><i class="ti ti-external-link"></i></button>
      </div>
      <div class="sub-card-bottom">
        <button class="btn btn-sm btn-g" onclick="openSubLinks('${esc(s.sub_id)}','${esc(s.name)}')"><i class="ti ti-link-plus"></i> کانفیگ‌ها</button>
        <button class="btn btn-sm btn-o" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('لینک ساب کپی شد','ok'))"><i class="ti ti-rss"></i> ساب</button>
        <button class="btn btn-sm btn-g btn-icon" onclick="showQR('${esc(s.sub_url)}')" title="QR"><i class="ti ti-qrcode"></i></button>
        <button class="btn btn-sm ${s.locked?'btn-g':'btn-amber'} btn-icon" onclick="toggleSubLock('${esc(s.sub_id)}',${!s.locked})" title="${s.locked?'باز کردن قفل گروه':'قفل کردن کل گروه'}"><i class="ti ${s.locked?'ti-lock-open':'ti-lock'}"></i></button>
        <button class="btn btn-sm btn-d btn-icon" onclick="deleteSub('${esc(s.sub_id)}')" title="حذف"><i class="ti ti-trash"></i></button>
      </div>
    </div>
  `).join('');
}
function filterSubs(q){
  q=q.trim().toLowerCase();
  if(!q){renderSubsGrid(allSubsRaw);return}
  renderSubsGrid(allSubsRaw.filter(s=>s.name.toLowerCase().includes(q)||(s.desc||'').toLowerCase().includes(q)));
}
async function createSub(){
  const name=document.getElementById('ns-name').value.trim()||'گروه جدید';
  const desc=document.getElementById('ns-desc').value.trim();
  const pw=document.getElementById('ns-pw').value;
  const pool_value=document.getElementById('ns-pool-val').value||0;
  const pool_unit=document.getElementById('ns-pool-unit').value;
  const client_can_delete=document.getElementById('ns-can-delete').checked;
  const client_can_disable=document.getElementById('ns-can-disable').checked;
  try{
    const r=await authF('/api/subs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,desc,password:pw,pool_value,pool_unit,client_can_delete,client_can_disable})});
    if(!r.ok)throw new Error('failed');
    ['ns-name','ns-desc','ns-pw','ns-pool-val'].forEach(id=>document.getElementById(id).value='');
    document.getElementById('ns-can-delete').checked=true;document.getElementById('ns-can-disable').checked=true;
    closeModal('modal-create-sub');
    toast('گروه ساخته شد ✓','ok');loadSubs();
  }catch(e){toast('خطا در ساخت گروه','err')}
}
async function deleteSub(sub_id){
  if(!confirm('حذف این گروه؟ کانفیگ‌ها حذف نمی‌شوند.'))return;
  try{const r=await authF('/api/subs/'+sub_id,{method:'DELETE'});if(!r.ok)throw new Error();toast('گروه حذف شد ✓','ok');loadSubs();loadLinks();}catch(e){toast('خطا','err')}
}
async function toggleSubLock(sub_id,locked){
  try{
    const r=await authF('/api/subs/'+sub_id+'/lock',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({locked})});
    if(!r.ok)throw new Error();
    toast(locked?'گروه قفل شد ✓':'قفل گروه باز شد ✓','ok');
    loadSubs();loadLinks();
  }catch(e){toast('خطا','err')}
}
async function setSubPerm(sub_id,key,value){
  try{
    const r=await authF('/api/subs/'+sub_id,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({[key]:value})});
    if(!r.ok)throw new Error();
    toast('ذخیره شد ✓','ok');
  }catch(e){toast('خطا در ذخیره','err');loadSubs()}
}
let lmodalLinks=[],lmodalInSub=new Set(),lmodalOriginal=new Set();
async function openSubLinks(sub_id,name){
  currentSubId=sub_id;
  document.getElementById('modal-sub-name').textContent=name;
  document.getElementById('modal-links-body').innerHTML='<div style="color:var(--t3);font-size:12px;padding:20px;text-align:center"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite;font-size:20px"></i></div>';
  document.getElementById('lmodal-search-inp').value='';
  openModal('modal-links');
  try{
    const [lr,sr]=await Promise.all([authF('/api/links'),authF('/api/subs')]);
    const {links=[]}=await lr.json();
    const {subs=[]}=await sr.json();
    const thisSub=subs.find(s=>s.sub_id===sub_id);
    lmodalInSub=new Set(thisSub?.link_ids||[]);
    lmodalOriginal=new Set(thisSub?.link_ids||[]);
    lmodalLinks=links;
    renderLmodalList(links);
  }catch(e){toast('خطا در بارگذاری','err')}
}
function renderLmodalList(links){
  const body=document.getElementById('modal-links-body');
  if(!links.length){body.innerHTML='<div class="empty" style="padding:30px"><i class="ti ti-link-off"></i><p>هنوز کانفیگی وجود ندارد</p></div>';updateLmodalCount();return}
  body.innerHTML=links.map(l=>{
    const checked=lmodalInSub.has(l.uuid);
    const on=l.active&&!l.expired;
    return `<div class="lrow-v2 ${checked?'checked':''}" data-uuid="${l.uuid}" data-name="${esc(l.label).toLowerCase()}" onclick="toggleLrow('${l.uuid}',this)">
      <div class="lrow-v2-check"><i class="ti ti-check"></i></div>
      <div class="lrow-v2-avatar"><i class="ti ti-key"></i></div>
      <div class="lrow-v2-info">
        <div class="lrow-v2-name">${esc(l.label)}</div>
        <div class="lrow-v2-meta"><i class="ti ti-database" style="font-size:10px"></i> ${fmtB(l.used_bytes)}</div>
      </div>
      <span class="lrow-v2-status ${on?'on':'off'}">${on?'فعال':'غیرفعال'}</span>
    </div>`;
  }).join('');
  updateLmodalCount();
}
function toggleLrow(uuid,el){
  if(lmodalInSub.has(uuid)){lmodalInSub.delete(uuid);el.classList.remove('checked')}
  else{lmodalInSub.add(uuid);el.classList.add('checked')}
  updateLmodalCount();
}
function lmodalSelectAll(state){
  lmodalLinks.forEach(l=>{if(state)lmodalInSub.add(l.uuid);else lmodalInSub.delete(l.uuid)});
  renderLmodalList(lmodalLinks);
}
function updateLmodalCount(){
  const el=document.getElementById('lmodal-count');
  if(el)el.textContent=toFa(lmodalInSub.size)+' انتخاب شده';
}
function filterLmodal(q){
  q=q.trim().toLowerCase();
  document.querySelectorAll('#modal-links-body .lrow-v2').forEach(row=>{
    row.style.display = !q || row.dataset.name.includes(q) ? '' : 'none';
  });
}
async function saveSubLinks(){
  if(!currentSubId)return;
  const link_ids=[...lmodalInSub];
  const added=[...lmodalInSub].filter(u=>!lmodalOriginal.has(u));
  const removed=[...lmodalOriginal].filter(u=>!lmodalInSub.has(u));
  try{
    const r=await authF('/api/subs/'+currentSubId,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({link_ids})});
    if(!r.ok)throw new Error();
    await Promise.all([
      ...added.map(uuid=>authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({sub_id:currentSubId})})),
      ...removed.map(uuid=>authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({sub_id:null})})),
    ]);
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
    if(!subs.length){el.innerHTML='<div class="empty"><i class="ti ti-rss-off"></i><p>هنوز گروهی ندارید</p></div>';return}
    el.innerHTML=subs.map(s=>`
      <div style="padding:13px 15px;background:var(--accent-d);border:1px solid var(--card-b);border-radius:10px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap">
        <div>
          <div style="font-weight:700;font-size:13px;margin-bottom:3px">${esc(s.name)}</div>
          <div style="font-family:ui-monospace,monospace;font-size:10px;color:#A78BFA">${esc(s.sub_url)}</div>
          <div style="font-size:10px;color:var(--t3);margin-top:3px">${toFa(s.links_count)} کانفیگ · ${esc(s.total_used_fmt)} مصرف ${s.has_password?'· 🔒 رمزدار':''}</div>
        </div>
        <div style="display:flex;gap:5px;flex-wrap:wrap">
          <button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-copy"></i> ساب</button>
          <button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-globe"></i> پابلیک</button>
          <button class="btn btn-sm btn-g" onclick="showQR('${esc(s.sub_url)}')"><i class="ti ti-qrcode"></i></button>
        </div>
      </div>
    `).join('');
  }catch(e){}
}
function cpSubAll(){navigator.clipboard.writeText(location.protocol+'//'+location.host+'/sub-all').then(()=>toast('کپی شد ✓','ok'))}
function parseBytesFmt(s){
  if(!s)return 0;
  const m=String(s).match(/([\d.]+)\s*([A-Za-z]+)/);
  if(!m)return 0;
  const n=parseFloat(m[1]),u=m[2].toUpperCase();
  const mult={B:1,KB:1024,MB:1024**2,GB:1024**3,TB:1024**4};
  return n*(mult[u]||1);
}
async function loadConns(){
  try{
    const r=await authF('/api/connections'),d=await r.json();
    const grid=document.getElementById('conns-grid'),ce=document.getElementById('conns-empty');
    document.getElementById('conns-live').innerHTML='<span class="dot dg pulse"></span> '+d.count+' اتصال';
    document.getElementById('ch-count').textContent=toFa(d.count);
    const conns=d.connections||[];
    if(!d.count){
      grid.innerHTML='';ce.style.display='block';
      document.getElementById('ch-traffic').textContent='—';
      document.getElementById('ch-avgdur').textContent='—';
      document.getElementById('ch-uniq').textContent='—';
      return;
    }
    ce.style.display='none';
    const totalBytes=conns.reduce((s,c)=>s+parseBytesFmt(c.bytes_fmt),0);
    document.getElementById('ch-traffic').textContent=fmtB(totalBytes);
    const uniqIps=new Set(conns.map(c=>c.ip)).size;
    document.getElementById('ch-uniq').textContent=toFa(uniqIps);
    const durs=conns.map(c=>c.connected_at?Math.max(0,Math.floor((Date.now()-new Date(c.connected_at).getTime())/1000)):0);
    const avgSec=durs.length?Math.floor(durs.reduce((a,b)=>a+b,0)/durs.length):0;
    document.getElementById('ch-avgdur').textContent=avgSec<60?avgSec+' ث':avgSec<3600?Math.floor(avgSec/60)+' د':Math.floor(avgSec/3600)+' س';
    const maxDur=Math.max(...durs,1);
    grid.innerHTML=conns.map(c=>{
      const secs=c.connected_at?Math.max(0,Math.floor((Date.now()-new Date(c.connected_at).getTime())/1000)):0;
      const dur=secs<60?secs+' ثانیه':secs<3600?Math.floor(secs/60)+' دقیقه':Math.floor(secs/3600)+' ساعت';
      const durPct=Math.min(100,Math.round((secs/maxDur)*100));
      const protoVal=c.transport==='vless-ws'?'vless-ws':(c.transport||'').replace('xhttp-','xhttp-');
      return `<div class="conn-card-v2">
        <div class="conn-card-v2-glow"></div>
        <div class="conn-card-v2-top">
          <div class="conn-avatar"><i class="ti ti-device-desktop"></i></div>
          <div class="conn-card-v2-id">
            <div class="conn-ip-v2">${esc(c.ip)}
              <button class="conn-ip-copy" onclick="navigator.clipboard.writeText('${esc(c.ip)}').then(()=>toast('IP کپی شد','ok'))" title="کپی IP"><i class="ti ti-copy"></i></button>
            </div>
            <div class="conn-label-v2">${esc(c.label)}</div>
          </div>
          <span class="conn-status-pill"><span class="dot dg pulse"></span> زنده</span>
        </div>
        <div class="conn-card-v2-divider"></div>
        <div class="conn-card-v2-body">
          <div class="conn-proto-row">${protoBadge(protoVal)}</div>
          <div class="conn-stat-row">
            <div class="conn-stat-box">
              <div class="conn-stat-icon"><i class="ti ti-transfer"></i></div>
              <div>
                <div class="conn-stat-text-label">ترافیک</div>
                <div class="conn-stat-text-val">${esc(c.bytes_fmt)}</div>
              </div>
            </div>
            <div class="conn-stat-box">
              <div class="conn-stat-icon time"><i class="ti ti-clock"></i></div>
              <div>
                <div class="conn-stat-text-label">مدت اتصال</div>
                <div class="conn-stat-text-val">${dur}</div>
              </div>
            </div>
          </div>
          <div class="conn-duration-track"><div class="conn-duration-fill" style="width:${durPct}%"></div></div>
        </div>
      </div>`;
    }).join('');
  }catch(e){console.error(e)}
  loadTopUsage();
}
async function loadTopUsage(){
  try{
    const r=await authF('/api/top-usage?limit=8'),d=await r.json();
    const box=document.getElementById('top-usage-list');
    const rows=d.top_total||[];
    if(!rows.length){box.innerHTML='<div class="empty"><i class="ti ti-chart-bar-off"></i><p>هنوز داده‌ای نیست</p></div>';return}
    box.innerHTML=rows.map((r,i)=>`
      <div class="sr">
        <span class="sr-k" style="gap:8px">
          <span style="width:20px;height:20px;border-radius:6px;background:${i<3?'var(--accent)':'var(--card-b)'};display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;color:#fff">${toFa(i+1)}</span>
          ${esc(r.label)}
          ${r.live_connections>0?`<span style="color:var(--green-t);font-size:10px"><i class="ti ti-plug-connected"></i> ${toFa(r.live_connections)} زنده</span>`:''}
        </span>
        <span class="sr-v" style="font-size:10.5px">${esc(r.used_fmt)} ${r.pct!==null?' · '+r.pct.toFixed(0)+'٪':''}</span>
      </div>
    `).join('');
  }catch(e){}
}
async function loadErrs(){try{const r=await authF('/stats'),d=await r.json();renderErrs(d.recent_errors||[]);}catch(e){}}
async function fetchDefaultVless(){
  try{
    const r=await authF('/api/links'),d=await r.json();
    const links=d.links||[];
    const def=links.find(l=>l.limit_bytes===0&&l.active&&!l.expired)||links.find(l=>l.active&&!l.expired)||links[0];
    document.getElementById('vless-main').textContent=def?def.vless_link:'هنوز کانفیگی وجود ندارد';
  }catch(e){
    console.error('fetchDefaultVless failed:',e);
    document.getElementById('vless-main').textContent='❌ خطا در دریافت کانفیگ — کنسول مرورگر (F12) را چک کنید';
  }
}
function cpText(id){navigator.clipboard.writeText(document.getElementById(id).textContent).then(()=>toast('کپی شد ✓','ok'))}
function qrFor(id){showQR(document.getElementById(id).textContent)}
function refreshAll(){fetchStats();fetchDefaultVless();loadLinks();if(document.getElementById('pg-subgroups').classList.contains('on'))loadSubs();if(document.getElementById('pg-subscriptions').classList.contains('on'))loadSubsPage();if(document.getElementById('pg-connections').classList.contains('on'))loadConns();if(document.getElementById('pg-logs').classList.contains('on'))loadActivity();toast('رفرش شد','ok')}
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
function togglePwField(id,btn){
  const inp=document.getElementById(id);
  const icon=btn.querySelector('i');
  const toText=inp.type==='password';
  inp.type=toText?'text':'password';
  icon.className='ti '+(toText?'ti-eye-off':'ti-eye');
}
function checkPwStrength(val){
  const segs=document.querySelectorAll('#pw-strength-bar .pw-strength-seg');
  const label=document.getElementById('pw-strength-label');
  const reqLen=document.getElementById('req-len'),reqNum=document.getElementById('req-num'),reqCase=document.getElementById('req-case');
  const hasLen=val.length>=4,hasNum=/\d/.test(val),hasCase=/[a-z]/.test(val)&&/[A-Z]/.test(val),hasLong=val.length>=8;
  reqLen.classList.toggle('met',hasLen);
  reqNum.classList.toggle('met',hasNum);
  reqCase.classList.toggle('met',hasCase);
  let score=0;if(hasLen)score++;if(hasNum)score++;if(hasCase)score++;if(hasLong)score++;
  const colors=['#EF4444','#F59E0B','#3B82F6','#10B981'],labels=['خیلی ضعیف','ضعیف','متوسط','قوی'];
  segs.forEach((s,i)=>{s.style.background=i<score?colors[Math.max(0,score-1)]:'rgba(100,116,139,.2)'});
  if(val.length===0){label.innerHTML='<i class="ti ti-shield"></i> قدرت رمز';return}
  label.innerHTML=`<i class="ti ti-shield-check" style="color:${colors[Math.max(0,score-1)]}"></i> ${labels[Math.max(0,score-1)]}`;
}
function makeGradient(ctx,color1,color2){
  const g=ctx.createLinearGradient(0,0,0,260);
  g.addColorStop(0,color1);g.addColorStop(1,color2);
  return g;
}
function initCharts(){
  const c1=document.getElementById('ch1').getContext('2d');
  const grad1=makeGradient(c1,'rgba(59,130,246,.38)','rgba(59,130,246,0)');
  const opts={
    responsive:true,maintainAspectRatio:false,
    interaction:{mode:'index',intersect:false},
    plugins:{
      legend:{display:false},
      tooltip:{
        backgroundColor:'rgba(13,27,46,.96)',borderColor:'rgba(59,130,246,.3)',borderWidth:1,
        titleColor:'#E8F4FF',bodyColor:'#7BAED4',padding:11,cornerRadius:10,displayColors:false,
        titleFont:{family:'Vazirmatn',size:11,weight:'700'},bodyFont:{family:'Vazirmatn',size:11},
        callbacks:{label:v=>`${v.parsed.y.toFixed(2)} مگابایت`}
      }
    },
    scales:{
      x:{grid:{display:false},border:{display:false},ticks:{color:'#3D6B8E',font:{size:9,family:'Vazirmatn'}}},
      y:{grid:{color:'rgba(59,130,246,.06)'},border:{display:false},ticks:{color:'#3D6B8E',font:{size:9,family:'Vazirmatn'},callback:v=>v+' MB'}}
    },
    elements:{line:{capBezierPoints:true}}
  };
  const ds1={label:'MB',data:[],borderColor:'#3B82F6',backgroundColor:grad1,fill:true,tension:.42,pointRadius:0,pointHoverRadius:6,pointHoverBackgroundColor:'#3B82F6',pointHoverBorderColor:'#fff',pointHoverBorderWidth:2,borderWidth:2.5};
  ch1=new Chart(document.getElementById('ch1'),{type:'line',data:{labels:[],datasets:[ds1]},options:opts});

  function makeGradientV2(ctx,c1,c2,c3){
    const g=ctx.createLinearGradient(0,0,0,320);
    g.addColorStop(0,c1);g.addColorStop(.6,c2);g.addColorStop(1,c3);
    return g;
  }
  const c3ctx=document.getElementById('ch3').getContext('2d');
  const gradFill3=makeGradientV2(c3ctx,'rgba(59,130,246,.45)','rgba(59,130,246,.08)','rgba(59,130,246,0)');
  ch3=new Chart(document.getElementById('ch3'),{
    type:'line',
    data:{labels:[],datasets:[
      {label:'مصرف',data:[],borderColor:'#3B82F6',backgroundColor:gradFill3,fill:true,tension:.45,pointRadius:0,pointHoverRadius:7,pointHoverBackgroundColor:'#fff',pointHoverBorderColor:'#3B82F6',pointHoverBorderWidth:3,borderWidth:3,order:2},
      {label:'میانگین',data:[],borderColor:'#F59E0B',borderDash:[6,5],borderWidth:1.6,pointRadius:0,fill:false,tension:0,order:1}
    ]},
    options:{
      responsive:true,maintainAspectRatio:false,
      interaction:{mode:'index',intersect:false},
      plugins:{
        legend:{display:false},
        tooltip:{
          backgroundColor:'rgba(13,27,46,.97)',borderColor:'rgba(59,130,246,.35)',borderWidth:1,
          titleColor:'#E8F4FF',bodyColor:'#9DC3E8',padding:13,cornerRadius:12,displayColors:true,boxPadding:4,
          titleFont:{family:'Vazirmatn',size:11.5,weight:'700'},bodyFont:{family:'Vazirmatn',size:11},
          callbacks:{label:v=>` ${v.dataset.label}: ${v.parsed.y.toFixed(2)} MB`}
        }
      },
      scales:{
        x:{grid:{display:false},border:{display:false},ticks:{color:'#3D6B8E',font:{size:9.5,family:'Vazirmatn'},maxRotation:0}},
        y:{grid:{color:'rgba(59,130,246,.05)'},border:{display:false},ticks:{color:'#3D6B8E',font:{size:9.5,family:'Vazirmatn'},callback:v=>v+' MB'}}
      }
    }
  });

  ch2=new Chart(document.getElementById('ch2'),{
    type:'doughnut',
    data:{labels:['VLESS/WS','XHTTP Ultra','HTTP Proxy'],datasets:[{
      data:[55,35,10],
      backgroundColor:['#3B82F6','#10B981','#8B5CF6'],
      borderColor:getComputedStyle(document.documentElement).getPropertyValue('--card')||'#0d1b2e',
      borderWidth:4,hoverOffset:10,borderRadius:6,spacing:3
    }]},
    options:{
      responsive:true,maintainAspectRatio:false,cutout:'72%',
      plugins:{
        legend:{position:'bottom',labels:{color:'var(--t2)',font:{size:10,family:'Vazirmatn'},padding:12,usePointStyle:true,pointStyle:'circle'}},
        tooltip:{backgroundColor:'rgba(13,27,46,.96)',borderColor:'rgba(59,130,246,.3)',borderWidth:1,padding:10,cornerRadius:10,bodyFont:{family:'Vazirmatn'},titleFont:{family:'Vazirmatn'}}
      }
    }
  });
}
let ws;
function wsLog(c,m){const l=document.getElementById('ws-log'),p=document.createElement('p');const colors={ok:'#34D399',err:'#F87171',info:'#7BAED4',sent:'#FCD34D'};p.style.color=colors[c]||'#fff';p.textContent='['+new Date().toLocaleTimeString('fa-IR')+'] '+m;l.appendChild(p);l.scrollTop=l.scrollHeight}
function wsConn(){const u=document.getElementById('ws-uuid').value.trim();if(!u){toast('UUID را وارد کنید','err');return}const url=(location.protocol==='https:'?'wss':'ws')+'://'+location.host+'/ws/'+u;wsLog('info','اتصال: '+url);ws=new WebSocket(url);ws.onopen=()=>wsLog('ok','✓ متصل - UUID معتبر');ws.onerror=()=>wsLog('err','✗ خطا - UUID نامعتبر یا غیرفعال');ws.onmessage=m=>wsLog('info','دریافت '+(m.data.size||m.data.length)+' byte');ws.onclose=e=>wsLog('err','قطع ('+e.code+')'+(e.code===1008?' - دسترسی رد شد':''))}
function wsSend(){const m=document.getElementById('ws-msg').value;if(!m||!ws||ws.readyState!==1)return;ws.send(m);wsLog('sent','ارسال: '+m);document.getElementById('ws-msg').value=''}
function wsDisc(){if(ws)ws.close()}

async function loadTelegramSettings(){
  try{
    const r=await authF('/api/settings/telegram'),d=await r.json();
    document.getElementById('tg-enabled').checked=!!d.enabled;
    document.getElementById('tg-token').value=d.bot_token_masked||'';
    document.getElementById('tg-chatid').value=d.chat_id||'';
    document.getElementById('tg-quota-pct').value=d.notify_quota_pct||90;
    document.getElementById('tg-exp-hours').value=d.notify_expiry_hours||24;
    document.getElementById('tg-api-ip').value=d.api_ip||'';
  }catch(e){}
}
async function saveTelegramSettings(){
  const body={
    enabled:document.getElementById('tg-enabled').checked,
    chat_id:document.getElementById('tg-chatid').value.trim(),
    notify_quota_pct:Number(document.getElementById('tg-quota-pct').value||90),
    notify_expiry_hours:Number(document.getElementById('tg-exp-hours').value||24),
    api_ip:document.getElementById('tg-api-ip').value.trim(),
  };
  const tokenVal=document.getElementById('tg-token').value.trim();
  if(tokenVal&&!tokenVal.includes('…'))body.bot_token=tokenVal;
  try{
    const r=await authF('/api/settings/telegram',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!r.ok)throw new Error();
    toast('تنظیمات ذخیره شد ✓','ok');
    loadTelegramSettings();
  }catch(e){toast('خطا در ذخیره','err')}
}
async function testTelegram(){
  try{
    const r=await authF('/api/settings/telegram/test',{method:'POST'});
    const d=await r.json().catch(()=>({}));
    if(!r.ok){toast(d.detail||'ارسال ناموفق بود','err');return}
    toast('پیام تست ارسال شد ✓ چک کن تلگرامت','ok');
  }catch(e){toast('خطا در ارسال تست','err')}
}

// 🌐 تنظیمات عمومی - جدید
async function loadPublicSettings() {
  try {
    const r = await authF('/api/settings/public');
    const d = await r.json();
    document.getElementById('pub-create').checked = d.allow_public_create !== false;
    document.getElementById('pub-delete').checked = d.allow_public_delete !== false;
    document.getElementById('pub-toggle').checked = d.allow_public_toggle !== false;
  } catch(e) { console.error(e); }
}

async function savePublicSettings() {
  const body = {
    allow_public_create: document.getElementById('pub-create').checked,
    allow_public_delete: document.getElementById('pub-delete').checked,
    allow_public_toggle: document.getElementById('pub-toggle').checked,
  };
  try {
    const r = await authF('/api/settings/public', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    });
    if (!r.ok) throw new Error();
    toast('تنظیمات ذخیره شد ✓', 'ok');
  } catch(e) {
    toast('خطا در ذخیره', 'err');
  }
}

async function loadJoinSettings() {
  try {
    const r = await authF('/api/settings/join');
    const d = await r.json();
    document.getElementById('join-enabled').checked = !!d.enabled;
    document.getElementById('join-channel').value = d.channel_username || 'TimAzadi';
    document.getElementById('join-channel-required').checked = d.channel_required !== false;
    document.getElementById('join-grant-gb').value = d.grant_gb ?? 100;
    document.getElementById('join-grant-days').value = d.grant_days ?? 0;
    document.getElementById('join-bot-username').value = d.bot_username || '';
  } catch(e) {
    console.error('loadJoinSettings error:', e);
  }
}

async function saveJoinSettings() {
  const body = {
    enabled: document.getElementById('join-enabled').checked,
    channel_username: document.getElementById('join-channel').value.trim(),
    channel_required: document.getElementById('join-channel-required').checked,
    grant_gb: Number(document.getElementById('join-grant-gb').value) || 0,
    grant_days: Number(document.getElementById('join-grant-days').value) || 0,
    bot_username: document.getElementById('join-bot-username').value.trim(),
  };

  try {
    const r = await authF('/api/settings/join', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    });
    if (!r.ok) throw new Error();
    toast('تنظیمات ذخیره شد ✓', 'ok');
    loadJoinSettings();
  } catch(e) {
    toast('خطا در ذخیره', 'err');
  }
}

let dailyChartInstance=null;
async function openDailyChart(uuid,label){
  document.getElementById('dc-title').textContent=label;
  openModal('modal-daily-chart');
  try{
    const r=await authF('/api/links/'+uuid+'/daily?days=14'),{days=[]}=await r.json();
    const ctx=document.getElementById('dc-canvas');
    if(dailyChartInstance)dailyChartInstance.destroy();
    dailyChartInstance=new Chart(ctx,{
      type:'bar',
      data:{
        labels:days.map(d=>new Date(d.date).toLocaleDateString('fa-IR',{month:'short',day:'numeric'})),
        datasets:[{label:'مصرف روزانه',data:days.map(d=>d.bytes/1024/1024),backgroundColor:'rgba(124,92,255,.55)',borderRadius:6}]
      },
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{ticks:{callback:v=>v+' MB'}}}}
    });
  }catch(e){}
}
document.addEventListener('DOMContentLoaded',async()=>{
  await checkAuth();
  initCharts();
  document.getElementById('set-host').textContent=location.host;
  document.getElementById('sub-all-url')&&(document.getElementById('sub-all-url').textContent=location.protocol+'//'+location.host+'/sub-all');
  loadTelegramSettings();
  loadJoinSettings();
  loadPublicSettings();
  fetchStats();fetchDefaultVless();loadLinks();loadSubs();
  setInterval(fetchStats,4000);
  setInterval(()=>{
    if(document.getElementById('pg-links').classList.contains('on'))loadLinks();
    if(document.getElementById('pg-subgroups').classList.contains('on'))loadSubs();
    if(document.getElementById('pg-subscriptions').classList.contains('on'))loadSubsPage();
    if(document.getElementById('pg-connections').classList.contains('on'))loadConns();
    if(document.getElementById('pg-logs').classList.contains('on'))loadActivity();
  },5000);
});
</script>
</body></html>""".replace("{{LOGO}}", LOGO_DATA_URI)


def get_public_page_html(uuid_key: str, white_label: bool = False) -> str:
    page_title = "کانفیگ‌های من" if white_label else "تیم آزادی Sub"
    header_html = "" if white_label else f"""
    <div class="brand">
      <div class="brand-img"><img src="{LOGO_DATA_URI}" alt="تیم آزادی"></div>
      <div><div class="brand-name">تیم آزادی</div><div class="brand-sub">تیم آزادی Gateway · v10.0</div></div>
    </div>"""
    telegram_btn_html = "" if white_label else '<a class="icon-btn" href="https://t.me/TimAzadi" target="_blank" title="کانال تلگرام"><i class="ti ti-brand-telegram"></i></a>'
    footer_html = "" if white_label else '<div class="footer">کانال رسمی: <a href="https://t.me/TimAzadi" target="_blank">@TimAzadi</a> · تیم آزادی Gateway v10.0</div>'
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>{page_title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
:root{{
  --bg:#060a14;--bg2:#0a1020;--bg3:#0d1428;
  --card:#0c1326;--card-b:rgba(96,148,246,0.12);--card-bh:rgba(96,148,246,0.28);
  --accent:#3B7CF6;--accent2:#6EA3FF;--accent-d:rgba(59,124,246,0.1);
  --green:#1FB87E;--green-bg:rgba(31,184,126,0.1);--green-t:#3FD79C;
  --red:#EF4444;--red-bg:rgba(239,68,68,0.1);--red-t:#FB8585;
  --amber:#F2A33D;--amber-bg:rgba(242,163,61,0.1);--amber-t:#F9C988;
  --purple:#9D7BF0;--purple-bg:rgba(157,123,240,0.1);--purple-t:#BCA4F7;
  --t1:#EFF4FF;--t2:#8AA0C4;--t3:#48577A;
  --radius:18px;--shadow:0 12px 40px rgba(0,0,0,0.45);
  --serif:'Vazirmatn',sans-serif;
}}
[data-theme="light"]{{
  --bg:#F0F3FA;--bg2:#E5ECF8;--bg3:#D9E3F4;
  --card:#FFFFFF;--card-b:rgba(59,124,246,0.14);--card-bh:rgba(59,124,246,0.32);
  --accent:#2E63D6;--accent2:#1E4CB8;--accent-d:rgba(46,99,214,0.08);
  --green:#0E9A6A;--green-bg:rgba(14,154,106,0.08);--green-t:#0A7553;
  --red:#DC2626;--red-bg:rgba(220,38,38,0.08);--red-t:#A51E1E;
  --amber:#C97A12;--amber-bg:rgba(201,122,18,0.08);--amber-t:#8F5A0C;
  --purple:#7350D6;--purple-bg:rgba(115,80,214,0.08);--purple-t:#5A3CAD;
  --t1:#101A30;--t2:#48577A;--t3:#8694B0;
  --shadow:0 12px 36px rgba(20,40,90,0.12);
}}
html,body{{min-height:100%;background:var(--bg);font-family:var(--serif);color:var(--t1);font-size:14px;transition:background .35s,color .35s}}
.bg-fx{{position:fixed;inset:0;background:radial-gradient(ellipse 70% 45% at 50% -8%,rgba(59,124,246,0.13),transparent 62%),var(--bg);z-index:0;pointer-events:none;transition:background .35s}}
.grid-fx{{position:fixed;inset:0;background-image:linear-gradient(rgba(96,148,246,0.025) 1px,transparent 1px),linear-gradient(90deg,rgba(96,148,246,0.025) 1px,transparent 1px);background-size:46px 46px;z-index:0;pointer-events:none}}
.wrap{{position:relative;z-index:10;max-width:800px;margin:0 auto;padding:24px 16px 64px}}
.top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:26px;gap:10px}}
.brand{{display:flex;align-items:center;gap:11px;min-width:0}}
.brand-img{{width:40px;height:40px;border-radius:12px;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 0 1px rgba(255,255,255,.02);flex-shrink:0}}
.brand-img img{{width:100%;height:100%;object-fit:cover}}
.brand-name{{font-size:14.5px;font-weight:800;color:var(--t1);letter-spacing:-.01em}}
.brand-sub{{font-size:9.5px;color:var(--t3);font-weight:500}}
.top-actions{{display:flex;align-items:center;gap:6px;flex-shrink:0}}
.icon-btn{{width:36px;height:36px;border-radius:11px;background:var(--card);border:1px solid var(--card-b);color:var(--t2);display:flex;align-items:center;justify-content:center;font-size:16px;cursor:pointer;transition:.18s}}
.icon-btn:hover{{background:var(--accent-d);color:var(--accent2);border-color:var(--card-bh)}}

.sub-info{{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:24px 24px 22px;margin-bottom:16px;box-shadow:var(--shadow);position:relative;overflow:hidden}}
.sub-info::before{{content:'';position:absolute;top:0;right:0;width:160px;height:160px;background:radial-gradient(circle at top right,rgba(59,124,246,.1),transparent 70%);pointer-events:none}}
.sub-eyebrow{{font-size:10px;font-weight:700;color:var(--accent2);text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px;display:flex;align-items:center;gap:6px}}
.sub-eyebrow i{{font-size:13px}}
.sub-name{{font-size:23px;font-weight:800;color:var(--t1);margin-bottom:6px;letter-spacing:-.02em}}
.sub-desc{{font-size:12.5px;color:var(--t2);line-height:1.8;margin-bottom:14px}}
.sub-meta-row{{font-size:10.5px;color:var(--t3);margin-bottom:14px;display:flex;align-items:center;gap:6px}}
.sub-sub-box{{background:var(--accent-d);border:1px solid var(--card-b);border-radius:13px;padding:12px 14px;display:flex;align-items:center;gap:9px;flex-wrap:wrap}}
.sub-sub-url{{font-family:ui-monospace,monospace;font-size:10px;color:var(--accent2);word-break:break-all;flex:1;min-width:140px}}

.stats-bar{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px}}
.stat-card{{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:16px 17px;transition:.2s}}
.stat-card:hover{{border-color:var(--card-bh);transform:translateY(-1px)}}
.stat-label{{font-size:9px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.07em;margin-bottom:7px}}
.stat-val{{font-size:22px;font-weight:800;color:var(--t1);line-height:1;letter-spacing:-.01em}}
.stat-sub{{font-size:9.5px;color:var(--t3);margin-top:6px}}

.copy-all-bar{{display:flex;align-items:center;gap:12px;background:linear-gradient(120deg,var(--accent) 0%,#2952C8 100%);border-radius:18px;padding:16px 19px;margin-bottom:18px;box-shadow:0 10px 30px rgba(59,124,246,.28);flex-wrap:wrap}}
.copy-all-text{{flex:1;min-width:160px}}
.copy-all-title{{font-size:13.5px;font-weight:800;color:#fff;display:flex;align-items:center;gap:6px}}
.copy-all-sub{{font-size:10px;color:rgba(255,255,255,.78);margin-top:3px}}
.copy-all-btn{{background:#fff;color:#1D4ED8;border:none;border-radius:12px;padding:10px 19px;font-family:inherit;font-size:12.5px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:6px;transition:.18s;white-space:nowrap}}
.copy-all-btn:hover{{transform:translateY(-1px);box-shadow:0 6px 16px rgba(0,0,0,.22)}}
.copy-all-btn:active{{transform:translateY(0) scale(.98)}}

.pool-card{{background:linear-gradient(135deg,rgba(157,123,240,.14),rgba(59,124,246,.06));border:1px solid rgba(157,123,240,.28);border-radius:20px;padding:20px 22px;margin-bottom:16px;position:relative;overflow:hidden}}
.pool-head{{display:flex;align-items:center;gap:8px;margin-bottom:12px}}
.pool-head i{{font-size:17px;color:var(--purple-t)}}
.pool-head span{{font-size:13px;font-weight:800;color:var(--t1)}}
.pool-gauge{{height:9px;border-radius:6px;background:rgba(157,123,240,.14);overflow:hidden;margin-bottom:9px}}
.pool-gauge-f{{height:100%;border-radius:6px;background:linear-gradient(90deg,var(--purple),var(--accent));transition:width .5s ease}}
.pool-txt{{font-size:11px;color:var(--t2);display:flex;justify-content:space-between;margin-bottom:14px}}
.split-form{{display:grid;grid-template-columns:1fr 90px;gap:8px;margin-bottom:10px}}
.split-form input,.split-form select{{font-family:inherit;font-size:12.5px;padding:10px 12px;border-radius:11px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);outline:none}}
[data-theme="light"] .split-form input,[data-theme="light"] .split-form select{{background:rgba(46,99,214,.04)}}
.split-form input:focus,.split-form select:focus{{border-color:var(--purple);box-shadow:0 0 0 3px var(--purple-bg)}}
.split-form-row2{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}}
.split-err{{color:var(--red-t);font-size:11px;margin-bottom:10px;display:none;align-items:center;gap:5px}}
.split-err.show{{display:flex}}
.split-result{{background:var(--green-bg);border:1px solid rgba(31,184,126,.3);border-radius:14px;padding:14px 16px;margin-top:12px;display:none}}
.split-result.show{{display:block}}
.split-result-title{{font-size:12px;font-weight:800;color:var(--green-t);display:flex;align-items:center;gap:6px;margin-bottom:9px}}
.split-result-url{{font-family:ui-monospace,monospace;font-size:10px;color:var(--t2);word-break:break-all;background:rgba(0,0,0,.15);border-radius:9px;padding:9px 11px;margin-bottom:9px}}
[data-theme="light"] .split-result-url{{background:rgba(0,0,0,.04)}}

.cfg-title{{font-size:12px;font-weight:800;color:var(--t2);margin-bottom:13px;display:flex;align-items:center;gap:6px;text-transform:uppercase;letter-spacing:.07em}}
.cfg-title i{{color:var(--accent);font-size:15px}}
.cfg-grid{{display:grid;gap:13px}}

.cfg-card{{background:var(--card);border:1px solid var(--card-b);border-radius:18px;transition:all .2s;position:relative;overflow:hidden}}
.cfg-card:hover{{border-color:var(--card-bh);box-shadow:var(--shadow)}}
.cfg-top{{padding:17px 19px 15px;position:relative}}
.cfg-top::after{{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--green)}}
.cfg-card.inactive .cfg-top::after{{background:var(--red)}}
.cfg-head{{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:12px;flex-wrap:wrap}}
.cfg-label{{font-size:14.5px;font-weight:700;color:var(--t1)}}
.cfg-badges{{display:flex;gap:5px;flex-wrap:wrap;margin-top:6px}}
.proto-chip{{font-size:9px;padding:3px 8px;border-radius:7px;font-weight:800;letter-spacing:.02em}}
.pc-ws{{background:var(--accent-d);color:var(--accent2)}}
.pc-xhttp{{background:var(--purple-bg);color:var(--purple-t)}}
.pc-ultra{{background:var(--green-bg);color:var(--green-t)}}
.pc-trojan{{background:rgba(239,68,68,.14);color:#f87171}}
.cfg-status{{display:flex;align-items:center;gap:5px;font-size:10px;font-weight:700;padding:4px 10px;border-radius:20px;white-space:nowrap}}
.cfg-status.ok{{background:var(--green-bg);color:var(--green-t)}}
.cfg-status.no{{background:var(--red-bg);color:var(--red-t)}}
.cfg-usage{{margin-bottom:4px}}
.ubar{{height:6px;border-radius:4px;background:rgba(96,148,246,0.1);overflow:hidden;margin-bottom:5px}}
.ubar-f{{height:100%;border-radius:4px;transition:width .5s ease}}
.utxt{{font-size:10px;color:var(--t3);display:flex;justify-content:space-between}}

.cfg-timer{{display:flex;align-items:center;gap:8px;margin-top:10px;padding:9px 12px;border-radius:12px;
  background:rgba(255,255,255,0.06);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  border:1px solid rgba(255,255,255,0.1);}}
[data-theme="light"] .cfg-timer{{background:rgba(255,255,255,0.55);border-color:rgba(46,99,214,0.14);box-shadow:0 4px 14px rgba(20,40,90,0.06)}}
.cfg-timer i{{font-size:14px;color:var(--accent2);flex-shrink:0}}
.cfg-timer-grid{{display:flex;gap:9px;font-family:ui-monospace,monospace;flex:1}}
.cfg-timer-seg{{display:flex;flex-direction:column;align-items:center;min-width:26px}}
.cfg-timer-val{{font-size:12.5px;font-weight:800;color:var(--t1)}}
.cfg-timer-lbl{{font-size:8px;color:var(--t3);font-weight:700}}
.cfg-timer.expiring .cfg-timer-val{{color:var(--red-t)}}

.locked-banner{{display:flex;align-items:center;gap:10px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);color:var(--red-t);border-radius:16px;padding:14px 18px;margin-bottom:16px;font-size:12.5px;font-weight:700}}
.locked-banner i{{font-size:18px;flex-shrink:0}}

.children-box{{margin-top:13px;padding-top:12px;border-top:1px dashed var(--card-b)}}
.children-title{{font-size:10.5px;font-weight:800;color:var(--t3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px;display:flex;align-items:center;gap:5px}}
.child-row{{display:flex;align-items:center;justify-content:space-between;gap:8px;background:rgba(255,255,255,.05);backdrop-filter:blur(8px);border:1px solid var(--card-b);border-radius:11px;padding:8px 11px;margin-bottom:6px}}
[data-theme="light"] .child-row{{background:rgba(255,255,255,.6)}}
.child-row-name{{font-size:11.5px;font-weight:700;color:var(--t1)}}
.child-row-meta{{font-size:9.5px;color:var(--t3);margin-top:2px}}
.child-row-actions{{display:flex;gap:5px;flex-shrink:0}}
.child-btn{{width:26px;height:26px;border-radius:8px;border:none;background:var(--accent-d);color:var(--accent2);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:12px;transition:.15s}}
.child-btn.danger{{background:var(--red-bg);color:var(--red-t)}}
.child-btn:hover{{filter:brightness(1.15)}}
.child-btn:disabled{{opacity:.35;cursor:not-allowed}}

.cfg-tear{{position:relative;height:0;border-top:1.5px dashed var(--card-b);margin:0 19px}}
.cfg-tear::before,.cfg-tear::after{{content:'';position:absolute;top:50%;width:18px;height:18px;border-radius:50%;background:var(--bg);transform:translateY(-50%);border:1px solid var(--card-b)}}
.cfg-tear::before{{right:-28px}}
.cfg-tear::after{{left:-28px}}

.cfg-bottom{{padding:15px 19px 18px}}
.cfg-link-toggle{{width:100%;display:flex;align-items:center;justify-content:space-between;gap:10px;background:transparent;border:1px dashed var(--card-b);border-radius:11px;padding:10px 13px;cursor:pointer;font-family:inherit;color:var(--t2);font-size:11.5px;font-weight:600;transition:.15s}}
.cfg-link-toggle:hover{{background:var(--accent-d);border-color:var(--card-bh);color:var(--accent2)}}
.cfg-link-toggle .ltl{{display:flex;align-items:center;gap:7px}}
.cfg-link-toggle i.ti-chevron-down{{transition:transform .2s}}
.cfg-link-toggle.open i.ti-chevron-down{{transform:rotate(180deg)}}
.cfg-vless-wrap{{display:grid;grid-template-rows:0fr;transition:grid-template-rows .25s ease}}
.cfg-vless-wrap.open{{grid-template-rows:1fr}}
.cfg-vless-inner{{overflow:hidden}}
.cfg-vless{{background:rgba(0,0,0,.22);border:1px solid var(--card-b);border-radius:10px;padding:11px 13px;font-size:9.8px;font-family:ui-monospace,monospace;color:var(--accent2);word-break:break-all;line-height:1.7;margin-top:9px;max-height:90px;overflow-y:auto}}
[data-theme="light"] .cfg-vless{{background:rgba(46,99,214,.05)}}
.cfg-actions{{display:flex;gap:7px;flex-wrap:wrap;margin-top:11px}}
.btn{{font-family:inherit;font-size:11.5px;font-weight:700;border-radius:10px;padding:8px 15px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s;white-space:nowrap}}
.btn i{{font-size:13px}}
.btn-p{{background:var(--accent);color:#fff;box-shadow:0 3px 12px rgba(59,124,246,.3)}}
.btn-p:hover{{background:var(--accent2)}}
.btn-g{{background:var(--accent-d);color:var(--accent2);border:1px solid rgba(96,148,246,.16)}}
.btn-g:hover{{background:rgba(96,148,246,.2)}}
.btn-pur{{background:var(--purple-bg);color:var(--purple-t);border:1px solid rgba(157,123,240,.2)}}
.btn-pur:hover{{background:rgba(157,123,240,.22)}}
.conn-chip{{display:inline-flex;align-items:center;gap:4px;font-size:9.5px;padding:3px 8px;border-radius:20px;background:var(--green-bg);color:var(--green-t);font-weight:700}}
.dot{{width:5px;height:5px;border-radius:50%;background:var(--green);display:inline-block;animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}

.lock-stage{{display:flex;align-items:center;justify-content:center;min-height:78vh;padding:20px 0}}
.lock-card{{background:var(--card);border:1px solid var(--card-b);border-radius:26px;padding:0;text-align:center;max-width:380px;width:100%;box-shadow:var(--shadow);overflow:hidden;position:relative}}
.lock-banner{{background:linear-gradient(150deg,rgba(59,124,246,.16),rgba(59,124,246,.02) 70%);padding:38px 30px 26px;position:relative}}
.lock-shield{{width:64px;height:64px;border-radius:18px;background:var(--accent-d);border:1px solid var(--card-bh);display:flex;align-items:center;justify-content:center;margin:0 auto 18px;position:relative}}
.lock-shield::after{{content:'';position:absolute;inset:-7px;border-radius:22px;border:1px solid var(--card-b);animation:breathe 2.6s ease-in-out infinite}}
@keyframes breathe{{0%,100%{{transform:scale(1);opacity:.5}}50%{{transform:scale(1.08);opacity:0}}}}
.lock-shield i{{font-size:28px;color:var(--accent2)}}
.lock-title{{font-size:18px;font-weight:800;margin-bottom:6px;color:var(--t1);letter-spacing:-.01em}}
.lock-sub{{font-size:12px;color:var(--t3);line-height:1.7}}
.lock-form{{padding:24px 30px 30px}}
.lock-field{{position:relative;margin-bottom:13px}}
.lock-inp{{width:100%;padding:13px 44px 13px 44px;border-radius:13px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:14px;outline:none;text-align:center;letter-spacing:.14em;transition:.18s}}
[data-theme="light"] .lock-inp{{background:rgba(46,99,214,.04)}}
.lock-inp:focus{{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-d)}}
.lock-eye{{position:absolute;left:13px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--t3);cursor:pointer;font-size:16px;padding:4px;display:flex}}
.lock-eye:hover{{color:var(--accent2)}}
.lock-lockicon{{position:absolute;right:14px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:15px;pointer-events:none}}
.lock-err{{color:var(--red-t);font-size:11.5px;margin-bottom:10px;min-height:16px;display:flex;align-items:center;justify-content:center;gap:5px}}
.lock-btn{{width:100%;justify-content:center;padding:13px;font-size:13px;border-radius:13px}}
.lock-footer{{padding:14px 30px;border-top:1px solid var(--card-b);font-size:10px;color:var(--t3);display:flex;align-items:center;justify-content:center;gap:6px}}

.empty-state{{text-align:center;padding:80px 20px;color:var(--t3)}}
.empty-state i{{font-size:38px;display:block;margin-bottom:14px}}

.toast{{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:12px;padding:10px 20px;font-size:12.5px;font-weight:600;opacity:0;transition:all .25s;z-index:999;pointer-events:none;display:flex;align-items:center;gap:7px;box-shadow:var(--shadow);white-space:nowrap}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
.toast.ok{{border-color:rgba(31,184,126,.35);background:var(--green-bg);color:var(--green-t)}}

.qr-modal{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.72);z-index:600;align-items:center;justify-content:center;backdrop-filter:blur(6px);padding:20px}}
.qr-modal.open{{display:flex}}
.qr-box{{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:26px;text-align:center;max-width:340px;width:100%;box-shadow:var(--shadow)}}
.qr-title{{font-size:13.5px;font-weight:800;margin-bottom:16px;color:var(--t1)}}
.qr-img{{border-radius:14px;overflow:hidden;margin-bottom:15px}}
.qr-img img{{width:100%;display:block;background:#fff;padding:10px;border-radius:14px}}

.footer{{text-align:center;padding-top:28px;font-size:10.5px;color:var(--t3)}}
.footer a{{color:var(--accent2);font-weight:700}}

@media(max-width:520px){{
  .stats-bar{{grid-template-columns:1fr 1fr}}
  .stats-bar .stat-card:nth-child(3){{grid-column:1/-1}}
  .sub-name{{font-size:19px}}
  .copy-all-bar{{flex-direction:column;align-items:stretch}}
  .copy-all-btn{{justify-content:center}}
  .wrap{{padding:16px 12px 50px}}
  .lock-banner{{padding:32px 22px 22px}}
  .lock-form{{padding:20px 22px 26px}}
}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
</style>
</head>
<body>
<div class="bg-fx"></div><div class="grid-fx"></div>
<div class="toast" id="toast"></div>
<div class="qr-modal" id="qr-modal" onclick="this.classList.remove('open')">
  <div class="qr-box" onclick="event.stopPropagation()">
    <div class="qr-title" id="qr-label">QR Code</div>
    <div class="qr-img"><img id="qr-img" src="" alt="QR"></div>
    <button class="btn btn-g" style="width:100%;justify-content:center" onclick="document.getElementById('qr-modal').classList.remove('open')"><i class="ti ti-x"></i> بستن</button>
  </div>
</div>
<div class="wrap">
  <div class="top">
    {header_html}
    <div class="top-actions">
      <button class="icon-btn" id="theme-toggle" onclick="toggleTheme()" title="تغییر تم"><i class="ti ti-sun" id="theme-icon"></i></button>
      {telegram_btn_html}
    </div>
  </div>
  <div id="root">
    <div class="empty-state"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i>در حال بارگذاری...</div>
  </div>
  {footer_html}
</div>
<script>
const UUID_KEY='{uuid_key}';
const WHITE_LABEL={str(white_label).lower()};
let savedPw='';

let isDark=localStorage.getItem('rvg-pub-theme')!=='light';
function applyTheme(dark){{
  document.documentElement.setAttribute('data-theme',dark?'dark':'light');
  document.getElementById('theme-icon').className='ti '+(dark?'ti-sun':'ti-moon');
}}
function toggleTheme(){{isDark=!isDark;localStorage.setItem('rvg-pub-theme',isDark?'dark':'light');applyTheme(isDark)}}
applyTheme(isDark);

function toast(msg,type=''){{
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2400);
}}
function esc(s){{return String(s||'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]))}}
function fmtB(b){{if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}}
function toFa(n){{return String(n).replace(/\\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d])}}
function protoChip(p){{
  if(p==='xhttp-stream-one')return '<span class="proto-chip pc-ultra"><i class="ti ti-bolt"></i> XHTTP ULTRA</span>';
  if(p&&p.startsWith('xhttp'))return '<span class="proto-chip pc-xhttp">'+esc(p)+'</span>';
  return '<span class="proto-chip pc-ws">VLESS · WS</span>';
}}

function showQR(label,link){{
  document.getElementById('qr-label').textContent=label;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(link);
  document.getElementById('qr-modal').classList.add('open');
}}

function toggleLink(i){{
  const wrap=document.getElementById('vw-'+i);
  const btn=document.getElementById('vt-'+i);
  const open=wrap.classList.toggle('open');
  btn.classList.toggle('open',open);
  btn.querySelector('.ltl span').textContent = open ? 'پنهان کردن لینک' : 'نمایش لینک کانفیگ';
}}

async function loadData(pw=''){{
  const url='/api/public/sub/'+UUID_KEY+(pw?'?pw='+encodeURIComponent(pw):'');
  const r=await fetch(url);
  return r.json();
}}

function renderLock(name,errMsg=''){{
  document.getElementById('root').innerHTML=`
    <div class="lock-stage">
      <div class="lock-card">
        <div class="lock-banner">
          <div class="lock-shield"><i class="ti ti-shield-lock"></i></div>
          <div class="lock-title">${{esc(name)}}</div>
          <div class="lock-sub">این گروه با رمز محافظت شده. برای دیدن کانفیگ‌ها رمز رو وارد کنید.</div>
        </div>
        <div class="lock-form">
          <div class="lock-err" id="lock-err">${{errMsg ? '<i class="ti ti-alert-circle"></i> '+esc(errMsg) : ''}}</div>
          <div class="lock-field">
            <i class="ti ti-lock lock-lockicon"></i>
            <input class="lock-inp" type="password" id="lock-pw" placeholder="••••••••" autofocus>
            <button class="lock-eye" type="button" onclick="togglePwVis()"><i class="ti ti-eye" id="lock-eye-icon"></i></button>
          </div>
          <button class="btn btn-p lock-btn" onclick="submitLock()"><i class="ti ti-lock-open"></i> ورود به گروه</button>
        </div>
        <div class="lock-footer"><i class="ti ti-shield-check"></i> اتصال شما رمزنگاری‌شده است</div>
      </div>
    </div>
  `;
  const inp=document.getElementById('lock-pw');
  inp.addEventListener('keydown',e=>{{if(e.key==='Enter')submitLock()}});
}}

function togglePwVis(){{
  const inp=document.getElementById('lock-pw');
  const icon=document.getElementById('lock-eye-icon');
  const toText = inp.type==='password';
  inp.type = toText ? 'text' : 'password';
  icon.className = 'ti '+(toText ? 'ti-eye-off' : 'ti-eye');
}}

async function submitLock(){{
  const pw=document.getElementById('lock-pw').value;
  const data=await loadData(pw);
  if(data.locked){{renderLock(data.name,'رمز اشتباه است');return}}
  savedPw=pw;
  renderContent(data);
}}

function renderContent(d){{
  const activeCount=d.links.filter(l=>l.active).length;
  const baseSubUrl = d.sub_url || (window.location.protocol + '//' + window.location.host + '/sub-group/' + UUID_KEY);
  const subUrl = baseSubUrl + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : '');

  window._rvgSubUrl  = subUrl;
  window._rvgSubName = d.name;
  window._rvgPool    = {{limit_fmt:d.pool_limit_fmt, available_fmt:d.pool_available_fmt, available_bytes:d.pool_available_bytes, limit_bytes:d.pool_limit_bytes}};
  window._rvgLinks   = d.links.map(l => ({{
    uuid  : l.uuid,
    vless : l.vless_link,
    sub   : l.sub_url + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : ''),
    label : l.label,
  }}));
  window._rvgPerms = d.permissions || {{client_can_delete:true, client_can_disable:true}};

  document.getElementById('root').innerHTML=`
    ${{d.locked_by_admin ? `<div class="locked-banner"><i class="ti ti-lock"></i><span>این گروه توسط مدیر قفل شده — همه‌ی کانفیگ‌ها موقتاً از کار افتاده‌اند تا زمانی که مدیر قفل را باز کند.</span></div>` : ''}}
    <div class="sub-info">
      <div class="sub-eyebrow"><i class="ti ti-folders"></i> گروه دسترسی</div>
      <div class="sub-name">${{esc(d.name)}}</div>
      ${{d.desc ? `<div class="sub-desc">${{esc(d.desc)}}</div>` : ''}}
      <div class="sub-meta-row"><i class="ti ti-clock"></i> آخرین بروزرسانی: ${{new Date().toLocaleTimeString('fa-IR')}}</div>
      <div class="sub-sub-box">
        <span class="sub-sub-url">${{esc(subUrl)}}</span>
        <button class="btn btn-pur" style="padding:7px 12px;font-size:10.5px"
          onclick="navigator.clipboard.writeText(window._rvgSubUrl).then(()=>toast('لینک ساب کپی شد ✓','ok'))">
          <i class="ti ti-copy"></i> کپی لینک ساب
        </button>
        <button class="btn btn-g" style="padding:7px 12px;font-size:10.5px"
          onclick="showQR(window._rvgSubName + ' — کل گروه', window._rvgSubUrl)">
          <i class="ti ti-qrcode"></i> QR کل
        </button>
      </div>
    </div>

    ${{d.pool_enabled ? renderPoolCard(d) : ''}}

    <div class="copy-all-bar">
      <div class="copy-all-text">
        <div class="copy-all-title"><i class="ti ti-copy"></i> کپی همه‌ی کانفیگ‌ها</div>
        <div class="copy-all-sub">تمام لینک‌های فعال این گروه را یک‌جا کپی کن</div>
      </div>
      <button class="copy-all-btn" onclick="copyAllConfigs()"><i class="ti ti-clipboard-copy"></i> کپی همه (${{toFa(activeCount)}})</button>
    </div>

    <div class="stats-bar">
      <div class="stat-card">
        <div class="stat-label">کانفیگ‌های فعال</div>
        <div class="stat-val">${{toFa(activeCount)}}</div>
        <div class="stat-sub">از ${{toFa(d.links.length)}} کانفیگ</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">اتصالات زنده</div>
        <div class="stat-val">${{toFa(d.active_connections)}}</div>
        <div class="stat-sub" style="color:var(--green-t);display:flex;align-items:center;gap:4px"><span class="dot"></span> آنلاین</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">کل مصرف</div>
        <div class="stat-val" style="font-size:17px;margin-top:3px">${{esc(d.total_used_fmt)}}</div>
        <div class="stat-sub">همه کانفیگ‌ها</div>
      </div>
    </div>

    <div class="cfg-title"><i class="ti ti-link"></i> کانفیگ‌ها (${{toFa(d.links.length)}} عدد)</div>
    <div class="cfg-grid">
      ${{d.links.map((l, i) => {{
        const pct = l.limit_bytes === 0 ? 0 : Math.min(100, l.used_bytes / l.limit_bytes * 100);
        const bc  = pct > 90 ? 'var(--red)' : pct > 70 ? 'var(--amber)' : 'var(--green)';
        const lim = l.limit_bytes === 0 ? '∞' : fmtB(l.limit_bytes);
        return `
          <div class="cfg-card${{l.active ? '' : ' inactive'}}">
            <div class="cfg-top">
              <div class="cfg-head">
                <div>
                  <div class="cfg-label">${{esc(l.label)}}</div>
                  <div class="cfg-badges">
                    ${{protoChip(l.protocol)}}
                    ${{l.connections > 0 ? `<span class="conn-chip"><span class="dot"></span> ${{toFa(l.connections)}} اتصال</span>` : ''}}
                  </div>
                </div>
                <span class="cfg-status ${{l.active ? 'ok' : 'no'}}">${{l.active ? '<i class="ti ti-circle-check"></i> فعال' : '<i class="ti ti-circle-x"></i> غیرفعال'}}</span>
              </div>
              <div class="cfg-usage">
                <div class="ubar"><div class="ubar-f" style="width:${{pct}}%;background:${{bc}}"></div></div>
                <div class="utxt"><span>${{esc(l.used_fmt)}} مصرف شده</span><span>سهمیه: ${{lim}}</span></div>
              </div>
              ${{l.expires_at ? `<div class="cfg-timer" data-expires="${{l.expires_at}}"><i class="ti ti-hourglass-high"></i><div class="cfg-timer-grid"><div class="cfg-timer-seg"><div class="cfg-timer-val cd-d">--</div><div class="cfg-timer-lbl">روز</div></div><div class="cfg-timer-seg"><div class="cfg-timer-val cd-h">--</div><div class="cfg-timer-lbl">ساعت</div></div><div class="cfg-timer-seg"><div class="cfg-timer-val cd-m">--</div><div class="cfg-timer-lbl">دقیقه</div></div><div class="cfg-timer-seg"><div class="cfg-timer-val cd-s">--</div><div class="cfg-timer-lbl">ثانیه</div></div></div></div>` : ''}}
            </div>
            <div class="cfg-tear"></div>
            <div class="cfg-bottom">
              <button class="cfg-link-toggle" id="vt-${{i}}" onclick="toggleLink(${{i}})">
                <span class="ltl"><i class="ti ti-eye"></i> <span>نمایش لینک کانفیگ</span></span>
                <i class="ti ti-chevron-down"></i>
              </button>
              <div class="cfg-vless-wrap" id="vw-${{i}}">
                <div class="cfg-vless-inner">
                  <div class="cfg-vless">${{esc(l.vless_link)}}</div>
                </div>
              </div>
              <div class="cfg-actions">
                <button class="btn btn-p"
                  onclick="navigator.clipboard.writeText(window._rvgLinks[${{i}}].vless).then(()=>toast('لینک کپی شد ✓','ok'))">
                  <i class="ti ti-copy"></i> کپی لینک
                </button>
                <button class="btn btn-g"
                  onclick="showQR(window._rvgLinks[${{i}}].label, window._rvgLinks[${{i}}].vless)">
                  <i class="ti ti-qrcode"></i> QR
                </button>
              </div>
              ${{renderChildrenBox(l)}}
            </div>
          </div>
        `;
      }}).join('')}}
    </div>
  `;
  document.querySelectorAll('.cfg-timer').forEach(tickTimerEl);
  if(window._rvgTimerInterval) clearInterval(window._rvgTimerInterval);
  window._rvgTimerInterval = setInterval(()=>document.querySelectorAll('.cfg-timer').forEach(tickTimerEl), 1000);
  setTimeout(() => autoRefresh(), 30000);
}}

function tickTimerEl(el){{
  const expires = el.getAttribute('data-expires');
  if(!expires)return;
  const diff = new Date(expires).getTime() - Date.now();
  const clamp = n => Math.max(0,n);
  const d = clamp(Math.floor(diff/86400000));
  const h = clamp(Math.floor(diff%86400000/3600000));
  const m = clamp(Math.floor(diff%3600000/60000));
  const s = clamp(Math.floor(diff%60000/1000));
  el.querySelector('.cd-d').textContent = toFa(d);
  el.querySelector('.cd-h').textContent = toFa(h);
  el.querySelector('.cd-m').textContent = toFa(m);
  el.querySelector('.cd-s').textContent = toFa(s);
  el.classList.toggle('expiring', diff <= 3600000);
}}

function renderChildrenBox(l){{
  const kids = l.children || [];
  if(!kids.length) return '';
  const perms = window._rvgPerms || {{client_can_delete:true, client_can_disable:true}};
  return `
    <div class="children-box">
      <div class="children-title"><i class="ti ti-users"></i> کاربرانی که از این کانفیگ سهم گرفته‌اند (${{toFa(kids.length)}})</div>
      ${{kids.map(c => `
        <div class="child-row">
          <div>
            <div class="child-row-name">${{esc(c.label)}}</div>
            <div class="child-row-meta">${{esc(c.used_fmt)}} از ${{esc(c.limit_fmt)}} · ${{c.active && !c.expired ? 'فعال' : 'غیرفعال'}}</div>
          </div>
          <div class="child-row-actions">
            <button class="child-btn" ${{perms.client_can_disable ? '' : 'disabled'}} title="${{perms.client_can_disable ? (c.active?'غیرفعال کردن':'فعال کردن') : 'این قابلیت توسط مدیر غیرفعال شده'}}"
              onclick="toggleChildCfg('${{l.uuid}}','${{c.uuid}}',${{!c.active}})"><i class="ti ${{c.active?'ti-power':'ti-play'}}"></i></button>
            <button class="child-btn danger" ${{perms.client_can_delete ? '' : 'disabled'}} title="${{perms.client_can_delete ? 'حذف' : 'این قابلیت توسط مدیر غیرفعال شده'}}"
              onclick="deleteChildCfg('${{l.uuid}}','${{c.uuid}}')"><i class="ti ti-trash"></i></button>
          </div>
        </div>
      `).join('')}}
    </div>
  `;
}}

async function toggleChildCfg(parentUuid, childUuid, active){{
  try{{
    const r=await fetch('/api/public/split/'+parentUuid+'/'+childUuid+'/toggle',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{active}})}});
    if(!r.ok){{const e=await r.json().catch(()=>({{}}));toast(e.detail||'خطا','');return}}
    toast(active?'فعال شد ✓':'غیرفعال شد','ok');
    autoRefresh();
  }}catch(e){{toast('خطا در ارتباط با سرور','')}}
}}
async function deleteChildCfg(parentUuid, childUuid){{
  if(!confirm('این کانفیگ حذف شود؟ حجم مصرف‌نشده‌اش برمی‌گردد.'))return;
  try{{
    const r=await fetch('/api/public/split/'+parentUuid+'/'+childUuid,{{method:'DELETE'}});
    if(!r.ok){{const e=await r.json().catch(()=>({{}}));toast(e.detail||'خطا','');return}}
    toast('حذف شد ✓','ok');
    autoRefresh();
  }}catch(e){{toast('خطا در ارتباط با سرور','')}}
}}

function copyAllConfigs(){{
  const links=window._rvgLinks||[];
  if(!links.length){{toast('کانفیگی برای کپی نیست','');return}}
  const text=links.map(l=>l.vless).join('\\n');
  navigator.clipboard.writeText(text).then(()=>toast('همه‌ی '+toFa(links.length)+' کانفیگ کپی شد ✓','ok'));
}}

function renderPoolCard(d){{
  const pct = d.pool_limit_bytes ? Math.min(100, (d.pool_allocated_bytes/d.pool_limit_bytes)*100) : 0;
  return `
    <div class="pool-card">
      <div class="pool-head"><i class="ti ti-chart-pie"></i><span>استخر تقسیم‌پذیر</span></div>
      <div class="pool-gauge"><div class="pool-gauge-f" style="width:${{pct}}%"></div></div>
      <div class="pool-txt"><span>باقی‌مانده برای تقسیم: <b style="color:var(--t1)">${{esc(d.pool_available_fmt)}}</b></span><span>سقف کل: ${{esc(d.pool_limit_fmt)}}</span></div>
      <div class="split-form">
        <input id="split-val" type="number" min="0" step="0.1" placeholder="مقدار (مثلاً 5)">
        <select id="split-unit"><option value="GB">GB</option><option value="MB">MB</option></select>
      </div>
      <div class="split-form-row2">
        <input id="split-label" placeholder="اسم کانفیگ (اختیاری)">
        <input id="split-name" placeholder="اسم ساب هدیه (اختیاری)">
      </div>
      <div class="split-err" id="split-err"><i class="ti ti-alert-circle"></i><span id="split-err-txt"></span></div>
      <button class="btn btn-pur" style="width:100%;justify-content:center" onclick="submitSplit()"><i class="ti ti-gift"></i> جدا کردن و ساخت ساب هدیه</button>
      <div class="split-result" id="split-result">
        <div class="split-result-title"><i class="ti ti-circle-check"></i> ساب هدیه ساخته شد ✓ (سفید-برند، بدون هیچ لوگو/نامی)</div>
        <div class="split-result-url" id="split-result-url"></div>
        <div class="cfg-actions">
          <button class="btn btn-p" onclick="copySplitUrl()"><i class="ti ti-copy"></i> کپی لینک</button>
          <button class="btn btn-g" onclick="showQR('ساب هدیه',window._rvgSplitUrl)"><i class="ti ti-qrcode"></i> QR</button>
          <button class="btn btn-g" onclick="window.open(window._rvgSplitUrl,'_blank')"><i class="ti ti-external-link"></i> باز کردن</button>
        </div>
      </div>
    </div>
  `;
}}

async function submitSplit(){{
  const errEl=document.getElementById('split-err'), errTxt=document.getElementById('split-err-txt');
  errEl.classList.remove('show');
  const amount_value=document.getElementById('split-val').value;
  const amount_unit=document.getElementById('split-unit').value;
  const label=document.getElementById('split-label').value.trim();
  const name=document.getElementById('split-name').value.trim();
  if(!amount_value||Number(amount_value)<=0){{errTxt.textContent='یک مقدار معتبر وارد کن';errEl.classList.add('show');return}}
  try{{
    const r=await fetch('/api/public/sub/'+UUID_KEY+'/split',{{method:'POST',headers:{{'Content-Type':'application/json'}},
      body:JSON.stringify({{pw:savedPw,amount_value,amount_unit,label,name}})}});
    const data=await r.json();
    if(!r.ok){{errTxt.textContent=data.detail||'خطا در ساخت ساب هدیه';errEl.classList.add('show');return}}
    window._rvgSplitUrl=data.public_url;
    document.getElementById('split-result-url').textContent=data.public_url;
    document.getElementById('split-result').classList.add('show');
    toast('ساب هدیه ('+data.amount_fmt+') ساخته شد ✓','ok');
    autoRefresh();
  }}catch(e){{errTxt.textContent='خطا در ارتباط با سرور';errEl.classList.add('show')}}
}}
function copySplitUrl(){{
  navigator.clipboard.writeText(window._rvgSplitUrl||'').then(()=>toast('لینک ساب هدیه کپی شد ✓','ok'));
}}

async function autoRefresh(){{
  try{{
    const data = await loadData(savedPw);
    if (!data.locked) renderContent(data);
  }} catch(e) {{}}
}}

async function init(){{
  try{{
    const data = await loadData();
    if (data.locked) {{ renderLock(data.name); return; }}
    renderContent(data);
  }} catch(e) {{
    document.getElementById('root').innerHTML =
      '<div class="empty-state" style="color:var(--red-t)"><i class="ti ti-alert-circle"></i>خطا در بارگذاری</div>';
  }}
}}

init();
</script>
</body></html>"""

def get_single_link_page_html(uuid: str, link_data: dict) -> str:
    import json as _json
    from urllib.parse import quote as _uq
    label = link_data.get("label", "بدون نام")
    vless_link = link_data.get("vless_link", "")
    vless_links = link_data.get("vless_links") or [{"protocol": link_data.get("protocol", "vless-ws"), "vless_link": vless_link}]
    vless_links_json = _json.dumps(vless_links, ensure_ascii=False)
    sub_url = link_data.get("sub_url", "")
    used_fmt = link_data.get("used_fmt", "0 B")
    limit_fmt = link_data.get("limit_fmt", "∞")
    limit_bytes = link_data.get("limit_bytes", 0)
    used_bytes = link_data.get("used_bytes", 0)
    active = link_data.get("active", True)
    expired = link_data.get("expired", False)
    created_at = link_data.get("created_at", "")
    protocol = link_data.get("protocol", "vless-ws")
    white_label = bool(link_data.get("white_label"))
    flag = link_data.get("flag", "") or ""
    flag_json = _json.dumps(flag)
    _country_names = {"🇺🇸": "آمریکا", "🇳🇱": "هلند", "🇩🇪": "آلمان", "🇬🇧": "بریتانیا", "🇫🇷": "فرانسه", "🇹🇷": "ترکیه", "🇸🇬": "سنگاپور", "🇯🇵": "ژاپن"}
    country_name = _country_names.get(flag, "")

    proto_names = {
        "vless-ws": "VLESS / WebSocket",
        "xhttp-packet-up": "XHTTP · packet-up",
        "xhttp-stream-up": "XHTTP · stream-up",
        "xhttp-stream-one": "XHTTP ULTRA"
    }
    proto_display = proto_names.get(protocol, protocol)

    pct = 0 if limit_bytes == 0 else min(100, used_bytes / limit_bytes * 100)
    bar_color = "var(--danger)" if pct > 90 else ("var(--accent)" if pct > 70 else "var(--ok)")

    def _fmtb(n):
        n = max(0, n)
        if n < 1024: return f"{n} B"
        if n < 1024**2: return f"{n/1024:.1f} KB"
        if n < 1024**3: return f"{n/1024**2:.2f} MB"
        return f"{n/1024**3:.2f} GB"
    remain_fmt = "∞" if limit_bytes == 0 else _fmtb(limit_bytes - used_bytes)
    expires_at = link_data.get("expires_at")
    expires_json = _json.dumps(expires_at)

    page_title = label if white_label else f"{label} · تیم آزادی"
    header_brand_html = "" if white_label else f"""
    <div class="brand">
      <div class="brand-img"><img src="{LOGO_DATA_URI}" alt="تیم آزادی"></div>
      <div><div class="brand-name">تیم آزادی</div><div class="brand-sub">Gateway · v10.0</div></div>
    </div>"""
    header_tg_html = "" if white_label else '<a href="https://t.me/TimAzadi" target="_blank" class="tg-badge"><i class="ti ti-brand-telegram"></i><span>@TimAzadi</span></a>'
    footer_html = "" if white_label else '<div class="footer">ساخته‌شده به یاد تمدن ایران‌زمین · <b>تیم آزادی Gateway</b> · <a href="https://t.me/TimAzadi" target="_blank">@TimAzadi</a></div>'
    manifesto_html = "" if white_label else """
  <div class="manifesto">
    <i class="ti ti-quote"></i>
    <span>به یاد پیام کوروش بزرگ در پاسارگاد: «آزادی، حق طبیعیِ هر انسان است»</span>
  </div>
  <div class="frieze-thin"><svg viewBox="0 0 600 8" preserveAspectRatio="none"><rect width="600" height="8" fill="url(#guilloche-thin)"/></svg></div>"""

    encoded_sub = _uq(sub_url, safe="")
    encoded_label = _uq(label, safe="")
    app_links = {
        "hiddify": f"hiddify://import/{encoded_sub}",
        "v2box": f"v2box://install-sub?url={encoded_sub}&name={encoded_label}",
        "streisand": f"streisand://import/{encoded_sub}",
        "v2rayng": f"v2rayng://install-sub?url={encoded_sub}&name={encoded_label}",
        "nekoray": "",
    }
    app_links_json = _json.dumps(app_links, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --bg:#0D0906;
  --panel:rgba(28,20,13,.72);
  --panel-solid:#1C140D;
  --border:rgba(201,162,39,.20);
  --border-soft:rgba(201,162,39,.08);
  --accent:#C9A227;
  --accent-soft:#E8C766;
  --ink:#F1E7D2;
  --ink-dim:#A99B79;
  --ink-faint:#6E6248;
  --danger:#C1524A; --danger-bg:rgba(193,82,74,.14);
  --ok:#2FA79D; --ok-bg:rgba(47,167,157,.14);
  --shadow:0 18px 46px rgba(0,0,0,.5);
  --mono:'JetBrains Mono',ui-monospace,monospace;
  --r-lg:22px; --r-md:15px; --r-sm:10px;
}}
html[data-dynasty="sassanid"]{{--accent:#2FA79D;--accent-soft:#7FD9CF;--border:rgba(47,167,157,.20);--border-soft:rgba(47,167,157,.08)}}
html[data-dynasty="median"]{{--accent:#A8434F;--accent-soft:#D98A93;--border:rgba(168,67,79,.20);--border-soft:rgba(168,67,79,.08)}}
html[data-dynasty="parthian"]{{--accent:#B5732E;--accent-soft:#E0A868;--border:rgba(181,115,46,.20);--border-soft:rgba(181,115,46,.08)}}
html[data-dynasty="elamite"]{{--accent:#4A5A9E;--accent-soft:#93A3D9;--border:rgba(74,90,158,.20);--border-soft:rgba(74,90,158,.08)}}
html[data-theme="light"]{{
  --bg:#F3EDE0; --panel:rgba(255,255,255,.85); --panel-solid:#FFFDF8;
  --border:rgba(40,30,15,.13); --border-soft:rgba(40,30,15,.06);
  --ink:#241C10; --ink-dim:#6B5D42; --ink-faint:#9C8F72;
  --shadow:0 12px 30px rgba(30,20,10,.10);
}}
html[data-theme="light"] .col-mark{{opacity:.05}}
html[data-theme="light"] .qr-img img{{background:#fff}}

html,body{{min-height:100%;background:var(--bg);font-family:'Vazirmatn',sans-serif;color:var(--ink);font-size:14px}}
html,body,.card,.badge,.btn,.icon-btn,.cfg-row,.tg-badge,.app-link-btn,.os-card{{transition:background .35s ease,border-color .35s ease,color .35s ease}}
.bg-layer{{position:fixed;inset:0;z-index:0;pointer-events:none;background:
  radial-gradient(ellipse 65% 40% at 50% -8%, color-mix(in srgb, var(--accent) 14%, transparent), transparent 60%),
  var(--bg)}}
.col-mark{{position:fixed;left:0;right:0;bottom:0;height:34vh;z-index:0;pointer-events:none;opacity:.07;
  background-repeat:repeat-x;background-position:bottom center;background-size:220px auto;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 220 340'%3E%3Cg fill='%23C9A227'%3E%3Crect x='95' y='40' width='30' height='260'/%3E%3Cpath d='M60,40 Q110,-10 160,40 L150,55 Q110,15 70,55 Z'/%3E%3Crect x='70' y='300' width='80' height='14'/%3E%3Crect x='55' y='314' width='110' height='16'/%3E%3C/g%3E%3C/svg%3E")}}
.wrap{{position:relative;z-index:10;max-width:660px;margin:0 auto;padding:26px 16px 60px}}

@keyframes fadeUp{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:translateY(0)}}}}
.fade-1{{animation:fadeUp .45s ease both .03s}}
.fade-2{{animation:fadeUp .5s ease both .1s}}
.fade-3{{animation:fadeUp .5s ease both .17s}}
.fade-4{{animation:fadeUp .5s ease both .24s}}
.fade-5{{animation:fadeUp .5s ease both .3s}}

.top{{position:relative;z-index:5;display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;flex-wrap:wrap;gap:10px}}
.brand{{display:flex;align-items:center;gap:11px}}
.brand-img{{width:42px;height:42px;border-radius:12px;overflow:hidden;border:1px solid var(--border);box-shadow:0 0 18px color-mix(in srgb, var(--accent) 30%, transparent);flex-shrink:0}}
.brand-img img{{width:100%;height:100%;object-fit:cover}}
.brand-name{{font-size:15px;font-weight:800;letter-spacing:.2px}}
.brand-sub{{font-size:9.5px;color:var(--ink-faint);font-family:var(--mono)}}
.top-actions{{display:flex;align-items:center;gap:8px}}
.icon-btn{{width:36px;height:36px;border-radius:10px;background:var(--border-soft);border:1px solid var(--border);color:var(--accent-soft);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:15px}}
.icon-btn:hover{{transform:translateY(-2px)}}
.theme-toggle i{{transition:transform .45s ease}}
.theme-toggle:hover i{{transform:rotate(25deg)}}
.live-clock{{display:flex;align-items:center;gap:6px;font-family:var(--mono);font-size:12px;font-weight:600;color:var(--accent-soft);background:rgba(0,0,0,.22);border:1px solid var(--border);border-radius:9px;padding:7px 11px;letter-spacing:.5px}}
.tg-badge{{display:inline-flex;align-items:center;gap:7px;padding:7px 13px;border-radius:20px;background:linear-gradient(135deg,var(--border-soft),transparent);border:1px solid var(--border);color:var(--accent-soft);text-decoration:none;font-size:11.5px;font-weight:700}}
.tg-badge:hover{{transform:translateY(-2px);background:var(--border)}}

.dyn-picker{{position:relative}}
.dyn-menu{{display:none;position:absolute;top:44px;left:0;background:var(--panel-solid);border:1px solid var(--border);border-radius:15px;padding:8px;flex-direction:column;gap:2px;box-shadow:var(--shadow);z-index:80;min-width:150px}}
.dyn-menu.open{{display:flex}}
.dyn-option{{display:flex;align-items:center;gap:9px;padding:8px 9px;border-radius:10px;cursor:pointer}}
.dyn-option:hover{{background:var(--border-soft)}}
.dyn-dot{{width:16px;height:16px;border-radius:50%;flex-shrink:0}}
.dyn-name{{font-size:11.5px;font-weight:600;color:var(--ink)}}
.dyn-check{{margin-right:auto;font-size:13px;color:var(--accent);opacity:0}}
.dyn-option.active .dyn-check{{opacity:1}}

.manifesto{{position:relative;z-index:5;text-align:center;font-size:11.5px;color:var(--accent-soft);line-height:1.9;padding:0 10px;margin-bottom:8px;display:flex;align-items:center;justify-content:center;gap:7px;flex-wrap:wrap}}
.manifesto i{{font-size:13px;opacity:.8}}
.frieze-thin{{max-width:420px;margin:0 auto 20px;opacity:.7}}
.frieze-thin svg{{width:100%;height:8px;display:block}}
.frieze{{margin:20px auto;max-width:100%;line-height:0}}
.frieze svg{{width:100%;height:16px;display:block}}

.card{{position:relative;z-index:1;background:var(--panel);backdrop-filter:blur(16px);border:1px solid var(--border);border-radius:var(--r-lg);box-shadow:var(--shadow)}}
.hero{{padding:0 24px 22px;margin-bottom:16px;overflow:hidden}}
.hero-cap{{margin:0 -24px 18px;line-height:0}}
.hero-cap svg{{width:100%;height:18px;display:block}}
.hero-title{{font-size:20px;font-weight:800;margin-bottom:8px;text-shadow:0 1px 1px rgba(0,0,0,.5),0 -1px 0 rgba(255,255,255,.05);letter-spacing:.2px}}
.hero-meta{{font-size:11px;color:var(--ink-faint);margin-bottom:20px;display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-family:var(--mono)}}
.badge{{font-size:10px;padding:4px 11px;border-radius:20px;font-weight:700;display:inline-flex;align-items:center;gap:5px;font-family:'Vazirmatn',sans-serif}}
.badge-ok{{background:var(--ok-bg);color:var(--ok)}}
.badge-off{{background:var(--danger-bg);color:var(--danger)}}
.badge-neutral{{background:var(--border-soft);color:var(--accent-soft)}}

.dial-row{{display:flex;align-items:center;gap:22px;margin-bottom:20px}}
.dial{{position:relative;width:122px;height:122px;flex-shrink:0}}
.dial-sun{{position:absolute;inset:-14px;opacity:.55}}
.dial-ring{{position:absolute;inset:0;border-radius:50%;display:flex;align-items:center;justify-content:center;transition:background .4s ease}}
.dial-inner{{width:90px;height:90px;border-radius:50%;background:var(--panel-solid);display:flex;flex-direction:column;align-items:center;justify-content:center;border:1px solid var(--border-soft)}}
.dial-pct{{font-size:22px;font-weight:800;font-family:var(--mono)}}
.dial-lbl{{font-size:9.5px;color:var(--ink-faint);margin-top:1px}}
.dial-stats{{flex:1;display:flex;flex-direction:column;gap:9px}}
.dial-stat{{display:flex;align-items:center;justify-content:space-between;font-size:12px}}
.dial-stat b{{font-family:var(--mono);font-size:13px;font-weight:700}}
.dial-stat span:first-child{{color:var(--ink-dim)}}

.term{{display:none;background:rgba(0,0,0,.24);border:1px solid var(--border);border-radius:var(--r-sm);padding:13px 8px;margin-bottom:18px}}
.term-title{{font-size:10.5px;color:var(--ink-faint);display:flex;align-items:center;gap:5px;justify-content:center;margin-bottom:9px;font-family:var(--mono)}}
.term-grid{{display:flex;align-items:center;justify-content:center;gap:4px;font-family:var(--mono)}}
.term-cell{{text-align:center;min-width:40px}}
.term-val{{font-size:18px;font-weight:700;color:var(--accent-soft)}}
.term-lbl{{font-size:8.5px;color:var(--ink-faint);margin-top:1px}}
.term-colon{{font-size:16px;color:var(--ink-faint);padding-bottom:11px}}

.cfg-title{{font-size:12px;font-weight:700;color:var(--ink-dim);margin-bottom:12px;display:flex;align-items:center;gap:6px}}
.cfg-row{{border:1px solid var(--border);border-radius:var(--r-sm);margin-bottom:8px;overflow:hidden;border-inline-start:2px solid var(--accent)}}
.cfg-row-head{{display:flex;align-items:center;justify-content:space-between;padding:11px 13px;cursor:pointer;background:rgba(0,0,0,.16)}}
.cfg-row-name{{font-size:12px;font-weight:700;display:flex;align-items:center;gap:7px}}
.cfg-row-actions{{display:flex;align-items:center;gap:4px}}
.mini-btn{{background:var(--border-soft);color:var(--accent-soft);border:none;border-radius:8px;width:27px;height:27px;display:flex;align-items:center;justify-content:center;cursor:pointer}}
.mini-btn:hover{{transform:translateY(-2px)}}
.cfg-chev{{font-size:14px;color:var(--ink-faint);transition:transform .2s;margin-right:2px}}
.cfg-row-body{{max-height:0;overflow:hidden;padding:0 13px;font-family:var(--mono);font-size:10.5px;color:var(--accent-soft);word-break:break-all;line-height:1.8;background:rgba(0,0,0,.2);transition:max-height .25s ease,padding .25s ease}}
.cfg-row-body.open{{max-height:400px;padding:12px 13px;border-top:1px solid var(--border)}}

.actions{{display:flex;gap:9px;flex-wrap:wrap;margin-top:16px}}
.btn{{font-family:inherit;font-size:12px;font-weight:600;border-radius:10px;padding:10px 16px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border:none}}
.btn i{{font-size:14px}}
.btn-primary{{background:linear-gradient(135deg,var(--accent),color-mix(in srgb, var(--accent) 70%, black));color:#0D0906;font-weight:700;box-shadow:0 4px 16px color-mix(in srgb, var(--accent) 35%, transparent)}}
.btn-primary:hover{{filter:brightness(1.08);transform:translateY(-2px)}}
.btn-ghost{{background:var(--border-soft);color:var(--accent-soft);border:1px solid var(--border)}}
.btn-ghost:hover{{background:var(--border);transform:translateY(-2px)}}
@media (max-width:480px){{.actions{{flex-direction:column}} .actions .btn{{width:100%;justify-content:center;padding:13px 16px;font-size:13px}}}}

.section{{padding:22px 24px;margin-bottom:16px}}
.section-title{{font-size:12px;font-weight:700;color:var(--ink-dim);margin-bottom:14px;display:flex;align-items:center;gap:6px}}

.app-link-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(78px,1fr));gap:10px;margin-bottom:18px}}
.app-link-btn{{display:flex;flex-direction:column;align-items:center;gap:6px;padding:14px 6px;border-radius:14px;background:var(--border-soft);border:1px solid var(--border);color:var(--ink);cursor:pointer}}
.app-link-btn:hover{{transform:translateY(-3px);background:var(--border)}}
.app-link-icon{{width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,var(--accent),color-mix(in srgb,var(--accent) 60%, black));display:flex;align-items:center;justify-content:center;color:#0D0906;font-size:16px}}
.app-link-name{{font-size:10.5px;font-weight:700;color:var(--ink-dim)}}

.guide-step{{display:flex;gap:11px;margin-bottom:12px;font-size:12px;color:var(--ink-dim);line-height:1.8}}
.guide-step:last-child{{margin-bottom:0}}
.guide-num{{flex-shrink:0;width:22px;height:22px;border-radius:50%;background:var(--border-soft);border:1px solid var(--border);color:var(--accent-soft);font-size:11px;font-weight:800;display:flex;align-items:center;justify-content:center;font-family:var(--mono)}}
.guide-step b{{color:var(--ink)}}

.split-card{{background:linear-gradient(135deg,color-mix(in srgb, var(--accent) 10%, transparent),transparent);border:1px solid var(--border)}}
.split-head{{display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:14px;font-weight:700}}
.split-head i{{color:var(--accent-soft);font-size:17px}}
.split-sub-note{{font-size:11.5px;color:var(--ink-faint);line-height:1.8;margin-bottom:14px}}
.split-form{{display:grid;grid-template-columns:1fr 90px;gap:8px;margin-bottom:10px}}
.split-form input,.split-form select,#split-label{{font-family:inherit;font-size:12.5px;padding:10px 12px;border-radius:10px;border:1px solid var(--border);background:rgba(0,0,0,.2);color:var(--ink);outline:none;width:100%}}
.split-form input:focus,.split-form select:focus,#split-label:focus{{border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb, var(--accent) 15%, transparent)}}
.split-err{{color:var(--danger);font-size:11px;margin-bottom:10px;display:none;align-items:center;gap:5px}}
.split-err.show{{display:flex}}
.split-result{{background:var(--ok-bg);border:1px solid color-mix(in srgb, var(--ok) 35%, transparent);border-radius:14px;padding:14px 16px;margin-top:14px;display:none}}
.split-result.show{{display:block}}
.split-result-title{{font-size:12px;font-weight:700;color:var(--ok);display:flex;align-items:center;gap:6px;margin-bottom:9px}}
.split-result-url{{font-family:var(--mono);font-size:10px;color:var(--ink-dim);word-break:break-all;background:rgba(0,0,0,.2);border-radius:9px;padding:9px 11px;margin-bottom:9px}}
.child-item{{display:flex;align-items:center;justify-content:space-between;gap:8px;background:rgba(0,0,0,.18);border-radius:11px;padding:10px 13px;margin-top:9px;font-size:11.5px}}
.child-item-name{{font-weight:700}}
.child-item-meta{{color:var(--ink-faint);font-size:10.5px;margin-top:2px}}
.child-revoke{{background:var(--danger-bg);color:var(--danger);border:none;border-radius:8px;padding:6px 10px;font-size:10.5px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:4px}}
.children-title{{font-size:11px;font-weight:700;color:var(--ink-faint);margin-top:16px;margin-bottom:4px}}

.footer{{text-align:center;padding-top:10px;padding-bottom:10px;font-size:10.5px;color:var(--ink-faint)}}
.footer a{{color:var(--accent-soft);font-weight:600;text-decoration:none}}

.toast{{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(60px);background:var(--panel-solid);border:1px solid var(--border);color:var(--ink);border-radius:12px;padding:12px 20px;font-size:13px;opacity:0;transition:all .3s cubic-bezier(.34,1.56,.64,1);z-index:999;pointer-events:none;display:flex;align-items:center;gap:8px;box-shadow:var(--shadow)}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
.toast.ok{{border-color:color-mix(in srgb, var(--ok) 40%, transparent);background:var(--ok-bg);color:var(--ok)}}

.qr-modal{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.72);backdrop-filter:blur(6px);z-index:600;align-items:center;justify-content:center}}
.qr-modal.open{{display:flex}}
.qr-box{{background:var(--panel-solid);border:1px solid var(--border);border-radius:20px;padding:22px;text-align:center;max-width:320px;width:calc(100% - 32px)}}
.qr-title{{font-size:12.5px;font-weight:700;margin-bottom:14px;color:var(--ink)}}
.qr-img{{border-radius:14px;overflow:hidden;margin-bottom:14px}}
.qr-img img{{width:100%;display:block;background:#fff;padding:8px;border-radius:14px}}

.os-card{{border:1px solid var(--border);border-radius:var(--r-sm);margin-bottom:8px;overflow:hidden}}
.os-head{{display:flex;align-items:center;gap:10px;padding:12px 14px;cursor:pointer;background:rgba(0,0,0,.16)}}
.os-icon{{width:30px;height:30px;border-radius:9px;background:var(--border-soft);display:flex;align-items:center;justify-content:center;color:var(--accent-soft);font-size:15px;flex-shrink:0}}
.os-name{{font-size:12.5px;font-weight:700;flex:1}}
.os-chev{{font-size:14px;color:var(--ink-faint);transition:transform .2s}}
.os-body{{max-height:0;overflow:hidden;transition:max-height .3s ease}}
.os-body.open{{max-height:400px}}
.os-body-inner{{padding:12px 14px;display:flex;flex-direction:column;gap:10px;border-top:1px solid var(--border)}}
.os-app-item{{display:flex;gap:9px;font-size:11.5px;color:var(--ink-dim);line-height:1.7}}
.os-app-item b{{color:var(--ink);flex-shrink:0;min-width:76px}}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute">
  <defs>
    <pattern id="guilloche-thin" width="34" height="8" patternUnits="userSpaceOnUse">
      <circle cx="8" cy="4" r="3.4" fill="none" stroke="var(--accent)" stroke-width="1"/>
      <circle cx="25" cy="4" r="3.4" fill="none" stroke="var(--accent)" stroke-width="1"/>
    </pattern>
    <pattern id="merlon" width="24" height="18" patternUnits="userSpaceOnUse">
      <rect x="0" y="10" width="12" height="8" fill="var(--accent)"/>
      <rect x="12" y="4" width="12" height="14" fill="var(--accent)"/>
    </pattern>
  </defs>
</svg>
<div class="bg-layer"></div><div class="col-mark"></div>
<div class="toast" id="toast"></div>
<div class="qr-modal" id="qr-modal" onclick="this.classList.remove('open')">
  <div class="qr-box" onclick="event.stopPropagation()">
    <div class="qr-title" id="qr-label">QR Code</div>
    <div class="qr-img"><img id="qr-img" src="" alt="QR"></div>
    <button class="btn btn-ghost" style="width:100%;justify-content:center" onclick="document.getElementById('qr-modal').classList.remove('open')"><i class="ti ti-x"></i> بستن</button>
  </div>
</div>

<div class="wrap">
  <div class="top">
    {header_brand_html}
    <div class="top-actions">
      <div class="live-clock"><i class="ti ti-clock"></i><span id="clock-time">--:--:--</span></div>
      <button class="icon-btn theme-toggle" onclick="toggleTheme()" title="تغییر حالت شب/روز"><i class="ti ti-sun" id="theme-icon"></i></button>
      <div class="dyn-picker">
        <button class="icon-btn" onclick="toggleDynMenu()" title="تغییر دودمان"><i class="ti ti-palette"></i></button>
        <div class="dyn-menu" id="dyn-menu">
          <div class="dyn-option" data-dyn="achaemenid" onclick="setDynasty('achaemenid')"><span class="dyn-dot" style="background:#C9A227"></span><span class="dyn-name">هخامنشی</span><i class="ti ti-check dyn-check"></i></div>
          <div class="dyn-option" data-dyn="sassanid" onclick="setDynasty('sassanid')"><span class="dyn-dot" style="background:#2FA79D"></span><span class="dyn-name">ساسانی</span><i class="ti ti-check dyn-check"></i></div>
          <div class="dyn-option" data-dyn="median" onclick="setDynasty('median')"><span class="dyn-dot" style="background:#A8434F"></span><span class="dyn-name">مادها</span><i class="ti ti-check dyn-check"></i></div>
          <div class="dyn-option" data-dyn="parthian" onclick="setDynasty('parthian')"><span class="dyn-dot" style="background:#B5732E"></span><span class="dyn-name">پارتی</span><i class="ti ti-check dyn-check"></i></div>
          <div class="dyn-option" data-dyn="elamite" onclick="setDynasty('elamite')"><span class="dyn-dot" style="background:#4A5A9E"></span><span class="dyn-name">عیلامی</span><i class="ti ti-check dyn-check"></i></div>
        </div>
      </div>
      {header_tg_html}
    </div>
  </div>
{manifesto_html}

  <div class="card hero fade-1">
    <div class="hero-cap"><svg viewBox="0 0 600 18" preserveAspectRatio="none"><rect width="600" height="18" fill="url(#merlon)" opacity=".5"/></svg></div>
    <div class="hero-title">{label}</div>
    <div class="hero-meta">
      <i class="ti ti-calendar"></i> {created_at[:10] if created_at else "—"}
      <span class="badge badge-neutral"><i class="ti ti-server-2"></i> {"Gateway" if white_label else "تیم آزادی Gateway"}</span>
      {f'<span class="badge badge-neutral">{flag} {country_name}</span>' if flag else ''}
      <span class="badge {'badge-ok' if active and not expired else 'badge-off'}">
        <i class="ti ti-{'circle-check' if active and not expired else 'circle-x'}"></i>
        {'فعال' if active and not expired else 'غیرفعال'}
      </span>
    </div>

    <div class="dial-row">
      <div class="dial">
        <svg class="dial-sun" viewBox="0 0 150 150"><g fill="none" stroke="var(--accent)" stroke-width="1.4" opacity=".7">
          <circle cx="75" cy="75" r="70"/>
          <path d="M75,4 L75,16 M75,134 L75,146 M4,75 L16,75 M134,75 L146,75 M23,23 L32,32 M118,118 L127,127 M23,127 L32,118 M118,32 L127,23" stroke-linecap="round"/>
        </g></svg>
        <div class="dial-ring" style="background:conic-gradient({bar_color} calc({pct}*1%),var(--border-soft) 0)">
          <div class="dial-inner">
            <div class="dial-pct">{pct:.0f}%</div>
            <div class="dial-lbl">مصرف</div>
          </div>
        </div>
      </div>
      <div class="dial-stats">
        <div class="dial-stat"><span>مصرف‌شده</span><b>{used_fmt}</b></div>
        <div class="dial-stat"><span>باقی‌مانده</span><b>{remain_fmt}</b></div>
        <div class="dial-stat"><span>سقف حجم</span><b>{limit_fmt}</b></div>
      </div>
    </div>

    <div class="term" id="countdown">
      <div class="term-title"><i class="ti ti-clock-hour-4"></i> تا انقضا</div>
      <div class="term-grid">
        <div class="term-cell"><div class="term-val" id="cd-d">--</div><div class="term-lbl">روز</div></div>
        <div class="term-colon">:</div>
        <div class="term-cell"><div class="term-val" id="cd-h">--</div><div class="term-lbl">ساعت</div></div>
        <div class="term-colon">:</div>
        <div class="term-cell"><div class="term-val" id="cd-m">--</div><div class="term-lbl">دقیقه</div></div>
        <div class="term-colon">:</div>
        <div class="term-cell"><div class="term-val" id="cd-s">--</div><div class="term-lbl">ثانیه</div></div>
      </div>
    </div>

    <div class="cfg-title"><i class="ti ti-list-details"></i> کانفیگ‌ها</div>
    <div class="cfg-list" id="cfg-list"></div>

    <div class="actions">
      <button class="btn btn-primary" onclick="copyAllProtocols()"><i class="ti ti-copy-plus"></i> کپی همه‌ی کانفیگ‌ها</button>
      <button class="btn btn-ghost" onclick="copyToClipboard('{sub_url}')"><i class="ti ti-rss"></i> کپی لینک ساب</button>
    </div>
  </div>

  <div class="card section fade-2">
    <div class="section-title"><i class="ti ti-apps"></i> باز کردن در برنامه</div>
    <div class="app-link-grid">
      <div class="app-link-btn" onclick="openInApp('hiddify')"><div class="app-link-icon"><i class="ti ti-bolt"></i></div><div class="app-link-name">Hiddify</div></div>
      <div class="app-link-btn" onclick="openInApp('v2box')"><div class="app-link-icon"><i class="ti ti-box"></i></div><div class="app-link-name">V2Box</div></div>
      <div class="app-link-btn" onclick="openInApp('streisand')"><div class="app-link-icon"><i class="ti ti-wind"></i></div><div class="app-link-name">Streisand</div></div>
      <div class="app-link-btn" onclick="openInApp('v2rayng')"><div class="app-link-icon"><i class="ti ti-brand-android"></i></div><div class="app-link-name">v2rayNG</div></div>
      <div class="app-link-btn" onclick="openInApp('nekoray')"><div class="app-link-icon"><i class="ti ti-cat"></i></div><div class="app-link-name">Nekoray</div></div>
    </div>
    <div class="guide-step"><div class="guide-num">۱</div><div>اپ دلخواه رو نصب کن و روش بزن.</div></div>
    <div class="guide-step"><div class="guide-num">۲</div><div>اگه خودکار باز نشد، لینک ساب رو کپی کن و توی اپ به‌صورت <b>Add Subscription</b> وارد کن.</div></div>
    <div class="guide-step"><div class="guide-num">۳</div><div><b>Connect</b> بزن و اجازه‌ی VPN رو تایید کن.</div></div>
  </div>

  <div class="card section fade-3">
    <div class="section-title"><i class="ti ti-info-circle"></i> راهنمای هر سیستم‌عامل</div>
    <div class="os-card">
      <div class="os-head" onclick="toggleOS(0)"><div class="os-icon"><i class="ti ti-brand-android"></i></div><div class="os-name">Android</div><i class="ti ti-chevron-down os-chev" id="os-chev-0"></i></div>
      <div class="os-body" id="os-body-0"><div class="os-body-inner">
        <div class="os-app-item"><b>v2rayNG</b><span>آیکون + → Import Config From URL → لینک ساب را وارد کنید</span></div>
        <div class="os-app-item"><b>Hiddify</b><span>New Profile → Add from URL → لینک ساب را جای‌گذاری کنید</span></div>
      </div></div>
    </div>
    <div class="os-card">
      <div class="os-head" onclick="toggleOS(1)"><div class="os-icon"><i class="ti ti-brand-apple"></i></div><div class="os-name">iOS</div><i class="ti ti-chevron-down os-chev" id="os-chev-1"></i></div>
      <div class="os-body" id="os-body-1"><div class="os-body-inner">
        <div class="os-app-item"><b>Streisand</b><span>Add Configuration → From URL → لینک ساب را وارد کنید</span></div>
        <div class="os-app-item"><b>V2Box</b><span>Subscribe → آیکون + → لینک را وارد و Save بزنید</span></div>
      </div></div>
    </div>
    <div class="os-card">
      <div class="os-head" onclick="toggleOS(2)"><div class="os-icon"><i class="ti ti-brand-windows"></i></div><div class="os-name">Windows</div><i class="ti ti-chevron-down os-chev" id="os-chev-2"></i></div>
      <div class="os-body" id="os-body-2"><div class="os-body-inner">
        <div class="os-app-item"><b>Hiddify</b><span>New Profile → Add from URL → لینک ساب را وارد کنید</span></div>
        <div class="os-app-item"><b>Nekoray</b><span>Program → Add profile from clipboard → لینک را اضافه کنید</span></div>
      </div></div>
    </div>
    <div class="os-card">
      <div class="os-head" onclick="toggleOS(3)"><div class="os-icon"><i class="ti ti-brand-ubuntu"></i></div><div class="os-name">Linux</div><i class="ti ti-chevron-down os-chev" id="os-chev-3"></i></div>
      <div class="os-body" id="os-body-3"><div class="os-body-inner">
        <div class="os-app-item"><b>Nekoray</b><span>Program → Add profile from clipboard → لینک کپی‌شده را اضافه کنید</span></div>
      </div></div>
    </div>
  </div>

  <div class="card section split-card fade-4">
    <div class="split-head"><i class="ti ti-gift"></i><span>جدا کردن حجم و ساخت کانفیگ هدیه</span></div>
    <div class="split-sub-note">می‌تونی بخشی از سهمیه‌ی همین کانفیگ رو جدا کنی و به یک کانفیگ کاملاً مستقل و بدون هیچ برند/لوگویی تبدیل کنی تا به هرکسی بدی. حجم جداشده از سهمیه‌ی خودت کم می‌شه.</div>
    <div class="split-form">
      <input id="split-val" type="number" min="0" step="0.1" placeholder="مقدار (مثلاً 5)">
      <select id="split-unit"><option value="GB">GB</option><option value="MB">MB</option></select>
    </div>
    <div class="split-form" style="margin-top:8px">
      <input id="split-exp" type="number" min="0" step="1" placeholder="انقضا (اختیاری، 0 = نامحدود)">
      <select id="split-exp-unit"><option value="hours">ساعت</option><option value="days" selected>روز</option></select>
    </div>
    <input id="split-label" style="margin-bottom:12px" placeholder="اسم کانفیگ هدیه (اختیاری)">
    <div class="split-err" id="split-err"><i class="ti ti-alert-circle"></i><span id="split-err-txt"></span></div>
    <button class="btn btn-ghost" style="width:100%;justify-content:center" onclick="submitSplitLink()"><i class="ti ti-gift"></i> جدا کردن و ساخت کانفیگ هدیه</button>
    <div class="split-result" id="split-result">
      <div class="split-result-title"><i class="ti ti-circle-check"></i> کانفیگ هدیه ساخته شد ✓ (بدون هیچ لوگو/نامی)</div>
      <div class="split-result-url" id="split-result-url"></div>
      <div class="actions">
        <button class="btn btn-primary" onclick="copySplitLinkUrl()"><i class="ti ti-copy"></i> کپی لینک</button>
        <button class="btn btn-ghost" onclick="window.open(window._rvgSplitUrl,'_blank')"><i class="ti ti-external-link"></i> باز کردن</button>
      </div>
    </div>
    <div id="children-list"></div>
  </div>

  {footer_html}
</div>

<script>
const LINK_UUID='{uuid}';
const VLESS_BUNDLE = {vless_links_json};
const EXPIRES_AT = {expires_json};
const APP_LINKS = {app_links_json};
const PROTO_TAG={{'vless-ws':'VLESS · WS','xhttp-packet-up':'XHTTP · packet-up','xhttp-stream-up':'XHTTP · stream-up','xhttp-stream-one':'XHTTP ULTRA','trojan-ws':'TROJAN · WS'}};
let curProtoIdx = 0;
function esc(s){{return String(s||'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]))}}
const FLAG = {flag_json};
function renderCfgList(){{
  document.getElementById('cfg-list').innerHTML = VLESS_BUNDLE.map((b,i)=>`
    <div class="cfg-row">
      <div class="cfg-row-head" onclick="toggleCfgRow(${{i}})">
        <div class="cfg-row-name">${{FLAG?FLAG+' ':''}}${{PROTO_TAG[b.protocol]||b.protocol}}</div>
        <div class="cfg-row-actions">
          <button class="mini-btn" onclick="event.stopPropagation();copyOne(${{i}})" title="کپی"><i class="ti ti-copy"></i></button>
          <button class="mini-btn" onclick="event.stopPropagation();showQRFor(${{i}})" title="QR"><i class="ti ti-qrcode"></i></button>
          <i class="ti ti-chevron-down cfg-chev" id="chev-${{i}}"></i>
        </div>
      </div>
      <div class="cfg-row-body" id="body-${{i}}">${{esc(b.vless_link)}}</div>
    </div>
  `).join('');
}}
function toggleCfgRow(i){{
  const body=document.getElementById('body-'+i), chev=document.getElementById('chev-'+i);
  const opening = !body.classList.contains('open');
  body.classList.toggle('open',opening);
  chev.style.transform = opening?'rotate(180deg)':'';
}}
function copyOne(i){{copyToClipboard(VLESS_BUNDLE[i].vless_link)}}
function showQRFor(i){{curProtoIdx=i;showQR()}}
renderCfgList();

function toggleOS(i){{
  const body = document.getElementById('os-body-'+i);
  const chev = document.getElementById('os-chev-'+i);
  const opening = !body.classList.contains('open');
  body.classList.toggle('open', opening);
  if(chev) chev.style.transform = opening ? 'rotate(180deg)' : '';
}}
function openInApp(key){{
  const link = APP_LINKS[key];
  if(!link){{
    copyToClipboard('{sub_url}');
    toast('این برنامه لینک مستقیم ندارد؛ لینک ساب کپی شد','ok');
    return;
  }}
  window.location.href = link;
  toast('در حال باز شدن در برنامه...','ok');
}}

function tickClock(){{
  const now=new Date();
  const el=document.getElementById('clock-time');
  if(el) el.textContent = now.toLocaleTimeString('fa-IR',{{hour:'2-digit',minute:'2-digit',second:'2-digit'}});
}}
tickClock();setInterval(tickClock,1000);

function setDynasty(name){{
  document.documentElement.setAttribute('data-dynasty',name);
  try{{localStorage.setItem('rvg_dynasty',name)}}catch(e){{}}
  document.querySelectorAll('.dyn-option').forEach(d=>d.classList.toggle('active',d.dataset.dyn===name));
  document.getElementById('dyn-menu').classList.remove('open');
}}
function toggleDynMenu(){{document.getElementById('dyn-menu').classList.toggle('open')}}
document.addEventListener('click',e=>{{
  if(!e.target.closest('.dyn-picker')) document.getElementById('dyn-menu')?.classList.remove('open');
}});
(function(){{
  let saved='achaemenid';
  try{{saved=localStorage.getItem('rvg_dynasty')||'achaemenid'}}catch(e){{}}
  document.documentElement.setAttribute('data-dynasty',saved);
  const opt=document.querySelector('.dyn-option[data-dyn="'+saved+'"]');
  if(opt) opt.classList.add('active');
}})();

function setTheme(theme){{
  document.documentElement.setAttribute('data-theme', theme);
  try{{localStorage.setItem('rvg_theme', theme)}}catch(e){{}}
  const icon = document.getElementById('theme-icon');
  if(icon) icon.className = theme==='light' ? 'ti ti-moon' : 'ti ti-sun';
}}
function toggleTheme(){{
  const cur = document.documentElement.getAttribute('data-theme') || 'dark';
  setTheme(cur === 'dark' ? 'light' : 'dark');
}}
(function(){{
  let saved='dark';
  try{{saved=localStorage.getItem('rvg_theme')||'dark'}}catch(e){{}}
  setTheme(saved);
}})();

function tickCountdown(){{
  const el=document.getElementById('countdown');
  if(!EXPIRES_AT){{el.style.display='none';return}}
  el.style.display='block';
  const diff = new Date(EXPIRES_AT).getTime() - Date.now();
  const d = Math.max(0,Math.floor(diff/86400000));
  const h = Math.max(0,Math.floor(diff%86400000/3600000));
  const m = Math.max(0,Math.floor(diff%3600000/60000));
  const s = Math.max(0,Math.floor(diff%60000/1000));
  document.getElementById('cd-d').textContent=d;
  document.getElementById('cd-h').textContent=h;
  document.getElementById('cd-m').textContent=m;
  document.getElementById('cd-s').textContent=s;
}}
tickCountdown();setInterval(tickCountdown,1000);

function toast(msg,type){{
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2400);
}}
function copyToClipboard(text){{
  navigator.clipboard.writeText(text).then(()=>toast('کپی شد ✓','ok'));
}}
function copyAllProtocols(){{
  navigator.clipboard.writeText(VLESS_BUNDLE.map(b=>b.vless_link).join('\\n'))
    .then(()=>toast('هر '+VLESS_BUNDLE.length+' کانفیگ کپی شد ✓','ok'));
}}
function showQR(){{
  document.getElementById('qr-label').textContent='{label}'+' · '+(PROTO_TAG[VLESS_BUNDLE[curProtoIdx].protocol]||'');
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(VLESS_BUNDLE[curProtoIdx].vless_link);
  document.getElementById('qr-modal').classList.add('open');
}}

function fmtB(b){{if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}}

async function submitSplitLink(){{
  const errEl=document.getElementById('split-err'), errTxt=document.getElementById('split-err-txt');
  errEl.classList.remove('show');
  const amount=document.getElementById('split-val').value;
  const unit=document.getElementById('split-unit').value;
  const label=document.getElementById('split-label').value.trim();
  const expires_value=document.getElementById('split-exp').value||0;
  const expires_unit=document.getElementById('split-exp-unit').value||'days';
  if(!amount||Number(amount)<=0){{errTxt.textContent='یک مقدار معتبر وارد کن';errEl.classList.add('show');return}}
  try{{
    const r=await fetch('/api/public/split/'+LINK_UUID,{{method:'POST',headers:{{'Content-Type':'application/json'}},
      body:JSON.stringify({{amount,unit,label,expires_value,expires_unit}})}});
    const data=await r.json();
    if(!r.ok){{errTxt.textContent=data.detail||'خطا در ساخت کانفیگ هدیه';errEl.classList.add('show');return}}
    window._rvgSplitUrl=data.child.sub_url;
    document.getElementById('split-result-url').textContent=data.child.sub_url;
    document.getElementById('split-result').classList.add('show');
    toast('کانفیگ هدیه ساخته شد ✓','ok');
    document.getElementById('split-val').value='';document.getElementById('split-label').value='';document.getElementById('split-exp').value='';
    loadChildren();
  }}catch(e){{errTxt.textContent='خطا در ارتباط با سرور';errEl.classList.add('show')}}
}}
function copySplitLinkUrl(){{
  navigator.clipboard.writeText(window._rvgSplitUrl||'').then(()=>toast('لینک کپی شد ✓','ok'));
}}
async function loadChildren(){{
  try{{
    const r=await fetch('/api/public/children/'+LINK_UUID);
    const {{children=[],permissions={{}}}}=await r.json();
    const perms = {{client_can_delete: permissions.client_can_delete!==false, client_can_disable: permissions.client_can_disable!==false}};
    const box=document.getElementById('children-list');
    if(!children.length){{box.innerHTML='';return}}
    box.innerHTML='<div class="children-title">کانفیگ‌های هدیه‌داده‌شده ('+children.length+')</div>'+
      children.map(c=>`
        <div class="child-item">
          <div>
            <div class="child-item-name">${{esc(c.label)}}</div>
            <div class="child-item-meta">${{esc(c.used_fmt)}} از ${{esc(c.limit_fmt)}} · ${{c.active&&!c.expired?'فعال':'غیرفعال'}}</div>
          </div>
          <div style="display:flex;gap:6px">
            <button class="child-revoke" ${{perms.client_can_disable?'':'disabled title="این قابلیت توسط مدیر غیرفعال شده"'}}
              onclick="toggleChild('${{c.uuid}}',${{!c.active}})" style="${{perms.client_can_disable?'':'opacity:.4;cursor:not-allowed'}}"><i class="ti ${{c.active?'ti-power':'ti-play'}}"></i></button>
            <button class="child-revoke" ${{perms.client_can_delete?'':'disabled title="این قابلیت توسط مدیر غیرفعال شده"'}}
              onclick="revokeChild('${{c.uuid}}')" style="${{perms.client_can_delete?'':'opacity:.4;cursor:not-allowed'}}"><i class="ti ti-trash"></i> لغو</button>
          </div>
        </div>
      `).join('');
  }}catch(e){{}}
}}
async function toggleChild(childUuid,active){{
  try{{
    const r=await fetch('/api/public/split/'+LINK_UUID+'/'+childUuid+'/toggle',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{active}})}});
    const data=await r.json().catch(()=>({{}}));
    if(!r.ok){{toast(data.detail||'خطا','');return}}
    toast(active?'فعال شد ✓':'غیرفعال شد','ok');
    loadChildren();
  }}catch(e){{toast('خطا در ارتباط با سرور','')}}
}}
async function revokeChild(childUuid){{
  if(!confirm('این کانفیگ هدیه لغو شود؟ حجم مصرف‌نشده‌اش به خودت برمی‌گردد.'))return;
  try{{
    const r=await fetch('/api/public/split/'+LINK_UUID+'/'+childUuid,{{method:'DELETE'}});
    const data=await r.json().catch(()=>({{}}));
    if(!r.ok){{toast(data.detail||'خطا در لغو','');return}}
    toast('لغو شد، حجم برگشت ✓','ok');
    loadChildren();
    setTimeout(()=>location.reload(),1200);
  }}catch(e){{toast('خطا در لغو','')}}
}}
loadChildren();
</script>
</body></html>"""
