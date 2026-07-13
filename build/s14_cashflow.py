from gen_common import *

# Month, Equip Purchases, Install&Comm, Facility Infra&FX, NRE/Eng, Quarter, Milestone, Notes
MONTHLY = [
    ("Apr-25", 3312500, 0, 512000, 122500, "Q2-2025", "G1: AR approved; long-lead POs placed",
     "Deposits: EQ-001/2/3/5/9/11/13/14/15; hazmat permit submitted"),
    ("May-25", 412500, 0, 431000, 97500, "Q2-2025", "EQ-004/006/012 deposits; civil works begin",
     "TEL furnace + Daifuku conveyor + Daikin chiller deposits"),
    ("Jun-25", 660000, 78000, 283000, 95000, "Q2-2025", "EQ-005 milestone; robot FAT prep",
     "Brooks SCARA manufacturing milestone payment"),
    ("Jul-25", 948000, 138000, 227000, 90000, "Q3-2025", "EQ-001/009/013 milestones; electrical infra",
     "Pump + DCS milestones; electrical feeds energized"),
    ("Aug-25", 1168000, 207000, 252000, 85000, "Q3-2025", "EQ-003/011 milestones; cooling loop",
     "Thermco furnace + ABB transformer manufacturing milestone"),
    ("Sep-25", 700000, 258000, 305000, 80000, "Q3-2025", "EQ-007/015 milestones; hazmat permit rcvd",
     "Air Liquide gas + MiR AMR milestones; permit closes"),
    ("Oct-25", 912500, 323000, 250000, 75000, "Q4-2025", "EQ-014 milestone; deliveries begin",
     "AMAT RTP manufacturing milestone; EUR equipment deliveries"),
    ("Nov-25", 577500, 353000, 230000, 70000, "Q4-2025", "EQ-001/009/013 deliveries; installation peak",
     "Pump sets + DCS delivered; mechanical installation begins"),
    ("Dec-25", 637000, 405000, 60000, 65000, "Q4-2025", "G3/G4: final deliveries; PQ begins",
     "Thermco + Air Liquide + Daikin + MiR delivered; PQ start"),
]

HEADERS = ["#", "Month", "Equip. Purchases (USD)", "Install & Commissioning (USD)",
           "Facility Infra & FX Reserve (USD)", "NRE/Engineering (USD)", "Total Period Spend (USD)",
           "Cumulative Spend (USD)", "% of AR Budget", "Quarter", "Planned Milestone", "Notes"]


def build(wb, ar_total_cell):
    ws = wb.create_sheet("S14_CashFlow_Model")
    set_tab_color(ws, 3)
    row = title_block(ws, 3, "S14", "CapEx Cash Flow Model — Monthly Detail & Quarterly Summary (2025 Program)",
                       "Program: Greenfield Expansion Phase II | Owner: Sourabh Tarodekar | Merged monthly/quarterly model — "
                       "quarterly totals derived from monthly rows (SUMIF). Payment terms: 25% Deposit / 40% Milestone / 35% Delivery.",
                       n_cols=12)

    row = section_header(ws, row, 1, "PAYMENT & PROGRAM ASSUMPTIONS", 3, 3)
    for label, val in [
        ("Deposit % at PO Placement", 0.25), ("Manufacturing Milestone %", 0.40),
        ("Delivery Payment %", 0.35), ("Total AR Budget", f"='{ar_total_cell[0]}'!{ar_total_cell[1]}"),
    ]:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=val)
        if isinstance(val, float):
            c.number_format = PCT1
            c.font = BLUE_INPUT
        else:
            c.number_format = USD0
            c.font = GREEN_LINK
        c.border = BORDER_ALL
        row += 1
    ar_budget_ref_row = row - 1
    row += 1

    row = section_header(ws, row, 1, "MONTHLY SPEND PROFILE — Apr 2025 through Dec 2025", 12, 3)
    header_row = write_headers(ws, row, 1, HEADERS, 3)
    first_row = header_row
    r = header_row
    for i, (month, eq, inst, fac, nre, qtr, milestone, notes) in enumerate(MONTHLY, start=1):
        ws.cell(row=r, column=1, value=i)
        ws.cell(row=r, column=2, value=month)
        ec = ws.cell(row=r, column=3, value=eq); ec.number_format = USD0; ec.font = BLUE_INPUT
        ic = ws.cell(row=r, column=4, value=inst); ic.number_format = USD0; ic.font = BLUE_INPUT
        fc = ws.cell(row=r, column=5, value=fac); fc.number_format = USD0; fc.font = BLUE_INPUT
        nc_ = ws.cell(row=r, column=6, value=nre); nc_.number_format = USD0; nc_.font = BLUE_INPUT
        tot = ws.cell(row=r, column=7, value=f"=SUM(C{r}:F{r})"); tot.number_format = USD0
        if i == 1:
            cum = ws.cell(row=r, column=8, value=f"=G{r}")
        else:
            cum = ws.cell(row=r, column=8, value=f"=H{r-1}+G{r}")
        cum.number_format = USD0
        pctb = ws.cell(row=r, column=9, value=f"=H{r}/$B${ar_budget_ref_row}"); pctb.number_format = PCT1
        ws.cell(row=r, column=10, value=qtr)
        ws.cell(row=r, column=11, value=milestone).alignment = LEFT_WRAP
        nc = ws.cell(row=r, column=12, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 13):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    total_row = r
    ws.cell(row=r, column=2, value="TOTAL 2025").font = BOLD
    for col_letter in ["C", "D", "E", "F", "G"]:
        c = ws.cell(row=r, column=ord(col_letter) - 64, value=f"=SUM({col_letter}{first_row}:{col_letter}{last_row})")
        c.number_format = USD0
        c.font = BOLD
    ws.cell(row=r, column=8, value=f"=H{last_row}").number_format = USD0
    ws.cell(row=r, column=8).font = BOLD
    ws.cell(row=r, column=9, value=f"=I{last_row}").number_format = PCT1
    ws.cell(row=r, column=9).font = BOLD
    for c in range(1, 13):
        ws.cell(row=r, column=c).border = BORDER_ALL
        ws.cell(row=r, column=c).fill = zone_fill_light(3)
    row = r + 2

    row = section_header(ws, row, 1, "QUARTERLY CASH FLOW SUMMARY — DERIVED FROM MONTHLY DETAIL", 8, 3)
    qheaders = ["Quarter", "Equip. Purchases", "Install & Commissioning", "Facility Infra & FX Reserve",
                "NRE/Engineering", "Total Quarter Spend", "Cumul. Spend", "% of AR Budget"]
    row = write_headers(ws, row, 1, qheaders, 3)
    q_first = row
    for q in ["Q2-2025", "Q3-2025", "Q4-2025"]:
        ws.cell(row=row, column=1, value=q)
        for col_letter, src in zip(["B", "C", "D", "E"], ["C", "D", "E", "F"]):
            c = ws.cell(row=row, column=ord(col_letter) - 64,
                         value=f'=SUMIF($J${first_row}:$J${last_row},A{row},{src}{first_row}:{src}{last_row})')
            c.number_format = USD0
        tot = ws.cell(row=row, column=6, value=f"=SUM(B{row}:E{row})"); tot.number_format = USD0
        row += 1
    q_last = row - 1
    for i, r0 in enumerate(range(q_first, q_last + 1)):
        if i == 0:
            cum = ws.cell(row=r0, column=7, value=f"=F{r0}")
        else:
            cum = ws.cell(row=r0, column=7, value=f"=G{r0-1}+F{r0}")
        cum.number_format = USD0
        pc = ws.cell(row=r0, column=8, value=f"=G{r0}/$B${ar_budget_ref_row}"); pc.number_format = PCT1
        for c in range(1, 9):
            ws.cell(row=r0, column=c).border = BORDER_ALL
    row += 1
    ws.cell(row=row, column=1, value="PROGRAM TOTAL").font = BOLD
    for col_letter in ["B", "C", "D", "E", "F"]:
        c = ws.cell(row=row, column=ord(col_letter) - 64, value=f"=SUM({col_letter}{q_first}:{col_letter}{q_last})")
        c.number_format = USD0
        c.font = BOLD
    ws.cell(row=row, column=7, value=f"=G{q_last}").number_format = USD0
    ws.cell(row=row, column=7).font = BOLD
    ws.cell(row=row, column=8, value=f"=H{q_last}").number_format = PCT1
    ws.cell(row=row, column=8).font = BOLD
    for c in range(1, 9):
        ws.cell(row=row, column=c).border = BORDER_ALL
        ws.cell(row=row, column=c).fill = zone_fill_light(3)

    autosize(ws, {1: 5, 2: 10, 3: 16, 4: 18, 5: 18, 6: 15, 7: 15, 8: 15, 9: 11, 10: 10, 11: 30, 12: 48})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title, "cumulative_final_cell": f"H{last_row}"}
