from gen_common import *
import db

_STATUS_FILL = {"st-green": RAG_GREEN, "st-amber": RAG_AMBER, "st-red": RAG_RED}


def build(wb, s02, s03, s16, s12):
    ws = wb.create_sheet("S33_Portfolio_Register")
    set_tab_color(ws, 6)
    row = title_block(ws, 6, "S33", "Portfolio Register — All Active & Proposed CapEx Programs",
                       "Portfolio Director: Sourabh Tarodekar | One row per program; financial and risk fields link live "
                       "to each program's own data sheets (S02, S03, S16) where a supporting model exists | "
                       "Program ID is the join key used across S33-S35", n_cols=17)

    def q(sheet, cell):
        return f"'{sheet}'!{cell}"

    headers = ["Program ID", "Program Name", "Sponsor", "Program Manager", "Business Unit", "Phase / Gate",
                "Status", "Total CapEx — Equip+Install (USD)", "Contingency Reserve (USD)",
                "Total Approved Budget (USD)", "Estimated IRR", "10-Yr NPV (USD)", "Payback (yrs)",
                "Avg Supply Chain Risk Score", "Equipment Platforms", "Strategic Capacity Impact", "Notes"]
    header_row = write_headers(ws, row, 1, headers, 6)
    first_row = header_row
    r = header_row

    prg1 = db.get_program("PRG-001")
    prg2 = db.get_program("PRG-002")

    # --- PRG-001: Greenfield Expansion Phase II (fully linked to its live model) ---
    ws.cell(row=r, column=1, value=prg1["program_ref"]).font = BOLD
    ws.cell(row=r, column=2, value=prg1["name"])
    ws.cell(row=r, column=3, value=prg1["sponsor"])
    ws.cell(row=r, column=4, value=prg1["program_manager"])
    ws.cell(row=r, column=5, value=prg1["business_unit"])
    ws.cell(row=r, column=6, value=prg1["phase"])
    stc = ws.cell(row=r, column=7, value=prg1["status"])
    stc.fill = PatternFill("solid", fgColor=_STATUS_FILL.get(prg1["phase_tag_class"], RAG_GREEN))
    capex1 = ws.cell(row=r, column=8, value=f"={q(s02['sheet'], s02['total_capex_cell'])}"); capex1.number_format = USD0; capex1.font = GREEN_LINK
    cont1 = ws.cell(row=r, column=9, value=f"={q(s12['sheet'], s12['contingency_cell'])}"); cont1.number_format = USD0; cont1.font = GREEN_LINK
    bud1 = ws.cell(row=r, column=10, value=f"={q(s12['sheet'], s12['total_ar_cell'])}"); bud1.number_format = USD0; bud1.font = GREEN_LINK
    irr1 = ws.cell(row=r, column=11, value=f"={q(s12['sheet'], s12['irr_cell'])}"); irr1.number_format = PCT1; irr1.font = GREEN_LINK
    npv1 = ws.cell(row=r, column=12, value=f"={q(s12['sheet'], s12['npv_cell'])}"); npv1.number_format = USD0; npv1.font = GREEN_LINK
    ws.cell(row=r, column=13, value=prg1["payback_yrs"]).font = BLUE_INPUT
    risk1 = ws.cell(row=r, column=14, value=f"={q(s16['sheet'], s16['prg1_avg_risk_cell'])}"); risk1.number_format = CUR2; risk1.font = GREEN_LINK
    plat1 = ws.cell(row=r, column=15, value=f"={q(s02['sheet'], s02['num_platforms_cell'])}"); plat1.font = GREEN_LINK
    ws.cell(row=r, column=16, value="+312,000 units/yr (35% customer volume increase)").alignment = LEFT_WRAP
    ws.cell(row=r, column=17, value="Full 33-sheet model (S00-S32); financials, schedule, and risk fully linked").alignment = LEFT_WRAP
    for c in range(1, 18):
        ws.cell(row=r, column=c).border = BORDER_ALL
    prg1_row = r
    r += 1

    # --- PRG-002: Riverside Automation Upgrade Phase I (lighter model — estimate-level financials) ---
    ws.cell(row=r, column=1, value=prg2["program_ref"]).font = BOLD
    ws.cell(row=r, column=2, value=prg2["name"])
    ws.cell(row=r, column=3, value=prg2["sponsor"])
    ws.cell(row=r, column=4, value=prg2["program_manager"])
    ws.cell(row=r, column=5, value=prg2["business_unit"])
    ws.cell(row=r, column=6, value=prg2["phase"])
    stc2 = ws.cell(row=r, column=7, value=prg2["status"])
    stc2.fill = PatternFill("solid", fgColor=_STATUS_FILL.get(prg2["phase_tag_class"], RAG_AMBER))
    capex2 = ws.cell(row=r, column=8,
                      value=f"={q(s02['sheet'], s02['prg2_total_equip_cell'])}+{q(s02['sheet'], s02['prg2_total_install_cell'])}")
    capex2.number_format = USD0
    capex2.font = GREEN_LINK
    cont2 = ws.cell(row=r, column=9, value=f"=H{r}*0.10"); cont2.number_format = USD0
    fx2 = prg2["fx_reserve"]
    nre2 = prg2["nre"]
    bud2 = ws.cell(row=r, column=10, value=f"=H{r}+I{r}+{fx2}+{nre2}"); bud2.number_format = USD0
    irr2 = ws.cell(row=r, column=11, value=prg2["irr"]); irr2.number_format = PCT1; irr2.font = BLUE_INPUT
    npv2 = ws.cell(row=r, column=12, value=prg2["npv"]); npv2.number_format = USD0; npv2.font = BLUE_INPUT
    ws.cell(row=r, column=13, value=prg2["payback_yrs"]).font = BLUE_INPUT
    risk2 = ws.cell(row=r, column=14, value=f"={q(s16['sheet'], s16['prg2_avg_risk_cell'])}"); risk2.number_format = CUR2; risk2.font = GREEN_LINK
    plat2 = ws.cell(row=r, column=15, value=f"=COUNTA({q(s02['sheet'], 'A' + str(s02['prg2_first_row']))}:{q(s02['sheet'], 'A' + str(s02['prg2_last_row']))})")
    plat2.font = GREEN_LINK
    ws.cell(row=r, column=16, value="+18% packaging line throughput (~45,000 cases/day incremental)").alignment = LEFT_WRAP
    ws.cell(row=r, column=17, value="Equipment/supplier/risk data live-linked (S02, S03, S16); IRR/NPV/payback are Finance FEL-2 estimates, not yet a full 10-yr TCO model").alignment = LEFT_WRAP
    for c in range(1, 18):
        ws.cell(row=r, column=c).border = BORDER_ALL
    prg2_row = r
    r += 1

    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "PORTFOLIO TOTALS", 2, 6)
    stats = [
        ("Active + Proposed Programs", f"=COUNTA(A{first_row}:A{last_row})", CUR0),
        ("Total Portfolio CapEx (USD)", f"=SUM(H{first_row}:H{last_row})", USD0),
        ("Total Portfolio Approved/Estimated Budget (USD)", f"=SUM(J{first_row}:J{last_row})", USD0),
        ("Blended Avg Supply Chain Risk Score", f"=AVERAGE(N{first_row}:N{last_row})", CUR2),
        ("Total Equipment Platforms (All Programs)", f"=SUM(O{first_row}:O{last_row})", CUR0),
    ]
    stat_rows = {}
    keys = ["program_count", "total_capex", "total_budget", "blended_risk", "total_platforms"]
    for key, (label, formula, fmt) in zip(keys, stats):
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.number_format = fmt
        c.font = BOLD
        c.border = BORDER_ALL
        stat_rows[key] = row
        row += 1

    autosize(ws, {1: 10, 2: 30, 3: 26, 4: 18, 5: 28, 6: 26, 7: 24, 8: 18, 9: 16, 10: 18, 11: 11,
                  12: 15, 13: 11, 14: 13, 15: 12, 16: 40, 17: 55})
    freeze_below(ws, header_row + 1)

    return {
        "sheet": ws.title,
        "first_row": first_row, "last_row": last_row,
        "prg1_row": prg1_row, "prg2_row": prg2_row,
        "program_count_cell": f"B{stat_rows['program_count']}",
        "total_capex_cell": f"B{stat_rows['total_capex']}",
        "total_budget_cell": f"B{stat_rows['total_budget']}",
        "blended_risk_cell": f"B{stat_rows['blended_risk']}",
        "total_platforms_cell": f"B{stat_rows['total_platforms']}",
    }
