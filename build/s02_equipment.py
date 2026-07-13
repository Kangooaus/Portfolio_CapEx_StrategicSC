from gen_common import *

# Equip ID, Category, Tool Type/Model, Supplier, Region, Currency, Unit Cost, Qty,
# Install Cost/Unit, Lifetime yrs, Energy kWh/hr, Maint Rate %, Throughput u/hr, Op Hrs/Yr, Notes
EQUIPMENT = [
    ("EQ-001", "Vacuum Pump System", "Dry Screw Vacuum Pump – 250 m³/hr", "Edwards Vacuum", "UK", "EUR", 185000, 4, 22000, 12, 18.5, 0.06, 0, 8320,
     "Requires N2 purge line; facility electrical upgrade needed prior to installation"),
    ("EQ-002", "Vacuum Pump System", "Turbomolecular Pump Assembly – 2000 L/s", "Pfeiffer Vacuum", "DE", "EUR", 310000, 3, 28000, 10, 12.0, 0.05, 0, 8320,
     "Single-source supplier; no qualified alt vendor as of Q1-2025; lead time under review"),
    ("EQ-003", "High-Temp Furnace", "Tube Furnace System – 1200°C / 8-zone", "Thermco Systems", "USA", "USD", 520000, 2, 45000, 15, 95.0, 0.04, 24, 8320,
     "FAT to be conducted at supplier site in Austin, TX; includes process recipe transfer"),
    ("EQ-004", "High-Temp Furnace", "Batch Oxidation Furnace – 1100°C", "Tokyo Electron Ltd", "JP", "JPY", 680000, 2, 52000, 15, 110.0, 0.045, 18, 8320,
     "JPY-denominated; FX hedge required; import duty ~3.2%; installation requires crane lift"),
    ("EQ-005", "Robotics / Automation", "6-Axis Wafer Transfer Robot – SCARA", "Brooks Automation", "USA", "USD", 275000, 6, 18000, 10, 4.2, 0.05, 120, 8320,
     "Software integration with fab MES required; vendor to supply integration team on-site"),
    ("EQ-006", "Robotics / Automation", "Overhead Track Conveyor – 50m loop", "Daifuku", "JP", "JPY", 420000, 1, 85000, 12, 22.0, 0.04, 0, 8320,
     "Single installation; civil works for track mounts included in install cost estimate"),
    ("EQ-007", "Gas Handling System", "Process Gas Cabinet – 6-zone manifold", "Air Liquide Engineering", "FR", "EUR", 195000, 4, 32000, 12, 0.8, 0.06, 0, 8320,
     "Hazmat classified; requires local regulatory permit; supplier quote under negotiation"),
    ("EQ-008", "Gas Handling System", "Bulk Gas Storage & Delivery – N2/O2/Ar", "Linde Engineering", "DE", "EUR", 340000, 1, 120000, 20, 2.5, 0.03, 0, 8320,
     "Facility infrastructure tie-in; utility coordination required with site civil team"),
    ("EQ-009", "PLC Control System", "Distributed Control System – Siemens S7-1500", "Siemens AG", "DE", "EUR", 165000, 5, 15000, 10, 1.2, 0.07, 0, 8320,
     "Software license included; annual subscription renewal at $12K/system; cybersecurity review pending"),
    ("EQ-010", "PLC Control System", "SCADA Integration Platform – Ignition", "Inductive Automation", "USA", "USD", 85000, 3, 8000, 8, 0.5, 0.08, 0, 8320,
     "Server hardware separate line item; IT/OT network segmentation required by InfoSec"),
    ("EQ-011", "Facility Infra – Power", "Dry-Type Transformer – 2 MVA / 480V", "ABB Ltd", "CH", "USD", 210000, 2, 35000, 25, 0.0, 0.02, 0, 8760,
     "Component reused from prior program (legacy); refurbishment cost included in install"),
    ("EQ-012", "Facility Infra – Cooling", "Process Chiller System – 200 kW", "Daikin Applied", "JP", "JPY", 295000, 3, 40000, 15, 68.0, 0.05, 0, 8760,
     "Glycol loop design pending; coordinate with mechanical engineering; JPY FX risk noted"),
    ("EQ-013", "Vacuum Pump System", "Roots Blower Booster – 500 m³/hr", "Busch Vacuum", "DE", "EUR", 125000, 6, 14000, 10, 28.0, 0.06, 0, 8320,
     "Paired with EQ-001 dry screw pumps; interdependent installation sequence required"),
    ("EQ-014", "High-Temp Furnace", "RTP – Rapid Thermal Processor", "Applied Materials", "USA", "USD", 875000, 2, 60000, 12, 85.0, 0.04, 32, 8320,
     "Highest unit cost item; finance approval gate required before PO issuance; AR pending"),
    ("EQ-015", "Robotics / Automation", "AMR Fleet – Autonomous Mobile Robots (×10)", "Mobile Industrial Robots (MiR)", "DK", "EUR", 380000, 1, 45000, 8, 6.0, 0.06, 0, 8320,
     "Fleet management software license included; Wi-Fi infrastructure upgrade required"),
]

# Program 2 — Riverside Automation Upgrade Phase I (PRG-002)
EQUIPMENT_PRG2 = [
    ("RV-001", "Robotics / Automation", "Palletizing Robot – 6-Axis, 40kg payload", "Fanuc America", "USA", "USD", 165000, 2, 20000, 10, 3.8, 0.05, 0, 6240,
     "Replaces manual end-of-line palletizing; guarding and safety scanner included in install"),
    ("RV-002", "Packaging Automation", "Case Packer / Cartoning System", "Krones AG", "DE", "EUR", 410000, 1, 55000, 12, 14.0, 0.05, 0, 6240,
     "Single-source specialized cartoning technology; no qualified alt vendor identified"),
    ("RV-003", "Robotics / Automation", "AGV Fleet – Tow/Unit Load (×6)", "Fetch Robotics", "USA", "USD", 85000, 6, 8000, 8, 1.1, 0.06, 0, 6240,
     "Fleet management software license included; warehouse Wi-Fi survey required pre-deployment"),
    ("RV-004", "Quality / Automation", "Vision Inspection System (×3)", "Cognex Corporation", "USA", "USD", 62000, 3, 6000, 8, 0.6, 0.04, 0, 6240,
     "In-line case/label inspection; integrates with existing MES via OPC-UA"),
    ("RV-005", "PLC Control System", "Warehouse Control System Integration", "Rockwell Automation", "USA", "USD", 145000, 1, 25000, 10, 1.0, 0.06, 0, 6240,
     "Integrates AGV fleet, conveyor, and WMS; software license + 1yr support included"),
    ("RV-006", "Material Handling", "Conveyor & Sortation System", "Dematic Corp", "USA", "USD", 520000, 1, 95000, 15, 26.0, 0.04, 0, 6240,
     "Longest lead item; civil floor anchoring required; phased cutover to avoid line downtime"),
]

HEADERS = ["Equip. ID", "Category", "Tool Type / Model", "Supplier", "Region", "Ccy",
           "Unit Cost (USD)", "Qty", "Total Equip. Cost (USD)", "Install Cost/Unit (USD)",
           "Install Total (USD)", "Life (yrs)", "Energy (kWh/hr)", "Annual Maint. Rate (%)",
           "Throughput (u/hr)", "Op Hrs/Yr", "Annual Energy Cost (USD)", "Engineering Notes", "Program ID"]


def _write_equipment_rows(ws, r, rows, energy_price_cell, program_id):
    for eq in rows:
        (eid, cat, tool, sup, region, ccy, unit_cost, qty, inst_unit, life, energy, maint, thr, ophrs, notes) = eq
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
    r = _write_equipment_rows(ws, r, EQUIPMENT, energy_price_cell, "PRG-001")
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
    r = _write_equipment_rows(ws, r, EQUIPMENT_PRG2, energy_price_cell, "PRG-002")
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
