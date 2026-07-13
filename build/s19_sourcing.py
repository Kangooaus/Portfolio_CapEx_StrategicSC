from gen_common import *

# Category, EquipRef, FEL Phase, RFI Date, RFQ Date, Award Date, Suppliers Bid, Awarded Supplier, Savings vs Budget(USD), Status
PIPELINE = [
    ("Vacuum Pump Systems", "EQ-001/002/013", "FEL-3", "2024-09-15", "2024-10-15", "2025-01-15", 4, "Edwards / Pfeiffer / Busch", 93000, "AWARDED"),
    ("High-Temp Furnace Systems", "EQ-003/004/014", "FEL-3", "2024-08-01", "2024-09-01", "2025-01-01", 3, "Thermco / TEL / AMAT", 207000, "AWARDED"),
    ("Robotics & Automation", "EQ-005/006/015", "FEL-3", "2024-09-01", "2024-10-01", "2025-01-01", 4, "Brooks / Daifuku / MiR", 119000, "AWARDED"),
    ("Gas Handling Systems", "EQ-007/008", "FEL-2", "2024-10-01", "2024-11-15", "2025-02-15 (target)", 3, "Air Liquide (pending) / Linde", 22000, "IN NEGOTIATION"),
    ("PLC / Control Systems", "EQ-009/010", "FEL-3", "2024-08-15", "2024-09-15", "2024-12-15", 3, "Siemens / Inductive Automation", 55000, "AWARDED"),
    ("Facility Infrastructure — Power", "EQ-011", "FEL-3", "2024-09-01", "2024-10-01", "2025-01-01", 2, "ABB Ltd", 0, "AWARDED"),
    ("Facility Infrastructure — Cooling", "EQ-012", "FEL-3", "2024-09-15", "2024-10-15", "2025-01-15", 3, "Daikin Applied", 41000, "AWARDED"),
    ("Spare Parts & Consumables", "S23 register", "FEL-2", "2025-01-15", "2025-02-15", "2025-04-01 (target)", 5, "Multiple", 0, "IN PROGRESS"),
    ("Field Service Contracts", "All platforms", "FEL-1", "2025-02-01", "2025-03-01 (target)", "TBD", None, "TBD", 0, "PLANNED"),
    ("Alt-Source Qualification — TMP", "EQ-002", "FEL-2", "2025-02-01", "2025-03-01", "2025-06-01 (target)", 1, "Shimadzu (qualifying)", 0, "IN QUALIFICATION"),
    ("Alt-Source Qualification — Gas Cabinet", "EQ-007", "FEL-1", "2025-03-01", "TBD", "TBD", 1, "Matheson Gas (RFQ issued)", 0, "RFQ ISSUED"),
    ("IT/OT Network Infrastructure", "EQ-009/010 DMZ", "FEL-2", "2025-04-15", "2025-05-01", "2025-06-01 (target)", 3, "TBD", 0, "IN PROGRESS"),
]

HEADERS = ["Sourcing Category", "Equipment Ref", "FEL Phase", "RFI Date", "RFQ Date", "Award Date",
           "# Suppliers Bid", "Awarded / Leading Supplier", "Savings vs Budget (USD)", "Status"]


def build(wb):
    ws = wb.create_sheet("S19_Strategic_Sourcing_Pipeline")
    set_tab_color(ws, 4)
    row = title_block(ws, 4, "S19", "Strategic Sourcing Pipeline — RFI to Award, Contract Status & Savings",
                       "Program: Greenfield Expansion Phase II | Owner: Sourabh Tarodekar / Strategic Sourcing | "
                       "FEL = Front-End Loading (1=Concept, 2=Feasibility, 3=Definition) | 12 sourcing categories tracked",
                       n_cols=10)
    header_row = write_headers(ws, row, 1, HEADERS, 4)
    first_row = header_row
    r = header_row
    for (cat, eq, fel, rfi, rfq, award, nbid, sup, sav, status) in PIPELINE:
        ws.cell(row=r, column=1, value=cat)
        ws.cell(row=r, column=2, value=eq)
        ws.cell(row=r, column=3, value=fel)
        ws.cell(row=r, column=4, value=rfi)
        ws.cell(row=r, column=5, value=rfq)
        ws.cell(row=r, column=6, value=award)
        ws.cell(row=r, column=7, value=nbid if nbid else "—")
        ws.cell(row=r, column=8, value=sup)
        sc = ws.cell(row=r, column=9, value=sav); sc.number_format = USD0; sc.font = BLUE_INPUT
        stc = ws.cell(row=r, column=10, value=status)
        if status == "AWARDED":
            stc.fill = PatternFill("solid", fgColor=RAG_GREEN)
        elif status in ("IN NEGOTIATION", "IN PROGRESS", "IN QUALIFICATION", "RFQ ISSUED"):
            stc.fill = PatternFill("solid", fgColor=RAG_AMBER)
        else:
            stc.fill = PatternFill("solid", fgColor="F2F2F2")
        for c in range(1, 11):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "SOURCING PIPELINE SUMMARY", 2, 4)
    stats = [
        ("Total Sourcing Categories", f"=COUNTA(A{first_row}:A{last_row})", CUR0),
        ("Categories Awarded", f'=COUNTIF(J{first_row}:J{last_row},"AWARDED")', CUR0),
        ("Categories In Progress / Negotiation", f'=COUNTA(A{first_row}:A{last_row})-COUNTIF(J{first_row}:J{last_row},"AWARDED")', CUR0),
        ("Total Savings vs Budget (USD)", f"=SUM(I{first_row}:I{last_row})", USD0),
        ("Avg Suppliers Bid per Category", f"=AVERAGE(G{first_row}:G{last_row})", CUR2),
    ]
    for label, formula, fmt in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 28, 2: 16, 3: 9, 4: 12, 5: 12, 6: 16, 7: 11, 8: 30, 9: 15, 10: 16})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
