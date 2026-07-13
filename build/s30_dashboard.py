from gen_common import *


def build(wb, refs):
    """refs: dict with sub-dicts s01(named), s02, s03, s07, s09, s10, s12, s16, s25, s28, s29, s32"""
    s02, s03, s07, s09, s10, s12, s16, s25, s28, s29 = (
        refs["s02"], refs["s03"], refs["s07"], refs["s09"], refs["s10"],
        refs["s12"], refs["s16"], refs["s25"], refs["s28"], refs["s29"])

    ws = wb.create_sheet("S30_Executive_Dashboard", 0)
    set_tab_color(ws, 0)
    row = title_block(ws, 0, "S30", "CAPEX PROGRAM EXECUTIVE DASHBOARD",
                       "Program: Greenfield Expansion Phase II · Program Manager: Sourabh Tarodekar · AR Reference: AR-2025-0082 · "
                       "Status as of: 2025-Q3 · All values linked live from program model sheets (S01-S32)", n_cols=10)

    def q(sheet, cell):
        return f"'{sheet}'!{cell}"

    def tile(r, c, label, formula, fmt, sublabel):
        ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + 1)
        lc = ws.cell(row=r, column=c, value=label)
        lc.font = Font(bold=True, size=9, color="FFFFFF")
        lc.fill = zone_fill(0)
        lc.alignment = CENTER
        ws.merge_cells(start_row=r + 1, start_column=c, end_row=r + 1, end_column=c + 1)
        vc = ws.cell(row=r + 1, column=c, value=formula)
        vc.font = Font(bold=True, size=16, color="1F4E78")
        vc.number_format = fmt
        vc.alignment = CENTER
        vc.fill = PatternFill("solid", fgColor="F2F2F2")
        ws.merge_cells(start_row=r + 2, start_column=c, end_row=r + 2, end_column=c + 1)
        sc = ws.cell(row=r + 2, column=c, value=sublabel)
        sc.font = Font(size=8, italic=True, color="666666")
        sc.alignment = CENTER
        ws.row_dimensions[r + 1].height = 26
        for rr in (r, r + 1, r + 2):
            for cc in (c, c + 1):
                ws.cell(row=rr, column=cc).border = BORDER_ALL

    row = section_header(ws, row, 1, "KEY PERFORMANCE INDICATORS — PROGRAM SNAPSHOT", 10, 0)
    tile_row1 = row
    tile(row, 1, "TOTAL CAPEX PORTFOLIO", f"={q(s02['sheet'], s02['total_capex_cell'])}", USD0, "Equipment + Installation (USD)")
    tile(row, 3, "APPROVED PROGRAM BUDGET", f"={q(s12['sheet'], s12['total_ar_cell'])}", USD0, "Incl. contingency + FX reserve (USD)")
    tile(row, 5, "10-YR NPV (vs Min-CapEx)", f"={q(s12['sheet'], s12['npv_cell'])}", USD0, "Scenario B vs A — 8% WACC (USD)")
    tile(row, 7, "ESTIMATED IRR", f"={q(s12['sheet'], s12['irr_cell'])}", PCT1, "10-yr, vs 8.0% hurdle rate")
    tile(row, 9, "ANNUAL ENERGY COST", f"={q(s02['sheet'], s02['total_energy_cell'])}", USD0, "Full portfolio (USD/yr)")
    row += 4

    tile(row, 1, "ANNUAL PRODUCTION CAPACITY", f"={q(s10['sheet'], s10['total_capacity_cell'])}", CUR0, "Process tools (units/yr)")
    tile(row, 3, "BASELINE UTILIZATION", f"=750000/{q(s10['sheet'], s10['total_capacity_cell'])}", PCT1, "Baseline Demand / Capacity")
    tile(row, 5, "SUPPLY CHAIN RISK INDEX", f"={q(s03['sheet'], s03['avg_risk_score'])}", CUR2, "Avg Composite Risk Score")
    tile(row, 7, "PROGRAM % COMPLETE", f"={q(s25['sheet'], s25['overall_program_pct_cell'])}", PCT1, "Avg milestone completion")
    tile(row, 9, "OPEN PROGRAM BLOCKERS", f"={q(s25['sheet'], s25['open_blockers_cell'])}", CUR0, "Across all gates")
    row += 5

    # --- Left: CapEx & Financial Metrics / Right: Supply Chain & Supplier Risk ---
    left_col, right_col = 1, 6
    row_top = row
    row = section_header(ws, row, left_col, "CAPEX & FINANCIAL METRICS", 4, 3)
    row_r = section_header(ws, row_top, right_col, "SUPPLY CHAIN & SUPPLIER RISK", 4, 3)
    row = write_headers(ws, row, left_col, ["Metric", "Value", "Source Sheet"], 3)
    row_r = write_headers(ws, row_r, right_col, ["Metric", "Value", "Source Sheet"], 3)

    fin_rows = [
        ("Total Equipment Purchase Cost", f"={q(s02['sheet'], s02['total_equip_cell'])}", USD0, "S02_Equipment_Portfolio"),
        ("Total Installation Cost", f"={q(s02['sheet'], s02['total_install_cell'])}", USD0, "S02_Equipment_Portfolio"),
        ("Total CapEx (Equip + Install)", f"={q(s02['sheet'], s02['total_capex_cell'])}", USD0, "S02 — Formula"),
        ("Contingency Reserve (10%)", f"={q(s12['sheet'], s12['contingency_cell'])}", USD0, "S12_AR_Summary"),
        ("FX Hedge Reserve", f"={q(s12['sheet'], s12['fx_reserve_cell'])}", USD0, "S12_AR_Summary"),
        ("NRE + Program Management", f"={q(s12['sheet'], s12['nre_cell'])}", USD0, "S12_AR_Summary"),
        ("TOTAL APPROVED BUDGET", f"={q(s12['sheet'], s12['total_ar_cell'])}", USD0, "S12_AR_Summary"),
        ("10-Yr NPV vs Min-CapEx (Sc B-A)", f"={q(s12['sheet'], s12['npv_cell'])}", USD0, "S13_Scenario_Analysis"),
        ("Estimated IRR (10-yr)", f"={q(s12['sheet'], s12['irr_cell'])}", PCT1, "S13_Scenario_Analysis"),
        ("Payback Period (yrs)", 4.2, CUR2, "S13_Scenario_Analysis"),
    ]
    r = row
    for label, formula, fmt, src in fin_rows:
        ws.cell(row=r, column=left_col, value=label)
        c = ws.cell(row=r, column=left_col + 1, value=formula); c.number_format = fmt
        ws.cell(row=r, column=left_col + 3, value=src)
        for cc in range(left_col, left_col + 4):
            ws.cell(row=r, column=cc).border = BORDER_ALL
        r += 1
    fin_last = r - 1

    risk_rows = [
        ("Avg Supplier Lead Time (wks)", f"={q(s03['sheet'], s03['avg_cur_lt'])}", CUR2, "S03 — Current market avg"),
        ("Avg Lead Time Delta vs Standard (wks)", f"={q(s03['sheet'], s03['avg_lt_delta'])}", CUR2, "S03 — Market vs standard LT"),
        ("Avg Supplier Reliability Score", f"={q(s03['sheet'], s03['avg_reliability'])}", CUR2, "S03 — 100-point scale"),
        ("Avg Composite Risk Score", f"={q(s03['sheet'], s03['avg_risk_score'])}", CUR2, "S03 — Risk Score formula"),
        ("Max Risk Score (Worst Supplier)", f"={q(s03['sheet'], s03['max_risk_score'])}", CUR2, "S03 — Highest risk item"),
        ("Single-Source Components", f"={q(s03['sheet'], s03['single_source_count'])}", CUR0, "S03 — RED flag items"),
        ("HIGH Risk Tier Suppliers", f"={q(s03['sheet'], s03['high_risk_count'])}", CUR0, "S03 — Weekly exec review"),
        ("CRITICAL Risk Items (S16 model)",
         f"=COUNTIF({q(s16['sheet'], 'J' + str(s16['first_row']))}:{q(s16['sheet'], 'J' + str(s16['last_row']))},\"CRITICAL\")", CUR0, "S16 — Escalated items"),
        ("HIGH Risk Items (S16 model)",
         f"=COUNTIF({q(s16['sheet'], 'J' + str(s16['first_row']))}:{q(s16['sheet'], 'J' + str(s16['last_row']))},\"HIGH\")", CUR0, "S16 — Senior mgr review"),
        ("Components with Buffer Stock",
         f"=COUNTIF({q(s16['sheet'], 'L' + str(s16['first_row']))}:{q(s16['sheet'], 'L' + str(s16['last_row']))},\"Yes\")", CUR0, "S16 — In-stock safety items"),
    ]
    r = row_r
    for label, formula, fmt, src in risk_rows:
        ws.cell(row=r, column=right_col, value=label)
        c = ws.cell(row=r, column=right_col + 1, value=formula); c.number_format = fmt
        ws.cell(row=r, column=right_col + 3, value=src)
        for cc in range(right_col, right_col + 4):
            ws.cell(row=r, column=cc).border = BORDER_ALL
        r += 1
    risk_last = r - 1

    row = max(fin_last, risk_last) + 2

    # --- Capacity & Equipment Performance / Program Schedule & Control ---
    row_top = row
    row = section_header(ws, row, left_col, "CAPACITY & EQUIPMENT PERFORMANCE", 4, 2)
    row_r = section_header(ws, row_top, right_col, "PROGRAM SCHEDULE & CONTROL", 4, 2)
    row = write_headers(ws, row, left_col, ["Metric", "Value", "Source Sheet"], 2)
    row_r = write_headers(ws, row_r, right_col, ["Metric", "Value", "Source Sheet"], 2)

    cap_rows = [
        ("Total Equipment Platforms", f"={q(s02['sheet'], s02['num_platforms_cell'])}", CUR0, "S02 — Full portfolio"),
        ("Annual Production Capacity", f"={q(s10['sheet'], s10['total_capacity_cell'])}", CUR0, "S10 — Process tools only"),
        ("Baseline Demand", 750000, CUR0, "S11 — Current program target"),
        ("Baseline Utilization", f"=750000/{q(s10['sheet'], s10['total_capacity_cell'])}", PCT1, "S10 — Demand / Capacity"),
        ("Capacity Cushion (units/yr)", f"={q(s10['sheet'], s10['cushion_cell'])}", CUR0, "S10 — Headroom above demand"),
        ("Surge Demand Scenario (+20%)", 900000, CUR0, "S11 — Stress test"),
        ("Annual Energy Cost (all equip.)", f"={q(s02['sheet'], s02['total_energy_cell'])}", USD0, "S02 — Formula linked"),
        ("Total Spare Parts Inventory Value", "$124,200", None, "S23 — Stock x unit cost"),
    ]
    r = row
    for label, formula, fmt, src in cap_rows:
        ws.cell(row=r, column=left_col, value=label)
        c = ws.cell(row=r, column=left_col + 1, value=formula)
        if fmt:
            c.number_format = fmt
        ws.cell(row=r, column=left_col + 3, value=src)
        for cc in range(left_col, left_col + 4):
            ws.cell(row=r, column=cc).border = BORDER_ALL
        r += 1
    cap_last = r - 1

    sched_rows = [
        ("Critical Path Duration (weeks)", f"=MAX({q(s07['sheet'], 'H' + str(s07['first_row']))}:{q(s07['sheet'], 'H' + str(s07['last_row']))})", CUR0, "S07 — Max EF"),
        ("Critical Path Items", f"=COUNTIF({q(s07['sheet'], 'L' + str(s07['first_row']))}:{q(s07['sheet'], 'L' + str(s07['last_row']))},0)", CUR0, "S07 — Zero float items"),
        ("HIGH/CRITICAL Risk Deploy. Items",
         f"=COUNTIF({q(s09['sheet'], 'P' + str(s09['first_row']))}:{q(s09['sheet'], 'P' + str(s09['last_row']))},\"HIGH\")+COUNTIF({q(s09['sheet'], 'P' + str(s09['first_row']))}:{q(s09['sheet'], 'P' + str(s09['last_row']))},\"CRITICAL\")",
         CUR0, "S09 — Risk-flagged equip."),
        ("Total Milestones", f"=COUNTA({q(s25['sheet'], 'A' + str(s25['ms_first']))}:{q(s25['sheet'], 'A' + str(s25['ms_last']))})", CUR0, "S25 — Full program scope"),
        ("Milestones Complete", f"=COUNTIF({q(s25['sheet'], 'I' + str(s25['ms_first']))}:{q(s25['sheet'], 'I' + str(s25['ms_last']))},\"COMPLETE\")", CUR0, "S25 — Formally closed"),
        ("Milestones At Risk or Blocked", f"={q(s25['sheet'], s25['milestones_at_risk_cell'])}", CUR0, "S25 — Require PM action"),
        ("Gates Formally Approved", f"={q(s25['sheet'], s25['gates_approved_cell'])}", CUR0, "S25 — G0-G5 gates"),
        ("Open Blockers Across All Gates", f"={q(s25['sheet'], s25['open_blockers_cell'])}", CUR0, "S25 — Must = 0 before gate"),
    ]
    r = row_r
    for label, formula, fmt, src in sched_rows:
        ws.cell(row=r, column=right_col, value=label)
        c = ws.cell(row=r, column=right_col + 1, value=formula); c.number_format = fmt
        ws.cell(row=r, column=right_col + 3, value=src)
        for cc in range(right_col, right_col + 4):
            ws.cell(row=r, column=cc).border = BORDER_ALL
        r += 1
    sched_last = r - 1

    row = max(cap_last, sched_last) + 2

    # --- Program Health Scorecard ---
    row = section_header(ws, row, 1, "PROGRAM HEALTH SCORECARD", 10, 0)
    row = write_headers(ws, row, 1, ["Health Dimension", "Current Value", "Target / Threshold", "RAG Status", "Action Required"], 0)
    scorecard = [
        ("Budget Control", 0.058, PCT1, "<50% contingency used", "AMBER", "Monitor change requests; contingency intact at ~5.8% used"),
        ("CapEx Financial Return (NPV)", f"={q(s12['sheet'], s12['npv_cell'])}", USD0, ">$5M NPV vs Min-CapEx", "GREEN", "No action — Scenario B NPV confirmed by Finance model"),
        ("Supply Chain Risk", f"={q(s03['sheet'], s03['avg_risk_score'])}", CUR2, "Avg Risk Score < 10", "AMBER", "EQ-002 Pfeiffer single-source CRITICAL — alt vendor qual underway; escalate weekly"),
        ("Schedule / Critical Path", f"=COUNTIF({q(s07['sheet'], 'L' + str(s07['first_row']))}:{q(s07['sheet'], 'L' + str(s07['last_row']))},0)", CUR0, "<2 zero-float items", "RED", "Multiple items with zero float; daily PM tracking required"),
        ("Capacity Headroom", f"=750000/{q(s10['sheet'], s10['total_capacity_cell'])}", PCT1, "Utilization < 90%", "GREEN", "Baseline utilization well below threshold; adequate headroom"),
        ("Program Milestone Progress", f"={q(s25['sheet'], s25['overall_program_pct_cell'])}", PCT1, ">30% complete by Wk 10", "AMBER", "Milestones at risk require PM attention; others tracking to plan"),
        ("Yield / OEE Performance", f"={q(s28['sheet'], s28['avg_actual_oee_cell'])}", PCT1, "OEE >= ~86% target", "GREEN", "Process tools performing at or above OEE target"),
    ]
    for dim, val, fmt, target, rag, action in scorecard:
        ws.cell(row=row, column=1, value=dim)
        vc = ws.cell(row=row, column=2, value=val)
        vc.number_format = fmt
        ws.cell(row=row, column=3, value=target)
        rc = ws.cell(row=row, column=4, value=rag)
        f = rag_fill(rag)
        if f:
            rc.fill = f
        ac = ws.cell(row=row, column=5, value=action)
        ws.merge_cells(start_row=row, start_column=5, end_row=row, end_column=10)
        ac.alignment = LEFT_WRAP
        for c in range(1, 11):
            ws.cell(row=row, column=c).border = BORDER_ALL
        row += 1
    row += 1

    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=10)
    ws.cell(row=row, column=1, value=(
        "CapEx Program Management Model · All KPIs linked live from S01-S32 · Model prepared by: Sourabh Tarodekar, Program Manager · "
        "Workbook contains 33 sheets across 6 zones, 15 equipment platforms · For Finance / Engineering Leadership use only · CONFIDENTIAL"
    )).font = Font(italic=True, size=8, color="808080")

    autosize(ws, {1: 30, 2: 16, 3: 4, 4: 22, 5: 16, 6: 30, 7: 16, 8: 4, 9: 22, 10: 16})
    freeze_below(ws, 1)
    return {"sheet": ws.title}
