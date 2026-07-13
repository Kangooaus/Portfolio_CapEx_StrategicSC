# Engineering CapEx and Supplier Execution

**Engineering Program Management – CapEx & Supplier Operations**  
Prepared by: Sourabh Tarodekar &nbsp;·&nbsp; [sourabh232@gmail.com](mailto:sourabh232@gmail.com)  
Live site: [quantumaster007.github.io/Portfolio_CapEx_StrategicSC](https://quantumaster007.github.io/Portfolio_CapEx_StrategicSC/)

---

## Overview

A portfolio demonstrating hands-on experience in capital equipment program management and strategic supply chain operations within advanced manufacturing environments — built as a genuine **multi-project portfolio tool**, not a single-program dashboard.

Two synthetic programs sit side by side under one Portfolio Director:

- **Greenfield Expansion Phase II** (PRG-001) — $13.87M, 15 equipment platforms, AR-approved and in execution (G2 gate)
- **Riverside Automation Upgrade Phase I** (PRG-002) — $2.38M (est.), 6 equipment platforms, FEL-2 feasibility, pre-AR

A portfolio-wide rollup layer sits above both: total portfolio CapEx, blended risk index, and a weighted capital-allocation scorecard that ranks the two programs for sequencing. The site's project switcher (top-right on every page) and the Excel workbook's Program ID columns both key off the same two programs, so the numbers agree everywhere.

> All data is synthetic and created for portfolio demonstration purposes only. It does not represent proprietary or confidential information from any employer or client.

---

## What This Covers

The portfolio spans the full lifecycle of a capital equipment programme — from initial appropriations request through post-commissioning ROI tracking — **and** the portfolio-management layer that sits above multiple concurrent programmes. Key areas demonstrated:

- **CapEx Governance** — AR submission, budget hierarchy, scenario analysis, cash flow modelling, and FX exposure management across a $16M appropriation
- **Strategic Sourcing** — FEL 1–3 sourcing methodology, should-cost modelling, RFI/RFP process, commercial negotiation, and $537K in confirmed savings across 9 closed contracts
- **Supply Chain Operations** — 15-supplier network across 5 countries, logistics lead time management, dual-source qualification, inventory and buffer planning
- **Program Execution** — WBS, CPM critical path scheduling (46-week programme), phase-gate governance (G0–G5), milestone tracking, and engineering change management
- **Risk & Performance** — Supply chain risk heatmap, yield/OEE tracking, vendor scorecard, asset lifecycle register, and post-commissioning ROI
- **Portfolio Management** — multi-program register, portfolio-wide KPI rollup, and a weighted capital-allocation scorecard for sequencing programmes against each other

---

## Dashboard Pages

Every page carries a **project switcher** (top-right nav) that persists the selected program across navigation via a `?program=` query param + `localStorage`.

| Page | Description | Multi-program? |
|---|---|---|
| **Home** | Portfolio-wide KPI rollup, program cards (click through to either program's dashboard), capability summary | ✅ Portfolio-level |
| **Executive Dashboard** | KPIs, CapEx allocation, deployment/sourcing status, capacity vs demand or path-to-AR, programme health/readiness, milestones | ✅ Fully data-driven per program |
| **Strategic Supply Chain** | Market concentration, supplier geography, negotiation savings, lead times, dual-source status | Greenfield Phase II |
| **Program Execution & Risk** | WBS, CPM critical path, milestone roadmap, risk distribution, inventory coverage, asset lifecycle | Greenfield Phase II |
| **Deep Dive** | Yield/OEE metrics, supplier capacity analysis, ECO register, asset snapshot, documentation | Greenfield Phase II |
| **Sourcing Framework** | FEL phase map, AACE cost estimating, RFI/RFP pipeline, should-cost methodology, FID checklist | Greenfield Phase II |

The Executive Dashboard is the flagship of the multi-project pattern: switch to **PRG-002 · Riverside Phase I** and the whole page adapts — deployment status becomes sourcing/qualification status, the capacity-vs-demand chart becomes a "Path to AR Approval" roadmap, and the milestone timeline becomes a "not yet in execution" notice, because that program genuinely doesn't have that data yet. The other four pages currently remain scoped to Greenfield Phase II; the same `PROGRAMS` registry in `assets/js/programs-data.js` is what you'd extend to bring them along.

---

## Excel Workbook

The workbook (`CapEx_StrategicSC_Portfolio.xlsx`) contains **36 sheets across 7 zones**, with 1,300+ active formulas and full cross-sheet traceability. Its core data (equipment, suppliers, risk register, assumptions, program register) lives in `db/capex_portfolio.db` and is generated into the workbook with the scripts in `build/` (`python3 build/build_workbook.py`), so the whole model is reproducible and auditable — see [Data Workflow](#data-workflow) below for how to edit it.

| Zone | Sheets | Content |
|---|---|---|
| Z0 — Governance | 3 | Index, Disclaimer, Assumptions |
| Z1 — Foundation | 4 | Equipment Portfolio, Supplier Dataset, Should-Cost Model, TCO |
| Z2 — Planning | 6 | WBS, CPM Schedule, Milestone Roadmap, Deployment Timeline, Capacity Planning, Demand Forecast |
| Z3 — Financial & Risk | 5 | AR Summary, Cash Flow, FX Exposure, Scenario Analysis, Supply Chain Risk |
| Z4 — Strategic Supply Chain | 8 | Market Analysis, Network Map, Sourcing Pipeline, Dual-Source Strategy, Negotiation Tracker, Supplier Capacity, Inventory Planning, Asset Tracking |
| Z5 — Execution & Control | 7 | Milestone Gate Tracker, ECO Register, Vendor Design Changes, Yield Metrics, ROI Tracker, Vendor Scorecard, Change Tracker |
| Z6 — Portfolio & Capital Allocation | 3 | Portfolio Register, Portfolio Dashboard, Portfolio Prioritization scorecard |

### Multi-program layer (Z6)

S02 (Equipment Portfolio), S03 (Supplier Dataset), and S16 (Supply Chain Risk) each carry a **Program ID** column (PRG-001 / PRG-002) and hold both programs' rows side by side. Three new sheets sit on top:

- **S33_Portfolio_Register** — one row per program; financial and risk fields are live-linked back to that program's own sheets where a supporting model exists (Greenfield's full 33-sheet model), and clearly labelled as FEL-2 planning estimates where it doesn't yet (Riverside's IRR/NPV/payback).
- **S34_Portfolio_Dashboard** — portfolio-wide KPI tiles (`SUMIFS`/`AVERAGEIFS` over the Program ID columns) plus a program-by-program comparison table. This is the sheet the site's Home page mirrors.
- **S35_Portfolio_Prioritization** — a weighted scorecard (financial return, strategic fit, risk, schedule readiness, capital efficiency, org readiness) that ranks programs for capital-allocation sequencing, using the same weighting mechanic as S13's scenario comparison, applied program-vs-program instead of scenario-vs-scenario.

To add a third program: append its equipment/supplier/risk rows to S02/S03/S16 with a new Program ID, add a row to S33, and S34/S35 pick it up automatically — no formula changes required.

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
│       ├── programs-data.js    → Portfolio registry (both programs' data), switcher helpers, portfolio rollups
│       ├── main.js             → Shared utilities, Chart.js defaults, footer, project switcher UI
│       ├── home.js             → Home page portfolio KPI strip + program cards
│       ├── executive.js        → Executive dashboard — fully data-driven per active program
│       ├── supply-chain.js     → Supply chain charts
│       ├── execution.js        → Execution & risk charts
│       ├── deep-dive.js        → Deep dive charts
│       └── sourcing.js         → Sourcing framework charts
├── downloads/
│   ├── CapEx_StrategicSC_Portfolio.xlsx   → Full 36-sheet, 2-program workbook (generated)
│   └── CapEx_StrategicSC_Portfolio.pdf    → Print export of the workbook
├── db/
│   ├── schema.sql               → Table/view definitions — the source of truth's structure
│   └── capex_portfolio.db       → SQLite database — the source of truth's data (committed, editable)
└── build/                       → Python/openpyxl scripts; everything here regenerates from db/capex_portfolio.db
    ├── db.py                    → Backend/data-access layer — the ONLY module that touches sqlite3
    ├── seed_from_current.py     → One-time: loads the original hardcoded data into a fresh DB
    ├── build_workbook.py        → DB → downloads/CapEx_StrategicSC_Portfolio.xlsx
    ├── export_site_data.py      → DB → assets/js/programs-data.js
    ├── refresh_all.py           → Runs both of the above, in order (run this after any DB edit)
    ├── import_excel.py          → Excel → DB sync, with a dry-run diff (see Data Workflow below)
    └── s*.py                    → One generator module per workbook sheet
```

---

## Data Workflow

`db/capex_portfolio.db` (SQLite) is the source of truth. The Excel workbook and the website's `programs-data.js` are both *generated* from it — never edited by hand — so the three can never quietly drift apart. There are two ways to make an edit:

**Option A — DB Browser for SQLite (recommended for structured edits: rows, flags, new suppliers)**

1. Install [DB Browser for SQLite](https://sqlitebrowser.org/) (free, Windows/Mac/Linux).
2. Open `db/capex_portfolio.db`.
3. Go to the **Browse Data** tab, pick a table (`equipment`, `suppliers`, `risk_items`, `assumptions`, `programs`), and edit cells directly. Yes/No flags (`single_source`, `alt_supplier_available`, `buffer_stock`) are stored as the literal text `Yes`/`No` — the same words the Excel sheet shows — not `0`/`1`, so there's nothing to decode.
4. Click **Write Changes** (or Ctrl+S) to save.
5. From `build/`, run `python3 refresh_all.py` to regenerate both the workbook and the site data from the updated DB.

**Option B — edit the Excel workbook directly, then import**

1. Open `downloads/CapEx_StrategicSC_Portfolio.xlsx` (the same file the site's "↓ Workbook" button downloads).
2. Edit any **blue-font input cell** — unit costs, lead times, reliability scores, assumption values, a program's IRR/NPV/payback estimate. Leave black-font formula cells and green cross-sheet links alone; those are recalculated, not stored.
3. Save the file to the same path.
4. From `build/`, run `python3 import_excel.py` — this is a **dry run** by default: it reports exactly which rows and fields changed, without writing anything.
5. Review the diff, then run `python3 import_excel.py --apply` to write it to the database.
6. Run `python3 refresh_all.py` so the workbook (now re-derived from the DB) and the site data stay in lockstep with what you just imported.

Only input cells are read back — formula cells (totals, calculated risk scores, cross-sheet links) are recomputed by the DB-driven generators, never imported. Two S33 fields (Strategic Capacity Impact, Notes) are Excel-only presentation text with no DB column, and PRG-002's FX Reserve/NRE reserve are baked into a formula literal rather than their own cell — edit those, if ever, directly in the `programs` table.

This is a one-way sync triggered explicitly by running a script, not a live link — if the same row is edited in Excel and in DB Browser before either is imported, whichever is imported second wins. For a single-editor portfolio like this one that's a non-issue; it's worth knowing if you extend this to a team workflow.

**Setup:** `pip install -r build/requirements.txt` (just `openpyxl`; everything else is standard library).

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
