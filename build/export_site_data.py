"""
export_site_data.py — regenerates assets/js/programs-data.js from the database.

Structural/numeric program fields (name, sponsor info, phase/status badge,
CapEx, budget, platform and supplier rollups) come straight from db.py — the
same functions the Excel generators use — so the website and the workbook
can never disagree about those numbers.

The rich dashboard narrative (KPI captions, insight call-outs, chart series
breakdowns, health-check cards, readiness path) is curated prose and
hand-picked chart groupings, not queryable rows, so it lives in
NARRATIVE_EXTRAS below rather than in a database table. Adding a new program
means adding a NARRATIVE_EXTRAS entry for it here, same as it always has —
the DB-backed fields for that program are then generated automatically.

Safe to re-run any time the database changes: this fully regenerates
assets/js/programs-data.js, it does not hand-edit it in place.
"""
import json
from pathlib import Path

import db

OUT_PATH = Path(__file__).resolve().parent.parent / "assets" / "js" / "programs-data.js"

PORTFOLIO_ORDER = ["PRG-001", "PRG-002"]
DEFAULT_PROGRAM_REF = "PRG-001"

NARRATIVE_EXTRAS = {
    "PRG-001": {
        "id": "greenfield-phase2",

        "kpis": [
            {"label": "Total CapEx Investment", "value": "$13.87M", "context": "Equip + install · $16.06M AR total", "cls": "navy", "valCls": "neutral"},
            {"label": "Equipment Portfolio Size", "value": "15 Platforms", "context": "45 total units · 6 categories", "cls": "", "valCls": "neutral"},
            {"label": "Annual Production Capacity", "value": "1,040,253", "context": "units/yr · process tools only", "cls": "success", "valCls": "positive"},
            {"label": "Portfolio Utilization", "value": "72.1%", "context": "Baseline 750K · surge 86.5%", "cls": "success", "valCls": "positive"},
            {"label": "Active OEM Suppliers", "value": "15", "context": "7 countries · avg 87.3 reliability", "cls": "blue", "valCls": "neutral"},
            {"label": "Single-Source Risk Count", "value": "2", "context": "Pfeiffer (EQ-002) · Daifuku (EQ-006)", "cls": "danger", "valCls": "danger"},
        ],

        "insights": [
            {"html": "Portfolio CapEx <strong>$13.87M</strong> — 4.3% under AR budget of $16.06M. $2.19M contingency &amp; FX reserve available.", "tag": "Under Budget", "tagCls": "tag-up"},
            {"html": "Annual capacity <strong>1,040,253 units/yr</strong> at 72.1% utilisation — 290K headroom above 750K baseline demand.", "tag": "Healthy", "tagCls": "tag-up"},
            {"html": "IRR <strong>14.2%</strong> vs 8% hurdle. Payback 4.2 years. 10-yr NPV $9.52M vs minimum-CapEx alternative.", "tag": "Exceeds Threshold", "tagCls": "tag-up"},
            {"html": "EQ-002 Pfeiffer TMP remains <strong>critical path single-source</strong> — Shimadzu qualification active, target Q3-2025.", "tag": "Monitor", "tagCls": "tag-down"},
        ],

        "capexDonut": {
            "labels": ["Vacuum Systems", "High-Temp Furnaces", "Robotics & Auto", "Gas Handling", "Controls / PLC", "Facility Infra"],
            "data": [24.2, 32.1, 19.4, 9.9, 8.5, 10.8],
            "colors": ["blue", "navy2", "green", "amber", "cyan", "gray"],
        },

        "deployBar": {
            "labels": ["Vacuum", "Furnaces", "Robotics", "Gas", "Controls", "Infra"],
            "series": [
                {"label": "In Production", "data": [9, 5, 5, 4, 6, 3], "color": "green"},
                {"label": "Qualified", "data": [3, 2, 2, 1, 2, 1], "color": "blue"},
                {"label": "Installed", "data": [1, 1, 0, 1, 0, 1], "color": "amber"},
                {"label": "Ordered", "data": [1, 0, 0, 1, 0, 0], "color": "gray"},
            ],
            "badge": "15 Platforms",
            "badgeCls": "badge-green",
            "insight": "13 of 15 platforms in production — EQ-004 furnace and EQ-006 conveyor completing qualification",
        },

        "capacityLine": {
            "labels": ["Q1-23", "Q2-23", "Q3-23", "Q4-23", "Q1-24", "Q2-24", "Q3-24", "Q4-24", "Q1-25", "Q2-25", "Q3-25", "Q4-25"],
            "capacity": [420, 480, 550, 600, 650, 720, 800, 880, 950, 1000, 1040, 1040],
            "demand": [505, 528, 571, 567, 580, 624, 618, 661, 675, 718, 740, 750],
            "footnote": "Capacity = process tools only (EQ-003, EQ-004, EQ-014). Support equipment excluded. Demand from S11_Demand_Forecast.",
        },

        "health": {
            "insight": "All three program dimensions on track as of Dec 2025 — supply chain has one active watch item",
            "cards": [
                {"label": "Schedule Status", "chip": "On Track", "chipCls": "chip-green", "note": "G5 Production Release achieved Q4-2025. No critical path delays. Program closed on schedule."},
                {"label": "Cost Status", "chip": "Under Budget", "chipCls": "chip-green", "note": "Actual $13.87M vs $16.06M AR. $2.19M reserve untouched. Zero budget overruns recorded."},
                {"label": "Supply Chain", "chip": "Watch", "chipCls": "chip-amber", "note": "Pfeiffer single-source risk (EQ-002) — Shimadzu qualification ongoing. All other OEMs on track."},
            ],
            "decisionList": [
                {"label": "Board Approved Budget", "value": "$16,062,000", "cls": ""},
                {"label": "Actual CapEx Spend", "value": "$13,870,000", "cls": "green"},
                {"label": "10-Year IRR", "value": "14.2%", "cls": "green"},
                {"label": "Simple Payback Period", "value": "4.2 years", "cls": ""},
                {"label": "10-Year NPV vs Min-CapEx", "value": "+$9,520,000", "cls": "green"},
            ],
        },
    },

    "PRG-002": {
        "id": "riverside-phase1",

        "kpis": [
            {"label": "Total CapEx Investment", "value": "$2.38M", "context": "Equip + install · $2.76M est. AR total", "cls": "navy", "valCls": "neutral"},
            {"label": "Equipment Platforms", "value": "6 Platforms", "context": "14 total units · 5 categories", "cls": "", "valCls": "neutral"},
            {"label": "Est. Throughput Uplift", "value": "+18%", "context": "packaging line · ~45,000 cases/day incremental", "cls": "success", "valCls": "positive"},
            {"label": "Est. Payback Period", "value": "3.1 yrs", "context": "16.8% IRR · $1.85M 10-yr NPV (est.)", "cls": "success", "valCls": "positive"},
            {"label": "Active OEM Suppliers", "value": "6", "context": "2 countries · avg 91.2 reliability", "cls": "blue", "valCls": "neutral"},
            {"label": "Single-Source Risk Count", "value": "1", "context": "Krones AG (RV-002 cartoning)", "cls": "warning", "valCls": "neutral"},
        ],

        "insights": [
            {"html": "Estimated CapEx <strong>$2.38M</strong> — FEL-2 planning estimate; full AR budget of $2.76M includes contingency, FX and NRE reserves.", "tag": "Pre-Approval", "tagCls": "tag-down"},
            {"html": "Est. throughput uplift <strong>+18%</strong> on the Riverside packaging line — ~45,000 cases/day incremental at full ramp.", "tag": "Business Case", "tagCls": "tag-up"},
            {"html": "Est. IRR <strong>16.8%</strong> vs 8% hurdle. Est. payback 3.1 years — faster payback and smaller ask than Greenfield.", "tag": "Attractive", "tagCls": "tag-up"},
            {"html": "RV-002 Krones cartoning system is the program’s only <strong>single-source risk</strong> — no qualified alternate identified yet.", "tag": "Monitor", "tagCls": "tag-down"},
        ],

        "capexDonut": {
            "labels": ["Robotics & Automation", "Packaging Automation", "Material Handling", "Quality / Automation", "Controls / PLC"],
            "data": [39.0, 19.5, 25.8, 8.6, 7.1],
            "colors": ["green", "navy2", "gray", "amber", "cyan"],
        },

        "sourcingBar": {
            "labels": ["Robotics", "Packaging", "Handling", "Quality", "Controls"],
            "series": [
                {"label": "Awarded / In Fab", "data": [0, 0, 0, 0, 0], "color": "green"},
                {"label": "RFQ / Negotiation", "data": [1, 1, 0, 0, 0], "color": "blue"},
                {"label": "Technical Evaluation", "data": [1, 0, 1, 1, 1], "color": "amber"},
                {"label": "Not Yet Started", "data": [0, 0, 0, 0, 0], "color": "gray"},
            ],
            "badge": "6 Platforms",
            "badgeCls": "badge-amber",
            "insight": "All 6 platforms are in RFQ or technical evaluation — no POs placed yet pending AR approval",
        },

        "health": {
            "insight": "Business case and technical feasibility are strong; organizational readiness is the pacing item ahead of AR submission",
            "readinessCards": [
                {"label": "Business Case", "chip": "Strong", "chipCls": "chip-green", "note": "16.8% est. IRR and 3.1-yr payback comfortably clear the 8% hurdle rate; smaller, capital-efficient ask."},
                {"label": "Technical Feasibility", "chip": "Validated", "chipCls": "chip-green", "note": "All 6 platforms use mature, commercially available technology; only RV-002 Krones lacks a qualified alternate."},
                {"label": "Organizational Readiness", "chip": "Building", "chipCls": "chip-amber", "note": "Program team standing up under new PM (E. Vargas); sequencing AR submission after Greenfield’s Q3-2025 capital peak."},
            ],
            "decisionList": [
                {"label": "FEL-2 Estimated Budget", "value": "$2,757,200", "cls": ""},
                {"label": "Estimated CapEx (Equip + Install)", "value": "$2,382,000", "cls": ""},
                {"label": "Estimated IRR", "value": "16.8%", "cls": "green"},
                {"label": "Estimated Payback Period", "value": "3.1 years", "cls": ""},
                {"label": "Estimated 10-Year NPV", "value": "+$1,850,000", "cls": "green"},
            ],
        },

        "readinessPath": [
            {"step": "FEL-2 Feasibility Study", "status": "IN PROGRESS", "note": "Business case, technical feasibility, and should-cost review underway"},
            {"step": "Supplier RFQ & Technical Evaluation", "status": "IN PROGRESS", "note": "All 6 platforms in RFQ or evaluation; Krones single-source risk being assessed"},
            {"step": "FEL-3 Definition & Should-Cost Lock", "status": "NOT STARTED", "note": "Target start: after Greenfield Q3-2025 peak capital draw clears"},
            {"step": "AR Submission (Target Q4-2025)", "status": "NOT STARTED", "note": "Formal capital appropriations request to VP Engineering + CFO"},
            {"step": "AR Approval & Long-Lead PO Placement", "status": "NOT STARTED", "note": "Pending AR approval — program has no execution history yet"},
        ],
    },
}

_NARRATIVE_KEYS = ("kpis", "insights", "capexDonut", "deployBar", "sourcingBar", "capacityLine", "health", "readinessPath")


def build_program(program_ref):
    p = db.get_program(program_ref)
    eq = db.program_equipment_totals(program_ref) or {}
    sup = db.program_supplier_totals(program_ref) or {}
    suppliers = db.list_suppliers(program_ref=program_ref)
    countries = len({s["region"] for s in suppliers if s["region"]})
    extras = NARRATIVE_EXTRAS[program_ref]

    capex = eq.get("total_capex") or 0

    out = {
        "id": extras["id"],
        "programRef": p["program_ref"],
        "name": p["name"],
        "shortName": p["short_name"],
        "businessUnit": p["business_unit"],
        "programManager": p["program_manager"],
        "phase": p["phase"],
        "phaseTag": p["phase_tag"],
        "phaseTagClass": p["phase_tag_class"],
        "hasExecutionHistory": bool(p["has_execution_history"]),
        "arReference": p["ar_reference"],
        "period": p["period"],
        "raw": {
            "capex": int(capex),
            "budget": int(p["total_ar_budget"]),
            "platforms": int(eq.get("platform_count") or 0),
            "suppliers": int(sup.get("supplier_count") or 0),
            "singleSource": int(sup.get("single_source_count") or 0),
            "countries": countries,
        },
    }

    for key in _NARRATIVE_KEYS:
        if key in extras:
            out[key] = extras[key]

    if "capexDonut" in out:
        out["capexDonut"] = dict(out["capexDonut"], totalBadge=f"${capex / 1e6:.2f}M Total")

    return out


FOOTER = """
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
"""


def render():
    programs = {}
    for ref in PORTFOLIO_ORDER:
        prog = build_program(ref)
        programs[prog["id"]] = prog

    default_id = NARRATIVE_EXTRAS[DEFAULT_PROGRAM_REF]["id"]
    order_ids = [NARRATIVE_EXTRAS[ref]["id"] for ref in PORTFOLIO_ORDER]

    lines = [
        "/* ============================================================",
        "   programs-data.js — portfolio registry",
        "   GENERATED FILE — do not hand-edit.",
        "   Structural/numeric fields are produced from capex_portfolio.db",
        "   by build/export_site_data.py; re-run that script after editing",
        "   the database. Narrative content (KPIs, insights, chart series,",
        "   health cards) is authored in NARRATIVE_EXTRAS in that script.",
        "   ============================================================ */",
        "",
        "const PROGRAMS = " + json.dumps(programs, indent=2) + ";",
        "",
        "const PORTFOLIO_ORDER = " + json.dumps(order_ids) + ";",
        f"const DEFAULT_PROGRAM = {json.dumps(default_id)};",
        FOOTER.strip("\n"),
        "",
    ]
    return "\n".join(lines)


def export():
    db.init_schema()
    content = render()
    OUT_PATH.write_text(content)
    print(f"Wrote {OUT_PATH} ({len(content)} bytes)")


if __name__ == "__main__":
    export()
