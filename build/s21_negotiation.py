from gen_common import *

# NegID, Supplier, Category, ContractValue, NegType, Start, Close, InitialQuote, InternalTarget, WalkAway, Leverage, BATNA, FinalAgreed, Status
NEGS = [
    ("N-001", "Pfeiffer Vacuum", "TMP Systems (EQ-002)", 930000, "Initial Award", "2024-Q4", "2025-Q1", 975000, 920000, 1000000,
     "Single-source risk acknowledged; Shimadzu qual threat", "Shimadzu TMP-3203L qualification", 930000, "CLOSED"),
    ("N-002", "Thermco Systems", "Tube Furnaces (EQ-003)", 1040000, "Competitive Award", "2024-Q3", "2024-Q4", 1122000, 1030000, 1180000,
     "BTU International valid alt; multi-unit volume", "BTU International — pre-qualified", 1040000, "CLOSED"),
    ("N-003", "Applied Materials", "RTP Tool (EQ-014)", 1750000, "Strategic Negotiation", "2024-Q2", "2025-Q1", 1875000, 1720000, 1900000,
     "Multi-unit commitment (2 units); Phase III expansion signal", "TEL — RTP alternative evaluated", 1750000, "CLOSED"),
    ("N-004", "Brooks Automation", "SCARA Robots (EQ-005)", 1650000, "Competitive Award", "2024-Q3", "2024-Q4", 1745000, 1630000, 1800000,
     "6-unit volume; Kawasaki technical evaluation in parallel", "Kawasaki Robotics — technical eval", 1650000, "CLOSED"),
    ("N-005", "Siemens AG", "DCS Platform (EQ-009)", 825000, "LTA Renewal", "2023-Q4", "2024-Q1", 880000, 810000, 920000,
     "Existing relationship; Phase II expansion commitment; SCADA alt", "Rockwell Automation as alt DCS", 825000, "CLOSED — LTA active"),
    ("N-006", "Air Liquide Eng.", "Gas Cabinets (EQ-007)", None, "Active Negotiation", "2025-Q1", "2025-Q2 target", 840000, 760000, 850000,
     "Matheson Gas RFQ in parallel; hazmat permit dependency", "Matheson Gas — RFQ issued parallel", None, "IN NEGOTIATION"),
    ("N-007", "Linde Engineering", "Bulk Gas (EQ-008)", 340000, "Competitive Award", "2024-Q4", "2025-Q1", 362000, 330000, 380000,
     "Existing site contract leverage; 32-wk LT accepted", "Air Products — RFQ issued", 340000, "CLOSED"),
    ("N-008", "Edwards Vacuum", "Dry Screw Pumps (EQ-001)", 740000, "Competitive — Dual Source", "2024-Q4", "2025-Q1", 788000, 725000, 810000,
     "Busch as dual-source alt; volume split threat", "Busch Vacuum — already qualified", 740000, "CLOSED"),
    ("N-009", "Daikin Applied", "Process Chillers (EQ-012)", 885000, "Competitive Award", "2024-Q4", "2025-Q1", 926000, 870000, 950000,
     "Carrier as competitive alt; glycol loop specification leverage", "Carrier Corporation", 885000, "CLOSED"),
    ("N-010", "Mobile Industrial Robots", "AMR Fleet (EQ-015)", 380000, "Competitive Award", "2024-Q4", "2025-Q1", 404000, 370000, 420000,
     "Locus Robotics and Omron in parallel eval; fleet SW requirement", "Omron AMR — evaluated but lower capability", 380000, "CLOSED"),
]

HEADERS = ["Neg ID", "Supplier", "Category", "Contract Value", "Neg Type", "Start", "Close",
           "Initial Quote (USD)", "Internal Target (USD)", "Walk-Away (USD)", "Key Leverage", "BATNA",
           "Final Agreed (USD)", "Savings (USD)", "Savings %", "Status"]


def build(wb):
    ws = wb.create_sheet("S21_Negotiation_Tracker")
    set_tab_color(ws, 4)
    row = title_block(ws, 4, "S21", "Negotiation Tracker — Commercial Negotiation Log & Savings Portfolio",
                       "Tracks all active and completed negotiations | Owner: Sourabh Tarodekar | "
                       "BATNA = Best Alternative to Negotiated Agreement | Feeds S19 Strategic Sourcing Pipeline",
                       n_cols=16)
    header_row = write_headers(ws, row, 1, HEADERS, 4)
    first_row = header_row
    r = header_row
    for (nid, sup, cat, cv, ntype, start, close, iq, it, wa, lev, batna, final, status) in NEGS:
        ws.cell(row=r, column=1, value=nid)
        ws.cell(row=r, column=2, value=sup)
        ws.cell(row=r, column=3, value=cat)
        cvc = ws.cell(row=r, column=4, value=cv if cv else "TBC (target)")
        if cv:
            cvc.number_format = USD0
        ws.cell(row=r, column=5, value=ntype)
        ws.cell(row=r, column=6, value=start)
        ws.cell(row=r, column=7, value=close)
        iqc = ws.cell(row=r, column=8, value=iq); iqc.number_format = USD0; iqc.font = BLUE_INPUT
        itc = ws.cell(row=r, column=9, value=it); itc.number_format = USD0; itc.font = BLUE_INPUT
        wac = ws.cell(row=r, column=10, value=wa); wac.number_format = USD0; wac.font = BLUE_INPUT
        ws.cell(row=r, column=11, value=lev).alignment = LEFT_WRAP
        ws.cell(row=r, column=12, value=batna).alignment = LEFT_WRAP
        if final:
            fc = ws.cell(row=r, column=13, value=final); fc.number_format = USD0; fc.font = BLUE_INPUT
            sav = ws.cell(row=r, column=14, value=f"=H{r}-M{r}"); sav.number_format = USD0
            savpct = ws.cell(row=r, column=15, value=f"=N{r}/H{r}"); savpct.number_format = PCT1
        else:
            ws.cell(row=r, column=13, value="TBC")
            ws.cell(row=r, column=14, value="TBC")
            ws.cell(row=r, column=15, value="TBC")
        stc = ws.cell(row=r, column=16, value=status)
        stc.fill = PatternFill("solid", fgColor=RAG_GREEN if "CLOSED" in status else RAG_AMBER)
        for c in range(1, 17):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "SAVINGS PORTFOLIO SUMMARY", 2, 4)
    stats = [
        ("Total Negotiations Logged", f"=COUNTA(A{first_row}:A{last_row})", CUR0),
        ("Closed Negotiations", f'=COUNTIF(P{first_row}:P{last_row},"CLOSED")+COUNTIF(P{first_row}:P{last_row},"CLOSED — LTA active")', CUR0),
        ("Total Confirmed Savings (Closed Negotiations, USD)",
         f'=SUMIF(P{first_row}:P{last_row},"CLOSED",N{first_row}:N{last_row})+SUMIF(P{first_row}:P{last_row},"CLOSED — LTA active",N{first_row}:N{last_row})', USD0),
        ("Average Savings % (vs Initial Quote, Closed Only)",
         f'=AVERAGEIF(P{first_row}:P{last_row},"CLOSED",O{first_row}:O{last_row})', PCT1),
    ]
    for label, formula, fmt in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 8, 2: 20, 3: 20, 4: 13, 5: 20, 6: 10, 7: 14, 8: 13, 9: 14, 10: 13, 11: 34, 12: 30, 13: 13, 14: 12, 15: 10, 16: 18})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
