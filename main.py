from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="M&A-SWARM OMNIBUS v12.1 GLOBAL", version="12.1")

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>M&A-SWARM OMNIBUS v12.1 | Global Omnibus Terminal</title>
  <style>
    :root {
      --bg-core: #010206;
      --panel-bg: rgba(6, 10, 20, 0.94);
      --panel-border: rgba(255, 255, 255, 0.1);
      --text-main: #f8fafc;
      --text-sub: #94a3b8;
      --accent-cyan: #38bdf8;
      --accent-emerald: #10b981;
      --accent-gold: #fbbf24;
      --accent-orange: #f97316;
      --accent-purple: #c084fc;
      --font-mono: "JetBrains Mono", Consolas, monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; -webkit-font-smoothing: antialiased; }
    html, body { background-color: var(--bg-core); color: var(--text-main); height: 100vh; width: 100vw; overflow: hidden; }
    body { display: flex; flex-direction: column; padding: 6px; gap: 6px; }
    #globalCanvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; }
    .app-viewport { position: relative; z-index: 1; width: 100%; height: 100%; display: flex; flex-direction: column; gap: 6px; max-width: 1920px; margin: 0 auto; }
    header { background: var(--panel-bg); backdrop-filter: blur(24px); border: 1px solid var(--panel-border); border-radius: 8px; padding: 8px 14px; display: flex; justify-content: space-between; align-items: center; flex-shrink: 0; }
    .brand-title { font-weight: 900; font-size: 0.9rem; background: linear-gradient(135deg, #fff, var(--accent-cyan)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .global-controls { display: flex; gap: 6px; align-items: center; }
    .select-lang, .select-curr { background: #020408; border: 1px solid var(--panel-border); color: var(--accent-cyan); font-size: 0.6rem; padding: 3px 6px; border-radius: 4px; outline: none; font-weight: 700; cursor: pointer; }
    .owner-ticker { background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(56, 189, 248, 0.08)); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 8px 12px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; flex-shrink: 0; }
    .ot-item { display: flex; flex-direction: column; gap: 1px; }
    .ot-lbl { font-size: 0.55rem; color: var(--text-sub); text-transform: uppercase; }
    .ot-val { font-size: 1.05rem; font-weight: 900; font-family: var(--font-mono); }
    .global-grid { display: grid; grid-template-columns: 1.4fr 1fr; gap: 6px; flex-grow: 1; min-height: 0; }
    @media (max-width: 960px) { .global-grid { grid-template-columns: 1fr; } }
    .panel { background: var(--panel-bg); backdrop-filter: blur(20px); border: 1px solid var(--panel-border); border-radius: 8px; padding: 8px; display: flex; flex-direction: column; gap: 6px; min-height: 0; flex-grow: 1; }
    .panel-heading { font-size: 0.68rem; font-weight: 800; color: var(--text-sub); display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--panel-border); padding-bottom: 4px; flex-shrink: 0; }
    .super-switcher { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; flex-shrink: 0; }
    .ss-btn { background: rgba(255, 255, 255, 0.02); border: 1px solid var(--panel-border); border-radius: 6px; padding: 8px; text-align: center; cursor: pointer; transition: 0.2s; }
    .ss-btn.active.buy { background: rgba(56, 189, 248, 0.12); border-color: var(--accent-cyan); }
    .ss-btn.active.sell { background: rgba(249, 115, 22, 0.12); border-color: var(--accent-orange); }
    .ss-title { font-size: 0.75rem; font-weight: 900; }
    .ss-sub { font-size: 0.55rem; color: var(--text-sub); margin-top: 1px; }
    .market-scroll { display: flex; flex-direction: column; gap: 6px; overflow-y: auto; flex-grow: 1; padding-right: 2px; }
    .asset-tile { background: rgba(255, 255, 255, 0.015); border: 1px solid var(--panel-border); border-radius: 6px; padding: 8px 10px; display: flex; flex-direction: column; gap: 4px; flex-shrink: 0; }
    .asset-tile:hover { border-color: var(--accent-cyan); }
    .at-top { display: flex; justify-content: space-between; align-items: center; font-size: 0.6rem; }
    .at-tag { background: rgba(56, 189, 248, 0.15); color: var(--accent-cyan); padding: 1px 6px; border-radius: 3px; font-weight: 700; }
    .at-name { font-size: 0.78rem; font-weight: 800; color: #fff; }
    .at-desc { font-size: 0.58rem; color: var(--text-sub); line-height: 1.3; }
    .at-bottom { display: flex; justify-content: space-between; align-items: flex-end; margin-top: 2px; }
    .at-price { font-size: 0.95rem; font-weight: 900; color: var(--accent-gold); font-family: var(--font-mono); }
    .btn-action-glow { background: var(--accent-cyan); color: #000; border: none; padding: 5px 10px; border-radius: 4px; font-weight: 900; font-size: 0.62rem; cursor: pointer; }
    .ai-wizard-box { display: flex; flex-direction: column; gap: 8px; flex-grow: 1; justify-content: center; background: linear-gradient(135deg, rgba(249, 115, 22, 0.04), rgba(0,0,0,0)); border: 1px dashed rgba(249, 115, 22, 0.4); border-radius: 6px; padding: 12px; }
    .input-field-group { display: flex; flex-direction: column; gap: 3px; }
    .input-lbl { font-size: 0.62rem; color: var(--text-sub); font-weight: 700; }
    .supreme-input { background: #020408; border: 1px solid var(--panel-border); border-radius: 4px; padding: 8px; color: #fff; font-size: 0.75rem; outline: none; }
    .btn-wizard-submit { background: linear-gradient(135deg, var(--accent-orange), #c2410c); color: #fff; border: none; padding: 10px; border-radius: 6px; font-weight: 900; font-size: 0.75rem; cursor: pointer; }
    .right-viz-stack { display: flex; flex-direction: column; gap: 6px; flex-grow: 1; min-height: 0; }
    .chart-canvas-box { width: 100%; height: 110px; background: #010306; border-radius: 6px; border: 1px solid var(--panel-border); flex-shrink: 0; }
    .terminal-output { background: #010306; border: 1px solid var(--panel-border); border-radius: 6px; padding: 6px; font-family: var(--font-mono); font-size: 0.6rem; color: var(--accent-cyan); flex-grow: 1; overflow: hidden; display: flex; flex-direction: column; gap: 3px; min-height: 0; }
    footer { background: var(--panel-bg); backdrop-filter: blur(20px); border: 1px solid var(--panel-border); border-radius: 8px; padding: 6px 12px; display: flex; justify-content: space-between; align-items: center; font-size: 0.6rem; color: var(--text-sub); flex-shrink: 0; }
    .harvest-glow-btn { background: linear-gradient(135deg, var(--accent-emerald), #059669); color: #fff; border: none; padding: 5px 12px; border-radius: 4px; font-weight: 900; font-size: 0.68rem; cursor: pointer; }
  </style>
</head>
<body>
  <canvas id="globalCanvas"></canvas>
  <div class="app-viewport">
    <header>
      <div class="brand-title">M&A-SWARM OMNIBUS v12.1 (5% COMMISSION ENGINE)</div>
      <div class="global-controls">
        <select class="select-curr" id="currSelect" onchange="changeCurrency()">
          <option value="JPY">JPY (¥)</option>
          <option value="USD">USD ($)</option>
          <option value="EUR">EUR (€)</option>
          <option value="USDC">USDC (Crypto)</option>
        </select>
        <select class="select-lang">
          <option>ENGLISH</option>
          <option selected>日本語</option>
          <option>中文</option>
          <option>DEUTSCH</option>
        </select>
      </div>
    </header>
    <div class="owner-ticker">
      <div class="ot-item">
        <div class="ot-lbl">GLOBAL REVENUE (24H)</div>
        <div class="ot-val" id="todayRev" style="color:var(--accent-emerald)">¥ 1,840,200</div>
      </div>
      <div class="ot-item">
        <div class="ot-lbl">MONTHLY AUTOPILOT POOL</div>
        <div class="ot-val" id="monthRev" style="color:var(--accent-cyan)">¥ 32,450,000</div>
      </div>
      <div class="ot-item">
        <div class="ot-lbl">COMMISSION RATE</div>
        <div class="ot-val" style="color:var(--accent-gold)">5.0% 自動中抜き</div>
      </div>
      <div class="ot-item">
        <div class="ot-lbl">GLOBAL FUNDS</div>
        <div class="ot-val" style="color:var(--accent-purple)">3,840 社</div>
      </div>
    </div>
    <div class="global-grid">
      <div class="panel">
        <div class="super-switcher">
          <div class="ss-btn active buy" id="modeBuy" onclick="switchMode('buy')">
            <div class="ss-title" style="color:var(--accent-cyan)">🛒 CROSS-BORDER ACQUISITION</div>
            <div class="ss-sub">Micro to Mega Assets (5% Platform Fee)</div>
          </div>
          <div class="ss-btn sell" id="modeSell" onclick="switchMode('sell')">
            <div class="ss-title" style="color:var(--accent-orange)">🚀 GLOBAL ASSET LISTING</div>
            <div class="ss-sub">Instant AI Valuation & Non-Name</div>
          </div>
        </div>
        <div id="buyContainer" style="display:flex; flex-direction:column; gap:6px; flex-grow:1; min-height:0;">
          <div class="panel-heading">
            <span>GLOBAL ASSET STREAM (MICRO TO MEGA)</span>
            <span style="color:var(--accent-cyan); font-size:0.58rem;">5% COMMISSION ACTIVE</span>
          </div>
          <div class="market-scroll" id="assetStream"></div>
        </div>
        <div id="sellContainer" style="display:none; flex-direction:column; gap:6px; flex-grow:1;">
          <div class="panel-heading">
            <span>GLOBAL AI VALUATION WIZARD</span>
            <span style="color:var(--accent-orange); font-size:0.58rem;">AUTO-COMMISSION SETUP</span>
          </div>
          <div class="ai-wizard-box">
            <div class="input-field-group">
              <div class="input-lbl">Enterprise / Asset Name</div>
              <input type="text" id="bizTitle" class="supreme-input" placeholder="e.g. Micro SaaS / AI Tool / Enterprise">
            </div>
            <div class="input-field-group">
              <div class="input-lbl">Annual Revenue (Local Currency)</div>
              <input type="number" id="bizSalesVal" class="supreme-input" placeholder="5000000">
            </div>
            <div class="input-field-group">
              <div class="input-lbl">Net Annual Profit (Local Currency)</div>
              <input type="number" id="bizProfitVal" class="supreme-input" placeholder="2000000">
            </div>
            <button class="btn-wizard-submit" onclick="executeGlobalValuation()">Execute AI Valuation & Global Listing</button>
          </div>
        </div>
      </div>
      <div class="panel">
        <div class="panel-heading">
          <span>GLOBAL LIQUIDITY TELEMETRY</span>
          <span style="color:var(--accent-emerald); font-size:0.58rem;">OMNIBUS MESH ACTIVE</span>
        </div>
        <div class="right-viz-stack">
          <canvas id="liveChart" class="chart-canvas-box"></canvas>
          <div class="panel-heading" style="margin-top:2px;">
            <span>GLOBAL SWARM AGENT AUTOPILOT LOG</span>
          </div>
          <div class="terminal-output" id="terminalFeed"></div>
        </div>
      </div>
    </div>
    <footer>
      <button class="harvest-glow-btn" onclick="triggerGlobalHarvest()">Execute Global Stripe Payout (Instant)</button>
      <div style="display:flex; gap:10px;">
        <span style="cursor:pointer;" onclick="alert('Global Legal Disclosures & Cross-Border Compliance')">Legal</span>
        <span>|</span>
        <span style="cursor:pointer;" onclick="alert('Terms of Global Omnibus Service')">Terms</span>
      </div>
    </footer>
  </div>
  <script>
    const canvas = document.getElementById('globalCanvas');
    const ctx = canvas.getContext('2d');
    function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    window.addEventListener('resize', resizeCanvas); resizeCanvas();
    let step = 0;
    function renderGlobalMesh() {
      step += 0.003;
      ctx.clearRect(0,0,canvas.width,canvas.height);
      const grad = ctx.createRadialGradient(canvas.width*0.5 + Math.sin(step)*140, canvas.height*0.3, 10, canvas.width*0.5, canvas.height*0.5, canvas.width*0.85);
      grad.addColorStop(0, 'rgba(56, 189, 248, 0.14)');
      grad.addColorStop(0.5, 'rgba(16, 185, 129, 0.04)');
      grad.addColorStop(1, 'rgba(1, 2, 6, 0)');
      ctx.fillStyle = grad; ctx.fillRect(0,0,canvas.width,canvas.height);
      requestAnimationFrame(renderGlobalMesh);
    }
    renderGlobalMesh();

    function switchMode(target) {
      const bCont = document.getElementById('buyContainer');
      const sCont = document.getElementById('sellContainer');
      const bBtn = document.getElementById('modeBuy');
      const sBtn = document.getElementById('modeSell');
      if(target === 'buy') {
        bCont.style.display = 'flex'; sCont.style.display = 'none';
        bBtn.classList.add('active'); sBtn.classList.remove('active');
      } else {
        bCont.style.display = 'none'; sCont.style.display = 'flex';
        sBtn.classList.add('active'); bBtn.classList.remove('active');
      }
    }

    let currentCurr = 'JPY';
    const rates = { JPY: 1, USD: 0.0065, EUR: 0.0060, USDC: 0.0065 };
    const symbols = { JPY: '¥ ', USD: '$ ', EUR: '€ ', USDC: 'USDC ' };

    function formatPrice(jpyVal) {
      const val = jpyVal * rates[currentCurr];
      if (currentCurr === 'JPY') {
        if (val >= 100000000) return symbols[currentCurr] + (val / 100000000).toFixed(1) + ' 億円';
        return symbols[currentCurr] + (val / 10000).toFixed(0) + ' 万円';
      }
      return symbols[currentCurr] + val.toLocaleString(undefined, {maximumFractionDigits: 0});
    }

    /* 低価格（個人開発・マイクロSaaS）から最高価格（メガ企業）までの全方位アセットプール */
    const globalAssets = [
      { area: "TOKYO • JAPAN", tag: "MICRO-SaaS", name: "AI自動ライティングツール (MRR 15万)", rawPrice: 1800000, desc: "個人開発の収益化済みマイクロSaaS。引き継ぎ即日可能。手数料5%自動徴収対象。" },
      { area: "SINGAPORE", tag: "MOBILE APP", name: "iOS/Android Utility App (Downloads 50k)", rawPrice: 8500000, desc: "安定した広告収益を生み出すユーティリティアプリ。完全自動運用モデル。" },
      { area: "NEW YORK • USA", tag: "AI/SaaS", name: "Autonomous LLM Workflow Engine (ARR $1.2M)", rawPrice: 320000000, desc: "Global enterprise client base across 40 countries. Fully autonomous M2M architecture." },
      { area: "LONDON • UK", tag: "FINTECH", name: "Cross-Border Crypto Payment Gateway", rawPrice: 540000000, desc: "Multi-jurisdiction compliant settlement pipeline with instant fiat conversion." }
    ];

    function renderStream() {
      const streamEl = document.getElementById('assetStream');
      streamEl.innerHTML = globalAssets.map(a => `
        <div class="asset-tile">
          <div class="at-top">
            <span class="at-tag">${a.area} • ${a.tag}</span>
            <span style="color:var(--accent-emerald); font-weight:700;">仲介手数料 5%自動中抜き</span>
          </div>
          <div class="at-name">${a.name}</div>
          <div class="at-desc">${a.desc}</div>
          <div class="at-bottom">
            <div>
              <div style="font-size:0.55rem; color:var(--text-sub);">Valuation</div>
              <div class="at-price">${formatPrice(a.rawPrice)}</div>
            </div>
            <button class="btn-action-glow" onclick="executeGlobalCheckout('${a.name}', ${a.rawPrice})">Stripe Escrow (5%自動中抜き)</button>
          </div>
        </div>
      `).join('');
    }
    renderStream();

    function changeCurrency() {
      currentCurr = document.getElementById('currSelect').value;
      renderStream();
    }

    async function executeGlobalCheckout(name, price) {
      const commission = price * 0.05;
      if(confirm(`[Global Omnibus 5% Commission] "${name}"\n取引価格: ${formatPrice(price)}\n-> プラットフォーム手数料（5%中抜き）: ${formatPrice(commission)} があなたのStripe口座へ自動入金されます。\n\nエスクロー決済を確定しますか？`)) {
        alert(`決済成功！ 手数料 ${formatPrice(commission)} があなたの中抜き口座へ即時チャリンチャリンとチャージされました！`);
      }
    }

    async function executeGlobalValuation() {
      const title = document.getElementById('bizTitle').value;
      const sales = parseFloat(document.getElementById('bizSalesVal').value) || 0;
      if(!title) { alert("Please enter asset title."); return; }
      const val = sales * 2.2;
      alert(`[AI Valuation Complete] "${title}"\nEstimated Enterprise Value: ${formatPrice(val)}\n(売買成立時に5%のプラットフォーム中抜き手数料が自動発生するように設定されました)`);
      switchMode('buy');
    }

    function triggerGlobalHarvest() {
      alert("Stripe Global Payout API executed successfully. 全世界での5%中抜き収益があなたの登録口座へ一括自動送金されました！");
    }

    const chartEl = document.getElementById('liveChart');
    const chCtx = chartEl.getContext('2d');
    function renderLiveChart() {
      chartEl.width = chartEl.clientWidth; chartEl.height = chartEl.clientHeight;
      chCtx.clearRect(0,0,chartEl.width,chartEl.height);
      chCtx.beginPath();
      chCtx.strokeStyle = '#38bdf8'; chCtx.lineWidth = 2.5;
      for(let i=0; i<18; i++) {
        let px = (i / 17) * chartEl.width;
        let py = chartEl.height - (Math.sin(i * 0.35 + Date.now()*0.002) * (chartEl.height*0.3) + chartEl.height*0.5);
        if(i===0) chCtx.moveTo(px,py); else chCtx.lineTo(px,py);
      }
      chCtx.stroke();
      requestAnimationFrame(renderLiveChart);
    }
    renderLiveChart();

    let totalRev = 32450000;
    setInterval(() => {
      totalRev += Math.floor(Math.random() * 65000) + 25000;
      document.getElementById('monthRev').innerText = "¥ " + totalRev.toLocaleString();
    }, 2500);

    const termEl = document.getElementById('terminalFeed');
    const feedLogs = [
      "Stripe API: マイクロSaaS売買から5%の手数料（¥90,000）を自動中抜き徴収",
      "Escrow Protocol: グローバルファンド間の大型案件から5%成功報酬を自動配分",
      "Omnibus Mesh: ニューヨーク・シンガポール・東京の決済ノードが同期完了",
      "Autopilot Payout: 24時間自動チャリンチャリン収益がプールへ加算されました"
    ];
    function pushLog() {
      const timeStr = new Date().toTimeString().split(' ')[0];
      const text = feedLogs[Math.floor(Math.random() * feedLogs.length)];
      const row = document.createElement('div');
      row.innerHTML = `<span style="color:var(--text-sub)">[${timeStr}]</span> ${text}`;
      termEl.prepend(row);
      if (termEl.children.length > 8) termEl.removeChild(termEl.lastChild);
    }
    setInterval(pushLog, 2000); pushLog();
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return HTML_CONTENT
