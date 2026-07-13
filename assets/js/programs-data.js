/* ============================================================
   programs-data.js — portfolio registry
   Single source of truth for every program shown on the site.
   Mirrors S33_Portfolio_Register in the Excel workbook — figures
   here are kept in sync with that sheet by hand; the workbook
   remains the source of truth for anyone who wants to audit them.
   ============================================================ */

const PROGRAMS = {

  'greenfield-phase2': {
    id: 'greenfield-phase2',
    programRef: 'PRG-001',
    name: 'Greenfield Expansion Phase II',
    shortName: 'Greenfield Phase II',
    businessUnit: 'Semiconductor & Advanced Process Division',
    programManager: 'Sourabh Tarodekar',
    phase: 'G2 — Equipment Build & FAT',
    phaseTag: 'IN EXECUTION',
    phaseTagClass: 'st-green',
    hasExecutionHistory: true,
    arReference: 'AR-2025-0082',
    period: 'Q2–Q4 2025',
    raw: { capex: 13870000, budget: 16062000, platforms: 15, suppliers: 15, singleSource: 2, countries: 5 },

    kpis: [
      { label: 'Total CapEx Investment', value: '$13.87M', context: 'Equip + install · $16.06M AR total', cls: 'navy', valCls: 'neutral' },
      { label: 'Equipment Portfolio Size', value: '15 Platforms', context: '45 total units · 6 categories', cls: '', valCls: 'neutral' },
      { label: 'Annual Production Capacity', value: '1,040,253', context: 'units/yr · process tools only', cls: 'success', valCls: 'positive' },
      { label: 'Portfolio Utilization', value: '72.1%', context: 'Baseline 750K · surge 86.5%', cls: 'success', valCls: 'positive' },
      { label: 'Active OEM Suppliers', value: '15', context: '5 countries · avg 87.3 reliability', cls: 'blue', valCls: 'neutral' },
      { label: 'Single-Source Risk Count', value: '2', context: 'Pfeiffer (EQ-002) · Daifuku (EQ-006)', cls: 'danger', valCls: 'danger' },
    ],

    insights: [
      { html: 'Portfolio CapEx <strong>$13.87M</strong> — 4.3% under AR budget of $16.06M. $2.19M contingency &amp; FX reserve available.', tag: 'Under Budget', tagCls: 'tag-up' },
      { html: 'Annual capacity <strong>1,040,253 units/yr</strong> at 72.1% utilisation — 290K headroom above 750K baseline demand.', tag: 'Healthy', tagCls: 'tag-up' },
      { html: 'IRR <strong>14.2%</strong> vs 8% hurdle. Payback 4.2 years. 10-yr NPV $9.52M vs minimum-CapEx alternative.', tag: 'Exceeds Threshold', tagCls: 'tag-up' },
      { html: 'EQ-002 Pfeiffer TMP remains <strong>critical path single-source</strong> — Shimadzu qualification active, target Q3-2025.', tag: 'Monitor', tagCls: 'tag-down' },
    ],

    capexDonut: {
      labels: ['Vacuum Systems', 'High-Temp Furnaces', 'Robotics & Auto', 'Gas Handling', 'Controls / PLC', 'Facility Infra'],
      data: [24.2, 32.1, 19.4, 9.9, 8.5, 10.8],
      colors: ['blue', 'navy2', 'green', 'amber', 'cyan', 'gray'],
      totalBadge: '$13.87M Total',
    },

    deployBar: {
      labels: ['Vacuum', 'Furnaces', 'Robotics', 'Gas', 'Controls', 'Infra'],
      series: [
        { label: 'In Production', data: [9, 5, 5, 4, 6, 3], color: 'green' },
        { label: 'Qualified', data: [3, 2, 2, 1, 2, 1], color: 'blue' },
        { label: 'Installed', data: [1, 1, 0, 1, 0, 1], color: 'amber' },
        { label: 'Ordered', data: [1, 0, 0, 1, 0, 0], color: 'gray' },
      ],
      badge: '15 Platforms',
      badgeCls: 'badge-green',
      insight: '13 of 15 platforms in production — EQ-004 furnace and EQ-006 conveyor completing qualification',
    },

    capacityLine: {
      labels: ['Q1-23', 'Q2-23', 'Q3-23', 'Q4-23', 'Q1-24', 'Q2-24', 'Q3-24', 'Q4-24', 'Q1-25', 'Q2-25', 'Q3-25', 'Q4-25'],
      capacity: [420, 480, 550, 600, 650, 720, 800, 880, 950, 1000, 1040, 1040],
      demand: [505, 528, 571, 567, 580, 624, 618, 661, 675, 718, 740, 750],
      footnote: 'Capacity = process tools only (EQ-003, EQ-004, EQ-014). Support equipment excluded. Demand from S11_Demand_Forecast.',
    },

    health: {
      insight: 'All three program dimensions on track as of Dec 2025 — supply chain has one active watch item',
      cards: [
        { label: 'Schedule Status', chip: 'On Track', chipCls: 'chip-green', note: 'G5 Production Release achieved Q4-2025. No critical path delays. Program closed on schedule.' },
        { label: 'Cost Status', chip: 'Under Budget', chipCls: 'chip-green', note: 'Actual $13.87M vs $16.06M AR. $2.19M reserve untouched. Zero budget overruns recorded.' },
        { label: 'Supply Chain', chip: 'Watch', chipCls: 'chip-amber', note: 'Pfeiffer single-source risk (EQ-002) — Shimadzu qualification ongoing. All other OEMs on track.' },
      ],
      decisionList: [
        { label: 'Board Approved Budget', value: '$16,062,000', cls: '' },
        { label: 'Actual CapEx Spend', value: '$13,870,000', cls: 'green' },
        { label: '10-Year IRR', value: '14.2%', cls: 'green' },
        { label: 'Simple Payback Period', value: '4.2 years', cls: '' },
        { label: '10-Year NPV vs Min-CapEx', value: '+$9,520,000', cls: 'green' },
      ],
    },
  },

  'riverside-phase1': {
    id: 'riverside-phase1',
    programRef: 'PRG-002',
    name: 'Riverside Automation Upgrade Phase I',
    shortName: 'Riverside Phase I',
    businessUnit: 'Packaging & Distribution Operations',
    programManager: 'Elena Vargas',
    phase: 'FEL-2 — Feasibility',
    phaseTag: 'PRE-EXECUTION',
    phaseTagClass: 'st-amber',
    hasExecutionHistory: false,
    arReference: 'Pending — targeting Q4-2025 submission',
    period: 'FEL-2 planning, 2025',
    raw: { capex: 2382000, budget: 2757200, platforms: 6, suppliers: 6, singleSource: 1, countries: 2 },

    kpis: [
      { label: 'Total CapEx Investment', value: '$2.38M', context: 'Equip + install · $2.76M est. AR total', cls: 'navy', valCls: 'neutral' },
      { label: 'Equipment Platforms', value: '6 Platforms', context: '14 total units · 5 categories', cls: '', valCls: 'neutral' },
      { label: 'Est. Throughput Uplift', value: '+18%', context: 'packaging line · ~45,000 cases/day incremental', cls: 'success', valCls: 'positive' },
      { label: 'Est. Payback Period', value: '3.1 yrs', context: '16.8% IRR · $1.85M 10-yr NPV (est.)', cls: 'success', valCls: 'positive' },
      { label: 'Active OEM Suppliers', value: '6', context: '1 country · avg 91.2 reliability', cls: 'blue', valCls: 'neutral' },
      { label: 'Single-Source Risk Count', value: '1', context: 'Krones AG (RV-002 cartoning)', cls: 'warning', valCls: 'neutral' },
    ],

    insights: [
      { html: 'Estimated CapEx <strong>$2.38M</strong> — FEL-2 planning estimate; full AR budget of $2.76M includes contingency, FX and NRE reserves.', tag: 'Pre-Approval', tagCls: 'tag-down' },
      { html: 'Est. throughput uplift <strong>+18%</strong> on the Riverside packaging line — ~45,000 cases/day incremental at full ramp.', tag: 'Business Case', tagCls: 'tag-up' },
      { html: 'Est. IRR <strong>16.8%</strong> vs 8% hurdle. Est. payback 3.1 years — faster payback and smaller ask than Greenfield.', tag: 'Attractive', tagCls: 'tag-up' },
      { html: 'RV-002 Krones cartoning system is the program’s only <strong>single-source risk</strong> — no qualified alternate identified yet.', tag: 'Monitor', tagCls: 'tag-down' },
    ],

    capexDonut: {
      labels: ['Robotics & Automation', 'Packaging Automation', 'Material Handling', 'Quality / Automation', 'Controls / PLC'],
      data: [39.0, 19.5, 25.8, 8.6, 7.1],
      colors: ['green', 'navy2', 'gray', 'amber', 'cyan'],
      totalBadge: '$2.38M Total',
    },

    sourcingBar: {
      labels: ['Robotics', 'Packaging', 'Handling', 'Quality', 'Controls'],
      series: [
        { label: 'Awarded / In Fab', data: [0, 0, 0, 0, 0], color: 'green' },
        { label: 'RFQ / Negotiation', data: [1, 1, 0, 0, 0], color: 'blue' },
        { label: 'Technical Evaluation', data: [1, 0, 1, 1, 1], color: 'amber' },
        { label: 'Not Yet Started', data: [0, 0, 0, 0, 0], color: 'gray' },
      ],
      badge: '6 Platforms',
      badgeCls: 'badge-amber',
      insight: 'All 6 platforms are in RFQ or technical evaluation — no POs placed yet pending AR approval',
    },

    health: {
      insight: 'Business case and technical feasibility are strong; organizational readiness is the pacing item ahead of AR submission',
      readinessCards: [
        { label: 'Business Case', chip: 'Strong', chipCls: 'chip-green', note: '16.8% est. IRR and 3.1-yr payback comfortably clear the 8% hurdle rate; smaller, capital-efficient ask.' },
        { label: 'Technical Feasibility', chip: 'Validated', chipCls: 'chip-green', note: 'All 6 platforms use mature, commercially available technology; only RV-002 Krones lacks a qualified alternate.' },
        { label: 'Organizational Readiness', chip: 'Building', chipCls: 'chip-amber', note: 'Program team standing up under new PM (E. Vargas); sequencing AR submission after Greenfield’s Q3-2025 capital peak.' },
      ],
      decisionList: [
        { label: 'FEL-2 Estimated Budget', value: '$2,757,200', cls: '' },
        { label: 'Estimated CapEx (Equip + Install)', value: '$2,382,000', cls: '' },
        { label: 'Estimated IRR', value: '16.8%', cls: 'green' },
        { label: 'Estimated Payback Period', value: '3.1 years', cls: '' },
        { label: 'Estimated 10-Year NPV', value: '+$1,850,000', cls: 'green' },
      ],
    },

    readinessPath: [
      { step: 'FEL-2 Feasibility Study', status: 'IN PROGRESS', note: 'Business case, technical feasibility, and should-cost review underway' },
      { step: 'Supplier RFQ & Technical Evaluation', status: 'IN PROGRESS', note: 'All 6 platforms in RFQ or evaluation; Krones single-source risk being assessed' },
      { step: 'FEL-3 Definition & Should-Cost Lock', status: 'NOT STARTED', note: 'Target start: after Greenfield Q3-2025 peak capital draw clears' },
      { step: 'AR Submission (Target Q4-2025)', status: 'NOT STARTED', note: 'Formal capital appropriations request to VP Engineering + CFO' },
      { step: 'AR Approval & Long-Lead PO Placement', status: 'NOT STARTED', note: 'Pending AR approval — program has no execution history yet' },
    ],
  },
};

const PORTFOLIO_ORDER = ['greenfield-phase2', 'riverside-phase1'];
const DEFAULT_PROGRAM = 'greenfield-phase2';

function getActiveProgramId() {
  const params = new URLSearchParams(window.location.search);
  const fromQuery = params.get('program');
  if (fromQuery && PROGRAMS[fromQuery]) return fromQuery;
  try {
    const stored = window.localStorage.getItem('activeProgram');
    if (stored && PROGRAMS[stored]) return stored;
  } catch (e) { /* localStorage unavailable */ }
  return DEFAULT_PROGRAM;
}

function setActiveProgram(id) {
  if (!PROGRAMS[id]) return;
  try { window.localStorage.setItem('activeProgram', id); } catch (e) { /* ignore */ }
  const url = new URL(window.location.href);
  url.searchParams.set('program', id);
  window.location.href = url.toString();
}

function getActiveProgram() {
  return PROGRAMS[getActiveProgramId()];
}

// Preserve the active program selection across in-site nav links.
function withProgramParam(href) {
  const id = getActiveProgramId();
  const sep = href.includes('?') ? '&' : '?';
  return id === DEFAULT_PROGRAM ? href : `${href}${sep}program=${id}`;
}

// Portfolio-wide rollup across every program — mirrors S33/S34 in the workbook.
function getPortfolioTotals() {
  const programs = PORTFOLIO_ORDER.map(id => PROGRAMS[id]);
  const sum = key => programs.reduce((acc, p) => acc + p.raw[key], 0);
  return {
    programCount: programs.length,
    totalCapex: sum('capex'),
    totalBudget: sum('budget'),
    totalPlatforms: sum('platforms'),
    totalSuppliers: sum('suppliers'),
    totalSingleSource: sum('singleSource'),
  };
}

function fmtUSD_M(n) { return '$' + (n / 1e6).toFixed(2) + 'M'; }

function esc(s) { return String(s); }
