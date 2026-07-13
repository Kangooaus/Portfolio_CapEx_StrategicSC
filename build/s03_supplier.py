from gen_common import *
import db

HEADERS = ["Supplier", "Component Type", "Equip. Ref", "Region", "Ccy", "Std LT (wks)",
           "Current LT (wks)", "LT Delta (wks)", "Reliability (0-100)", "Single Source Risk",
           "Alt Supplier Available", "Calc. Risk Score", "Risk Tier", "Engineering Notes", "Program ID"]


def _write_supplier_rows(ws, r, rows, program_id):
    """rows: list of dicts from db.list_suppliers()."""
    for s in rows:
        sup, comp, eqref = s["supplier_name"], s["component_type"], s["equip_ref"]
        region, ccy = s["region"], s["currency"]
        stdlt, curlt, rel = s["std_lt_wks"], s["current_lt_wks"], s["reliability"]
        single = s["single_source"]
        alt = s["alt_supplier_available"]
        notes = s["notes"]
        ws.cell(row=r, column=1, value=sup).font = BLUE_INPUT
        ws.cell(row=r, column=2, value=comp).font = BLUE_INPUT
        ws.cell(row=r, column=3, value=eqref).font = BLUE_INPUT
        ws.cell(row=r, column=4, value=region).font = BLUE_INPUT
        ws.cell(row=r, column=5, value=ccy).font = BLUE_INPUT
        ws.cell(row=r, column=6, value=stdlt).font = BLUE_INPUT
        ws.cell(row=r, column=7, value=curlt).font = BLUE_INPUT
        ws.cell(row=r, column=8, value=f"=G{r}-F{r}")
        ws.cell(row=r, column=9, value=rel).font = BLUE_INPUT
        ws.cell(row=r, column=10, value=single).font = BLUE_INPUT
        ws.cell(row=r, column=11, value=alt).font = BLUE_INPUT
        risk = ws.cell(row=r, column=12, value=f"=ROUND((G{r}/F{r})*(100-I{r}),2)")
        risk.number_format = CUR2
        ws.cell(row=r, column=13, value=f'=IF(L{r}>15,"HIGH",IF(L{r}>=5,"MODERATE","LOW"))')
        notes_c = ws.cell(row=r, column=14, value=notes)
        notes_c.alignment = LEFT_WRAP
        pid = ws.cell(row=r, column=15, value=program_id)
        pid.font = BLUE_INPUT
        pid.alignment = CENTER
        for c in range(1, 16):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    return r


def build(wb):
    ws = wb.create_sheet("S03_Supplier_Dataset")
    set_tab_color(ws, 1)
    row = title_block(ws, 1, "S03", "Supplier & Supply Chain Dataset — Advanced Manufacturing CapEx Program",
                       "Last Updated: 2025-Q3 | Owner: Supply Chain / Sourcing Team | "
                       "Risk Score = (Current LT ÷ Standard LT) × (100 − Reliability Score)  |  Risk Tier: LOW < 5 | MODERATE 5–15 | HIGH > 15 | "
                       "Program ID column enables portfolio-wide rollups",
                       n_cols=15)
    header_row = write_headers(ws, row, 1, HEADERS, 1)
    first_data_row = header_row
    r = header_row
    r = _write_supplier_rows(ws, r, db.list_suppliers(program_ref="PRG-001"), "PRG-001")
    last_data_row = r - 1

    row = r + 1
    row = section_header(ws, row, 1, "PRG-001 SUPPLY CHAIN RISK SUMMARY — Greenfield Expansion Phase II", 2, 1)
    stats = [
        ("Avg Standard Lead Time (wks)", f"=AVERAGE(F{first_data_row}:F{last_data_row})", CUR2),
        ("Avg Current Lead Time (wks)", f"=AVERAGE(G{first_data_row}:G{last_data_row})", CUR2),
        ("Avg Lead Time Delta (wks)", f"=AVERAGE(H{first_data_row}:H{last_data_row})", CUR2),
        ("Avg Reliability Score (0-100)", f"=AVERAGE(I{first_data_row}:I{last_data_row})", CUR2),
        ("Avg Calculated Risk Score", f"=AVERAGE(L{first_data_row}:L{last_data_row})", CUR2),
        ("Max Risk Score (Worst Supplier)", f"=MAX(L{first_data_row}:L{last_data_row})", CUR2),
        ("# Single-Source Components", f'=COUNTIF(J{first_data_row}:J{last_data_row},"Yes")', CUR0),
        ("# Components with Alt Supplier", f'=COUNTIF(K{first_data_row}:K{last_data_row},"Yes")', CUR0),
        ("# HIGH Risk Tier Suppliers", f'=COUNTIF(M{first_data_row}:M{last_data_row},"HIGH")', CUR0),
    ]
    stat_start = row
    for label, formula, fmt in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.number_format = fmt
        c.font = BOLD
        c.border = BORDER_ALL
        row += 1
    row += 1

    # --- Program 2 block ---
    row = section_header(ws, row, 1, "PRG-002 SUPPLIERS — Riverside Automation Upgrade Phase I", 15, 1)
    prg2_header_row = write_headers(ws, row, 1, HEADERS, 1)
    prg2_first_row = prg2_header_row
    r = prg2_header_row
    r = _write_supplier_rows(ws, r, db.list_suppliers(program_ref="PRG-002"), "PRG-002")
    prg2_last_row = r - 1
    row = r + 1

    row = section_header(ws, row, 1, "PRG-002 SUPPLY CHAIN RISK SUMMARY — Riverside Automation Upgrade Phase I", 2, 1)
    prg2_stats = [
        ("Avg Calculated Risk Score", f"=AVERAGE(L{prg2_first_row}:L{prg2_last_row})", CUR2),
        ("Max Risk Score (Worst Supplier)", f"=MAX(L{prg2_first_row}:L{prg2_last_row})", CUR2),
        ("# Single-Source Components", f'=COUNTIF(J{prg2_first_row}:J{prg2_last_row},"Yes")', CUR0),
        ("# HIGH Risk Tier Suppliers", f'=COUNTIF(M{prg2_first_row}:M{prg2_last_row},"HIGH")', CUR0),
    ]
    prg2_stat_start = row
    for label, formula, fmt in prg2_stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.number_format = fmt
        c.font = BOLD
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 26, 2: 24, 3: 10, 4: 8, 5: 6, 6: 10, 7: 11, 8: 10, 9: 12, 10: 12, 11: 12, 12: 12, 13: 11, 14: 50, 15: 12})
    freeze_below(ws, header_row + 1)

    return {
        "sheet": ws.title,
        "program_id_col": "O",
        "first_data_row": first_data_row,
        "last_data_row": last_data_row,
        "avg_std_lt": f"B{stat_start}",
        "avg_cur_lt": f"B{stat_start+1}",
        "avg_lt_delta": f"B{stat_start+2}",
        "avg_reliability": f"B{stat_start+3}",
        "avg_risk_score": f"B{stat_start+4}",
        "max_risk_score": f"B{stat_start+5}",
        "single_source_count": f"B{stat_start+6}",
        "alt_supplier_count": f"B{stat_start+7}",
        "high_risk_count": f"B{stat_start+8}",
        "prg2_first_row": prg2_first_row,
        "prg2_last_row": prg2_last_row,
        "prg2_avg_risk_score": f"B{prg2_stat_start}",
        "prg2_max_risk_score": f"B{prg2_stat_start+1}",
        "prg2_single_source_count": f"B{prg2_stat_start+2}",
        "prg2_high_risk_count": f"B{prg2_stat_start+3}",
    }
