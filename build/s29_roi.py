from gen_common import *

# EqID, Tool, PlannedThroughput, ActualThroughput, PlannedUptime, ActualUptime, PlannedEnergy, ActualEnergy, CorrectiveAction, Checkpoint, Status
ROI_ROWS = [
    ("EQ-003", "Tube Furnace — Thermco", 24, 23, 0.92, 0.905, 86944, "Pending",
     "Monitor zone temperature uniformity; recipe 3 showing 0.3% yield below target", "30-Day", "IN PROGRESS"),
    ("EQ-004", "Batch Oxidation Furnace — TEL", 18, 18, 0.92, 0.910, 100672, "Pending",
     "TEL FSE reviewing batch loading algorithm; minor throughput shortfall under investigation", "30-Day", "IN PROGRESS"),
    ("EQ-005", "SCARA Robot — Brooks (x6)", 120, 118, 0.92, 0.935, 3844, "Pending",
     "Robot uptime exceeding plan. MES integration performing well. No action required.", "30-Day", "ABOVE PLAN"),
    ("EQ-014", "RTP — Applied Materials (x2)", 32, 32, 0.92, 0.930, 77792, "Pending",
     "Edge ring yield at 97.2% vs 96% target. Lamp array performing well. No action.", "30-Day", "ABOVE PLAN"),
    ("EQ-001", "Dry Screw Vacuum Pump (x4)", None, None, 0.92, 0.880, 16931, "Pending",
     "Uptime below plan — bearing set replacement needed on pump 2. CR raised.", "90-Day", "BELOW PLAN"),
    ("EQ-002", "Turbomolecular Pump — Pfeiffer (x3)", None, None, 0.92, None, 10982, "Pending",
     "90-day checkpoint pending. Safety stock in place.", "90-Day", "PENDING"),
    ("EQ-006", "Overhead Conveyor — Daifuku", None, None, 0.92, None, 20134, "Pending",
     "Track system performing nominally. Wi-Fi integration stable. No issues to date.", "90-Day", "PENDING"),
    ("EQ-007", "Gas Handling Cabinet — Air Liquide (x4)", None, None, 0.92, None, 732, "Pending",
     "Gas cabinet operational. MFC calibration rotation in schedule. No events.", "90-Day", "PENDING"),
    ("EQ-009", "DCS — Siemens S7-1500 (x5)", None, None, 0.92, None, 1098, "Pending",
     "DCS fully operational. Cybersecurity audit scheduled Month 4.", "180-Day", "PENDING"),
    ("EQ-011", "Dry-Type Transformer (x2)", None, None, 0.99, None, 0, "Pending",
     "Transformer operating within thermal limits. Cooling fans checked. No issues.", "180-Day", "PENDING"),
    ("EQ-012", "Process Chiller — Daikin (x3)", None, None, 0.99, None, 65525, "Pending",
     "Glycol loop stable. Compressor discharge pressure nominal. 180-day checkpoint due.", "180-Day", "PENDING"),
    ("EQ-015", "AMR Fleet — MiR (x10)", None, None, 0.92, None, 5491, "Pending",
     "Fleet routing optimisation Phase 2 scheduled Month 5. Battery health nominal.", "180-Day", "PENDING"),
]

HEADERS = ["Equipment ID", "Equipment / Tool", "Planned Throughput (u/hr)", "Actual Throughput (u/hr)",
           "Throughput Variance", "Planned Uptime %", "Actual Uptime %", "Uptime Variance",
           "Planned Annual Energy Cost", "Actual Annual Energy Cost", "Checkpoint", "Status", "Notes"]


def build(wb):
    ws = wb.create_sheet("S29_Equipment_ROI_Tracker")
    set_tab_color(ws, 5)
    row = title_block(ws, 5, "S29", "Equipment ROI & Performance Tracker — Actual vs Plan (Post-Commissioning)",
                       "Program: Greenfield Expansion Phase II | Populated after G5 Production Release | "
                       "30-day / 90-day / 180-day checkpoints | Actual inputs in BLUE | Variances auto-calculated | "
                       "Planned values pulled from S02 (throughput/uptime) and S10 (capacity model)", n_cols=13)
    header_row = write_headers(ws, row, 1, HEADERS, 5)
    first_row = header_row
    r = header_row
    for (eq, tool, pthr, athr, puptime, auptime, penergy, aenergy, notes, checkpoint, status) in ROI_ROWS:
        ws.cell(row=r, column=1, value=eq)
        ws.cell(row=r, column=2, value=tool)
        ws.cell(row=r, column=3, value=pthr if pthr else "N/A")
        if athr is not None:
            atc = ws.cell(row=r, column=4, value=athr); atc.font = BLUE_INPUT
            varc = ws.cell(row=r, column=5, value=f"=D{r}-C{r}")
        else:
            ws.cell(row=r, column=4, value="Pending")
            ws.cell(row=r, column=5, value="—")
        puc = ws.cell(row=r, column=6, value=puptime); puc.number_format = PCT1
        if auptime is not None:
            auc = ws.cell(row=r, column=7, value=auptime); auc.number_format = PCT1; auc.font = BLUE_INPUT
            uv = ws.cell(row=r, column=8, value=f"=G{r}-F{r}"); uv.number_format = PCT1
        else:
            ws.cell(row=r, column=7, value="Pending")
            ws.cell(row=r, column=8, value="—")
        pec = ws.cell(row=r, column=9, value=penergy); pec.number_format = USD0; pec.font = GREEN_LINK
        ws.cell(row=r, column=10, value=aenergy)
        ws.cell(row=r, column=11, value=checkpoint)
        stc = ws.cell(row=r, column=12, value=status)
        if status == "ABOVE PLAN":
            stc.fill = PatternFill("solid", fgColor=RAG_GREEN)
        elif status == "BELOW PLAN":
            stc.fill = PatternFill("solid", fgColor=RAG_RED)
        elif status == "PENDING":
            stc.fill = PatternFill("solid", fgColor="FFF2CC")
        else:
            stc.fill = PatternFill("solid", fgColor="DDEBF7")
        nc = ws.cell(row=r, column=13, value=notes)
        nc.alignment = LEFT_WRAP
        for c in range(1, 14):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "POST-COMMISSIONING PERFORMANCE SUMMARY", 2, 5)
    stats = [
        ("Equipment Platforms Tracked", f"=COUNTA(A{first_row}:A{last_row})", CUR0),
        ("Platforms with 30-Day Data", f'=COUNTIF(K{first_row}:K{last_row},"30-Day")', CUR0),
        ("Platforms Above or On Plan", f'=COUNTIF(L{first_row}:L{last_row},"ABOVE PLAN")', CUR0),
        ("Platforms Below Plan", f'=COUNTIF(L{first_row}:L{last_row},"BELOW PLAN")', CUR0),
        ("Platforms Pending Data", f'=COUNTIF(L{first_row}:L{last_row},"PENDING")', CUR0),
    ]
    for label, formula, fmt in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 10, 2: 30, 3: 14, 4: 14, 5: 12, 6: 12, 7: 12, 8: 12, 9: 15, 10: 15, 11: 10, 12: 12, 13: 50})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title, "first_row": first_row, "last_row": last_row}
