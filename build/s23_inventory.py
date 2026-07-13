from gen_common import *

# PartID, Desc, EqRef, Supplier, Class, MTBF, MTTR, AnnualFailures, SafetyStock, UnitCost, AnnualConsumption, Notes
SPARES = [
    ("SP-001", "Dry Screw Pump Seal Set", "EQ-001", "Edwards Vacuum", "A", 8760, 4, 1, 2, 3200, 2,
     "Seals degrade; annual replacement expected; 2-set safety stock"),
    ("SP-002", "Turbomolecular Pump Bearing", "EQ-002", "Pfeiffer Vacuum", "A", 4380, 8, 2, 2, 8500, 4,
     "CRITICAL — bearing failure = tool down; 2-set stock maintained"),
    ("SP-003", "Turbomolecular Pump Controller", "EQ-002", "Pfeiffer Vacuum", "A", 8760, 16, 1, 1, 12000, 1,
     "Proprietary controller; no drop-in alt; Pfeiffer safety stock commitment"),
    ("SP-004", "Furnace Heating Elements (8-zone set)", "EQ-003", "Thermco Systems", "B", 4380, 6, 2, 2, 4800, 4,
     "Zone element failure predictable; 2-set buffer; 2-4 wk replacement"),
    ("SP-005", "Batch Furnace Process Tube", "EQ-004", "Tokyo Electron Ltd", "B", 8760, 12, 1, 1, 6500, 1,
     "Quartz tube — 12-wk lead time from TEL; must stock 1 spare"),
    ("SP-006", "SCARA Robot Servo Drive", "EQ-005", "Brooks Automation", "B", 8760, 4, 1, 2, 3800, 2,
     "Drive failure low frequency; 2-unit stock adequate"),
    ("SP-007", "Gas Cabinet MFC Assembly", "EQ-007", "Air Liquide Eng.", "A", 4380, 8, 2, 2, 5200, 4,
     "MFC drift = recalibration or replacement; high-use spare"),
    ("SP-008", "DCS CPU Module — S7-1500", "EQ-009", "Siemens AG", "A", 43800, 2, 0.2, 2, 4200, 1,
     "CPU failure rare; 2 on-site + Siemens depot replenishment"),
    ("SP-009", "Chiller Compressor Capacitor Kit", "EQ-012", "Daikin Applied", "C", 8760, 2, 1, 2, 850, 2,
     "Capacitor kit; standard maintenance item; low cost"),
    ("SP-010", "RTP Lamp Array (set of 12)", "EQ-014", "Applied Materials", "A", 4380, 8, 2, 2, 18500, 4,
     "Highest-value spare; AMAT recommends 2-set safety stock; 8-wk LT"),
    ("SP-011", "AMR Battery Pack", "EQ-015", "MiR", "C", 4380, 1, 2, 4, 1200, 8,
     "Battery degradation predictable; 4-pack standard; MiR swap warranty"),
    ("SP-012", "Roots Blower Booster Rotor", "EQ-013", "Busch Vacuum", "B", 8760, 6, 1, 1, 2800, 1,
     "Coordinated with Edwards EQ-001 maintenance schedule"),
]

CONSUMABLES = [
    ("CM-001", "Process N2 Gas (cylinder sets)", "Process Gas", "Air Liquide / Linde", 2, 12, 3, 0.98, 10, 34, 50, 45, 380,
     "High-consumption; order weekly; dual-source reduces stockout risk"),
    ("CM-002", "Quartz Process Tubes (spare)", "Process Consumable", "Heraeus / Shin-Etsu", 6, 0.5, 0.2, 0.99, 4, 7, 6, 8, 2200,
     "Long-lead quartz; 6-wk LT drives high safety stock"),
    ("CM-003", "Photoresist (process grade)", "Process Chemical", "JSR Corporation", 4, 8, 2.5, 0.99, 10, 42, 60, 55, 1800,
     "High-value chemical; 4-wk LT; temperature-controlled storage"),
    ("CM-004", "Argon Gas (bulk, per cylinder)", "Process Gas", "Linde Engineering", 1, 6, 1.5, 0.97, 5, 17, 40, 30, 290,
     "Low risk; Linde on-site contract; auto-replenishment"),
    ("CM-005", "Chemical Mechanical Planarization Slurry", "Process Chemical", "Cabot Microelectronics", 3, 4, 1.5, 0.99, 8, 20, 40, 25, 1500,
     "Specialty chemical; 2 approved sources; shelf life 6 months"),
    ("CM-006", "Cleaning Solvents (IPA, Acetone)", "Facility Chemical", "VWR / Fisher Scientific", 1, 10, 3, 0.95, 8, 18, 80, 65, 45,
     "Commodity; easy dual-source; low-cost; broad availability"),
]

SP_HEADERS = ["Part ID", "Part Description", "Equip Ref", "Supplier", "Class", "MTBF (hrs)", "MTTR (hrs)",
              "Annual Failures (Est.)", "Safety Stock (units)", "Unit Cost (USD)", "Annual Consumption (units)",
              "Inventory Value (USD)", "Annual Carry Cost (20%)", "Downtime Avoidance (hrs/yr)",
              "Annual Downtime Value Avoided (USD/yr)", "Notes"]

CM_HEADERS = ["Item ID", "Item Description", "Category", "Supplier", "Lead Time (wks)", "Avg Weekly Demand (units)",
              "Demand Std Dev", "Service Level Target", "Safety Stock (units)", "Reorder Point (units)",
              "EOQ (units)", "Current Stock", "Unit Cost (USD)", "Inventory Value (USD)", "Notes"]


def build(wb, named):
    ws = wb.create_sheet("S23_Inventory_Buffer_Planning")
    set_tab_color(ws, 4)
    row = title_block(ws, 4, "S23", "Inventory & Buffer Planning — Consumables, Spare Parts & Safety Stock",
                       "Covers production consumables, critical spares (MTBF/MTTR model), and safety stock | Owner: Sourabh Tarodekar | "
                       "Carrying cost = 20% | Production value from S01_Disclaimer_Assumptions", n_cols=16)

    prod_value = cellref(named, "Production Value per Hour")

    row = section_header(ws, row, 1, "SECTION A — CRITICAL SPARE PARTS (MTBF / MTTR MODEL)", 16, 4)
    header_row = write_headers(ws, row, 1, SP_HEADERS, 4)
    first_row = header_row
    r = header_row
    for (pid, desc, eq, sup, cls, mtbf, mttr, fails, ss, cost, cons, notes) in SPARES:
        ws.cell(row=r, column=1, value=pid)
        ws.cell(row=r, column=2, value=desc)
        ws.cell(row=r, column=3, value=eq)
        ws.cell(row=r, column=4, value=sup)
        ws.cell(row=r, column=5, value=cls)
        ws.cell(row=r, column=6, value=mtbf).font = BLUE_INPUT
        ws.cell(row=r, column=7, value=mttr).font = BLUE_INPUT
        ws.cell(row=r, column=8, value=fails).font = BLUE_INPUT
        ws.cell(row=r, column=9, value=ss).font = BLUE_INPUT
        cc = ws.cell(row=r, column=10, value=cost); cc.number_format = USD0; cc.font = BLUE_INPUT
        ws.cell(row=r, column=11, value=cons).font = BLUE_INPUT
        iv = ws.cell(row=r, column=12, value=f"=J{r}*I{r}"); iv.number_format = USD0
        cc2 = ws.cell(row=r, column=13, value=f"=L{r}*0.2"); cc2.number_format = USD0
        dta = ws.cell(row=r, column=14, value=f"=G{r}*H{r}"); dta.number_format = CUR2
        dva = ws.cell(row=r, column=15, value=f"=N{r}*{prod_value}"); dva.number_format = USD0
        nc = ws.cell(row=r, column=16, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 17):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    total_row = r
    ws.cell(row=r, column=1, value="SPARE PARTS TOTAL").font = BOLD
    tc = ws.cell(row=r, column=12, value=f"=SUM(L{first_row}:L{last_row})"); tc.number_format = USD0; tc.font = BOLD
    tc2 = ws.cell(row=r, column=13, value=f"=SUM(M{first_row}:M{last_row})"); tc2.number_format = USD0; tc2.font = BOLD
    for c in range(1, 17):
        ws.cell(row=r, column=c).border = BORDER_ALL
        ws.cell(row=r, column=c).fill = zone_fill_light(4)
    row = r + 2

    row = section_header(ws, row, 1, "SECTION B — PRODUCTION CONSUMABLES & RAW MATERIALS", 15, 4)
    header_row2 = write_headers(ws, row, 1, CM_HEADERS, 4)
    cm_first = row + 1
    r = cm_first
    for (iid, desc, cat, sup, lt, wdem, sd, sl, ss, rop, eoq, cur, cost, notes) in CONSUMABLES:
        ws.cell(row=r, column=1, value=iid)
        ws.cell(row=r, column=2, value=desc)
        ws.cell(row=r, column=3, value=cat)
        ws.cell(row=r, column=4, value=sup)
        ws.cell(row=r, column=5, value=lt).font = BLUE_INPUT
        ws.cell(row=r, column=6, value=wdem).font = BLUE_INPUT
        ws.cell(row=r, column=7, value=sd).font = BLUE_INPUT
        slc = ws.cell(row=r, column=8, value=sl); slc.number_format = PCT1; slc.font = BLUE_INPUT
        ws.cell(row=r, column=9, value=ss).font = BLUE_INPUT
        ws.cell(row=r, column=10, value=rop).font = BLUE_INPUT
        ws.cell(row=r, column=11, value=eoq).font = BLUE_INPUT
        ws.cell(row=r, column=12, value=cur).font = BLUE_INPUT
        cc = ws.cell(row=r, column=13, value=cost); cc.number_format = USD0; cc.font = BLUE_INPUT
        iv = ws.cell(row=r, column=14, value=f"=M{r}*L{r}"); iv.number_format = USD0
        nc = ws.cell(row=r, column=15, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 16):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    cm_last = r - 1
    ws.cell(row=r, column=1, value="CONSUMABLES TOTAL").font = BOLD
    ivt = ws.cell(row=r, column=14, value=f"=SUM(N{cm_first}:N{cm_last})"); ivt.number_format = USD0; ivt.font = BOLD
    for c in range(1, 16):
        ws.cell(row=r, column=c).border = BORDER_ALL
        ws.cell(row=r, column=c).fill = zone_fill_light(4)

    autosize(ws, {1: 8, 2: 30, 3: 9, 4: 20, 5: 7, 6: 10, 7: 9, 8: 8, 9: 10, 10: 10, 11: 12, 12: 12, 13: 13, 14: 12, 15: 14, 16: 46})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title, "spares_total_row": total_row}
