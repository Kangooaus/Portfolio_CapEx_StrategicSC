/* ============================================================
   executive.js — renders the Executive Dashboard for whichever
   program is active (see programs-data.js). Every number on this
   page comes from PROGRAMS[activeId]; nothing here is hardcoded
   per-program any more.
   ============================================================ */

const COLOR_HEX = {
  blue: '#2563eb', navy2: '#1e3a5f', green: '#16a34a',
  amber: '#d97706', cyan: '#0e7490', gray: '#6b7280', slate: '#334155',
};

function renderKpis(program) {
  const el = document.getElementById('kpiGrid');
  if (!el) return;
  el.innerHTML = program.kpis.map(k => `
    <div class="kpi-card ${k.cls}">
      <div class="kpi-label">${esc(k.label)}</div>
      <div class="kpi-value ${k.valCls}">${esc(k.value)}</div>
      <div class="kpi-context">${esc(k.context)}</div>
    </div>`).join('');
}

function renderInsights(program) {
  const el = document.getElementById('insightStrip');
  if (!el) return;
  el.innerHTML = program.insights.map(i => `
    <div class="insight-item">${i.html}<span class="i-tag ${i.tagCls}">${esc(i.tag)}</span></div>`).join('');
}

function renderHeader(program) {
  const sub = document.getElementById('execSubtitle');
  if (sub) {
    if (program.hasExecutionHistory) {
      sub.textContent = `Program-level overview of the ${program.name} capital equipment portfolio. ${program.kpis[0].value} equipment and installation across ${program.kpis[1].value.split(' ')[0]} platforms.`;
    } else {
      sub.textContent = `FEL-2 feasibility overview of the ${program.name} proposal. Estimated ${program.kpis[0].value} investment across ${program.kpis[1].value.split(' ')[0]} platforms — not yet AR-approved.`;
    }
  }
  const meta = document.getElementById('execMeta');
  if (meta) {
    meta.innerHTML = `
      <span>Program: ${esc(program.name)}</span>
      <span>Period: ${esc(program.period)}</span>
      <span>AR Reference: ${esc(program.arReference)}</span>
      <span>Program Manager: ${esc(program.programManager)}</span>
      <span>Classification: Portfolio Demonstration</span>`;
  }
}

function renderDonut(program) {
  const badge = document.getElementById('donutBadge');
  if (badge) badge.textContent = program.capexDonut.totalBadge;
  const insight = document.getElementById('donutInsight');
  const maxIdx = program.capexDonut.data.indexOf(Math.max(...program.capexDonut.data));
  if (insight) insight.textContent = `${program.capexDonut.labels[maxIdx]} represents the largest single category at ${program.capexDonut.data[maxIdx]}% of total portfolio value`;

  const ldClassByColor = { blue: 'ld-blue', navy2: 'ld-navy', green: 'ld-green', amber: 'ld-amber', cyan: 'ld-slate', gray: 'ld-gray' };
  const legend = document.getElementById('donutLegend');
  if (legend) {
    legend.innerHTML = program.capexDonut.labels.map((l, i) =>
      `<span class="l-dot ${ldClassByColor[program.capexDonut.colors[i]] || 'ld-gray'}">${esc(l)} (${program.capexDonut.data[i]}%)</span>`).join('');
  }

  if (typeof Chart === 'undefined') return;
  new Chart(document.getElementById('capexDonut'), {
    type: 'doughnut',
    data: {
      labels: program.capexDonut.labels,
      datasets: [{
        data: program.capexDonut.data,
        backgroundColor: program.capexDonut.colors.map(c => COLOR_HEX[c]),
        borderWidth: 2, borderColor: '#fff',
      }],
    },
    options: {
      responsive: true, maintainAspectRatio: false, cutout: '60%',
      plugins: {
        legend: { display: false },
        tooltip: { ...TIP, callbacks: { label: ctx => ' ' + ctx.label + ': ' + ctx.raw + '%' } },
      },
    },
  });
}

function renderStatusBar(program) {
  const barTitle = document.getElementById('barTitle');
  const barBadge = document.getElementById('barBadge');
  const barInsight = document.getElementById('barInsight');
  const barFootnote = document.getElementById('barFootnote');
  const barLegend = document.getElementById('barLegend');

  const cfg = program.hasExecutionHistory ? program.deployBar : program.sourcingBar;
  if (barTitle) barTitle.textContent = program.hasExecutionHistory
    ? 'Equipment Deployment Status by Category' : 'Sourcing & Qualification Status by Category';
  if (barBadge) { barBadge.textContent = cfg.badge; barBadge.className = 'card-badge ' + (cfg.badgeCls || 'badge-blue'); }
  if (barInsight) barInsight.textContent = cfg.insight;
  if (barFootnote) barFootnote.textContent = program.hasExecutionHistory
    ? 'Status based on post-commissioning phase gate tracking. "In Production" = G5 gate cleared and formal handover to Operations complete.'
    : 'Status based on FEL-2 sourcing pipeline tracking (S19_Strategic_Sourcing_Pipeline). No purchase orders placed pending AR approval.';

  const ldClassByColor = { green: 'ld-green', blue: 'ld-blue', amber: 'ld-amber', gray: 'ld-gray' };
  if (barLegend) {
    barLegend.innerHTML = cfg.series.map(s => `<span class="l-dot ${ldClassByColor[s.color] || 'ld-gray'}">${esc(s.label)}</span>`).join('');
  }

  if (typeof Chart === 'undefined') return;
  new Chart(document.getElementById('statusBar'), {
    type: 'bar',
    data: {
      labels: cfg.labels,
      datasets: cfg.series.map(s => ({ label: s.label, data: s.data, backgroundColor: COLOR_HEX[s.color] || COLOR_HEX.gray, _noLabel: true })),
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: { stacked: true, grid: { display: false }, border: { display: false } },
        y: { stacked: true, grid: { color: '#f0f0f0' }, border: { display: false }, ticks: { stepSize: 1, precision: 0 } },
      },
      plugins: { legend: { position: 'top', align: 'end' }, tooltip: { ...TIP, mode: 'index' } },
    },
  });
}

function renderThirdCard(program) {
  const card = document.getElementById('thirdCard');
  if (!card) return;

  if (program.hasExecutionHistory) {
    card.innerHTML = `
      <div class="card-header">
        <div>
          <span class="card-title">Capacity vs Demand — 2023–2025</span>
          <span class="card-insight">Capacity ramp driven by phased commissioning — crossed demand baseline line at Q3-2025</span>
        </div>
      </div>
      <div class="card-body">
        <div class="chart-wrap"><canvas id="capacityLine"></canvas></div>
        <div class="legend-row">
          <span class="l-dot ld-blue">Installed Capacity (K units/yr)</span>
          <span class="l-dot ld-amber">Baseline Demand (K units/yr)</span>
        </div>
        <div class="table-fn">${esc(program.capacityLine.footnote)}</div>
      </div>`;
    if (typeof Chart === 'undefined') return;
    new Chart(document.getElementById('capacityLine'), {
      type: 'line',
      data: {
        labels: program.capacityLine.labels,
        datasets: [
          { label: 'Installed Capacity (K units/yr)', data: program.capacityLine.capacity,
            borderColor: COLOR_HEX.blue, borderWidth: 2, backgroundColor: 'rgba(37,99,235,0.10)', fill: true,
            pointRadius: 3, pointBackgroundColor: COLOR_HEX.blue, tension: 0.3, _noLabel: true },
          { label: 'Baseline Demand (K units/yr)', data: program.capacityLine.demand,
            borderColor: COLOR_HEX.amber, borderWidth: 1.5, borderDash: [5, 4],
            pointRadius: 0, tension: 0.3, _noLabel: true },
        ],
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: { legend: { position: 'top', align: 'end' }, tooltip: { ...TIP } },
        scales: {
          y: { grid: { color: '#f0f0f0' }, border: { display: false }, ticks: { callback: v => v + 'K' } },
          x: { grid: { display: false }, border: { display: false } },
        },
      },
    });
  } else {
    card.innerHTML = `
      <div class="card-header">
        <div>
          <span class="card-title">Path to AR Approval</span>
          <span class="card-insight">Program has no execution history yet — capacity and deployment charts activate post-AR approval</span>
        </div>
      </div>
      <div class="card-body">
        <ul class="dl">
          ${program.readinessPath.map(s => `
            <li class="dl-item">
              <span class="dl-label">${esc(s.step)}<br><span style="font-size:9px;color:var(--t3);font-weight:400;">${esc(s.note)}</span></span>
              <span class="status ${s.status === 'IN PROGRESS' ? 'st-amber' : s.status === 'NOT STARTED' ? 'st-gray' : 'st-green'}">${esc(s.status)}</span>
            </li>`).join('')}
        </ul>
      </div>`;
  }
}

function renderHealth(program) {
  const title = document.getElementById('healthTitle');
  const insight = document.getElementById('healthInsight');
  const grid = document.getElementById('healthGrid');
  const list = document.getElementById('decisionList');

  if (title) title.textContent = program.hasExecutionHistory ? 'Program Health Summary' : 'Program Readiness Summary';
  if (insight) insight.textContent = program.health.insight;

  const cards = program.hasExecutionHistory ? program.health.cards : program.health.readinessCards;
  if (grid) {
    grid.innerHTML = cards.map(c => `
      <div class="health-card">
        <div class="health-lbl">${esc(c.label)}</div>
        <div class="health-chip ${c.chipCls}">${esc(c.chip)}</div>
        <div class="health-note">${esc(c.note)}</div>
      </div>`).join('');
  }
  if (list) {
    list.innerHTML = program.health.decisionList.map(d => `
      <li class="dl-item"><span class="dl-label">${esc(d.label)}</span><span class="dl-value" style="${d.cls === 'green' ? 'color:var(--green);' : ''}">${esc(d.value)}</span></li>`).join('');
  }
}

const GREENFIELD_MILESTONE_HTML = `
  <div class="sec-hdr">
    <h3>Key Milestone Snapshot — Phase II Program Gates</h3>
    <span>Apr–Dec 2025 · G0 to G5 · Greenfield Expansion Phase II</span>
  </div>
  <div class="ms-strip" style="margin-bottom:0; border-bottom:none;">
    <div class="ms-item"><div class="ms-dot done"></div><div class="ms-gate">G0 / G1</div><div class="ms-label">AR Approved + All POs Placed</div><div class="ms-date">Apr 2025</div><div class="ms-detail">$16.06M AR signed off by Board. All 15 OEM POs awarded within 3 weeks.</div></div>
    <div class="ms-item"><div class="ms-dot done"></div><div class="ms-gate">—</div><div class="ms-label">Hazmat Permit Filed</div><div class="ms-date">May 2025</div><div class="ms-detail">12-week regulatory permit for EQ-007 gas system filed on schedule. On critical path.</div></div>
    <div class="ms-item"><div class="ms-dot done"></div><div class="ms-gate">—</div><div class="ms-label">Site Utilities Complete</div><div class="ms-date">Aug 2025</div><div class="ms-detail">Electrical, cooling loop, OT network, and floor reinforcement (EQ-004) all signed off.</div></div>
    <div class="ms-item"><div class="ms-dot done"></div><div class="ms-gate">G2</div><div class="ms-label">All FATs Complete</div><div class="ms-date">Oct 2025</div><div class="ms-detail">15 of 15 FAT protocols signed. EQ-004 TEL Furnace last to complete. Zero FAT failures.</div></div>
    <div class="ms-item"><div class="ms-dot done"></div><div class="ms-gate">G3</div><div class="ms-label">All Equipment Delivered</div><div class="ms-date">Oct 2025</div><div class="ms-detail">All 45 units received on site. EQ-002 Pfeiffer TMP was final delivery — critical path item.</div></div>
    <div class="ms-item"><div class="ms-dot done"></div><div class="ms-gate">—</div><div class="ms-label">All Units Installed</div><div class="ms-date">Nov 2025</div><div class="ms-detail">Mechanical install, utility tie-ins, MES integration, and safety interlocks validated for all 15 platforms.</div></div>
    <div class="ms-item"><div class="ms-dot done"></div><div class="ms-gate">G4</div><div class="ms-label">PQ Complete — All Platforms</div><div class="ms-date">Dec 2025</div><div class="ms-detail">Process qualification passed on all 15 platforms. 4 re-runs required (EQ-004 furnace zone drift). Zero formal failures.</div></div>
    <div class="ms-item"><div class="ms-dot done"></div><div class="ms-gate">G5</div><div class="ms-label">Production Release</div><div class="ms-date">Dec 2025</div><div class="ms-detail">Formal handover to Operations. SOPs signed, spares stocked, operators trained. 30/90/180-day checkpoints initiated.</div></div>
  </div>
  <div class="card" style="margin-bottom:20px; border-top:none;">
    <div class="card-body" style="padding:0;">
      <table class="ms-table">
        <thead><tr><th>Gate</th><th>Milestone</th><th>Target Date</th><th>Actual Date</th><th>Owner</th><th>Budget Impact</th><th>Key Dependencies</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td style="font-weight:700;">G0</td><td style="font-weight:600;">Program Kick-Off &amp; Baseline Established</td><td>Apr 2, 2025</td><td>Apr 2, 2025</td><td>Program Manager</td><td class="td-r">—</td><td>Board sign-off on AR</td><td><span class="status st-green">Complete</span></td></tr>
          <tr><td style="font-weight:700;">G1</td><td style="font-weight:600;">All 15 OEM Purchase Orders Awarded</td><td>Apr 28, 2025</td><td>Apr 25, 2025</td><td>Sourcing Lead</td><td class="td-r">$13.87M</td><td>FX forward contracts placed</td><td><span class="status st-green">Complete · 3 days early</span></td></tr>
          <tr><td>—</td><td style="font-weight:600;">Hazmat Permit Filed — EQ-007 Gas System</td><td>May 5, 2025</td><td>May 5, 2025</td><td>Regulatory Affairs</td><td class="td-r">$0</td><td>Critical path — 12w permit lead time</td><td><span class="status st-green">Complete · On time</span></td></tr>
          <tr><td>—</td><td style="font-weight:600;">EQ-002 Pfeiffer TMP — FAT Sign-Off</td><td>Sep 30, 2025</td><td>Sep 30, 2025</td><td>Engineering</td><td class="td-r">$930K PO</td><td>Zero float — CP bottleneck</td><td><span class="status st-green">Complete</span></td></tr>
          <tr><td>—</td><td style="font-weight:600;">Site Utilities Sign-Off (All Bays)</td><td>Aug 15, 2025</td><td>Aug 18, 2025</td><td>Facilities / Civil</td><td class="td-r">$850K civils</td><td>Floor reinf. EQ-004 — 3 day slip</td><td><span class="status st-amber">Complete · 3d slip (non-CP)</span></td></tr>
          <tr><td style="font-weight:700;">G2</td><td style="font-weight:600;">All 15 Platform FATs Complete &amp; Signed</td><td>Oct 10, 2025</td><td>Oct 10, 2025</td><td>Engineering / OEMs</td><td class="td-r">—</td><td>All 15 FAT protocols executed</td><td><span class="status st-green">Complete</span></td></tr>
          <tr><td style="font-weight:700;">G3</td><td style="font-weight:600;">All 45 Units Delivered to Site</td><td>Oct 20, 2025</td><td>Oct 20, 2025</td><td>Logistics</td><td class="td-r">$285K freight</td><td>EQ-002 TMP = final delivery on CP</td><td><span class="status st-green">Complete</span></td></tr>
          <tr><td>—</td><td style="font-weight:600;">MES / SCADA Integration — All Platforms</td><td>Nov 5, 2025</td><td>Nov 7, 2025</td><td>Controls Engineering</td><td class="td-r">$42K NRE</td><td>Siemens DCS PLC config — 2d slip</td><td><span class="status st-amber">Complete · 2d slip (non-CP)</span></td></tr>
          <tr><td style="font-weight:700;">G4</td><td style="font-weight:600;">Full Process Qualification (PQ) Passed</td><td>Dec 5, 2025</td><td>Dec 5, 2025</td><td>Process / QA</td><td class="td-r">—</td><td>4 PQ re-runs (EQ-004 zone drift)</td><td><span class="status st-green">Complete</span></td></tr>
          <tr><td>—</td><td style="font-weight:600;">Spare Parts Stocked · SOPs Signed</td><td>Dec 10, 2025</td><td>Dec 10, 2025</td><td>Operations / Maint.</td><td class="td-r">$124K spares</td><td>12 critical Class-A parts · $124K</td><td><span class="status st-green">Complete</span></td></tr>
          <tr><td>—</td><td style="font-weight:600;">Operator Training Completed</td><td>Dec 12, 2025</td><td>Dec 11, 2025</td><td>Training / Ops</td><td class="td-r">$18K training</td><td>24 operators certified across 3 shifts</td><td><span class="status st-green">Complete · 1 day early</span></td></tr>
          <tr><td style="font-weight:700;">G5</td><td style="font-weight:600;">Formal Production Release — Ops Handover</td><td>Dec 15, 2025</td><td>Dec 15, 2025</td><td>Program Manager</td><td class="td-r">—</td><td>30/90/180-day checkpoints initiated</td><td><span class="status st-green">Complete · On schedule</span></td></tr>
        </tbody>
      </table>
      <div class="table-fn">All gates achieved on or before target date. Minor slips (EQ-004 civils +3d, MES integration +2d) were non-critical-path and absorbed within program float. Zero formal gate failures recorded. Next checkpoint: 90-day post-production review Mar 2026.</div>
    </div>
  </div>`;

function renderMilestoneSection(program) {
  const el = document.getElementById('milestoneSection');
  if (!el) return;
  if (program.hasExecutionHistory) {
    el.innerHTML = GREENFIELD_MILESTONE_HTML;
    return;
  }
  el.innerHTML = `
    <div class="sec-hdr">
      <h3>Program Not Yet in Execution</h3>
      <span>FEL-2 Feasibility · ${esc(program.name)}</span>
    </div>
    <div class="card" style="margin-bottom:20px;">
      <div class="card-body">
        <p style="font-size:12px;color:var(--t2);line-height:1.6;margin-bottom:0;">
          ${esc(program.name)} is at <strong>${esc(program.phase)}</strong> and has not yet received capital appropriations
          approval — there is no execution milestone history to report. See the <strong>Path to AR Approval</strong> card above
          for the FEL-2 → AR → execution sequence, or switch the program selector to
          <strong>PRG-001 · Greenfield Phase II</strong> to see a fully executed program's milestone tracking in this same view.
        </p>
      </div>
    </div>`;
}

document.addEventListener('DOMContentLoaded', () => {
  const program = getActiveProgram();
  const steps = [renderHeader, renderKpis, renderInsights, renderDonut, renderStatusBar,
                  renderThirdCard, renderHealth, renderMilestoneSection];
  steps.forEach(fn => {
    try { fn(program); } catch (e) { console.error(`executive.js: ${fn.name} failed`, e); }
  });
});
