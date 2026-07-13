from gen_common import *

# EqID, Tool, Period, Avail, Perf, Quality, PlannedYield(or None), ActualYield, UnitsProduced, UnitsScrapped, TopDefect, CorrectiveAction
YIELD_ROWS = [
    ("EQ-003", "Tube Furnace — Thermco", "Jul-2025", 0.905, 0.960, 0.978, 0.96, 94.1, 15200, 890,
     "Zone 3 temp uniformity +/-1.8C", "TEL FSE reviewed; zone 3 element replaced; uniformity now +/-1.2C"),
    ("EQ-003", "Tube Furnace — Thermco", "Aug-2025", 0.920, 0.970, 0.983, 0.96, 95.8, 16400, 277,
     "Minor particle contamination — wafer edge", "Cleaning protocol updated; edge exclusion improved"),
    ("EQ-003", "Tube Furnace — Thermco", "Sep-2025", 0.930, 0.970, 0.987, 0.96, 96.6, 17200, 228,
     "Within spec — no dominant defect", "No action required"),
    ("EQ-004", "Batch Oxidation Furnace — TEL", "Jul-2025", 0.910, 0.955, 0.975, 0.96, 93.3, 10800, 270,
     "Batch loading uniformity — slot 1/24 variation", "TEL batch loading algorithm updated; batch review at G4 gate"),
    ("EQ-004", "Batch Oxidation Furnace — TEL", "Aug-2025", 0.910, 0.965, 0.978, 0.96, 94.1, 11200, 246,
     "Improving — loading fix effective", "Monitor; target 95%+ OEE next period"),
    ("EQ-004", "Batch Oxidation Furnace — TEL", "Sep-2025", 0.920, 0.970, 0.982, 0.96, 95.4, 11850, 195,
     "Minor recipe drift — within SPC control", "SPC limits tightened; no action required"),
    ("EQ-005", "SCARA Robot — Brooks (x6)", "Jul-2025", 0.935, 0.985, 0.999, None, 95.6, 62800, 63,
     "Isolated pick error — Wrist B calibration", "Calibration corrected; all 6 robots re-verified"),
    ("EQ-005", "SCARA Robot — Brooks (x6)", "Aug-2025", 0.945, 0.990, 1.000, None, 97.1, 66200, 0,
     "None — zero defects this period", "No action required"),
    ("EQ-005", "SCARA Robot — Brooks (x6)", "Sep-2025", 0.940, 0.990, 1.000, None, 96.7, 67100, 0,
     "None", "No action required"),
    ("EQ-014", "RTP — Applied Materials (x2)", "Jul-2025", 0.930, 0.975, 0.983, 0.96, 95.9, 8900, 107,
     "Edge ring thermal non-uniformity — pre-ECO-003", "ECO-003 CVD SiC edge ring replacement — resolved"),
    ("EQ-014", "RTP — Applied Materials (x2)", "Aug-2025", 0.935, 0.980, 0.991, 0.96, 97.1, 9200, 56,
     "Below spec — none; edge exclusion improved", "ECO-003 effective; no action required"),
    ("EQ-014", "RTP — Applied Materials (x2)", "Sep-2025", 0.940, 0.980, 0.993, 0.96, 97.3, 9450, 47,
     "Within spec — lamp uniformity nominal", "AMAT lamp performance meeting spec; no action"),
]

HEADERS = ["Equip ID", "Tool", "Period", "Availability (%)", "Performance (%)", "Quality Rate (%)", "OEE (%)",
           "Planned Yield (%)", "Actual Yield (%)", "Yield Variance (pp)", "Units Produced", "Units Scrapped",
           "Scrap Rate (%)", "Top Defect Mode", "Corrective Action"]


def build(wb):
    ws = wb.create_sheet("S28_Yield_Production_Metrics")
    set_tab_color(ws, 5)
    row = title_block(ws, 5, "S28", "Yield & Production Metrics — OEE, Process Yield & Quality Tracking",
                       "OEE = Availability x Performance x Quality | Yield target: 96% (S01 Assumptions) | Owner: Sourabh Tarodekar | "
                       "Monthly reporting by process tool | Feeds S29 ROI Tracker", n_cols=15)
    header_row = write_headers(ws, row, 1, HEADERS, 5)
    first_row = header_row
    r = header_row
    for (eq, tool, period, avail, perf, qual, plan_yield, act_yield, units, scrap, defect, action) in YIELD_ROWS:
        ws.cell(row=r, column=1, value=eq)
        ws.cell(row=r, column=2, value=tool)
        ws.cell(row=r, column=3, value=period)
        ac = ws.cell(row=r, column=4, value=avail); ac.number_format = PCT1; ac.font = BLUE_INPUT
        pc = ws.cell(row=r, column=5, value=perf); pc.number_format = PCT1; pc.font = BLUE_INPUT
        qc = ws.cell(row=r, column=6, value=qual); qc.number_format = PCT1; qc.font = BLUE_INPUT
        oee = ws.cell(row=r, column=7, value=f"=D{r}*E{r}*F{r}"); oee.number_format = PCT1
        if plan_yield is not None:
            pyc = ws.cell(row=r, column=8, value=plan_yield); pyc.number_format = PCT1; pyc.font = BLUE_INPUT
        else:
            ws.cell(row=r, column=8, value="N/A")
        ayc = ws.cell(row=r, column=9, value=act_yield / 100); ayc.number_format = PCT1; ayc.font = BLUE_INPUT
        if plan_yield is not None:
            var = ws.cell(row=r, column=10, value=f"=I{r}-H{r}"); var.number_format = PCT1
        else:
            ws.cell(row=r, column=10, value="N/A")
        ws.cell(row=r, column=11, value=units).font = BLUE_INPUT
        ws.cell(row=r, column=12, value=scrap).font = BLUE_INPUT
        sr = ws.cell(row=r, column=13, value=f"=L{r}/K{r}"); sr.number_format = PCT1
        ws.cell(row=r, column=14, value=defect).alignment = LEFT_WRAP
        ws.cell(row=r, column=15, value=action).alignment = LEFT_WRAP
        for c in range(1, 16):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "PROGRAM OEE SUMMARY", 2, 5)
    stats = [
        ("OEE Target (Avail 92% x Perf 97% x Quality 96%)", "=0.92*0.97*0.96", PCT1),
        ("Average Actual OEE (Process Tools, Q3-2025)", f"=AVERAGE(G{first_row}:G{last_row})", PCT1),
        ("Yield Target (S01 Assumptions)", 0.96, PCT1),
        ("Average Actual Yield (Q3-2025)", f"=AVERAGE(I{first_row}:I{last_row})", PCT1),
        ("Tools Below OEE Target this Period", f'=COUNTIF(G{first_row}:G{last_row},"<"&0.92*0.97*0.96)', CUR0),
        ("Total Units Produced (Q3-2025)", f"=SUM(K{first_row}:K{last_row})", CUR0),
        ("Total Units Scrapped (Q3-2025)", f"=SUM(L{first_row}:L{last_row})", CUR0),
    ]
    stat_rows = {}
    stat_keys = ["oee_target", "avg_actual_oee", "yield_target", "avg_actual_yield",
                 "tools_below_target", "total_units", "total_scrapped"]
    for key, (label, formula, fmt) in zip(stat_keys, stats):
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        stat_rows[key] = row
        row += 1

    autosize(ws, {1: 9, 2: 26, 3: 10, 4: 12, 5: 12, 6: 12, 7: 9, 8: 12, 9: 12, 10: 12, 11: 12, 12: 12, 13: 11, 14: 36, 15: 46})
    freeze_below(ws, header_row + 1)
    return {
        "sheet": ws.title, "first_row": first_row, "last_row": last_row,
        "avg_actual_oee_cell": f"B{stat_rows['avg_actual_oee']}",
    }
