from gen_common import *
import db


HEADERS = ["Equip. ID", "Category", "Tool Type / Model", "Supplier", "Region", "Ccy",
           "Unit Cost (USD)", "Qty", "Total Equip. Cost (USD)", "Install Cost/Unit (USD)",
           "Install Total (USD)", "Life (yrs)", "Energy (kWh/hr)", "Annual Maint. Rate (%)",
           "Throughput (u/hr)", "Op Hrs/Yr", "Annual Energy Cost (USD)", "Engineering Notes", "Program ID"]


def _write_equipment_rows(ws, r, rows, energy_price_cell, program_id):
    """rows: list of dicts from db.list_equipment()."""
    for eq in rows:
        eid, cat, tool, sup = eq["equip_id"], eq["category"], eq["tool_type"], eq["supplier"]
        region, ccy = eq["region"], eq["currency"]
        unit_cost, qty, inst_unit = eq["unit_cost"], eq["qty"], eq["install_cost_unit"]
        life, energy, maint = eq["life_yrs"], eq["energy_kwh_hr"], eq["maint_rate_pct"]
        thr, ophrs, notes = eq["throughput_uhr"], eq["op_hrs_yr"], eq["notes"]
        ws.cell(row=r, column=1, value=eid).font = BLUE_INPUT
        ws.cell(row=r, column=2, value=cat).font = BLUE_INPUT
        ws.cell(row=r, column=3, value=tool).font = BLUE_INPUT
        ws.cell(row=r, column=4, value=sup).font = BLUE_INPUT
        ws.cell(row=r, column=5, value=region).font = BLUE_INPUT
        ws.cell(row=r, column=6, value=ccy).font = BLUE_INPUT
        cuc = ws.cell(row=r, column=7, value=unit_cost); cuc.number_format = USD0; cuc.font = BLUE_INPUT
        cq = ws.cell(row=r, column=8, value=qty); cq.font = BLUE_INPUT
        ctc = ws.cell(row=r, column=9, value=f"=G{r}*H{r}"); ctc.number_format = USD0
        cinst = ws.cell(row=r, column=10, value=inst_unit); cinst.number_format = USD0; cinst.font = BLUE_INPUT
        cinstt = ws.cell(row=r, column=11, value=f"=J{r}*H{r}"); cinstt.number_format = USD0
        cl = ws.cell(row=r, column=12, value=life); cl.font = BLUE_INPUT
        cen = ws.cell(row=r, column=13, value=energy); cen.font = BLUE_INPUT
        cm = ws.cell(row=r, column=14, value=maint); cm.number_format = PCT1; cm.font = BLUE_INPUT
        cth = ws.cell(row=r, column=15, value=thr); cth.font = BLUE_INPUT
        coh = ws.cell(row=r, column=16, value=ophrs); coh.font = BLUE_INPUT
        cec = ws.cell(row=r, column=17, value=f"=M{r}*P{r}*{energy_price_cell}")
        cec.number_format = USD0
        cec.font = GREEN_LINK
        cnotes = ws.cell(row=r, column=18, value=notes)
        cnotes.alignment = LEFT_WRAP
        pid = ws.cell(row=r, column=19, value=program_id)
        pid.font = BLUE_INPUT
        pid.alignment = CENTER
        for c in range(1, 20):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    return r


def build(wb, named):
    ws = wb.create_sheet("S02_Equipment_Portfolio")
    set_tab_color(ws, 1)
    row = title_block(ws, 1, "S02", "CapEx Equipment Portfolio Dataset — Advanced Manufacturing Program",
                       "Fiscal Year: 2025 | Portfolio Director: Sourabh Tarodekar | Status: Active | "
                       "Blue = Hardcoded Input · Black = Formula · Green = Cross-sheet Link | "
                       "Program ID column (right-most) enables portfolio-wide SUMIFS rollups in S33-S35", n_cols=19)

    header_row = write_headers(ws, row, 1, HEADERS, 1)
    first_data_row = header_row
    r = header_row
    energy_price_cell = cellref(named, "Energy Price – Electricity")
    r = _write_equipment_rows(ws, r, db.list_equipment(program_ref="PRG-001"), energy_price_cell, "PRG-001")
    last_data_row = r - 1

    # Totals row (Program 1 — Greenfield Expansion Phase II)
    ws.cell(row=r, column=1, value="PRG-001 TOTAL — Greenfield Expansion Phase II").font = BOLD
    ws.cell(row=r, column=8, value=f"=SUM(H{first_data_row}:H{last_data_row})").font = BOLD
    tot_equip = ws.cell(row=r, column=9, value=f"=SUM(I{first_data_row}:I{last_data_row})")
    tot_equip.number_format = USD0; tot_equip.font = BOLD
    tot_inst = ws.cell(row=r, column=11, value=f"=SUM(K{first_data_row}:K{last_data_row})")
    tot_inst.number_format = USD0; tot_inst.font = BOLD
    tot_energy = ws.cell(row=r, column=17, value=f"=SUM(Q{first_data_row}:Q{last_data_row})")
    tot_energy.number_format = USD0; tot_energy.font = BOLD
    for c in range(1, 20):
        ws.cell(row=r, column=c).border = BORDER_ALL
        ws.cell(row=r, column=c).fill = zone_fill_light(1)
    totals_row = r
    r += 2

    # Portfolio Summary Statistics (Program 1 only — feeds S30 Executive Dashboard)
    row = section_header(ws, r, 1, "PRG-001 SUMMARY STATISTICS — Greenfield Expansion Phase II", 2, 1)
    stats = [
        ("Total Equipment Purchase Cost (USD)", f"=I{totals_row}", USD0),
        ("Total Installation Cost (USD)", f"=K{totals_row}", USD0),
        ("Total Portfolio CapEx (USD)", f"=B{row}+B{row+1}", USD0),
        ("Total Annual Energy Cost (USD)", f"=Q{totals_row}", USD0),
        ("Number of Equipment Platforms", f"=COUNTA(A{first_data_row}:A{last_data_row})", CUR0),
        ("Total Equipment Units", f"=H{totals_row}", CUR0),
        ("Average Unit Cost (USD)", f"=AVERAGE(G{first_data_row}:G{last_data_row})", USD0),
        ("Highest Unit Cost Item (USD)", f"=MAX(G{first_data_row}:G{last_data_row})", USD0),
    ]
    stat_start = row
    for label, formula, fmt in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.number_format = fmt
        c.border = BORDER_ALL
        c.font = BOLD
        row += 1
    row += 1

    # --- Program 2 block: Riverside Automation Upgrade Phase I ---
    row = section_header(ws, row, 1, "PRG-002 EQUIPMENT — Riverside Automation Upgrade Phase I", 19, 1)
    prg2_header_row = write_headers(ws, row, 1, HEADERS, 1)
    prg2_first_row = prg2_header_row
    r = prg2_header_row
    r = _write_equipment_rows(ws, r, db.list_equipment(program_ref="PRG-002"), energy_price_cell, "PRG-002")
    prg2_last_row = r - 1

    ws.cell(row=r, column=1, value="PRG-002 TOTAL — Riverside Automation Upgrade Phase I").font = BOLD
    ws.cell(row=r, column=8, value=f"=SUM(H{prg2_first_row}:H{prg2_last_row})").font = BOLD
    prg2_tot_equip = ws.cell(row=r, column=9, value=f"=SUM(I{prg2_first_row}:I{prg2_last_row})")
    prg2_tot_equip.number_format = USD0; prg2_tot_equip.font = BOLD
    prg2_tot_inst = ws.cell(row=r, column=11, value=f"=SUM(K{prg2_first_row}:K{prg2_last_row})")
    prg2_tot_inst.number_format = USD0; prg2_tot_inst.font = BOLD
    prg2_tot_energy = ws.cell(row=r, column=17, value=f"=SUM(Q{prg2_first_row}:Q{prg2_last_row})")
    prg2_tot_energy.number_format = USD0; prg2_tot_energy.font = BOLD
    for c in range(1, 20):
        ws.cell(row=r, column=c).border = BORDER_ALL
        ws.cell(row=r, column=c).fill = zone_fill_light(1)
    prg2_totals_row = r
    row = r + 2

    autosize(ws, {1: 10, 2: 20, 3: 34, 4: 24, 5: 8, 6: 6, 7: 12, 8: 6, 9: 14, 10: 14,
                  11: 13, 12: 8, 13: 13, 14: 12, 15: 12, 16: 10, 17: 14, 18: 46, 19: 12})
    freeze_below(ws, header_row + 1)

    return {
        "sheet": ws.title,
        "program_id_col": "S",
        "data_first_row": first_data_row,
        "data_last_row": prg2_last_row,
        "first_data_row": first_data_row,
        "last_data_row": last_data_row,
        "totals_row": totals_row,
        "total_equip_cell": f"I{totals_row}",
        "total_install_cell": f"K{totals_row}",
        "total_capex_cell": f"B{stat_start+2}",
        "total_energy_cell": f"Q{totals_row}",
        "num_platforms_cell": f"B{stat_start+4}",
        "total_units_cell": f"B{stat_start+5}",
        "avg_unit_cost_cell": f"B{stat_start+6}",
        "max_unit_cost_cell": f"B{stat_start+7}",
        "prg2_first_row": prg2_first_row,
        "prg2_last_row": prg2_last_row,
        "prg2_totals_row": prg2_totals_row,
        "prg2_total_equip_cell": f"I{prg2_totals_row}",
        "prg2_total_install_cell": f"K{prg2_totals_row}",
        "prg2_total_energy_cell": f"Q{prg2_totals_row}",
    }
