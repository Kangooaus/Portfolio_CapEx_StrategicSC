from gen_common import *

# Supplier, Country, City, EquipRef, Mode, TransitWks, Incoterm, Tier2Visibility, CustomsComplexity
NETWORK = [
    ("Edwards Vacuum", "UK", "Crawley", "EQ-001", "Ocean + Road", 3, "DDP", "Partial", "Moderate — post-Brexit customs"),
    ("Pfeiffer Vacuum", "DE", "Asslar", "EQ-002", "Ocean + Road", 3, "DDP", "Partial", "Low — EU/US standard lanes"),
    ("Thermco Systems", "USA", "Austin, TX", "EQ-003", "Road", 1, "FOB Origin", "Full", "Low — domestic"),
    ("Tokyo Electron Ltd", "JP", "Tokyo", "EQ-004", "Ocean", 4, "DDP", "Partial", "High — JPY invoicing, import duty"),
    ("Brooks Automation", "USA", "Chelmsford, MA", "EQ-005", "Road", 1, "FOB Origin", "Full", "Low — domestic"),
    ("Daifuku", "JP", "Osaka", "EQ-006", "Ocean", 4, "DDP", "Low — custom civil scope", "High — custom project logistics"),
    ("Air Liquide Engineering", "FR", "Frankfurt (hub)", "EQ-007", "Ocean + Road", 3, "DDP", "Partial", "Moderate — hazmat classification"),
    ("Linde Engineering", "DE", "Pullach", "EQ-008", "Ocean + Road", 4, "DDP", "Partial", "Moderate — pressure vessel cert"),
    ("Siemens AG", "DE", "Karlsruhe", "EQ-009", "Ocean + Road", 3, "DDP", "Full", "Low — standard EU/US lanes"),
    ("Inductive Automation", "USA", "Folsom, CA", "EQ-010", "N/A — Software", 0, "N/A", "Full", "None — digital delivery"),
    ("ABB Ltd", "CH", "Zurich", "EQ-011", "Ocean + Road", 3, "DDP", "Full", "Low — standard EU/US lanes"),
    ("Daikin Applied", "JP", "Osaka", "EQ-012", "Ocean", 3, "DDP", "Partial", "High — JPY invoicing, import duty"),
    ("Busch Vacuum", "DE", "Maulburg", "EQ-013", "Ocean + Road", 3, "DDP", "Partial", "Low — EU/US standard lanes"),
    ("Applied Materials", "USA", "Santa Clara, CA", "EQ-014", "Road", 1, "FOB Origin", "Full", "Low — domestic"),
    ("Mobile Industrial Robots (MiR)", "DK", "Odense", "EQ-015", "Ocean + Road", 3, "DDP", "Full", "Moderate — EU export docs"),
]

HEADERS = ["Supplier", "Country", "City / Site", "Equip Ref", "Transport Mode", "Ocean/Intl Transit (wks)",
           "Incoterm", "Tier-2 Sub-Supplier Visibility", "Customs Complexity"]


def build(wb):
    ws = wb.create_sheet("S18_Supply_Chain_Network")
    set_tab_color(ws, 4)
    row = title_block(ws, 4, "S18", "Supply Chain Network Map — Supplier Geography, Routes & Tier-2 Visibility",
                       "Program: Greenfield Expansion Phase II | Owner: Sourabh Tarodekar / Logistics | "
                       "15 suppliers across 5 countries | Feeds S19 Sourcing Pipeline and S14 Cash Flow logistics timing",
                       n_cols=9)
    header_row = write_headers(ws, row, 1, HEADERS, 4)
    first_row = header_row
    r = header_row
    for (sup, country, city, eq, mode, transit, inco, tier2, customs) in NETWORK:
        ws.cell(row=r, column=1, value=sup)
        ws.cell(row=r, column=2, value=country).font = BLUE_INPUT
        ws.cell(row=r, column=3, value=city)
        ws.cell(row=r, column=4, value=eq)
        ws.cell(row=r, column=5, value=mode)
        ws.cell(row=r, column=6, value=transit).font = BLUE_INPUT
        ws.cell(row=r, column=7, value=inco)
        ws.cell(row=r, column=8, value=tier2)
        ws.cell(row=r, column=9, value=customs)
        for c in range(1, 10):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "NETWORK SUMMARY", 2, 4)
    stats = [
        ("Total Suppliers in Network", f"=COUNTA(A{first_row}:A{last_row})", CUR0),
        ("Countries Represented", f"=SUMPRODUCT(1/COUNTIF(B{first_row}:B{last_row},B{first_row}:B{last_row}))", CUR0),
        ("Avg Ocean/International Transit (wks)", f"=AVERAGE(F{first_row}:F{last_row})", CUR2),
        ("Suppliers Requiring Ocean Freight", f'=COUNTIF(E{first_row}:E{last_row},"*Ocean*")', CUR0),
        ("Domestic (Road-Only) Suppliers", f'=COUNTIF(E{first_row}:E{last_row},"Road")', CUR0),
    ]
    for label, formula, fmt in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 28, 2: 8, 3: 16, 4: 10, 5: 16, 6: 16, 7: 12, 8: 24, 9: 32})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
