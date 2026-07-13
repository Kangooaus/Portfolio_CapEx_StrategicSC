from gen_common import *

# EqID, Tool, Supplier, Mfg, FAT, Ship, Inst, Util, PQ, ProgStart, CritYN, RiskFlag, Predecessor, Notes
DEPLOY = [
    ("EQ-014", "RTP – Applied Materials (CRITICAL PATH)", "AMAT", 24, 2, 3, 4, 2, 6, 1, "YES", "HIGH", "None — first install",
     "Highest-value item; finance AR approval gate at Week 2; 30% deposit required; longest total duration"),
    ("EQ-004", "Batch Oxidation Furnace", "TEL", 28, 2, 3, 4, 2, 5, 1, "YES", "HIGH", "EQ-013 (pump) must install first",
     "JPY FX exposure; overseas FAT at TEL Japan; import clearance estimated 1 week"),
    ("EQ-003", "Tube Furnace System", "Thermco", 20, 2, 3, 4, 2, 5, 2, "YES", "MODERATE", "EQ-013 (pump) must install first",
     "Parallel install path with EQ-004 possible; process recipe transfer at FAT"),
    ("EQ-006", "Overhead Track Conveyor", "Daifuku", 30, 2, 3, 5, 2, 0, 1, "YES", "HIGH", "Civil mounts must be complete (Week 8)",
     "Civil interface drawings required 8 wks before delivery; structural review required"),
    ("EQ-002", "Turbomolecular Pump", "Pfeiffer", 26, 2, 3, 3, 1, 0, 1, "YES", "CRITICAL", "EQ-003, EQ-004 dependent",
     "SINGLE SOURCE – CRITICAL RISK; no qualified alt; escalated to VP; daily status"),
    ("EQ-008", "Bulk Gas Storage", "Linde", 32, 2, 3, 5, 3, 0, 1, "YES", "HIGH", "EQ-007 (gas cabinet) install after",
     "Longest lead time in portfolio (32 wks mfg); PO must be placed Week 1; civil pad parallel"),
    ("EQ-001", "Dry Screw Vacuum Pump", "Edwards", 18, 2, 3, 3, 1, 0, 2, "No", "MODERATE", "EQ-003 dependent",
     "Alt vendor (Busch) available; paired install with EQ-013; N2 purge line required"),
    ("EQ-013", "Roots Blower Booster", "Busch", 15, 2, 3, 3, 1, 0, 2, "No", "LOW", "EQ-001 must install first",
     "Paired with EQ-001; coordinated delivery schedule; low supply risk"),
    ("EQ-007", "Gas Cabinet", "Air Liquide", 22, 2, 3, 4, 2, 0, 2, "No", "MODERATE", "EQ-008 (bulk gas) commissioned first",
     "Hazmat permit on critical path; permit application must be filed immediately"),
    ("EQ-005", "SCARA Robot (x6)", "Brooks", 14, 2, 3, 4, 1, 0, 3, "No", "MODERATE", "EQ-006 (conveyor) operational first",
     "MES integration requires 4 wks; SW engineer on-site for FAT and site install"),
    ("EQ-009", "DCS – Siemens S7-1500 (x5)", "—", 14, 2, 3, 3, 1, 0, 2, "No", "LOW", "None — independent",
     "Cybersecurity review adds 3 wks; submit InfoSec package 6 wks pre-install"),
    ("EQ-010", "SCADA Platform", "Inductive Automation", 0, 2, 0, 2, 1, 0, 4, "No", "LOW", "EQ-009 DCS must be installed",
     "Software license; no physical shipping; IT infrastructure and server required on-site first"),
    ("EQ-011", "Dry-Type Transformer", "ABB", 20, 2, 3, 3, 2, 0, 1, "No", "MODERATE", "None — utility infrastructure",
     "Partial reuse from legacy program; refurbishment scope adds 2 wks to schedule"),
    ("EQ-012", "Process Chiller (x3)", "Daikin", 20, 2, 3, 4, 2, 0, 2, "No", "MODERATE", "EQ-011 (transformer) must be live",
     "Glycol loop design must be finalized by Week 6; coordinate with mechanical engineering"),
    ("EQ-015", "AMR Fleet (x10)", "MiR", 18, 2, 3, 3, 1, 0, 5, "No", "LOW", "EQ-006 (conveyor) track complete",
     "Wi-Fi infrastructure upgrade required 6 wks before delivery; IT lead time on critical path"),
]

HEADERS = ["Equipment ID", "Equipment / Tool", "Supplier", "Mfg (wks)", "FAT (wks)", "Shipping (wks)",
           "Installation (wks)", "Utility Hookup (wks)", "Process Qual (wks)", "Total Deploy Duration (wks)",
           "Program Start Week", "Delivery/Install Compl. (Wk#)", "PQ Complete (Wk#)", "Critical Path?",
           "Float (wks)", "Risk Flag", "Predecessor Dependency", "Engineering Notes"]


def build(wb):
    ws = wb.create_sheet("S09_Deployment_Timeline")
    set_tab_color(ws, 2)
    row = title_block(ws, 2, "S09", "Equipment Deployment Timeline & Critical Path Model — CapEx Phase II Program",
                       "All durations in weeks | Program Start: Week 1 (2025-Q2) | Critical Path items highlighted in RED | Inputs in BLUE | "
                       "[MFG] Mfg  [FAT] Factory Accept. Test  [SHP] Shipping  [INS] Installation  [UTL] Utility Hookup  [PQ] Process Qual",
                       n_cols=18)
    header_row = write_headers(ws, row, 1, HEADERS, 2)
    first_row = header_row
    r = header_row
    for (eid, tool, sup, mfg, fat, ship, inst, util, pq, start, crit, riskflag, pred, notes) in DEPLOY:
        ws.cell(row=r, column=1, value=eid).font = BOLD
        ws.cell(row=r, column=2, value=tool)
        ws.cell(row=r, column=3, value=sup)
        for i, v in enumerate([mfg, fat, ship, inst, util, pq]):
            cc = ws.cell(row=r, column=4 + i, value=v)
            cc.font = BLUE_INPUT
        total = ws.cell(row=r, column=10, value=f"=SUM(D{r}:I{r})")
        pstart = ws.cell(row=r, column=11, value=start); pstart.font = BLUE_INPUT
        compl = ws.cell(row=r, column=12, value=f"=K{r}+J{r}-F{r}")
        pqc = ws.cell(row=r, column=13, value=f"=K{r}+J{r}")
        cp = ws.cell(row=r, column=14, value=crit)
        if crit == "YES":
            cp.fill = PatternFill("solid", fgColor=RAG_RED)
        floatc = ws.cell(row=r, column=15, value=f'=IF(N{r}="YES",0,4)')
        rf = ws.cell(row=r, column=16, value=riskflag)
        fill = rag_fill(riskflag)
        if fill:
            rf.fill = fill
        ws.cell(row=r, column=17, value=pred)
        nc = ws.cell(row=r, column=18, value=notes)
        nc.alignment = LEFT_WRAP
        for c in range(1, 19):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "PROGRAM SCHEDULE SUMMARY", 2, 2)
    facts = [
        ("Earliest Equipment Delivery (Week #)", f"=MIN(L{first_row}:L{last_row})"),
        ("Latest PQ Completion (Week #)", f"=MAX(M{first_row}:M{last_row})"),
        ("Critical Path Duration (Program End, weeks)", f"=MAX(M{first_row}:M{last_row})"),
        ("Total Equipment Platforms", f"=COUNTA(A{first_row}:A{last_row})"),
        ("Critical Path Items", f'=COUNTIF(N{first_row}:N{last_row},"YES")'),
        ("HIGH or CRITICAL Risk Items", f'=COUNTIF(P{first_row}:P{last_row},"HIGH")+COUNTIF(P{first_row}:P{last_row},"CRITICAL")'),
        ("Avg Total Deployment Duration (wks)", f"=AVERAGE(J{first_row}:J{last_row})"),
        ("Items with Zero Float (No Schedule Flexibility)", f'=COUNTIF(O{first_row}:O{last_row},0)'),
    ]
    for label, val in facts:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=val)
        c.font = BOLD
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 10, 2: 32, 3: 16, 4: 8, 5: 8, 6: 9, 7: 9, 8: 9, 9: 8, 10: 10, 11: 9,
                  12: 11, 13: 10, 14: 9, 15: 8, 16: 10, 17: 26, 18: 55})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title, "first_row": first_row, "last_row": last_row}
