from gen_common import *

SECTIONS = [
    ("CAPITAL EXPENDITURE (CAPEX)", [
        ("Total Equipment Purchase Cost", "$", 24500000, 32800000, 38500000, "B", "Scenario A uses domestic/value suppliers; C uses premium OEM across all platforms"),
        ("Total Installation Cost", "$", 2800000, 3600000, 4200000, "A", "Installation costs scale with equipment complexity and supplier requirements"),
        ("Total CapEx (Equipment + Install)", "$", 27300000, 36400000, 42700000, "A", "Formula: Purchase + Install; Scenario A ~33% lower CapEx than C"),
        ("Contingency Reserve (10% of CapEx)", "$", 2730000, 3640000, 4270000, "A", "Standard 10% contingency; Scenario C highest absolute contingency"),
        ("Total Program Budget (incl. contingency)", "$", 30030000, 40040000, 46970000, "A", "Total appropriations request basis for each scenario"),
    ]),
    ("OPERATING EXPENDITURE (OPEX — ANNUAL)", [
        ("Annual Energy Cost (all equipment)", "$/yr", 1850000, 1620000, 1380000, "C", "Scenario A older/less efficient equipment; Scenario C latest-gen low-energy platforms"),
        ("Annual Maintenance Cost", "$/yr", 1960000, 1475000, 1225000, "C", "Scenario A value-tier has higher failure rate and maint burden"),
        ("Annual Spare Parts Cost", "$/yr", 520000, 385000, 295000, "C", "Premium OEM (Scenario C) has longer MTBF; fewer spare parts events"),
        ("Annual Downtime Cost (MTBF/MTTR model)", "$/yr", 1260000, 720000, 396000, "C", "MTBF-based: Sc A avg MTBF 2,400hr; Sc B 3,500hr; Sc C 5,200hr"),
        ("Total Annual OpEx", "$/yr", 5590000, 4200000, 3296000, "C", "Formula: Sum of above OpEx lines; C saves $2.3M/yr vs A"),
    ]),
    ("FINANCIAL MODEL (10-YEAR HORIZON)", [
        ("10-Year Cumulative OpEx", "$", 55900000, 42000000, 32960000, "C", "Escalated at 2.5%/yr inflation; C significantly lower over 10-yr horizon"),
        ("NPV of OpEx Savings vs Scenario A", "$", 0, 9520000, 14630000, "C", "NPV at 8% discount rate; Scenario C generates $14.6M NPV savings vs A"),
        ("Estimated IRR", "%", None, 0.142, 0.187, "C", "IRR on incremental investment relative to Scenario A baseline"),
        ("Simple Payback vs Scenario A (yrs)", "yrs", None, 4, 4, "C", "Payback of incremental CapEx premium through OpEx savings"),
    ]),
    ("CAPACITY & PERFORMANCE", [
        ("Annual Production Capacity (units/yr)", "units", 228000, 312000, 368000, "C", "Scenario C premium equipment delivers highest throughput and uptime"),
        ("Equipment Uptime (%)", "%", 0.88, 0.92, 0.955, "C", "Scenario A value-tier has higher unplanned downtime; C has best SLA terms"),
        ("Process Yield (%)", "%", 0.935, 0.96, 0.975, "C", "Process yield linked to equipment precision and repeatability spec"),
    ]),
    ("SUPPLY CHAIN RISK", [
        ("Single-Source Components", "count", 8, 5, 3, "C", "Scenario A relies on more sole-source suppliers due to cost-driven selection"),
        ("Avg Supplier Lead Time (wks)", "wks", 23.4, 19.8, 17.2, "C", "Premium suppliers (Scenario C) have better supply chain infrastructure"),
        ("Supply Chain Risk Index (composite)", "score", 38.5, 24.2, 16.8, "C", "Composite index; lower = lower risk"),
    ]),
    ("SCHEDULE & DEPLOYMENT", [
        ("Critical Path Duration (weeks)", "wks", 46.0, 42.0, 38.0, "C", "Scenario C suppliers have shorter manufacturing lead times and dedicated PM support"),
        ("Program End Date (Week # from start)", "wks", 52.0, 47.0, 43.0, "C", "Earlier qualification in Scenario C allows faster ramp to production revenue"),
        ("Schedule Risk Items", "count", 7, 5, 3, "C", "Fewer risk items in Scenario C; better supplier program management"),
    ]),
]

SCORECARD = [
    ("Capital Cost (Lower = Better)", 0.20, 5, 3, 2, "A", "Scenario A lowest CapEx"),
    ("10-Yr Total Cost of Ownership", 0.20, 2, 4, 5, "C", "Scenario C lowest lifecycle cost"),
    ("Financial Return (NPV/IRR)", 0.15, 1, 4, 5, "C", "Scenario C best financial returns"),
    ("Production Capacity", 0.10, 2, 4, 5, "C", "Scenario C highest throughput"),
    ("Supply Chain Risk", 0.15, 2, 4, 5, "C", "Scenario C least single-source exposure"),
    ("Schedule & Deployment Risk", 0.10, 2, 4, 5, "C", "Scenario C shortest critical path"),
    ("Operational Reliability / Uptime", 0.10, 2, 4, 5, "C", "Scenario C highest uptime spec"),
]


def build(wb):
    ws = wb.create_sheet("S13_Scenario_Analysis")
    set_tab_color(ws, 3)
    row = title_block(ws, 3, "S13", "Scenario Analysis — CapEx Program Investment Decision Framework",
                       "Compares three capital investment scenarios across NPV, TCO, capacity, supply chain risk, and schedule | "
                       "Scenario A = Minimum CapEx (Low Upfront / Higher OpEx) | Scenario B = Baseline Program (Balanced) | "
                       "Scenario C = Premium Build (High CapEx / Lowest OpEx)", n_cols=9)

    headers = ["Parameter", "Units", "Scenario A", "Scenario B", "Scenario C", "B vs A Delta", "C vs B Delta", "Best Scenario", "Notes"]
    opex_total_row = None
    for sect_title, rows_data in SECTIONS:
        row = section_header(ws, row, 1, sect_title, 9, 3)
        row = write_headers(ws, row, 1, headers, 3)
        for label, units, a, b, c, best, note in rows_data:
            ws.cell(row=row, column=1, value=label)
            ws.cell(row=row, column=2, value=units)
            fmt = None
            if units in ("$", "$/yr"):
                fmt = USD0
            elif units == "%":
                fmt = PCT1
            elif units in ("wks", "count", "units", "score", "yrs"):
                fmt = CUR2 if isinstance(a, float) and a is not None and a != int(a) else CUR0
            for col, val in zip((3, 4, 5), (a, b, c)):
                cc = ws.cell(row=row, column=col, value=val if val is not None else "N/A")
                if fmt and val is not None:
                    cc.number_format = fmt
                cc.font = BLUE_INPUT
            if a is not None:
                d1 = ws.cell(row=row, column=6, value=f"=D{row}-C{row}")
                if fmt:
                    d1.number_format = fmt
            else:
                ws.cell(row=row, column=6, value="N/A")
            d2 = ws.cell(row=row, column=7, value=f"=E{row}-D{row}")
            if fmt:
                d2.number_format = fmt
            ws.cell(row=row, column=8, value=f"Scenario {best}")
            nc = ws.cell(row=row, column=9, value=note)
            nc.alignment = LEFT_WRAP
            for cidx in range(1, 10):
                ws.cell(row=row, column=cidx).border = BORDER_ALL
            if label == "Total Annual OpEx":
                opex_total_row = row
            row += 1
        row += 1

    # fix Best Scenario column with an actual heuristic afterwards is messy; instead just leave manual text below.
    autosize(ws, {1: 34, 2: 8, 3: 16, 4: 16, 5: 16, 6: 15, 7: 15, 8: 13, 9: 55})

    row = section_header(ws, row, 1, "WEIGHTED DECISION SCORECARD & PROGRAM RECOMMENDATION", 9, 3)
    sheaders = ["Dimension", "Weight", "Score A (1-5)", "Score B (1-5)", "Score C (1-5)",
                "Wtd Score A", "Wtd Score B", "Wtd Score C", "Winner"]
    row = write_headers(ws, row, 1, sheaders, 3)
    score_first = row
    for dim, wt, sa, sb, sc, winner, note in SCORECARD:
        ws.cell(row=row, column=1, value=dim)
        wc = ws.cell(row=row, column=2, value=wt); wc.number_format = PCT1; wc.font = BLUE_INPUT
        ws.cell(row=row, column=3, value=sa).font = BLUE_INPUT
        ws.cell(row=row, column=4, value=sb).font = BLUE_INPUT
        ws.cell(row=row, column=5, value=sc).font = BLUE_INPUT
        wa = ws.cell(row=row, column=6, value=f"=B{row}*C{row}"); wa.number_format = CUR2
        wb_ = ws.cell(row=row, column=7, value=f"=B{row}*D{row}"); wb_.number_format = CUR2
        wcc = ws.cell(row=row, column=8, value=f"=B{row}*E{row}"); wcc.number_format = CUR2
        ws.cell(row=row, column=9, value=winner)
        for cidx in range(1, 10):
            ws.cell(row=row, column=cidx).border = BORDER_ALL
        row += 1
    score_last = row - 1
    ws.cell(row=row, column=1, value="TOTAL WEIGHTED SCORE").font = BOLD
    tw = ws.cell(row=row, column=2, value=f"=SUM(B{score_first}:B{score_last})"); tw.number_format = PCT1; tw.font = BOLD
    twa = ws.cell(row=row, column=6, value=f"=SUM(F{score_first}:F{score_last})"); twa.number_format = CUR2; twa.font = BOLD
    twb = ws.cell(row=row, column=7, value=f"=SUM(G{score_first}:G{score_last})"); twb.number_format = CUR2; twb.font = BOLD
    twc = ws.cell(row=row, column=8, value=f"=SUM(H{score_first}:H{score_last})"); twc.number_format = CUR2; twc.font = BOLD
    for cidx in range(1, 10):
        ws.cell(row=row, column=cidx).border = BORDER_ALL
        ws.cell(row=row, column=cidx).fill = zone_fill_light(3)
    total_score_row = row
    row += 2

    row = section_header(ws, row, 1, "PROGRAM RECOMMENDATION", 9, 3)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=9)
    ws.cell(row=row, column=1, value="RECOMMENDED SCENARIO: SCENARIO B — Baseline Program (APPROVED)").font = Font(bold=True, color="006100")
    row += 1
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=9)
    ws.cell(row=row, column=1, value=(
        "Scenario B delivers 312,000 units/yr capacity, 14.2% IRR, and $9.5M NPV over 10 years vs Scenario A. While Scenario C "
        "scores marginally higher on the weighted scorecard, it was not selected because the $47M total budget exceeds the "
        "divisional CapEx approval ceiling for a single program phase. Scenario B provides the optimal balance of financial "
        "return, risk profile, and capital efficiency within approved limits. Total budget $40.04M is within the $42M divisional "
        "CapEx approval ceiling; 14.2% IRR exceeds the 8% hurdle rate with a 4.2-year payback; 312,000 units/yr capacity supports "
        "the committed 35% customer volume increase. AR-2025-0082 was submitted and approved on this basis."
    )).alignment = LEFT_WRAP
    ws.row_dimensions[row].height = 60
    row += 2

    freeze_below(ws, 1)
    return {"sheet": ws.title, "total_score_row": total_score_row, "opex_total_row": opex_total_row}
