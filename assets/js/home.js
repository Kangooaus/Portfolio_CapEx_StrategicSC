/* ============================================================
   home.js — renders the portfolio-wide KPI strip and per-program
   cards on index.html. Aggregates come from getPortfolioTotals()
   in programs-data.js, which mirrors S33/S34 in the workbook.
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  if (typeof PROGRAMS === 'undefined') return;

  const totals = getPortfolioTotals();
  const kpiEl = document.getElementById('portfolioKpiGrid');
  if (kpiEl) {
    kpiEl.innerHTML = `
      <div class="kpi-card navy"><div class="kpi-label">Total Portfolio CapEx</div><div class="kpi-value neutral">${fmtUSD_M(totals.totalCapex)}</div><div class="kpi-context">Across ${totals.programCount} programs</div></div>
      <div class="kpi-card"><div class="kpi-label">Active + Proposed Programs</div><div class="kpi-value neutral">${totals.programCount}</div><div class="kpi-context">1 in execution · 1 in FEL-2</div></div>
      <div class="kpi-card success"><div class="kpi-label">Equipment Platforms</div><div class="kpi-value positive">${totals.totalPlatforms}</div><div class="kpi-context">Combined across portfolio</div></div>
      <div class="kpi-card blue"><div class="kpi-label">Total Approved/Est. Budget</div><div class="kpi-value neutral">${fmtUSD_M(totals.totalBudget)}</div><div class="kpi-context">Incl. contingency &amp; reserves</div></div>
      <div class="kpi-card blue"><div class="kpi-label">Active OEM Suppliers</div><div class="kpi-value neutral">${totals.totalSuppliers}</div><div class="kpi-context">Combined across portfolio</div></div>
      <div class="kpi-card danger"><div class="kpi-label">Single-Source Risks</div><div class="kpi-value danger">${totals.totalSingleSource}</div><div class="kpi-context">Combined across portfolio</div></div>`;
  }

  const countLabel = document.getElementById('programCountLabel');
  if (countLabel) countLabel.textContent = `${totals.programCount} programs · click a card for its Executive Dashboard`;

  const cardsEl = document.getElementById('programCards');
  if (cardsEl) {
    cardsEl.innerHTML = PORTFOLIO_ORDER.map(id => {
      const p = PROGRAMS[id];
      const borderColor = p.hasExecutionHistory ? 'var(--green)' : 'var(--amber)';
      return `
      <div style="background:var(--bg2);border:1px solid var(--border);border-top:3px solid ${borderColor};padding:18px;box-shadow:var(--shadow);cursor:pointer;" onclick="setActiveProgram('${id}'); go('executive.html');">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
          <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:var(--t3);">${esc(p.programRef)}</div>
          <span class="status ${p.phaseTagClass}">${esc(p.phaseTag)}</span>
        </div>
        <div style="font-family:var(--fs);font-size:clamp(13px,1.1vw,16px);font-weight:600;margin-bottom:4px;">${esc(p.name)}</div>
        <div style="font-size:10px;color:var(--t3);margin-bottom:12px;">${esc(p.businessUnit)} · ${esc(p.programManager)}</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:10px;">
          <div><div style="font-size:14px;font-weight:700;">${fmtUSD_M(p.raw.capex)}</div><div style="font-size:9px;color:var(--t3);">CapEx</div></div>
          <div><div style="font-size:14px;font-weight:700;">${p.raw.platforms}</div><div style="font-size:9px;color:var(--t3);">Platforms</div></div>
          <div><div style="font-size:14px;font-weight:700;color:${p.raw.singleSource > 0 ? 'var(--red)' : 'var(--green)'};">${p.raw.singleSource}</div><div style="font-size:9px;color:var(--t3);">Single-Source</div></div>
        </div>
        <span style="font-size:11px;font-weight:600;color:var(--slate);">View Executive Dashboard →</span>
      </div>`;
    }).join('');
  }
});
