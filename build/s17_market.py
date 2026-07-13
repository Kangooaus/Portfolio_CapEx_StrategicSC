from gen_common import *

# Commodity, #Suppliers Global, Top3 Share%, HHI, PriceTrend12mo, LeadTimeTrend, KeyRisk
COMMODITIES = [
    ("Vacuum Pumps (Turbo/Dry Screw)", 6, 0.72, 2450, "+4.2%", "Extending", "Pfeiffer/Edwards/Busch concentration; semiconductor demand surge"),
    ("High-Temp Furnace Systems", 5, 0.81, 3100, "+6.8%", "Extending", "TEL/Thermco/Kokusai oligopoly; long qualification cycles limit new entrants"),
    ("Precision Robotics (SCARA/6-axis)", 8, 0.65, 1980, "+2.1%", "Stable", "Brooks/Yaskawa/Fanuc/Kawasaki competitive field; servo chip shortage easing"),
    ("Process Gas Handling Systems", 7, 0.58, 1620, "+3.5%", "Extending", "Air Liquide/Linde/Matheson; hazmat regulatory burden raises entry barriers"),
    ("PLC / DCS Control Systems", 4, 0.85, 3400, "+1.8%", "Stable", "Siemens/Rockwell/ABB/Schneider dominate; software licensing model shift"),
    ("Facility Power Infrastructure (Transformers)", 9, 0.52, 1340, "+8.5%", "Extending", "Grid-scale transformer demand surge (data centers); 18-24mo lead times industry-wide"),
    ("Industrial Chillers / Cooling", 6, 0.61, 1710, "+3.0%", "Stable", "Daikin/Trane/Carrier; refrigerant transition (R-454B) driving redesigns"),
    ("Mobile Robotics (AMR Fleets)", 10, 0.48, 1120, "-2.5%", "Improving", "MiR/Locus/Omron/Fetch; maturing market with price competition intensifying"),
]

HEADERS = ["Commodity / Category", "# Global Suppliers", "Top-3 Market Share (%)", "HHI (Concentration Index)",
           "12-Mo Price Trend", "Lead Time Trend", "Key Market Risk / Notes"]


def build(wb):
    ws = wb.create_sheet("S17_Supply_Market_Analysis")
    set_tab_color(ws, 4)
    row = title_block(ws, 4, "S17", "Supply Market Structure Analysis — Commodity Concentration & Pricing",
                       "Program: Greenfield Expansion Phase II | Owner: Sourabh Tarodekar / Strategic Sourcing | "
                       "HHI = Herfindahl-Hirschman Index (sum of squared market shares x10,000) | HHI > 2500 = highly concentrated market",
                       n_cols=7)
    header_row = write_headers(ws, row, 1, HEADERS, 4)
    first_row = header_row
    r = header_row
    for (name, nsup, top3, hhi, ptrend, lttrend, notes) in COMMODITIES:
        ws.cell(row=r, column=1, value=name)
        ws.cell(row=r, column=2, value=nsup).font = BLUE_INPUT
        c3 = ws.cell(row=r, column=3, value=top3); c3.number_format = PCT1; c3.font = BLUE_INPUT
        c4 = ws.cell(row=r, column=4, value=hhi); c4.font = BLUE_INPUT
        f = None
        if hhi > 2500:
            f = PatternFill("solid", fgColor=RAG_RED)
        elif hhi > 1500:
            f = PatternFill("solid", fgColor=RAG_AMBER)
        else:
            f = PatternFill("solid", fgColor=RAG_GREEN)
        c4.fill = f
        ws.cell(row=r, column=5, value=ptrend)
        ws.cell(row=r, column=6, value=lttrend)
        nc = ws.cell(row=r, column=7, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 8):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "MARKET INTELLIGENCE SUMMARY", 2, 4)
    stats = [
        ("Commodities Tracked", f"=COUNTA(A{first_row}:A{last_row})"),
        ("Avg HHI (Portfolio Commodities)", f"=AVERAGE(D{first_row}:D{last_row})"),
        ("Highly Concentrated Markets (HHI>2500)", f'=COUNTIF(D{first_row}:D{last_row},">2500")'),
        ("Avg Top-3 Market Share", f"=AVERAGE(C{first_row}:C{last_row})"),
    ]
    fmts = [CUR0, CUR0, CUR0, PCT1]
    for (label, formula), fmt in zip(stats, fmts):
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 34, 2: 14, 3: 16, 4: 14, 5: 14, 6: 13, 7: 55})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
