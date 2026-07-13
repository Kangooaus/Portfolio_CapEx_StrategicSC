from gen_common import *

# Category, Cost Element, Mat Wt(kg), Mat Price(USD/kg), LaborHrs, RateType('shop'/'eng'/None), Subcomp(USD), Notes
ROWS = [
    ("Vacuum Pump System", "Raw Material – Stainless Steel Body", 280, 3.80, 0, None, 0,
     "Precision-cast SS housing; 304SS at market rate"),
    ("Vacuum Pump System", "Machining & Fabrication Labor", 0, 0, 95, "shop", 0,
     "CNC turning & milling; pump body, rotor, stator components"),
    ("Vacuum Pump System", "Purchased Subcomponents – Seals/Bearings", 0, 0, 0, None, 18500,
     "Ceramic bearings, PTFE seals, shaft seals; sourced from FAG/SKF"),
    ("Vacuum Pump System", "Electronics & Motor Drive System", 0, 0, 0, None, 22000,
     "VFD drive, PLC I/O cards, HMI touchscreen, wiring harness"),
    ("Vacuum Pump System", "Assembly Labor", 0, 0, 32, "shop", 0,
     "Final assembly, alignment, internal leak test; 32 hrs per unit"),
    ("Vacuum Pump System", "Quality / Acceptance Testing", 0, 0, 12, "eng", 0,
     "Performance characterization, helium leak test, ultimate pressure verification"),

    ("High-Temp Furnace", "Raw Material – Inconel / Quartz / Refractory", 420, 6.84, 0, None, 0,
     "Inconel 625 hot zone; quartz liner; ceramic refractory bricks"),
    ("High-Temp Furnace", "Machining & Fabrication Labor", 0, 0, 180, "shop", 0,
     "Welding, machining, tube bending; complex multi-zone fabrication"),
    ("High-Temp Furnace", "Purchased Subcomponents – Heating Elements", 0, 0, 0, None, 45000,
     "SiC heating elements, 8-zone; Kanthal A1 backup; sourced from Kanthal"),
    ("High-Temp Furnace", "Electronics & Control Systems", 0, 0, 0, None, 38000,
     "Multi-zone PID controllers, SCR power units, thermocouple arrays"),
    ("High-Temp Furnace", "Assembly Labor", 0, 0, 65, "shop", 0,
     "Zone assembly, insulation packing, wiring, pre-commissioning"),
    ("High-Temp Furnace", "Quality / Acceptance Testing", 0, 0, 20, "eng", 0,
     "Temperature uniformity survey (9-point), ramp rate validation, atmosphere leak test"),

    ("Robotics / Automation", "Raw Material – Aluminum Frame & Structure", 85, 4.20, 0, None, 0,
     "6061 AL structural extrusions, machined joints, end-effector blanks"),
    ("Robotics / Automation", "Machining & Fabrication Labor", 0, 0, 40, "shop", 0,
     "CNC machining of end-effectors, links, flanges; anodizing finish"),
    ("Robotics / Automation", "Purchased Subcomponents – Servo / Drive Train", 0, 0, 0, None, 52000,
     "Harmonic drive reducers, servo motors, encoders; Yaskawa / Nabtesco"),
    ("Robotics / Automation", "Electronics & Vision System", 0, 0, 0, None, 28000,
     "Robot controller, teach pendant, vision camera + lighting, safety scanner"),
    ("Robotics / Automation", "Software & Integration", 0, 0, 35, "eng", 0,
     "MES/SEMI interface SW development, recipe upload, FAT validation scripts"),
    ("Robotics / Automation", "Quality / Acceptance Testing", 0, 0, 10, "eng", 0,
     "Path accuracy, repeatability ±0.05mm, cycle time validation, safety relay test"),

    ("Gas Handling System", "Raw Material – 316L SS Tubing & Fittings", 60, 4.56, 0, None, 0,
     "316L EP-grade tubing, VCR fittings, valves; electropolished internal surfaces"),
    ("Gas Handling System", "Machining & Fabrication Labor", 0, 0, 55, "shop", 0,
     "Tube bending, orbital welding, manifold assembly; cleanroom fabrication"),
    ("Gas Handling System", "Purchased Subcomponents – Valves & Regulators", 0, 0, 0, None, 32000,
     "Swagelok/Parker pneumatic valves, MFCs, pressure regulators, check valves"),
    ("Gas Handling System", "Electronics & Safety Interlock System", 0, 0, 0, None, 18000,
     "Gas detection sensors, PLC safety relays, solenoid driver cards, HMI"),
    ("Gas Handling System", "Assembly & Leak Testing", 0, 0, 28, "shop", 0,
     "Assembly, helium leak test (<1E-9 atm·cc/s), pressure hold test, passivation"),
    ("Gas Handling System", "Quality / Acceptance Testing", 0, 0, 8, "eng", 0,
     "Gas purity validation, flow calibration, emergency shutoff functional test"),

    ("PLC Control System", "Purchased Subcomponents – PLC Hardware", 0, 0, 0, None, 42000,
     "Siemens S7-1500 CPU, I/O cards, power supplies, HMI panel; list price"),
    ("PLC Control System", "Panel Fabrication & Wiring", 0, 0, 45, "shop", 0,
     "Control panel fabrication, DIN rail mounting, cable management, labeling"),
    ("PLC Control System", "Software Development & Programming", 0, 0, 80, "eng", 0,
     "Ladder logic/FBD development, HMI graphics, alarm management, I/O mapping"),
    ("PLC Control System", "Factory Acceptance Testing", 0, 0, 16, "eng", 0,
     "FAT protocol execution, point-to-point I/O check, interlock simulation"),
]

CAT_QUOTE = {
    "Vacuum Pump System": 195000,
    "High-Temp Furnace": 540000,
    "Robotics / Automation": 285000,
    "Gas Handling System": 205000,
    "PLC Control System": 175000,
}

HEADERS = ["Equipment Category", "Cost Element", "Mat. Wt (kg)", "Mat. Price (USD/kg)", "Mat. Cost",
           "Labor Hrs", "Shop Rate", "Labor Cost", "Subcomp/Electronics", "Sub-Total",
           "Overhead (12%)", "Supplier Margin", "TOTAL Cost", "Notes"]


def build(wb, named):
    ws = wb.create_sheet("S04_Should_Cost_Model")
    set_tab_color(ws, 1)
    row = title_block(ws, 1, "S04", "First-Principles Should-Cost Model — Advanced Manufacturing Capital Equipment",
                       "Clean-sheet cost build-up per equipment category | All inputs in BLUE | Formulas in BLACK | Cross-sheet links in GREEN | "
                       "Independent cost estimate used to challenge supplier quotes and identify cost reduction opportunities.",
                       n_cols=14)

    shop_rate = cellref(named, "Fabrication Shop Rate")
    eng_rate = cellref(named, "Engineering Labor Rate")
    margin_hi = cellref(named, "Supplier Margin – High")

    header_row = write_headers(ws, row, 1, HEADERS, 1)
    first_data_row = header_row
    r = header_row
    cat_ranges = {}
    for (cat, elem, wt, price, hrs, rate_type, subcomp, notes) in ROWS:
        cat_ranges.setdefault(cat, [r, r])
        cat_ranges[cat][1] = r
        ws.cell(row=r, column=1, value=cat).font = BLUE_INPUT
        ws.cell(row=r, column=2, value=elem).font = BLUE_INPUT
        ws.cell(row=r, column=3, value=wt).font = BLUE_INPUT
        pc = ws.cell(row=r, column=4, value=price); pc.number_format = USD2; pc.font = BLUE_INPUT
        matcost = ws.cell(row=r, column=5, value=f"=C{r}*D{r}"); matcost.number_format = USD0
        ws.cell(row=r, column=6, value=hrs).font = BLUE_INPUT
        if rate_type == "shop":
            rate_formula = f"={shop_rate}"
        elif rate_type == "eng":
            rate_formula = f"={eng_rate}"
        else:
            rate_formula = 0
        rc = ws.cell(row=r, column=7, value=rate_formula); rc.number_format = USD2
        if rate_type:
            rc.font = GREEN_LINK
        laborcost = ws.cell(row=r, column=8, value=f"=F{r}*G{r}"); laborcost.number_format = USD0
        sc = ws.cell(row=r, column=9, value=subcomp); sc.number_format = USD0
        if subcomp:
            sc.font = BLUE_INPUT
        subtotal = ws.cell(row=r, column=10, value=f"=E{r}+H{r}+I{r}"); subtotal.number_format = USD0
        oh = ws.cell(row=r, column=11, value=f"=J{r}*0.12"); oh.number_format = USD0
        marg = ws.cell(row=r, column=12, value=f"=(J{r}+K{r})*{margin_hi}"); marg.number_format = USD0
        marg.font = GREEN_LINK
        total = ws.cell(row=r, column=13, value=f"=J{r}+K{r}+L{r}"); total.number_format = USD0
        nc = ws.cell(row=r, column=14, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 15):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_data_row = r - 1
    row = r + 1

    row = section_header(ws, row, 1, "SHOULD-COST SUMMARY BY EQUIPMENT CATEGORY", 11, 1)
    sheaders = ["Equipment Category", "Material Cost", "Labor Cost", "Subcomponents", "Sub-Total",
                "Overhead (12%)", "Supplier Margin", "TOTAL Should-Cost", "Supplier Quote (Budget Est.)",
                "Variance (Quote-SC)", "Variance %"]
    row = write_headers(ws, row, 1, sheaders, 1)
    sum_first = row
    for cat, (r0, r1) in cat_ranges.items():
        ws.cell(row=row, column=1, value=cat)
        m = ws.cell(row=row, column=2, value=f"=SUM(E{r0}:E{r1})"); m.number_format = USD0
        l = ws.cell(row=row, column=3, value=f"=SUM(H{r0}:H{r1})"); l.number_format = USD0
        sc = ws.cell(row=row, column=4, value=f"=SUM(I{r0}:I{r1})"); sc.number_format = USD0
        st = ws.cell(row=row, column=5, value=f"=B{row}+C{row}+D{row}"); st.number_format = USD0
        oh = ws.cell(row=row, column=6, value=f"=E{row}*0.12"); oh.number_format = USD0
        mg = ws.cell(row=row, column=7, value=f"=(E{row}+F{row})*{margin_hi}"); mg.number_format = USD0
        tsc = ws.cell(row=row, column=8, value=f"=E{row}+F{row}+G{row}"); tsc.number_format = USD0
        quote = ws.cell(row=row, column=9, value=CAT_QUOTE[cat]); quote.number_format = USD0; quote.font = BLUE_INPUT
        var = ws.cell(row=row, column=10, value=f"=I{row}-H{row}"); var.number_format = USD0
        varpct = ws.cell(row=row, column=11, value=f"=J{row}/H{row}"); varpct.number_format = PCT1
        for c in range(1, 12):
            ws.cell(row=row, column=c).border = BORDER_ALL
        row += 1
    sum_last = row - 1

    ws.cell(row=row, column=1, value="GRAND TOTAL").font = BOLD
    for col, letter in [(2, "B"), (3, "C"), (4, "D"), (5, "E"), (6, "F"), (7, "G"), (8, "H"), (9, "I"), (10, "J")]:
        c = ws.cell(row=row, column=col, value=f"=SUM({letter}{sum_first}:{letter}{sum_last})")
        c.number_format = USD0
        c.font = BOLD
    ws.cell(row=row, column=11, value=f"=J{row}/H{row}").number_format = PCT1
    ws.cell(row=row, column=11).font = BOLD
    for c in range(1, 12):
        ws.cell(row=row, column=c).border = BORDER_ALL
        ws.cell(row=row, column=c).fill = zone_fill_light(1)
    grand_total_row = row

    autosize(ws, {1: 20, 2: 34, 3: 10, 4: 12, 5: 11, 6: 9, 7: 9, 8: 11, 9: 14, 10: 11,
                  11: 12, 12: 12, 13: 12, 14: 46})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title, "grand_total_row": grand_total_row}
