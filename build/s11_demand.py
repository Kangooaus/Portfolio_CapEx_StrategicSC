from gen_common import *

QUARTERS = [
    ("Q1-2023", 520000, 505000, "ACTUAL", "S&OP Review", "Production ramp; new process tools qualified Q1"),
    ("Q2-2023", 540000, 528000, "ACTUAL", "S&OP Review", "Slight volume shortfall; MES integration delay"),
    ("Q3-2023", 565000, 571000, "ACTUAL", "S&OP Review", "On track; customer pull-in request +6K units"),
    ("Q4-2023", 575000, 567000, "ACTUAL", "S&OP Review", "Seasonal demand pattern confirmed"),
    ("Q1-2024", 590000, 580000, "ACTUAL", "S&OP Review", "Q1 softness as expected; customer forecast revised"),
    ("Q2-2024", 610000, 624000, "ACTUAL", "S&OP Review", "Strong pull; customer volume commitment +35K"),
    ("Q3-2024", 630000, 618000, "ACTUAL", "S&OP Review", "Slight miss due to competitor product shift"),
    ("Q4-2024", 650000, 661000, "ACTUAL", "S&OP Review", "Year-end strong; customer forecast upgrade for 2025 Phase II program"),
    ("Q1-2025", 680000, 675000, "ACTUAL", "S&OP Review", "Phase II program approved; capacity expansion underway"),
    ("Q2-2025", 710000, 718000, "ACTUAL", "S&OP Review", "All POs placed; equipment in fabrication"),
    ("Q3-2025", 735000, None, "FORECAST", "S&OP Review", "Forecast confirmed; delivery/install on schedule"),
    ("Q4-2025", 750000, None, "FORECAST", "S&OP Review", "TARGET: G5 production release; full capacity online"),
]

HEADERS = ["Period", "Baseline Forecast", "Upside (+20%)", "Downside (-20%)", "Actual/Committed",
           "Forecast Accuracy (%)", "Rolling 3-Qtr Avg", "Variance vs Fcst", "Status", "Forecast Source", "Notes"]

PRODUCT_FAMILIES = [
    ("PF-A", "Advanced Process Products (High-Temp Furnace)", 210000, 260000, 70000, 73000, 78000, 79000, "EQ-003/004", 1,
     "Core product line; furnace utilization primary constraint"),
    ("PF-B", "Precision Robotics Assembly", 150000, 190000, 54000, 56000, 58000, 57000, "EQ-005", 2,
     "Growing line; Brooks robot fleet capacity adequate through 2025"),
    ("PF-C", "Gas-Phase Deposition (RTP Products)", 115000, 142000, 36000, 37000, 38000, 39000, "EQ-014", 3,
     "High-value product; RTP qualification critical"),
    ("PF-D", "Infrastructure / Support Builds", 75000, 58000, 18000, 18500, 19000, 19500, "EQ-009/010", 4,
     "Control systems; demand stable; not capacity-constrained"),
]


def build(wb):
    ws = wb.create_sheet("S11_Demand_Forecast")
    set_tab_color(ws, 2)
    row = title_block(ws, 2, "S11", "Demand Forecast Model — Advanced Manufacturing Program (2023-2025)",
                       "Time-series demand forecast by product family | Owner: Sourabh Tarodekar | "
                       "Feeds S10_Capacity_Planning (baseline demand input) | Forecast accuracy tracked quarterly", n_cols=11)

    row = section_header(ws, row, 1, "FORECAST ASSUMPTIONS", 2, 2)
    for label, val, fmt in [
        ("Baseline Annual Demand (2025 program target)", 750000, CUR0),
        ("Surge Scenario (+20%)", 900000, CUR0),
        ("Downside Scenario (-20%)", 600000, CUR0),
        ("Committed Customer Volume (Phase II driver, incremental)", 312000, CUR0),
    ]:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=val); c.number_format = fmt; c.border = BORDER_ALL; c.font = BLUE_INPUT
        row += 1
    row += 1

    row = section_header(ws, row, 1, "QUARTERLY FORECAST vs ACTUALS — 2023 THROUGH 2025", 11, 2)
    header_row = write_headers(ws, row, 1, HEADERS, 2)
    first_row = header_row
    r = header_row
    for i, (period, base, actual, status, src, notes) in enumerate(QUARTERS):
        ws.cell(row=r, column=1, value=period)
        bc = ws.cell(row=r, column=2, value=base); bc.number_format = CUR0; bc.font = BLUE_INPUT
        up = ws.cell(row=r, column=3, value=f"=B{r}*1.2"); up.number_format = CUR0
        down = ws.cell(row=r, column=4, value=f"=B{r}*0.8"); down.number_format = CUR0
        if actual is not None:
            ac = ws.cell(row=r, column=5, value=actual); ac.number_format = CUR0; ac.font = BLUE_INPUT
            acc = ws.cell(row=r, column=6, value=f"=E{r}/B{r}"); acc.number_format = PCT1
            var = ws.cell(row=r, column=8, value=f"=E{r}-B{r}"); var.number_format = CUR0
        else:
            ws.cell(row=r, column=5, value="TBC")
            ws.cell(row=r, column=6, value="TBC")
            ws.cell(row=r, column=8, value="TBC")
        if i >= 2:
            avail = [f"E{r-2}", f"E{r-1}", f"E{r}"] if actual is not None else [f"E{r-2}", f"E{r-1}"]
            roll = ws.cell(row=r, column=7, value=f"=IFERROR(AVERAGE(E{r-2}:E{r}),AVERAGE(E{r-2}:E{r-1}))")
            roll.number_format = CUR0
        else:
            ws.cell(row=r, column=7, value="TBC")
        sc = ws.cell(row=r, column=9, value=status)
        sc.fill = PatternFill("solid", fgColor=RAG_GREEN if status == "ACTUAL" else "DDEBF7")
        ws.cell(row=r, column=10, value=src)
        nc = ws.cell(row=r, column=11, value=notes)
        nc.alignment = LEFT_WRAP
        for c in range(1, 12):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "DEMAND BY PRODUCT FAMILY — 2025 ANNUAL FORECAST", 13, 2)
    pf_headers = ["Product Family", "Description", "2023 Actual", "2024 Actual", "Q1-2025", "Q2-2025",
                  "Q3-2025", "Q4-2025", "2025 Forecast", "CAGR 2023->25", "Required Capacity (u/hr)",
                  "Constrained by Equip", "Priority"]
    header_row2 = write_headers(ws, row, 1, pf_headers, 2)
    pf_first = row + 1
    r = pf_first
    for (code, desc, a23, a24, q1, q2, q3, q4, eq, prio, note) in PRODUCT_FAMILIES:
        ws.cell(row=r, column=1, value=code)
        ws.cell(row=r, column=2, value=desc)
        c23 = ws.cell(row=r, column=3, value=a23); c23.number_format = CUR0; c23.font = BLUE_INPUT
        c24 = ws.cell(row=r, column=4, value=a24); c24.number_format = CUR0; c24.font = BLUE_INPUT
        for i, v in enumerate([q1, q2, q3, q4]):
            cc = ws.cell(row=r, column=5 + i, value=v); cc.number_format = CUR0; cc.font = BLUE_INPUT
        fcast = ws.cell(row=r, column=9, value=f"=SUM(E{r}:H{r})"); fcast.number_format = CUR0
        cagr = ws.cell(row=r, column=10, value=f"=IFERROR((I{r}/C{r})^(1/2)-1,0)"); cagr.number_format = PCT1
        reqcap = ws.cell(row=r, column=11, value=f"=I{r}/8320/0.88/0.96")
        reqcap.number_format = CUR2
        ws.cell(row=r, column=12, value=eq)
        ws.cell(row=r, column=13, value=prio)
        for c in range(1, 14):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    pf_last = r - 1
    ws.cell(row=r, column=1, value="TOTAL").font = BOLD
    ws.cell(row=r, column=2, value="All Product Families").font = BOLD
    for col_letter in ["C", "D", "E", "F", "G", "H", "I"]:
        c = ws.cell(row=r, column=ord(col_letter) - 64, value=f"=SUM({col_letter}{pf_first}:{col_letter}{pf_last})")
        c.number_format = CUR0
        c.font = BOLD
    for c in range(1, 14):
        ws.cell(row=r, column=c).border = BORDER_ALL
        ws.cell(row=r, column=c).fill = zone_fill_light(2)

    autosize(ws, {1: 10, 2: 34, 3: 13, 4: 13, 5: 12, 6: 13, 7: 12, 8: 12, 9: 13, 10: 12, 11: 16, 12: 15, 13: 9})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
