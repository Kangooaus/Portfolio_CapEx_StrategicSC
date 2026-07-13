-- ============================================================
-- CapEx Strategic Portfolio — SQLite schema (Phase 1)
--
-- Scope: programs, equipment, suppliers, risk_items, assumptions.
-- These five tables are the source of truth for:
--   - S02_Equipment_Portfolio, S03_Supplier_Dataset, S16_Supply_Chain_Risk,
--     S33_Portfolio_Register (Excel workbook)
--   - The website (via export_site_data.py -> programs-data.js)
--
-- Everything else in the workbook (WBS, CPM, gates, negotiations,
-- inventory, ECOs, yield, ROI, vendor scorecard, change tracker...)
-- stays hardcoded in build/*.py until Phase 2.
--
-- Access rule: only build/db.py opens this file directly. Every other
-- script/generator goes through db.py's functions. That boundary is
-- what lets the editing surface (DB Browser today, a real admin UI
-- later) change without this schema or the Excel generators changing.
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- programs — one row per program (PRG-001, PRG-002, ...)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS programs (
    program_ref            TEXT PRIMARY KEY,       -- 'PRG-001'
    name                    TEXT NOT NULL,          -- 'Greenfield Expansion Phase II'
    short_name              TEXT NOT NULL,          -- 'Greenfield Phase II'
    sponsor                 TEXT,
    program_manager         TEXT,
    business_unit           TEXT,
    phase                   TEXT,                   -- 'G2 — Equipment Build & FAT'
    status                  TEXT,                   -- 'APPROVED — IN EXECUTION'
    phase_tag               TEXT,                   -- 'IN EXECUTION' (short badge text)
    phase_tag_class         TEXT,                   -- 'st-green' | 'st-amber' | 'st-red' (site status pill class)
    has_execution_history   INTEGER NOT NULL DEFAULT 0,  -- 0/1 boolean
    ar_reference             TEXT,
    period                  TEXT,
    -- financial summary (authoritative for programs without their own detailed AR
    -- sheet, e.g. PRG-002; for PRG-001 these mirror S12_AR_Summary's own totals so
    -- S33's cross-sheet formulas and this table never disagree)
    equip_cost               REAL,
    install_cost             REAL,
    contingency               REAL,
    fx_reserve                REAL,
    nre                       REAL,
    total_ar_budget           REAL,
    irr                       REAL,                 -- e.g. 0.142 = 14.2%
    npv                       REAL,
    payback_yrs               REAL,
    is_estimate                INTEGER NOT NULL DEFAULT 0,  -- 1 = IRR/NPV/payback are FEL-stage estimates, not a built TCO model
    sort_order                 INTEGER NOT NULL DEFAULT 0,
    notes                       TEXT
);

-- ------------------------------------------------------------
-- equipment — one row per equipment platform
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS equipment (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    program_ref          TEXT NOT NULL REFERENCES programs(program_ref) ON DELETE CASCADE,
    equip_id             TEXT NOT NULL,        -- 'EQ-001', 'RV-001'
    category             TEXT NOT NULL,
    tool_type            TEXT NOT NULL,
    supplier             TEXT NOT NULL,
    region               TEXT,
    currency             TEXT,
    unit_cost            REAL NOT NULL,
    qty                  INTEGER NOT NULL,
    install_cost_unit    REAL NOT NULL,
    life_yrs             REAL,
    energy_kwh_hr        REAL,
    maint_rate_pct       REAL,
    throughput_uhr       REAL,
    op_hrs_yr            INTEGER,
    notes                TEXT,
    sort_order           INTEGER NOT NULL DEFAULT 0,
    UNIQUE(program_ref, equip_id)
);
CREATE INDEX IF NOT EXISTS idx_equipment_program ON equipment(program_ref);

-- ------------------------------------------------------------
-- suppliers — one row per supplier relationship (usually 1:1 with equipment)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS suppliers (
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    program_ref               TEXT NOT NULL REFERENCES programs(program_ref) ON DELETE CASCADE,
    supplier_name             TEXT NOT NULL,
    component_type            TEXT NOT NULL,
    equip_ref                  TEXT NOT NULL,     -- matches equipment.equip_id within the same program
    region                     TEXT,
    currency                   TEXT,
    std_lt_wks                 REAL NOT NULL,
    current_lt_wks              REAL NOT NULL,
    reliability                 REAL NOT NULL,      -- 0-100
    single_source                TEXT NOT NULL DEFAULT 'No',  -- 'Yes' | 'No' -- matches Excel's own column text, so DB Browser's Browse Data tab is self-explanatory
    alt_supplier_available       TEXT NOT NULL DEFAULT 'No',  -- 'Yes' | 'No'
    notes                         TEXT,
    sort_order                    INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_suppliers_program ON suppliers(program_ref);

-- ------------------------------------------------------------
-- risk_items — supply chain risk register (component-level, can be
-- more granular than equipment, e.g. software/permit risk with no
-- physical lead time)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS risk_items (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    program_ref            TEXT NOT NULL REFERENCES programs(program_ref) ON DELETE CASCADE,
    equip_ref              TEXT NOT NULL,
    supplier               TEXT NOT NULL,
    component               TEXT NOT NULL,
    std_lead                REAL,                  -- nullable: non-hardware risks have no lead time
    current_lead             REAL,
    delay_prob                REAL NOT NULL,        -- 0-1
    sched_impact               REAL NOT NULL,        -- 1-5
    replace_difficulty          REAL NOT NULL,        -- 1-5
    single_source                TEXT NOT NULL DEFAULT 'No',  -- 'Yes' | 'No' -- matches Excel's own column text, so DB Browser's Browse Data tab is self-explanatory
    buffer_stock                  TEXT NOT NULL DEFAULT 'No',  -- 'Yes' | 'No'
    mitigation                    TEXT,
    status                        TEXT,
    sort_order                    INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_risk_items_program ON risk_items(program_ref);

-- ------------------------------------------------------------
-- assumptions — global model parameters (S01_Disclaimer_Assumptions).
-- program_ref NULL = applies to every program.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS assumptions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    program_ref          TEXT REFERENCES programs(program_ref) ON DELETE CASCADE,  -- NULL = global
    section              TEXT NOT NULL,       -- 'ENERGY & UTILITIES'
    parameter            TEXT NOT NULL,       -- 'Energy Price – Electricity'
    value                 REAL,
    value_text            TEXT,                -- for non-numeric values e.g. 'MACRS 7-yr'
    unit                  TEXT,
    source                TEXT,
    date_validated         TEXT,
    notes                  TEXT,
    sort_order             INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_assumptions_program ON assumptions(program_ref);

-- ------------------------------------------------------------
-- Portfolio rollup views — the Zone 6 sheets (S33/S34/S35) have no
-- input tables of their own; they're SUMs/AVERAGEs over the tables
-- above, in Excel and here alike.
-- ------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_program_equipment_totals AS
SELECT
    program_ref,
    COUNT(*)                                   AS platform_count,
    SUM(qty)                                    AS unit_count,
    SUM(unit_cost * qty)                        AS total_equip_cost,
    SUM(install_cost_unit * qty)                AS total_install_cost,
    SUM(unit_cost * qty) + SUM(install_cost_unit * qty) AS total_capex
FROM equipment
GROUP BY program_ref;

CREATE VIEW IF NOT EXISTS v_program_supplier_totals AS
SELECT
    program_ref,
    COUNT(*)                                    AS supplier_count,
    SUM(CASE WHEN single_source = 'Yes' THEN 1 ELSE 0 END) AS single_source_count,
    AVG(current_lt_wks)                          AS avg_current_lt_wks,
    AVG(reliability)                             AS avg_reliability
FROM suppliers
GROUP BY program_ref;

CREATE VIEW IF NOT EXISTS v_program_risk_totals AS
SELECT
    program_ref,
    COUNT(*)                                     AS risk_item_count,
    AVG(delay_prob * sched_impact * replace_difficulty) AS avg_risk_score,
    MAX(delay_prob * sched_impact * replace_difficulty) AS max_risk_score,
    SUM(CASE WHEN single_source = 'Yes' THEN 1 ELSE 0 END) AS single_source_risk_count
FROM risk_items
GROUP BY program_ref;

CREATE VIEW IF NOT EXISTS v_portfolio_totals AS
SELECT
    (SELECT COUNT(*) FROM programs)                                   AS program_count,
    (SELECT COALESCE(SUM(total_capex), 0) FROM v_program_equipment_totals) AS total_capex,
    (SELECT COALESCE(SUM(total_ar_budget), 0) FROM programs)          AS total_budget,
    (SELECT COALESCE(SUM(platform_count), 0) FROM v_program_equipment_totals) AS total_platforms,
    (SELECT COALESCE(SUM(supplier_count), 0) FROM v_program_supplier_totals)  AS total_suppliers,
    (SELECT COALESCE(SUM(single_source_count), 0) FROM v_program_supplier_totals) AS total_single_source;
