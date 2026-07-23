import json

with open("/home/claude/EV_Adoption_India_Analysis/assets/dashboard_data.json") as f:
    DATA = json.load(f)

DATA_JSON = json.dumps(DATA)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Driving the Future — EV Adoption Intelligence, India</title>
<style>
:root{
  --bg:#080B10;
  --panel:#10151D;
  --panel-2:#141B25;
  --border:#1E2733;
  --text:#EDF1F7;
  --text-dim:#7C8A9C;
  --green:#00E5A0;
  --blue:#2F80ED;
  --gold:#F2C94C;
  --red:#EB5757;
  --purple:#9B6BFF;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{
  background:
    radial-gradient(1200px 600px at 15% -10%, rgba(0,229,160,0.07), transparent 60%),
    radial-gradient(1000px 500px at 90% 0%, rgba(47,128,237,0.08), transparent 60%),
    var(--bg);
  color:var(--text);
  font-family:'Inter',-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  min-height:100vh;
}
@font-face{font-family:'SoraFallback';src:local('Arial');}
h1,h2,h3,.display{font-family:'Sora','Segoe UI',sans-serif;}
.mono{font-family:'JetBrains Mono','Consolas',monospace;}

/* ---------- Layout shell ---------- */
.shell{display:grid;grid-template-columns:220px 1fr;min-height:100vh;}
.rail{
  background:linear-gradient(180deg,var(--panel),var(--bg));
  border-right:1px solid var(--border);
  padding:28px 0 20px;
  display:flex;flex-direction:column;
  position:relative;
}
.brand{padding:0 24px 26px;border-bottom:1px solid var(--border);margin-bottom:10px;}
.brand-mark{display:flex;align-items:center;gap:8px;margin-bottom:6px;}
.bolt{width:20px;height:20px;flex:none;}
.brand-title{font-size:13px;font-weight:700;letter-spacing:0.02em;color:var(--text);}
.brand-sub{font-size:10.5px;color:var(--text-dim);letter-spacing:0.08em;text-transform:uppercase;}

.rail-line{position:absolute;left:24px;top:118px;bottom:100px;width:1px;background:var(--border);overflow:hidden;}
.rail-line::after{
  content:'';position:absolute;left:0;top:-40%;width:100%;height:40%;
  background:linear-gradient(180deg, transparent, var(--green), transparent);
  animation: flow 2.6s linear infinite;
}
@keyframes flow{0%{top:-40%;}100%{top:100%;}}

nav{display:flex;flex-direction:column;padding:14px 12px;gap:2px;position:relative;z-index:1;}
.navbtn{
  display:flex;align-items:center;gap:12px;
  padding:11px 12px;border-radius:8px;cursor:pointer;
  color:var(--text-dim);font-size:13px;font-weight:600;
  border:1px solid transparent;transition:all .18s ease;
  background:transparent;
}
.navbtn svg{width:16px;height:16px;flex:none;opacity:0.85;}
.navbtn:hover{color:var(--text);background:rgba(255,255,255,0.03);}
.navbtn.active{
  color:var(--green);background:rgba(0,229,160,0.08);
  border-color:rgba(0,229,160,0.25);
}
.navbtn .idx{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--text-dim);width:16px;}
.navbtn.active .idx{color:var(--green);}

.rail-foot{margin-top:auto;padding:16px 24px 0;border-top:1px solid var(--border);}
.rail-foot .foot-label{font-size:9.5px;color:var(--text-dim);letter-spacing:.08em;text-transform:uppercase;}
.rail-foot .foot-val{font-size:11px;color:var(--text);margin-top:3px;}

/* ---------- Main ---------- */
main{padding:26px 34px 60px;max-width:1400px;}
.topbar{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:22px;gap:20px;flex-wrap:wrap;}
.page-title{font-size:22px;font-weight:700;margin:0;}
.page-sub{font-size:12.5px;color:var(--text-dim);margin-top:4px;}

.filters{display:flex;gap:10px;flex-wrap:wrap;}
select{
  background:var(--panel-2);color:var(--text);border:1px solid var(--border);
  border-radius:7px;padding:8px 12px;font-size:12.5px;font-family:inherit;
  cursor:pointer;outline:none;
}
select:focus{border-color:var(--green);}

.page{display:none;animation:fadeUp .5s ease both;}
.page.active{display:block;}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:translateY(0);}}

.grid{display:grid;gap:16px;}
.g4{grid-template-columns:repeat(4,1fr);}
.g3{grid-template-columns:repeat(3,1fr);}
.g2{grid-template-columns:1.4fr 1fr;}
.g2b{grid-template-columns:1fr 1fr;}
@media(max-width:1000px){.g4,.g3,.g2,.g2b{grid-template-columns:1fr;}}

.card{
  background:linear-gradient(180deg,var(--panel-2),var(--panel));
  border:1px solid var(--border);border-radius:12px;padding:18px 20px;
  position:relative;overflow:hidden;
}
.card h3{margin:0 0 14px;font-size:12px;color:var(--text-dim);font-weight:600;text-transform:uppercase;letter-spacing:.06em;}

/* KPI cards with battery-charge fill */
.kpi{padding:18px 20px 16px;}
.kpi-top{display:flex;justify-content:space-between;align-items:flex-start;}
.kpi-label{font-size:11.5px;color:var(--text-dim);text-transform:uppercase;letter-spacing:.06em;font-weight:600;}
.kpi-value{font-size:30px;font-weight:700;margin-top:8px;font-family:'JetBrains Mono',monospace;}
.kpi-delta{font-size:11.5px;margin-top:6px;font-weight:600;}
.kpi-delta.up{color:var(--green);}
.kpi-delta.down{color:var(--red);}
.charge-track{height:4px;background:rgba(255,255,255,0.06);border-radius:3px;margin-top:14px;overflow:hidden;}
.charge-fill{height:100%;border-radius:3px;width:0%;transition:width 1.4s cubic-bezier(.16,1,.3,1);}
.g-green{background:linear-gradient(90deg,var(--green),#00ffc2);}
.g-blue{background:linear-gradient(90deg,var(--blue),#63a4ff);}
.g-gold{background:linear-gradient(90deg,var(--gold),#ffe08a);}
.g-purple{background:linear-gradient(90deg,var(--purple),#c9a6ff);}

.chart-wrap{position:relative;height:280px;}
.chart-wrap.tall{height:340px;}
.chart-wrap.short{height:200px;}

table{width:100%;border-collapse:collapse;font-size:12.5px;}
th{
  text-align:left;color:var(--text-dim);font-weight:600;font-size:10.5px;
  text-transform:uppercase;letter-spacing:.05em;padding:8px 10px;
  border-bottom:1px solid var(--border);
}
td{padding:9px 10px;border-bottom:1px solid rgba(255,255,255,0.03);}
tr:hover td{background:rgba(255,255,255,0.02);}
.rank-pill{
  display:inline-flex;align-items:center;justify-content:center;
  width:22px;height:22px;border-radius:6px;font-size:11px;font-weight:700;
  background:rgba(255,255,255,0.05);color:var(--text-dim);
  font-family:'JetBrains Mono',monospace;
}
.bar-cell{display:flex;align-items:center;gap:8px;}
.bar-track{flex:1;height:6px;background:rgba(255,255,255,0.05);border-radius:3px;overflow:hidden;}
.bar-fill{height:100%;border-radius:3px;width:0%;transition:width 1s cubic-bezier(.16,1,.3,1);}
.badge{padding:3px 9px;border-radius:20px;font-size:10.5px;font-weight:700;}
.badge.crit{background:rgba(235,87,87,.14);color:var(--red);}
.badge.mod{background:rgba(242,201,76,.14);color:var(--gold);}
.badge.ok{background:rgba(0,229,160,.14);color:var(--green);}

.cat-strip{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:16px;}
.cat-chip{
  background:var(--panel-2);border:1px solid var(--border);border-radius:10px;
  padding:14px;text-align:center;
}
.cat-chip .cval{font-size:20px;font-weight:700;font-family:'JetBrains Mono',monospace;margin-top:4px;}
.cat-chip .cshare{font-size:11px;color:var(--text-dim);margin-top:2px;}
@media(max-width:900px){.cat-strip{grid-template-columns:repeat(2,1fr);}}

.insight{
  font-size:12.5px;color:var(--text-dim);line-height:1.55;
  border-left:2px solid var(--green);padding:4px 0 4px 12px;margin-top:14px;
}
.insight b{color:var(--text);}

.legend-row{display:flex;gap:16px;flex-wrap:wrap;margin-top:10px;}
.legend-item{display:flex;align-items:center;gap:6px;font-size:11.5px;color:var(--text-dim);}
.legend-dot{width:9px;height:9px;border-radius:50%;}

.scroll-x{overflow-x:auto;}
</style>
</head>
<body>
<div id="loadError" style="display:none;position:fixed;top:0;left:0;right:0;z-index:999;background:#3a1414;color:#ffdada;padding:12px 20px;font:600 13px/1.4 'Inter',sans-serif;border-bottom:1px solid #EB5757;">
  ⚠ Charts couldn't load (Chart.js failed to fetch from every CDN tried — likely no internet connection or a network/firewall block on this machine). KPI numbers and tables below still work. Try opening this file on a device with internet access, or a different network/browser.
</div>
<div class="shell">

  <aside class="rail">
    <div class="brand">
      <div class="brand-mark">
        <svg class="bolt" viewBox="0 0 24 24" fill="none"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z" fill="#00E5A0"/></svg>
        <div class="brand-title">DRIVING THE FUTURE</div>
      </div>
      <div class="brand-sub">EV Intelligence · India</div>
    </div>
    <div class="rail-line"></div>
    <nav id="nav"></nav>
    <div class="rail-foot">
      <div class="foot-label">Data Coverage</div>
      <div class="foot-val mono">2018 – 2025 · 24 States</div>
    </div>
  </aside>

  <main>
    <div class="topbar">
      <div>
        <h1 class="page-title" id="pageTitle">Executive Overview</h1>
        <div class="page-sub" id="pageSub">National EV adoption at a glance</div>
      </div>
      <div class="filters">
        <select id="fState"></select>
        <select id="fCategory"></select>
        <select id="fYear"></select>
      </div>
    </div>

    <!-- PAGE 1: EXECUTIVE OVERVIEW -->
    <section class="page active" data-page="0">
      <div class="grid g4" style="margin-bottom:16px;">
        <div class="card kpi">
          <div class="kpi-top"><div class="kpi-label">Total EV Registrations</div></div>
          <div class="kpi-value" id="kpiTotal">0</div>
          <div class="kpi-delta up">▲ cumulative, 2018–2025</div>
          <div class="charge-track"><div class="charge-fill g-green" id="chargeTotal"></div></div>
        </div>
        <div class="card kpi">
          <div class="kpi-top"><div class="kpi-label">Charging Stations</div></div>
          <div class="kpi-value" id="kpiStations">0</div>
          <div class="kpi-delta up">▲ across all states</div>
          <div class="charge-track"><div class="charge-fill g-blue" id="chargeStations"></div></div>
        </div>
        <div class="card kpi">
          <div class="kpi-top"><div class="kpi-label">2024 YoY Growth</div></div>
          <div class="kpi-value" id="kpiGrowth">0%</div>
          <div class="kpi-delta up" id="kpiGrowthDelta">▲ vs 2023</div>
          <div class="charge-track"><div class="charge-fill g-gold" id="chargeGrowth"></div></div>
        </div>
        <div class="card kpi">
          <div class="kpi-top"><div class="kpi-label">States / UTs Tracked</div></div>
          <div class="kpi-value" id="kpiStates">0</div>
          <div class="kpi-delta up">▲ pan-India coverage</div>
          <div class="charge-track"><div class="charge-fill g-purple" id="chargeStates"></div></div>
        </div>
      </div>

      <div class="grid g2">
        <div class="card">
          <h3>EV Growth Trend — National (2018–2025)</h3>
          <div class="chart-wrap tall"><canvas id="chartTrend"></canvas></div>
          <div class="insight">India's EV market shows a <b>COVID-era dip in 2020</b>, followed by acceleration post-FAME-II policy support — <b>~42% CAGR</b> from 2019–2024.</div>
        </div>
        <div class="card">
          <h3>Category Market Share</h3>
          <div class="chart-wrap"><canvas id="chartDonutMini"></canvas></div>
        </div>
      </div>

      <div class="grid g2b" style="margin-top:16px;">
        <div class="card">
          <h3>Top 5 States by Registrations</h3>
          <div class="chart-wrap short"><canvas id="chartTop5"></canvas></div>
        </div>
        <div class="card">
          <h3>Infrastructure Snapshot</h3>
          <div class="chart-wrap short"><canvas id="chartInfraMini"></canvas></div>
        </div>
      </div>
    </section>

    <!-- PAGE 2: STATE-WISE ANALYSIS -->
    <section class="page" data-page="1">
      <div class="grid g2" style="align-items:start;">
        <div class="card">
          <h3>EV Registrations by State (Top 15)</h3>
          <div class="chart-wrap tall"><canvas id="chartStateBar"></canvas></div>
        </div>
        <div class="card">
          <h3>State Ranking</h3>
          <div class="scroll-x" style="max-height:380px;overflow-y:auto;">
            <table id="stateTable">
              <thead><tr><th>#</th><th>State / UT</th><th>Registrations</th><th></th></tr></thead>
              <tbody></tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="grid g2b" style="margin-top:16px;">
        <div class="card">
          <h3>Top 10 States</h3>
          <div class="chart-wrap short"><canvas id="chartTop10"></canvas></div>
        </div>
        <div class="card">
          <h3>Bottom 10 States</h3>
          <div class="chart-wrap short"><canvas id="chartBottom10"></canvas></div>
        </div>
      </div>
    </section>

    <!-- PAGE 3: VEHICLE CATEGORY -->
    <section class="page" data-page="2">
      <div class="cat-strip" id="catStrip"></div>
      <div class="grid g2">
        <div class="card">
          <h3>Category Trend Over Time</h3>
          <div class="chart-wrap tall"><canvas id="chartCatTrend"></canvas></div>
        </div>
        <div class="card">
          <h3>Overall Market Share</h3>
          <div class="chart-wrap"><canvas id="chartCatDonut"></canvas></div>
          <div class="insight" id="fastestGrowing"></div>
        </div>
      </div>
      <div class="card" style="margin-top:16px;">
        <h3>Top Manufacturers by Category</h3>
        <div class="scroll-x">
          <table id="manuCatTable">
            <thead><tr><th>Category</th><th>Manufacturer</th><th>Registrations</th><th></th></tr></thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- PAGE 4: CHARGING INFRASTRUCTURE -->
    <section class="page" data-page="3">
      <div class="grid g2b">
        <div class="card">
          <h3>Charging Stations by State</h3>
          <div class="chart-wrap tall"><canvas id="chartStationsByState"></canvas></div>
        </div>
        <div class="card">
          <h3>EV-to-Charging-Station Ratio (Gap Indicator)</h3>
          <div class="chart-wrap tall"><canvas id="chartGapRatio"></canvas></div>
        </div>
      </div>
      <div class="card" style="margin-top:16px;">
        <h3>Infrastructure Gap Analysis</h3>
        <div class="scroll-x">
          <table id="gapTable">
            <thead><tr><th>State</th><th>EV Registrations</th><th>Charging Stations</th><th>EV / Station</th><th>Status</th></tr></thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- PAGE 5: TIME SERIES -->
    <section class="page" data-page="4">
      <div class="card">
        <h3>Monthly Registration Trend (Full Time Series)</h3>
        <div class="chart-wrap tall"><canvas id="chartMonthly"></canvas></div>
      </div>
      <div class="grid g2b" style="margin-top:16px;">
        <div class="card">
          <h3>Yearly Trend</h3>
          <div class="chart-wrap short"><canvas id="chartYearlyBar"></canvas></div>
        </div>
        <div class="card">
          <h3>Seasonal Pattern (Avg by Calendar Month)</h3>
          <div class="chart-wrap short"><canvas id="chartSeasonal"></canvas></div>
        </div>
      </div>
    </section>

    <!-- PAGE 6: FORECAST -->
    <section class="page" data-page="5">
      <div class="grid g3" style="margin-bottom:16px;">
        <div class="card kpi">
          <div class="kpi-label">Projected 2030 Registrations</div>
          <div class="kpi-value" id="fcst2030">0</div>
          <div class="kpi-delta up">▲ ensemble forecast</div>
          <div class="charge-track"><div class="charge-fill g-green" id="chargeFcst"></div></div>
        </div>
        <div class="card kpi">
          <div class="kpi-label">Projected CAGR (2024–2030)</div>
          <div class="kpi-value" id="fcstCagr">0%</div>
          <div class="kpi-delta up">▼ moderating from ~42%</div>
          <div class="charge-track"><div class="charge-fill g-blue" id="chargeCagr"></div></div>
        </div>
        <div class="card kpi">
          <div class="kpi-label">5-Yr Volume Multiple</div>
          <div class="kpi-value" id="fcstMultiple">0x</div>
          <div class="kpi-delta up">▲ vs 2024 baseline</div>
          <div class="charge-track"><div class="charge-fill g-gold" id="chargeMultiple"></div></div>
        </div>
      </div>
      <div class="card">
        <h3>Historical &amp; 5-Year Forecast with 95% Confidence Interval</h3>
        <div class="chart-wrap tall"><canvas id="chartForecast"></canvas></div>
        <div class="legend-row">
          <div class="legend-item"><span class="legend-dot" style="background:#00E5A0"></span>Historical</div>
          <div class="legend-item"><span class="legend-dot" style="background:#2F80ED"></span>Ensemble Forecast</div>
          <div class="legend-item"><span class="legend-dot" style="background:rgba(47,128,237,0.35)"></span>95% Confidence Band</div>
        </div>
      </div>
      <div class="card" style="margin-top:16px;">
        <h3>Model Comparison (2026–2030)</h3>
        <table id="fcstTable">
          <thead><tr><th>Year</th><th>Log-Linear</th><th>Damped Holt's Trend</th><th>Ensemble</th><th>95% CI</th></tr></thead>
          <tbody></tbody>
        </table>
      </div>
    </section>

  </main>
</div>

<script>
function startDashboard(){
const DATA = __DATA_JSON__;
const COLORS = {green:'#00E5A0',blue:'#2F80ED',gold:'#F2C94C',red:'#EB5757',purple:'#9B6BFF',dim:'#7C8A9C'};
const CAT_COLORS = ['#00E5A0','#2F80ED','#F2C94C','#EB5757','#9B6BFF'];
Chart.defaults.color = COLORS.dim;
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.borderColor = 'rgba(255,255,255,0.05)';

const inr = n => Math.round(n).toLocaleString('en-IN');
const gridOpt = {color:'rgba(255,255,255,0.05)', drawTicks:false};

// ---------- Nav ----------
const pages = [
  {name:'Executive Overview', sub:'National EV adoption at a glance', icon:'grid'},
  {name:'State-wise Analysis', sub:'Ranking states by adoption volume', icon:'map'},
  {name:'Vehicle Category', sub:'2W · 3W · Car · Bus · Commercial breakdown', icon:'car'},
  {name:'Charging Infrastructure', sub:'Where supply is falling behind demand', icon:'plug'},
  {name:'Time Series', sub:'Monthly, yearly and seasonal patterns', icon:'clock'},
  {name:'Forecast', sub:'Projected growth through 2030', icon:'trend'},
];
const ICONS = {
  grid:'<path d="M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z" stroke="currentColor" stroke-width="1.6" fill="none"/>',
  map:'<path d="M12 21s7-6.4 7-12a7 7 0 10-14 0c0 5.6 7 12 7 12z" stroke="currentColor" stroke-width="1.6" fill="none"/><circle cx="12" cy="9" r="2.4" stroke="currentColor" stroke-width="1.6" fill="none"/>',
  car:'<path d="M3 13l1.6-5A2 2 0 016.5 6.5h11a2 2 0 011.9 1.5L21 13v5a1 1 0 01-1 1h-1a1 1 0 01-1-1v-1H6v1a1 1 0 01-1 1H4a1 1 0 01-1-1v-5z" stroke="currentColor" stroke-width="1.5" fill="none"/><circle cx="7.5" cy="16.5" r="1.3" fill="currentColor"/><circle cx="16.5" cy="16.5" r="1.3" fill="currentColor"/>',
  plug:'<path d="M9 3v5M15 3v5M7 8h10v4a5 5 0 01-10 0V8z" stroke="currentColor" stroke-width="1.6" fill="none"/><path d="M12 17v4" stroke="currentColor" stroke-width="1.6"/>',
  clock:'<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6" fill="none"/><path d="M12 7v5l3.5 2" stroke="currentColor" stroke-width="1.6" fill="none"/>',
  trend:'<path d="M3 17l6-6 4 4 7-8" stroke="currentColor" stroke-width="1.8" fill="none"/><path d="M15 7h5v5" stroke="currentColor" stroke-width="1.8" fill="none"/>',
};
const navEl = document.getElementById('nav');
pages.forEach((p,i)=>{
  const btn = document.createElement('div');
  btn.className = 'navbtn' + (i===0?' active':'');
  btn.innerHTML = `<span class="idx">0${i+1}</span><svg viewBox="0 0 24 24">${ICONS[p.icon]}</svg><span>${p.name}</span>`;
  btn.onclick = ()=> showPage(i);
  navEl.appendChild(btn);
});

function showPage(i){
  document.querySelectorAll('.navbtn').forEach((b,j)=>b.classList.toggle('active', j===i));
  document.querySelectorAll('.page').forEach(s=>s.classList.toggle('active', s.dataset.page==i));
  document.getElementById('pageTitle').textContent = pages[i].name;
  document.getElementById('pageSub').textContent = pages[i].sub;
}

// ---------- Filters ----------
const fState = document.getElementById('fState');
const fCategory = document.getElementById('fCategory');
const fYear = document.getElementById('fYear');
fState.innerHTML = '<option value="__all__">All States</option>' + DATA.state.map(s=>`<option value="${s.State_UT}">${s.State_UT}</option>`).join('');
fCategory.innerHTML = '<option value="__all__">All Categories</option>' + DATA.categories.map(c=>`<option value="${c}">${c}</option>`).join('');
fYear.innerHTML = '<option value="__all__">All Years</option>' + DATA.yearly.map(y=>`<option value="${y.year}">${y.year}</option>`).join('');
[fState,fCategory,fYear].forEach(el=>el.addEventListener('change', ()=>highlightState(fState.value)));

// ---------- Animated counter ----------
function animateCount(el, target, suffix='', decimals=0){
  const start = 0, duration = 1200, startTime = performance.now();
  function step(now){
    const t = Math.min((now-startTime)/duration, 1);
    const eased = 1 - Math.pow(1-t, 3);
    const val = start + (target-start)*eased;
    el.textContent = (decimals>0 ? val.toFixed(decimals) : inr(val)) + suffix;
    if(t<1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
function fillCharge(el, pct){ requestAnimationFrame(()=> el.style.width = Math.min(pct,100)+'%'); }

// ---------- KPIs (Page 1) ----------
animateCount(document.getElementById('kpiTotal'), DATA.kpis.total_registrations);
animateCount(document.getElementById('kpiStations'), DATA.kpis.total_charging_stations);
animateCount(document.getElementById('kpiGrowth'), DATA.kpis.yoy_growth_2024, '%', 1);
animateCount(document.getElementById('kpiStates'), DATA.kpis.total_states);
fillCharge(document.getElementById('chargeTotal'), 92);
fillCharge(document.getElementById('chargeStations'), 68);
fillCharge(document.getElementById('chargeGrowth'), Math.min(DATA.kpis.yoy_growth_2024*3,100));
fillCharge(document.getElementById('chargeStates'), (DATA.kpis.total_states/28)*100);

// ---------- Chart: Trend (Executive) ----------
new Chart(document.getElementById('chartTrend'), {
  type:'line',
  data:{
    labels: DATA.yearly.map(y=>y.year),
    datasets:[{
      label:'EV Registrations', data: DATA.yearly.map(y=>y.total),
      borderColor: COLORS.green, backgroundColor:'rgba(0,229,160,0.12)',
      fill:true, tension:0.35, pointRadius:3, pointBackgroundColor:COLORS.green, borderWidth:2.5,
    }]
  },
  options:{
    responsive:true, maintainAspectRatio:false,
    animation:{duration:1400, easing:'easeOutCubic'},
    plugins:{legend:{display:false}, tooltip:{callbacks:{label:c=>' '+inr(c.parsed.y)+' registrations'}}},
    scales:{ y:{grid:gridOpt, ticks:{callback:v=>inr(v)}}, x:{grid:{display:false}} }
  }
});

// ---------- Chart: Category donut mini ----------
function makeDonut(canvasId){
  return new Chart(document.getElementById(canvasId), {
    type:'doughnut',
    data:{
      labels: DATA.category_totals.map(c=>c.category),
      datasets:[{ data: DATA.category_totals.map(c=>c.total), backgroundColor: CAT_COLORS, borderColor:'#10151D', borderWidth:3 }]
    },
    options:{
      responsive:true, maintainAspectRatio:false, cutout:'68%',
      animation:{animateRotate:true, duration:1200},
      plugins:{legend:{position:'bottom', labels:{boxWidth:9, padding:12, font:{size:10.5}}}}
    }
  });
}
makeDonut('chartDonutMini');
makeDonut('chartCatDonut');

// ---------- Chart: Top 5 states mini (Executive) ----------
const top5 = DATA.state.slice(0,5);
new Chart(document.getElementById('chartTop5'), {
  type:'bar',
  data:{ labels: top5.map(s=>s.State_UT), datasets:[{ data: top5.map(s=>s.total), backgroundColor: COLORS.green, borderRadius:5, maxBarThickness:26 }] },
  options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:{duration:1000},
    plugins:{legend:{display:false}, tooltip:{callbacks:{label:c=>' '+inr(c.parsed.x)}}},
    scales:{ x:{grid:gridOpt, ticks:{callback:v=>inr(v)}}, y:{grid:{display:false}} } }
});

// ---------- Chart: Infra mini (Executive) ----------
const infraTop5 = [...DATA.state].sort((a,b)=>b.ev_per_station-a.ev_per_station).slice(0,5);
new Chart(document.getElementById('chartInfraMini'), {
  type:'bar',
  data:{ labels: infraTop5.map(s=>s.State_UT), datasets:[{ data: infraTop5.map(s=>s.ev_per_station), backgroundColor: COLORS.red, borderRadius:5, maxBarThickness:26 }] },
  options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:{duration:1000},
    plugins:{legend:{display:false}, tooltip:{callbacks:{label:c=>' '+c.parsed.x+' EVs per station'}}},
    scales:{ x:{grid:gridOpt}, y:{grid:{display:false}} } }
});

// ---------- Page 2: State-wise ----------
const stateSorted = [...DATA.state].sort((a,b)=>b.total-a.total);
let chartStateBar = new Chart(document.getElementById('chartStateBar'), {
  type:'bar',
  data:{ labels: stateSorted.slice(0,15).map(s=>s.State_UT),
    datasets:[{ data: stateSorted.slice(0,15).map(s=>s.total), backgroundColor: COLORS.blue, borderRadius:5, maxBarThickness:22 }] },
  options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:{duration:1200},
    plugins:{legend:{display:false}, tooltip:{callbacks:{label:c=>' '+inr(c.parsed.x)}}},
    scales:{ x:{grid:gridOpt, ticks:{callback:v=>inr(v)}}, y:{grid:{display:false}} } }
});

const maxTotal = Math.max(...stateSorted.map(s=>s.total));
const tbody = document.querySelector('#stateTable tbody');
stateSorted.forEach((s,i)=>{
  const tr = document.createElement('tr');
  tr.innerHTML = `<td><span class="rank-pill">${i+1}</span></td><td>${s.State_UT}</td>
    <td class="mono">${inr(s.total)}</td>
    <td><div class="bar-cell"><div class="bar-track"><div class="bar-fill g-blue" data-w="${(s.total/maxTotal*100).toFixed(1)}"></div></div></div></td>`;
  tbody.appendChild(tr);
});
setTimeout(()=>document.querySelectorAll('#stateTable .bar-fill').forEach(el=>el.style.width=el.dataset.w+'%'), 150);

new Chart(document.getElementById('chartTop10'), {
  type:'bar',
  data:{ labels: stateSorted.slice(0,10).map(s=>s.State_UT), datasets:[{ data: stateSorted.slice(0,10).map(s=>s.total), backgroundColor: COLORS.green, borderRadius:5 }] },
  options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:{duration:1000},
    plugins:{legend:{display:false}}, scales:{ x:{grid:gridOpt, ticks:{callback:v=>inr(v)}}, y:{grid:{display:false}, ticks:{font:{size:10}}} } }
});
const bottom10 = [...stateSorted].slice(-10).reverse();
new Chart(document.getElementById('chartBottom10'), {
  type:'bar',
  data:{ labels: bottom10.map(s=>s.State_UT), datasets:[{ data: bottom10.map(s=>s.total), backgroundColor: COLORS.red, borderRadius:5 }] },
  options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:{duration:1000},
    plugins:{legend:{display:false}}, scales:{ x:{grid:gridOpt, ticks:{callback:v=>inr(v)}}, y:{grid:{display:false}, ticks:{font:{size:10}}} } }
});

function highlightState(name){
  chartStateBar.data.datasets[0].backgroundColor = stateSorted.slice(0,15).map(s=> (name==='__all__'||s.State_UT===name) ? COLORS.blue : 'rgba(47,128,237,0.18)');
  chartStateBar.update();
}

// ---------- Page 3: Vehicle Category ----------
const catStrip = document.getElementById('catStrip');
const catTotalSum = DATA.category_totals.reduce((a,c)=>a+c.total,0);
DATA.category_totals.forEach((c,i)=>{
  const share = (c.total/catTotalSum*100).toFixed(1);
  const div = document.createElement('div');
  div.className='cat-chip';
  div.innerHTML = `<div style="font-size:11px;color:${CAT_COLORS[i]};font-weight:700;letter-spacing:.04em;">${c.category}</div>
    <div class="cval">${inr(c.total)}</div><div class="cshare">${share}% share</div>`;
  catStrip.appendChild(div);
});

const catYearYears = DATA.category_year.map(r=>r.Year);
let catTrendDatasets = DATA.categories.map((cat,i)=>({
  label:cat, data: DATA.category_year.map(r=>r[cat]||0),
  backgroundColor: CAT_COLORS[i], borderColor: CAT_COLORS[i],
  fill:true, tension:0.3, stack:'cat'
}));
new Chart(document.getElementById('chartCatTrend'), {
  type:'line',
  data:{ labels: catYearYears, datasets: catTrendDatasets },
  options:{ responsive:true, maintainAspectRatio:false, animation:{duration:1300},
    plugins:{legend:{position:'bottom', labels:{boxWidth:9,font:{size:10.5}}}},
    scales:{ y:{stacked:true, grid:gridOpt, ticks:{callback:v=>inr(v)}}, x:{stacked:true, grid:{display:false}} } }
});

// fastest growing category insight (computed from data)
const firstYear = Math.min(...DATA.category_year.map(r=>r.Year));
const lastFullYear = 2024;
const firstRow = DATA.category_year.find(r=>r.Year===firstYear);
const lastRow = DATA.category_year.find(r=>r.Year===lastFullYear);
let fastest = {cat:'', cagr:-999};
DATA.categories.forEach(cat=>{
  const s = firstRow[cat]||0, e = lastRow[cat]||0;
  if(s>0){ const cagr = Math.pow(e/s, 1/(lastFullYear-firstYear))-1; if(cagr>fastest.cagr) fastest={cat,cagr}; }
});
document.getElementById('fastestGrowing').innerHTML = `<b>${fastest.cat}</b> is the fastest-growing category at a <b>${(fastest.cagr*100).toFixed(0)}% CAGR</b> (${firstYear}–${lastFullYear}), though from a smaller base than Two-Wheelers.`;

const manuTbody = document.querySelector('#manuCatTable tbody');
const manuMax = Math.max(...DATA.manufacturer_by_category.map(r=>r.Monthly_EV_Registrations));
DATA.manufacturer_by_category.forEach(r=>{
  const tr = document.createElement('tr');
  tr.innerHTML = `<td>${r.Vehicle_Category}</td><td>${r.Manufacturer}</td><td class="mono">${inr(r.Monthly_EV_Registrations)}</td>
    <td><div class="bar-cell"><div class="bar-track"><div class="bar-fill g-purple" data-w="${(r.Monthly_EV_Registrations/manuMax*100).toFixed(1)}"></div></div></div></td>`;
  manuTbody.appendChild(tr);
});
setTimeout(()=>document.querySelectorAll('#manuCatTable .bar-fill').forEach(el=>el.style.width=el.dataset.w+'%'), 150);

// ---------- Page 4: Charging Infrastructure ----------
const stateByStations = [...DATA.state].sort((a,b)=>b.charging_stations-a.charging_stations).slice(0,15);
new Chart(document.getElementById('chartStationsByState'), {
  type:'bar',
  data:{ labels: stateByStations.map(s=>s.State_UT), datasets:[{ data: stateByStations.map(s=>s.charging_stations), backgroundColor: COLORS.blue, borderRadius:5 }] },
  options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:{duration:1200},
    plugins:{legend:{display:false}}, scales:{ x:{grid:gridOpt}, y:{grid:{display:false}, ticks:{font:{size:10}}} } }
});
const gapSorted = [...DATA.state].sort((a,b)=>b.ev_per_station-a.ev_per_station).slice(0,15);
const avgRatio = DATA.state.reduce((a,s)=>a+s.ev_per_station,0)/DATA.state.length;
new Chart(document.getElementById('chartGapRatio'), {
  type:'bar',
  data:{ labels: gapSorted.map(s=>s.State_UT),
    datasets:[{ data: gapSorted.map(s=>s.ev_per_station),
      backgroundColor: gapSorted.map(s=> s.ev_per_station>avgRatio*1.3?COLORS.red : s.ev_per_station>avgRatio?COLORS.gold:COLORS.green),
      borderRadius:5 }] },
  options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:{duration:1200},
    plugins:{legend:{display:false}, tooltip:{callbacks:{label:c=>' '+c.parsed.x+' EVs per charging station'}}},
    scales:{ x:{grid:gridOpt}, y:{grid:{display:false}, ticks:{font:{size:10}}} } }
});

const gapTbody = document.querySelector('#gapTable tbody');
[...DATA.state].sort((a,b)=>b.ev_per_station-a.ev_per_station).forEach(s=>{
  let badge = s.ev_per_station>avgRatio*1.3 ? ['crit','Critical Gap'] : s.ev_per_station>avgRatio ? ['mod','Moderate Gap'] : ['ok','Adequate'];
  const tr = document.createElement('tr');
  tr.innerHTML = `<td>${s.State_UT}</td><td class="mono">${inr(s.total)}</td><td class="mono">${inr(s.charging_stations)}</td>
    <td class="mono">${s.ev_per_station}</td><td><span class="badge ${badge[0]}">${badge[1]}</span></td>`;
  gapTbody.appendChild(tr);
});

// ---------- Page 5: Time Series ----------
new Chart(document.getElementById('chartMonthly'), {
  type:'line',
  data:{ labels: DATA.monthly_trend.map(r=>r.label),
    datasets:[{ data: DATA.monthly_trend.map(r=>r.total), borderColor: COLORS.blue, backgroundColor:'rgba(47,128,237,0.1)',
      fill:true, tension:0.25, pointRadius:0, borderWidth:2 }] },
  options:{ responsive:true, maintainAspectRatio:false, animation:{duration:1500},
    plugins:{legend:{display:false}}, scales:{ y:{grid:gridOpt, ticks:{callback:v=>inr(v)}}, x:{grid:{display:false}, ticks:{maxTicksLimit:12, font:{size:9}}} } }
});
new Chart(document.getElementById('chartYearlyBar'), {
  type:'bar',
  data:{ labels: DATA.yearly.map(y=>y.year), datasets:[{ data: DATA.yearly.map(y=>y.total), backgroundColor: COLORS.green, borderRadius:6 }] },
  options:{ responsive:true, maintainAspectRatio:false, animation:{duration:1100},
    plugins:{legend:{display:false}}, scales:{ y:{grid:gridOpt, ticks:{callback:v=>inr(v)}}, x:{grid:{display:false}} } }
});
const monthNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
new Chart(document.getElementById('chartSeasonal'), {
  type:'line',
  data:{ labels: DATA.seasonality.map(r=>monthNames[r.month-1]), datasets:[{ data: DATA.seasonality.map(r=>r.avg),
    borderColor: COLORS.gold, backgroundColor:'rgba(242,201,76,0.12)', fill:true, tension:0.4, pointBackgroundColor:COLORS.gold, borderWidth:2.5 }] },
  options:{ responsive:true, maintainAspectRatio:false, animation:{duration:1200},
    plugins:{legend:{display:false}}, scales:{ y:{grid:gridOpt}, x:{grid:{display:false}} } }
});

// ---------- Page 6: Forecast ----------
const hist = DATA.yearly.map(y=>({year:y.year, val:y.total}));
const fc = DATA.forecast;
const fc2024 = hist.find(h=>h.year===2024).val;
const fc2030 = fc.find(r=>r.year===2030).forecast_ensemble;
const cagrFcst = (Math.pow(fc2030/fc2024, 1/6)-1)*100;
animateCount(document.getElementById('fcst2030'), fc2030);
animateCount(document.getElementById('fcstCagr'), cagrFcst, '%', 1);
animateCount(document.getElementById('fcstMultiple'), fc2030/fc2024, 'x', 1);
fillCharge(document.getElementById('chargeFcst'), 88);
fillCharge(document.getElementById('chargeCagr'), Math.min(cagrFcst*2.2,100));
fillCharge(document.getElementById('chargeMultiple'), Math.min((fc2030/fc2024)*16,100));

const allYears = [...hist.map(h=>h.year), ...fc.map(r=>r.year)];
const histSeries = allYears.map(y=>{ const h = hist.find(x=>x.year===y); return h? h.val : null; });
const ensSeries = allYears.map(y=>{ const f = fc.find(x=>x.year===y); return f? f.forecast_ensemble : (y===2025? hist.find(x=>x.year===2025).val : null); });
const lowerSeries = allYears.map(y=>{ const f = fc.find(x=>x.year===y); return f? f.lower_95_ci : null; });
const upperSeries = allYears.map(y=>{ const f = fc.find(x=>x.year===y); return f? f.upper_95_ci : null; });

new Chart(document.getElementById('chartForecast'), {
  type:'line',
  data:{ labels: allYears,
    datasets:[
      { label:'Upper CI', data:upperSeries, borderColor:'transparent', backgroundColor:'rgba(47,128,237,0.15)', fill:'+1', pointRadius:0, tension:0.3 },
      { label:'Lower CI', data:lowerSeries, borderColor:'transparent', backgroundColor:'rgba(47,128,237,0.15)', fill:false, pointRadius:0, tension:0.3 },
      { label:'Forecast (Ensemble)', data:ensSeries, borderColor:COLORS.blue, borderDash:[6,4], pointRadius:3, pointBackgroundColor:COLORS.blue, tension:0.3, borderWidth:2.5 },
      { label:'Historical', data:histSeries, borderColor:COLORS.green, pointRadius:3, pointBackgroundColor:COLORS.green, tension:0.3, borderWidth:2.5 },
    ]
  },
  options:{ responsive:true, maintainAspectRatio:false, animation:{duration:1600, easing:'easeOutCubic'},
    plugins:{legend:{display:false}, tooltip:{filter:i=>i.datasetIndex>=2, callbacks:{label:c=>' '+inr(c.parsed.y)}}},
    scales:{ y:{grid:gridOpt, ticks:{callback:v=>inr(v)}}, x:{grid:{display:false}} } }
});

const fcstTbody = document.querySelector('#fcstTable tbody');
fc.forEach(r=>{
  const tr = document.createElement('tr');
  tr.innerHTML = `<td>${r.year}</td><td class="mono">${inr(r.forecast_log_linear)}</td><td class="mono">${inr(r.forecast_damped_holt)}</td>
    <td class="mono" style="color:${COLORS.green};font-weight:700;">${inr(r.forecast_ensemble)}</td>
    <td class="mono" style="color:var(--text-dim);font-size:11.5px;">${inr(r.lower_95_ci)} – ${inr(r.upper_95_ci)}</td>`;
  fcstTbody.appendChild(tr);
});
} // end startDashboard()

// ---------- Resilient Chart.js loader (tries several CDNs, falls back gracefully) ----------
(function loadChartJs(){
  var sources = [
    'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.4/chart.umd.min.js',
    'https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js',
    'https://unpkg.com/chart.js@4.4.4/dist/chart.umd.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.0/chart.umd.min.js'
  ];
  var i = 0, started = false;

  function begin(){
    if(started) return;
    started = true;
    startDashboard();
  }

  function useStub(){
    document.getElementById('loadError').style.display = 'block';
    if(typeof window.Chart === 'undefined'){
      window.Chart = function(ctx, cfg){ this.data = (cfg&&cfg.data)||{datasets:[]}; this.options=(cfg&&cfg.options)||{}; };
      Chart.prototype.update = function(){};
      Chart.defaults = { font:{}, plugins:{} };
    }
    begin();
  }

  function tryNext(){
    if(i >= sources.length){ useStub(); return; }
    var s = document.createElement('script');
    s.src = sources[i++];
    var done = false;
    var timeout = setTimeout(function(){ if(!done){ done = true; tryNext(); } }, 4000);
    s.onload = function(){
      if(done) return; done = true; clearTimeout(timeout);
      if(typeof Chart !== 'undefined'){ begin(); } else { tryNext(); }
    };
    s.onerror = function(){
      if(done) return; done = true; clearTimeout(timeout); tryNext();
    };
    document.head.appendChild(s);
  }

  tryNext();
})();
</script>
</body>
</html>
"""

HTML = HTML.replace("__DATA_JSON__", DATA_JSON)

out_path = "/mnt/user-data/outputs/EV_Adoption_Dashboard.html"
with open(out_path, "w") as f:
    f.write(HTML)

print(f"Written {len(HTML):,} chars to {out_path}")
