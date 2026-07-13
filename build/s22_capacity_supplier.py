from gen_common import *

# EqRef, Supplier, Component, AnnualCapacity, ProgramVolReq, ConstraintRisk, LeadTimeAddl, FlexCap, MOQ, OrderFreq, SafetyStockWks, BufferRec, Notes
ROWS = [
    ("EQ-001", "Edwards Vacuum", "Dry Screw Vacuum Pumps", 120, 4, "LOW", 16, 20, 1, "Per program", 8, "2-unit buffer on-site",
     "Edwards produces ~120 units/yr globally; 4 units = low concentration"),
    ("EQ-002", "Pfeiffer Vacuum", "Turbomolecular Pumps", 60, 3, "HIGH", 18, 10, 1, "Per program", 12, "2-unit safety stock critical",
     "Pfeiffer TMP production ~60 units/yr globally; 3 units = 5% of output. Supply constraint at volume. Alt qualification essential."),
    ("EQ-003", "Thermco Systems", "High-Temp Tube Furnaces", 45, 2, "LOW-MOD", 20, 8, 1, "Per program", 10, "1 spare hot-zone set",
     "Thermco capacity adequate; BTU alt available"),
    ("EQ-004", "Tokyo Electron Ltd", "Batch Oxidation Furnaces", 150, 2, "LOW", 24, 15, 1, "Per program", 14, "Coordinated with TEL FSE",
     "TEL large OEM; 2 units = minimal fraction of global capacity"),
    ("EQ-005", "Brooks Automation", "SCARA Robots", 800, 6, "VERY LOW", 12, 50, 2, "Per program", 6, "Standard stock level",
     "Brooks Automation high-volume producer; 6 units trivial"),
    ("EQ-006", "Daifuku", "Overhead Track Conveyor", 25, 1, "MOD — custom design", 30, 5, 1, "Per project", 0, "No standard buffer — custom",
     "Each Daifuku conveyor is a custom civil project; capacity = design+install bandwidth, not inventory"),
    ("EQ-007", "Air Liquide Eng.", "Process Gas Cabinets", 200, 4, "LOW", 16, 20, 1, "Per program", 8, "1 spare manifold assembly",
     "Air Liquide Eng. large manufacturer; 4 units = low share"),
    ("EQ-008", "Linde Engineering", "Bulk Gas Storage Vessels", 80, 1, "LOW", 28, 5, 1, "Per program", 0, "Long-lead only — no buffer",
     "Vessel is bespoke; 32-wk LT is design/fabrication not inventory"),
    ("EQ-009", "Siemens AG", "DCS PLC S7-1500", 50000, 5, "VERY LOW", 10, 500, 5, "Annual blanket", 12, "Standard depot stock — Siemens USA",
     "Mass-manufactured; 5 units = negligible supply risk"),
    ("EQ-010", "Inductive Automation", "SCADA Software Licenses", None, 3, "VERY LOW", 0, None, 1, "On demand", 0, "Software — no physical buffer needed",
     "SaaS-adjacent model; license delivery instantaneous"),
    ("EQ-011", "ABB Ltd", "Dry-Type Transformers", 300, 2, "LOW", 18, 10, 1, "Per program", 0, "Long-lead; no buffer practical",
     "ABB large transformer OEM; 2 units = negligible share"),
    ("EQ-012", "Daikin Applied", "Process Chiller Systems", 400, 3, "LOW", 18, 15, 1, "Per program", 6, "Standard refrigerant spares kit",
     "Daikin Applied large US/JP manufacturer; low concentration"),
    ("EQ-013", "Busch Vacuum", "Roots Blower Boosters", 250, 6, "LOW", 14, 20, 1, "Per program", 8, "2-unit buffer coordinated with EQ-001",
     "Busch high-volume vacuum manufacturer; 6 units = low share"),
    ("EQ-014", "Applied Materials", "RTP Tools", 40, 2, "MOD-HIGH", 24, 5, 1, "Per program", 0, "No buffer — high-value; 30% deposit commitment",
     "AMAT RTP production limited; 2 units = notable share. Finance pre-approval required."),
    ("EQ-015", "Mobile Industrial Robots", "AMR Fleet (x10 robots)", 5000, 10, "VERY LOW", 14, 100, 10, "Per program", 0, "Standard warranty + software update coverage",
     "MiR high-volume AMR producer; 10 units negligible"),
]

HEADERS = ["Equip Ref", "Supplier", "Component", "Est. Supplier Annual Capacity (units/yr)",
           "Program Volume Required (units/yr)", "% of Supplier Capacity Consumed", "Capacity Constraint Risk",
           "Lead Time to Add'l Capacity (wks)", "Flex Capacity Available (units)", "MOQ", "Order Frequency",
           "Safety Stock Coverage (wks)", "Buffer Recommendation", "Notes"]


def build(wb):
    ws = wb.create_sheet("S22_Capacity_Supplier_Facing")
    set_tab_color(ws, 4)
    row = title_block(ws, 4, "S22", "Supplier Capacity Assessment — Program Demand vs Supplier Available Capacity",
                       "Identifies capacity concentration risk at supplier level | Owner: Sourabh Tarodekar | "
                       "Complements S10 Capacity Planning (equipment-side view) with a supply-side capacity view",
                       n_cols=14)
    header_row = write_headers(ws, row, 1, HEADERS, 4)
    first_row = header_row
    r = header_row
    for (eq, sup, comp, cap, vol, risk, lt, flex, moq, freq, sscov, buf, notes) in ROWS:
        ws.cell(row=r, column=1, value=eq)
        ws.cell(row=r, column=2, value=sup)
        ws.cell(row=r, column=3, value=comp)
        cc = ws.cell(row=r, column=4, value=cap if cap else "Unlimited (SaaS)")
        if cap:
            cc.number_format = CUR0
            cc.font = BLUE_INPUT
        vc = ws.cell(row=r, column=5, value=vol); vc.font = BLUE_INPUT
        if cap:
            pc = ws.cell(row=r, column=6, value=f"=E{r}/D{r}")
            pc.number_format = PCT1
        else:
            ws.cell(row=r, column=6, value="N/A")
        rc = ws.cell(row=r, column=7, value=risk)
        f = rag_fill(risk)
        if f:
            rc.fill = f
        ws.cell(row=r, column=8, value=lt).font = BLUE_INPUT
        ws.cell(row=r, column=9, value=flex if flex else "N/A")
        ws.cell(row=r, column=10, value=moq).font = BLUE_INPUT
        ws.cell(row=r, column=11, value=freq)
        ws.cell(row=r, column=12, value=sscov)
        ws.cell(row=r, column=13, value=buf).alignment = LEFT_WRAP
        nc = ws.cell(row=r, column=14, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 15):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1

    autosize(ws, {1: 9, 2: 22, 3: 26, 4: 16, 5: 14, 6: 14, 7: 20, 8: 13, 9: 14, 10: 7, 11: 14, 12: 14, 13: 26, 14: 48})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
