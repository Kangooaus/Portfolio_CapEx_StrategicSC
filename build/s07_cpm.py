from gen_common import *

# ActID, WBS, Desc, Resp, Dur, Pred, ES, EF, LS, LF, Float, Crit(Y/N), RiskFlag, Notes
ACTIVITIES = [
    ("A01", "1.1.1", "Program Kick-off & AR Execution", "PM / Finance", 1, "—", 1, 1, 1, 1, "LOW", "Start node — AR signed, POs authorized"),
    ("A02", "1.2.1", "RFQ Issue — Long-Lead Equipment", "Sourcing", 1, "A01", 2, 2, 2, 2, "LOW", "RFQs to Pfeiffer, TEL, AMAT, Linde"),
    ("A03", "1.3.1", "Equipment Technical Spec Review", "Process Eng", 2, "A01", 2, 3, 2, 3, "LOW", "Specs signed off before RFQ response due"),
    ("A04", "1.2.2", "Supplier Commercial Evaluation & BAFO", "Sourcing", 2, "A02,A03", 4, 5, 4, 5, "LOW", "Bid tabs; BAFO received from all"),
    ("A05", "1.2.7", "FX Forward Contract Execution", "Finance", 1, "A04", 5, 5, 5, 5, "MOD", "EUR+JPY hedges before PO — finance gate"),
    ("A06", "1.2.4", "PO Award — EQ-002 Pfeiffer TMP (CRITICAL)", "Sourcing", 1, "A04,A05", 6, 6, 6, 6, "HIGH", "CRITICAL PATH anchor — 26-wk mfg starts here"),
    ("A07", "1.2.3", "PO Award — EQ-014 AMAT RTP", "Sourcing", 1, "A04,A05", 6, 6, 7, 7, "MOD", "1-wk float; 30% deposit = $437.5K at PO"),
    ("A08", "1.2.5", "PO Award — EQ-004 TEL Batch Furnace", "Sourcing", 1, "A04,A05", 6, 6, 8, 8, "MOD", "2-wk float; JPY hedge confirmed"),
    ("A09", "1.2.6", "PO Award — All Remaining Equipment", "Sourcing", 2, "A04,A05", 6, 7, 6, 7, "LOW", "EQ-001,003,005,006,007,008,009,010,011,012,013,015"),
    ("A10", "1.3.4", "Site Layout & Equipment Placement Freeze", "Facilities", 3, "A01", 2, 4, 2, 4, "LOW", "Civil works blocked until layout approved"),
    ("A11", "1.6.4", "Gas System / Hazmat Permit", "Facilities/Regulatory", 12, "A10", 5, 16, 5, 16, "CRIT", "CRITICAL — permit on critical path; submit immediately"),
    ("A12", "1.6.2", "Electrical Infrastructure (Transformers)", "Electrical Eng", 10, "A10", 5, 14, 5, 14, "MOD", "480V feeds; EQ-011 transformer on order wk1"),
    ("A13", "1.6.1", "Floor Reinforcement — EQ-004 Zone", "Civil Eng", 6, "A10", 5, 10, 5, 10, "LOW", "Must complete before furnace delivery (Wk 28)"),
    ("A14", "1.6.3", "Cooling Loop Installation", "Mech Eng", 8, "A12", 15, 22, 15, 22, "LOW", "Glycol loop after electrical infrastructure"),
    ("A15", "1.4.2", "EQ-002 Pfeiffer TMP — Mfg & FAT (CRITICAL)", "Pfeiffer", 26, "A06", 7, 32, 7, 32, "CRIT", "CRITICAL PATH — longest manufacturing chain"),
    ("A16", "1.4.1", "EQ-014 AMAT RTP — Mfg & FAT", "AMAT", 24, "A07", 7, 30, 8, 31, "MOD", "1-wk float; highest-value item"),
    ("A17", "1.4.3", "EQ-004 TEL Batch Furnace — Mfg & FAT", "TEL", 28, "A08", 7, 34, 9, 36, "HIGH", "28-wk mfg; JPY risk; FAT 3 wks"),
    ("A18", "1.4.4", "EQ-003 Thermco Tube Furnace — Mfg & FAT", "Thermco", 20, "A09", 8, 27, 8, 27, "LOW", "FAT at Austin TX; recipe transfer"),
    ("A19", "1.4.5", "EQ-005 Brooks SCARA — Mfg & FAT", "Brooks", 14, "A09", 8, 21, 8, 21, "MOD", "MES integration tested at FAT"),
    ("A20", "1.4.6", "EQ-008 Linde Bulk Gas — Manufacturing", "Linde", 32, "A09", 8, 39, 8, 39, "MOD", "Longest-lead item in remaining equipment"),
    ("A21", "1.4.7", "Remaining Equipment — Mfg & FAT", "Various", 18, "A09", 8, 25, 8, 25, "LOW", "EQ-006,007,009,010,011,012,013,015"),
    ("A22", "1.5.2", "Freight & Customs — EUR Equipment", "Logistics", 3, "A18,A21", 26, 28, 26, 28, "LOW", "Road/air freight; customs clearance EUR items"),
    ("A23", "1.5.1", "Freight & Customs — JPY/EQ-002 (CRITICAL)", "Logistics", 3, "A15", 33, 35, 33, 35, "MOD", "CRITICAL: sea freight after Pfeiffer FAT"),
    ("A24", "1.5.1", "Freight & Customs — JPY Other (TEL/Daikin)", "Logistics", 3, "A17", 35, 37, 37, 39, "MOD", "TEL/Daikin/Daifuku sea freight"),
    ("A25", "1.7.1", "EQ-014 RTP Installation", "Installation", 2, "A16,A12,A14", 31, 32, 32, 33, "LOW", "RTP installed before furnaces"),
    ("A26", "1.7.3", "EQ-005 Robot Install & MES Integration", "Installation/IT", 3, "A19,A12", 22, 24, 22, 24, "MOD", "MES integration — critical dependency"),
    ("A27", "1.7.2", "EQ-003/004 Furnace Installation", "Installation", 3, "A18,A22,A13", 29, 31, 29, 31, "LOW", "Crane lift; N2 purge connection"),
    ("A28", "1.7.6", "EQ-002 TMP Installation (CRITICAL)", "Installation/Pfeiffer", 2, "A23", 36, 37, 36, 37, "CRIT", "CRITICAL PATH: TMPs installed week 36-37"),
    ("A29", "1.7.7", "EQ-008 Bulk Gas Final Installation", "Linde/Facilities", 2, "A20,A11", 40, 41, 40, 41, "MOD", "Permit must be closed; bulk vessel on-site"),
    ("A30", "1.7.4", "EQ-006 Daifuku Conveyor Install", "Daifuku/Civil", 4, "A24,A12", 38, 41, 38, 41, "HIGH", "Single-source; civil interface frozen Wk 6"),
    ("A31", "1.7.5", "Utility Tie-In — All Equipment", "Facilities", 4, "A25,A26,A27,A28", 38, 41, 38, 41, "LOW", "All utilities connected; interlock test"),
    ("A32", "1.3.2", "FAT Protocol Development", "Process Eng", 3, "A03", 4, 6, 4, 6, "LOW", "FAT protocols issued to all suppliers"),
    ("A33", "1.3.5", "MES/SCADA/DCS Integration Spec", "Controls/IT", 4, "A03", 4, 7, 4, 7, "MOD", "Integration spec required before FAT testing"),
    ("A34", "1.8.1", "G4 Qualification — EQ-014 RTP", "Process Eng", 3, "A25,A31", 42, 44, 42, 44, "LOW", "First tool qualified"),
    ("A35", "1.8.2", "G4 Qualification — Furnaces", "Process Eng", 4, "A27,A31", 42, 45, 42, 45, "MOD", "Temperature uniformity certification"),
    ("A36", "1.8.3", "G4 Qualification — Robots & MES", "Process Eng", 3, "A26,A31", 42, 44, 42, 44, "MOD", "Robot repeatability + MES validation"),
    ("A37", "1.8.4", "G4 Qualification — All Remaining", "Process Eng", 3, "A28,A29,A30,A31", 42, 44, 42, 44, "LOW", "All 15 platforms qualified"),
    ("A38", "1.8.5", "SOP Documentation & Operator Training", "Training/Ops", 3, "A34,A35,A36,A37", 45, 47, 44, 46, "LOW", "SOPs issued; all operators certified"),
    ("A39", "1.8.7", "G5 Production Release — Program Close", "PM/Ops", 2, "A38", 46, 47, 46, 47, "LOW", "Formal handover; program closed"),
]

HEADERS = ["Act ID", "WBS Ref", "Activity Description", "Responsible", "Duration (wks)",
           "Predecessor(s)", "Early Start (ES)", "Early Finish (EF)", "Late Start (LS)",
           "Late Finish (LF)", "Total Float", "Critical Path?", "Risk Flag", "Notes"]


def build(wb):
    ws = wb.create_sheet("S07_CPM_Master_Schedule")
    set_tab_color(ws, 2)
    row = title_block(ws, 2, "S07", "Critical Path Method (CPM) Master Schedule — Greenfield Expansion Phase II",
                       "Activity durations in weeks | Program start: Week 1 = Apr-2025 | Owner: Sourabh Tarodekar | "
                       "Critical path: EQ-002 Pfeiffer TMP chain = 46 weeks | Total Float = LS − ES = LF − EF | "
                       "Activities with Float = 0 are on the Critical Path.", n_cols=14)
    header_row = write_headers(ws, row, 1, HEADERS, 2)
    first_row = header_row
    r = header_row
    for (aid, wbs, desc, resp, dur, pred, es, ef, ls, lf, riskflag, notes) in ACTIVITIES:
        ws.cell(row=r, column=1, value=aid).font = BOLD
        ws.cell(row=r, column=2, value=wbs)
        ws.cell(row=r, column=3, value=desc)
        ws.cell(row=r, column=4, value=resp)
        ws.cell(row=r, column=5, value=dur).font = BLUE_INPUT
        ws.cell(row=r, column=6, value=pred).font = BLUE_INPUT
        ws.cell(row=r, column=7, value=es).font = BLUE_INPUT
        ws.cell(row=r, column=8, value=ef).font = BLUE_INPUT
        ws.cell(row=r, column=9, value=ls).font = BLUE_INPUT
        ws.cell(row=r, column=10, value=lf).font = BLUE_INPUT
        floatc = ws.cell(row=r, column=11, value=f"=I{r}-G{r}")
        crit = ws.cell(row=r, column=12, value=f'=IF(K{r}=0,"YES","NO")')
        rf = ws.cell(row=r, column=13, value=riskflag)
        fill = rag_fill(riskflag)
        if fill:
            rf.fill = fill
        nc = ws.cell(row=r, column=14, value=notes)
        nc.alignment = LEFT_WRAP
        for c in range(1, 15):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "CRITICAL PATH SUMMARY", 2, 2)
    facts = [
        ("Total program duration (critical path, weeks)", f"=MAX(H{first_row}:H{last_row})"),
        ("Number of critical path activities (Float = 0)", f'=COUNTIF(K{first_row}:K{last_row},0)'),
        ("Critical path sequence", "A01 → A06 → A15 → A23 → A28 → A31 → A34/35/36/37 → A38 → A39"),
        ("Longest chain", "EQ-002 Pfeiffer TMP: PO → 26-wk mfg → FAT → freight → install → PQ; spans Weeks 6-44"),
        ("Key schedule risk", "A11 Gas System / Hazmat Permit — 12-week permit must start Week 5; any delay blocks gas system install"),
        ("Key commercial risk", "A06 EQ-002 Pfeiffer PO — single-source; no float; 30-day PO delay = 30-day program delay"),
    ]
    for label, val in facts:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=val)
        c.border = BORDER_ALL
        c.alignment = LEFT_WRAP
        row += 1

    autosize(ws, {1: 8, 2: 8, 3: 44, 4: 20, 5: 11, 6: 15, 7: 8, 8: 8, 9: 8, 10: 8, 11: 8, 12: 10, 13: 9, 14: 50})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title, "first_row": first_row, "last_row": last_row}
