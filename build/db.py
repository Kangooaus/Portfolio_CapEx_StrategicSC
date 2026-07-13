"""
db.py — the backend for the CapEx portfolio data layer.

This is the ONLY module in this project that imports sqlite3. Every script
and Excel-sheet generator that needs data goes through the functions below,
never through raw SQL of its own. That boundary is deliberate: it's what
lets the editing surface change later (DB Browser today, a real web admin
UI + API tomorrow) without touching the schema, the Excel generators, or
the site export script. A future API server would wrap these exact
functions as HTTP endpoints rather than reimplementing them.

Every function returns plain dicts/lists (JSON-serializable, no ORM
objects, no open cursors) so it's trivial to expose over HTTP later.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "capex_portfolio.db"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "db" / "schema.sql"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn=None):
    """Create the schema if it doesn't exist yet. Safe to call repeatedly."""
    own = conn is None
    conn = conn or get_connection()
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())
    conn.commit()
    if own:
        conn.close()


def _rows(cur):
    return [dict(r) for r in cur.fetchall()]


# ---------------------------------------------------------------- programs

def list_programs(conn=None):
    own = conn is None
    conn = conn or get_connection()
    rows = _rows(conn.execute("SELECT * FROM programs ORDER BY sort_order, program_ref"))
    if own:
        conn.close()
    return rows


def get_program(program_ref, conn=None):
    own = conn is None
    conn = conn or get_connection()
    row = conn.execute("SELECT * FROM programs WHERE program_ref = ?", (program_ref,)).fetchone()
    if own:
        conn.close()
    return dict(row) if row else None


def upsert_program(row, conn=None):
    own = conn is None
    conn = conn or get_connection()
    cols = ["program_ref", "name", "short_name", "sponsor", "program_manager", "business_unit",
            "phase", "status", "phase_tag", "phase_tag_class", "has_execution_history",
            "ar_reference", "period", "equip_cost", "install_cost", "contingency", "fx_reserve",
            "nre", "total_ar_budget", "irr", "npv", "payback_yrs", "is_estimate", "sort_order", "notes"]
    values = [row.get(c) for c in cols]
    placeholders = ",".join("?" for _ in cols)
    update_clause = ",".join(f"{c}=excluded.{c}" for c in cols if c != "program_ref")
    conn.execute(
        f"INSERT INTO programs ({','.join(cols)}) VALUES ({placeholders}) "
        f"ON CONFLICT(program_ref) DO UPDATE SET {update_clause}",
        values,
    )
    conn.commit()
    if own:
        conn.close()


# --------------------------------------------------------------- equipment

def list_equipment(program_ref=None, conn=None):
    own = conn is None
    conn = conn or get_connection()
    if program_ref:
        rows = _rows(conn.execute(
            "SELECT * FROM equipment WHERE program_ref = ? ORDER BY sort_order, equip_id", (program_ref,)))
    else:
        rows = _rows(conn.execute("SELECT * FROM equipment ORDER BY program_ref, sort_order, equip_id"))
    if own:
        conn.close()
    return rows


def upsert_equipment(row, conn=None):
    own = conn is None
    conn = conn or get_connection()
    cols = ["program_ref", "equip_id", "category", "tool_type", "supplier", "region", "currency",
            "unit_cost", "qty", "install_cost_unit", "life_yrs", "energy_kwh_hr", "maint_rate_pct",
            "throughput_uhr", "op_hrs_yr", "notes", "sort_order"]
    values = [row.get(c) for c in cols]
    placeholders = ",".join("?" for _ in cols)
    update_clause = ",".join(f"{c}=excluded.{c}" for c in cols if c not in ("program_ref", "equip_id"))
    conn.execute(
        f"INSERT INTO equipment ({','.join(cols)}) VALUES ({placeholders}) "
        f"ON CONFLICT(program_ref, equip_id) DO UPDATE SET {update_clause}",
        values,
    )
    conn.commit()
    if own:
        conn.close()


# --------------------------------------------------------------- suppliers

def list_suppliers(program_ref=None, conn=None):
    own = conn is None
    conn = conn or get_connection()
    if program_ref:
        rows = _rows(conn.execute(
            "SELECT * FROM suppliers WHERE program_ref = ? ORDER BY sort_order, id", (program_ref,)))
    else:
        rows = _rows(conn.execute("SELECT * FROM suppliers ORDER BY program_ref, sort_order, id"))
    if own:
        conn.close()
    return rows


def upsert_supplier(row, conn=None):
    own = conn is None
    conn = conn or get_connection()
    cols = ["program_ref", "supplier_name", "component_type", "equip_ref", "region", "currency",
            "std_lt_wks", "current_lt_wks", "reliability", "single_source", "alt_supplier_available",
            "notes", "sort_order"]
    values = [row.get(c) for c in cols]
    if row.get("id"):
        conn.execute(
            f"UPDATE suppliers SET {','.join(f'{c}=?' for c in cols)} WHERE id = ?",
            values + [row["id"]],
        )
    else:
        placeholders = ",".join("?" for _ in cols)
        conn.execute(f"INSERT INTO suppliers ({','.join(cols)}) VALUES ({placeholders})", values)
    conn.commit()
    if own:
        conn.close()


# -------------------------------------------------------------- risk_items

def list_risk_items(program_ref=None, conn=None):
    own = conn is None
    conn = conn or get_connection()
    if program_ref:
        rows = _rows(conn.execute(
            "SELECT * FROM risk_items WHERE program_ref = ? ORDER BY sort_order, id", (program_ref,)))
    else:
        rows = _rows(conn.execute("SELECT * FROM risk_items ORDER BY program_ref, sort_order, id"))
    if own:
        conn.close()
    return rows


def upsert_risk_item(row, conn=None):
    own = conn is None
    conn = conn or get_connection()
    cols = ["program_ref", "equip_ref", "supplier", "component", "std_lead", "current_lead",
            "delay_prob", "sched_impact", "replace_difficulty", "single_source", "buffer_stock",
            "mitigation", "status", "sort_order"]
    values = [row.get(c) for c in cols]
    if row.get("id"):
        conn.execute(
            f"UPDATE risk_items SET {','.join(f'{c}=?' for c in cols)} WHERE id = ?",
            values + [row["id"]],
        )
    else:
        placeholders = ",".join("?" for _ in cols)
        conn.execute(f"INSERT INTO risk_items ({','.join(cols)}) VALUES ({placeholders})", values)
    conn.commit()
    if own:
        conn.close()


# ------------------------------------------------------------- assumptions

def list_assumptions(program_ref=None, conn=None):
    """program_ref=None returns global assumptions only; pass a program_ref to also
    get that program's global assumptions (there are no per-program overrides yet)."""
    own = conn is None
    conn = conn or get_connection()
    rows = _rows(conn.execute(
        "SELECT * FROM assumptions WHERE program_ref IS NULL ORDER BY sort_order, id"))
    if own:
        conn.close()
    return rows


def get_assumption(parameter, conn=None):
    own = conn is None
    conn = conn or get_connection()
    row = conn.execute(
        "SELECT * FROM assumptions WHERE parameter = ? AND program_ref IS NULL", (parameter,)
    ).fetchone()
    if own:
        conn.close()
    return dict(row) if row else None


def upsert_assumption(row, conn=None):
    own = conn is None
    conn = conn or get_connection()
    cols = ["program_ref", "section", "parameter", "value", "value_text", "unit", "source",
            "date_validated", "notes", "sort_order"]
    values = [row.get(c) for c in cols]
    if row.get("id"):
        conn.execute(
            f"UPDATE assumptions SET {','.join(f'{c}=?' for c in cols)} WHERE id = ?",
            values + [row["id"]],
        )
    else:
        placeholders = ",".join("?" for _ in cols)
        conn.execute(f"INSERT INTO assumptions ({','.join(cols)}) VALUES ({placeholders})", values)
    conn.commit()
    if own:
        conn.close()


# ------------------------------------------------------------ portfolio rollups

def portfolio_totals(conn=None):
    own = conn is None
    conn = conn or get_connection()
    row = conn.execute("SELECT * FROM v_portfolio_totals").fetchone()
    if own:
        conn.close()
    return dict(row) if row else None


def program_equipment_totals(program_ref, conn=None):
    own = conn is None
    conn = conn or get_connection()
    row = conn.execute(
        "SELECT * FROM v_program_equipment_totals WHERE program_ref = ?", (program_ref,)
    ).fetchone()
    if own:
        conn.close()
    return dict(row) if row else None


def program_supplier_totals(program_ref, conn=None):
    own = conn is None
    conn = conn or get_connection()
    row = conn.execute(
        "SELECT * FROM v_program_supplier_totals WHERE program_ref = ?", (program_ref,)
    ).fetchone()
    if own:
        conn.close()
    return dict(row) if row else None


def program_risk_totals(program_ref, conn=None):
    own = conn is None
    conn = conn or get_connection()
    row = conn.execute(
        "SELECT * FROM v_program_risk_totals WHERE program_ref = ?", (program_ref,)
    ).fetchone()
    if own:
        conn.close()
    return dict(row) if row else None
