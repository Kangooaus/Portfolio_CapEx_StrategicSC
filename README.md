# Engineering CapEx and Supplier Execution

**Engineering Program Management – CapEx & Supplier Operations**  
Prepared by: Sourabh Tarodekar &nbsp;·&nbsp; [sourabh232@gmail.com](mailto:sourabh232@gmail.com)  
Live site: [quantumaster007.github.io/Portfolio_CapEx_StrategicSC](https://quantumaster007.github.io/Portfolio_CapEx_StrategicSC/)

---

## Overview

A portfolio demonstrating hands-on experience in capital equipment program management and strategic supply chain operations within advanced manufacturing environments.

The work is built around a synthetic $13.87M capital equipment programme — **Greenfield Expansion Phase II** — covering 15 equipment platforms across sourcing, logistics, execution, and financial governance. It is visualised through a static web dashboard deployed on GitHub Pages, backed by a 33-sheet Excel model.

> All data is synthetic and created for portfolio demonstration purposes only. It does not represent proprietary or confidential information from any employer or client.

---

## What This Covers

The portfolio spans the full lifecycle of a capital equipment programme — from initial appropriations request through post-commissioning ROI tracking. Key areas demonstrated:

- **CapEx Governance** — AR submission, budget hierarchy, scenario analysis, cash flow modelling, and FX exposure management across a $16M appropriation
- **Strategic Sourcing** — FEL 1–3 sourcing methodology, should-cost modelling, RFI/RFP process, commercial negotiation, and $537K in confirmed savings across 9 closed contracts
- **Supply Chain Operations** — 15-supplier network across 5 countries, logistics lead time management, dual-source qualification, inventory and buffer planning
- **Program Execution** — WBS, CPM critical path scheduling (46-week programme), phase-gate governance (G0–G5), milestone tracking, and engineering change management
- **Risk & Performance** — Supply chain risk heatmap, yield/OEE tracking, vendor scorecard, asset lifecycle register, and post-commissioning ROI

---

## Dashboard Pages

| Page | Description |
|---|---|
| **Home** | Programme overview, capability summary, workbook zone architecture |
| **Executive Dashboard** | KPIs, CapEx allocation, deployment status, capacity vs demand, programme health |
| **Strategic Supply Chain** | Market concentration, supplier geography, negotiation savings, lead times, dual-source status |
| **Program Execution & Risk** | WBS, CPM critical path, milestone roadmap, risk distribution, inventory coverage, asset lifecycle |
| **Deep Dive** | Yield/OEE metrics, supplier capacity analysis, ECO register, asset snapshot, documentation |
| **Sourcing Framework** | FEL phase map, AACE cost estimating, RFI/RFP pipeline, should-cost methodology, FID checklist |

---

## Excel Workbook

The workbook (`CapEx_StrategicSC_Portfolio.xlsx`) contains **33 sheets across 6 zones**, with 1,300+ active formulas and full cross-sheet traceability. It is generated from source with the scripts in `build/` (`python3 build/build_workbook.py`), so the whole model is reproducible and auditable.

| Zone | Sheets | Content |
|---|---|---|
| Z0 — Governance | 3 | Index, Disclaimer, Assumptions |
| Z1 — Foundation | 4 | Equipment Portfolio, Supplier Dataset, Should-Cost Model, TCO |
| Z2 — Planning | 6 | WBS, CPM Schedule, Milestone Roadmap, Deployment Timeline, Capacity Planning, Demand Forecast |
| Z3 — Financial & Risk | 5 | AR Summary, Cash Flow, FX Exposure, Scenario Analysis, Supply Chain Risk |
| Z4 — Strategic Supply Chain | 8 | Market Analysis, Network Map, Sourcing Pipeline, Dual-Source Strategy, Negotiation Tracker, Supplier Capacity, Inventory Planning, Asset Tracking |
| Z5 — Execution & Control | 7 | Milestone Gate Tracker, ECO Register, Vendor Design Changes, Yield Metrics, ROI Tracker, Vendor Scorecard, Change Tracker |

---

## Site Structure

```
Portfolio_CapEx_StrategicSC/
├── index.html                  → Home page
├── executive.html              → Executive Dashboard
├── supply-chain.html           → Strategic Supply Chain Intelligence
├── execution-risk.html         → Program Execution & Risk
├── deep-dive.html              → Deep Dive / Model Explorer
├── sourcing.html               → Sourcing Framework
├── README.md
├── assets/
│   ├── css/
│   │   └── styles.css          → Global design system
│   └── js/
│       ├── main.js             → Shared utilities, Chart.js defaults, footer
│       ├── executive.js        → Executive dashboard charts
│       ├── supply-chain.js     → Supply chain charts
│       ├── execution.js        → Execution & risk charts
│       ├── deep-dive.js        → Deep dive charts
│       └── sourcing.js         → Sourcing framework charts
├── downloads/
│   ├── CapEx_StrategicSC_Portfolio.xlsx   → Full 33-sheet workbook (generated)
│   └── CapEx_StrategicSC_Portfolio.pdf    → Print export of the workbook
└── build/                      → Python/openpyxl scripts that generate the .xlsx from source
    └── build_workbook.py       → Entry point: `python3 build/build_workbook.py`
```

---

## Deploying on GitHub Pages

1. Clone or push this folder to a GitHub repository
2. Go to **Settings → Pages**
3. Set source to `main` branch / root
4. Site will be live at `[https://[username].github.io/[repo-name]/`

---

## Disclaimer

This portfolio contains synthetic sample data created for demonstration purposes only. The data does not represent proprietary or confidential information from any employer or client.

**Prepared by:** Sourabh Tarodekar  
**For demonstration of:** Engineering Program Management – CapEx & Supply Chain Operations  
**Contact:** [sourabh232@gmail.com](mailto:sourabh232@gmail.com)  
**Programme period shown:** 2023–2025 (synthetic)
