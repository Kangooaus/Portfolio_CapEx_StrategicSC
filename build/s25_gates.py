from gen_common import *

GATES = [
    ("G0", "Program Concept & Business Case", "2025-02-28", "2025-03-10", "APPROVED", 1.00, "VP Engineering + CFO", "2025-03-10", 0, "GO",
     "Business case approved. Scenario B selected. AR-2025-0082 submitted. All G0 criteria met."),
    ("G1", "Supplier Selection & AR Approval", "2025-04-07", "2025-04-05", "APPROVED", 0.95, "VP Engineering + CFO", "2025-04-07", 1, "CONDITIONAL GO",
     "AR approved. All POs placed except EQ-007 (Air Liquide quote negotiation ongoing). Conditional GO: EQ-007 PO must be placed within 2 weeks."),
    ("G2", "Equipment Build & FAT Complete", "2025-09-01", "2025-09-08", "IN PROGRESS", 0.60, "Director of Engineering", "TBD", 3, "PENDING",
     "EQ-003 FAT complete. EQ-004, EQ-014 FAT scheduled. EQ-002 at risk due to Pfeiffer lead time. 3 open blockers: EQ-002 delivery, EQ-007 hazmat permit, EQ-006 civil drawing freeze."),
    ("G3", "Site Installation & Utility Commissioning", "2025-10-27", "2025-10-27", "NOT STARTED", 0.00, "Program Manager", "TBD", 0, "TBD",
     "Gate G3 not yet in scope. Entry criteria to be reviewed at G2 approval. Key dependency: all equipment delivered and installed; utility hookup complete."),
    ("G4", "Process Qualification (PQ) Complete", "2025-11-24", "2025-11-24", "NOT STARTED", 0.00, "Director of Engineering", "TBD", 0, "TBD",
     "Gate G4 requires: PQ protocol approved; first-article wafer data reviewed; yield >94%; equipment uptime demonstrated >90% over 30-day window."),
    ("G5", "Production Release & Ramp", "2025-12-08", "2025-12-08", "NOT STARTED", 0.00, "VP Engineering", "TBD", 0, "TBD",
     "Gate G5 requires: G4 approved; SOP training complete; spare parts inventory stocked; maintenance schedule published; manufacturing handover signed off."),
]

MILESTONES = [
    ("M-001", "G0", "Business case and scenario analysis", "ALL", "2025-03-10", "2025-03-10", "2025-03-10", "Sourabh Tarodekar", "COMPLETE", 1.00, "—",
     "Scenario B approved; S13 model signed off by Finance"),
    ("M-002", "G0", "Capital AR (AR-2025-0082) submitted to Finance", "ALL", "2025-03-19", "2025-03-19", "2025-03-19", "R. Patel", "COMPLETE", 1.00, "M-001",
     "AR submitted with full TCO and NPV justification"),
    ("M-003", "G1", "AR approval received from VP Eng + CFO", "ALL", "2025-04-07", "2025-04-05", "2025-04-05", "Sourabh Tarodekar", "COMPLETE", 1.00, "M-002",
     "Approved ahead of schedule — enables early PO placement"),
    ("M-004", "G1", "Long-lead POs placed (EQ-002, EQ-004, EQ-008, EQ-014)", "Multiple", "2025-04-07", "2025-04-05", "2025-04-05", "S. Kim", "COMPLETE", 1.00, "M-003",
     "All 4 long-lead POs placed. Supplier delivery schedules confirmed."),
    ("M-005", "G1", "EQ-007 hazmat permit application filed", "EQ-007", "2025-03-24", "2025-03-22", "2025-03-22", "D. Walsh", "COMPLETE", 1.00, "M-003",
     "Filed 2 days early. Consultant engaged. Permit approval pending."),
    ("M-006", "G1", "All remaining equipment POs placed", "Multiple", "2025-04-21", "2025-04-18", "2025-04-18", "S. Kim", "COMPLETE", 1.00, "M-003",
     "11 remaining POs placed. Full portfolio committed."),
    ("M-007", "G1", "FX hedge contracts executed (EUR + JPY)", "EQ-004/007", "2025-05-08", "2025-05-08", "2025-05-08", "R. Patel", "COMPLETE", 1.00, "M-004",
     "Forward contracts locked. EUR 1.09, JPY 149.0."),
    ("M-008", "G2", "EQ-003 Thermco FAT complete", "EQ-003", "2025-07-14", "2025-07-14", None, "M. Chen", "IN PROGRESS", 0.40, "M-006",
     "Protocol approved. FAT scheduled Week 22. Recipe transfer plan agreed."),
    ("M-009", "G2", "EQ-001 & EQ-013 pump FATs complete", "EQ-001/013", "2025-07-28", "2025-07-28", None, "S. Kim", "NOT STARTED", 0.00, "M-006",
     "Coordinated FAT schedule required; confirm with both suppliers"),
    ("M-010", "G2", "EQ-004 TEL batch furnace FAT complete (Japan)", "EQ-004", "2025-08-11", "2025-08-18", None, "M. Chen", "AT RISK", 0.15, "M-006",
     "Extended lead time (28 wks) puts FAT at Week 29 — 1 week behind plan"),
    ("M-011", "G2", "EQ-014 AMAT RTP FAT complete", "EQ-014", "2025-08-04", "2025-08-04", None, "M. Chen", "IN PROGRESS", 0.25, "M-004",
     "AMAT FAT protocol approved. Edge ring lot included. Site visit booked."),
    ("M-012", "G2", "EQ-002 Pfeiffer TMP FAT complete", "EQ-002", "2025-08-18", "2025-09-01", None, "S. Kim", "AT RISK", 0.05, "M-004",
     "CRITICAL: 26-wk LT pushes FAT to Week 30. Single-source risk active."),
    ("M-013", "G2", "EQ-007 hazmat permit received", "EQ-007", "2025-05-30", "2025-05-30", None, "D. Walsh", "IN PROGRESS", 0.50, "M-005",
     "Consultant tracking. Risk of 2-week overrun if permit delayed."),
    ("M-014", "G2", "EQ-006 conveyor civil drawings frozen", "EQ-006", "2025-05-19", "2025-05-19", None, "T. Okonkwo", "IN PROGRESS", 0.80, "M-006",
     "Layout review in progress. Freeze confirmed by Week 6."),
    ("M-015", "G3", "All equipment delivered to site", "ALL", "2025-09-08", "2025-09-08", None, "S. Kim", "NOT STARTED", 0.00, "M-012",
     "Delivery schedule contingent on EQ-002 and EQ-004 manufacturing completion"),
    ("M-016", "G3", "Site electrical sub-panel installation", "EQ-001", "2025-08-18", "2025-08-18", None, "T. Okonkwo", "IN PROGRESS", 0.35, "M-006",
     "Contractor engaged. Sub-panel installation Weeks 28-29."),
    ("M-017", "G3", "EQ-004 structural floor reinforcement complete", "EQ-004", "2025-07-28", "2025-07-28", None, "T. Okonkwo", "IN PROGRESS", 0.70, "M-006",
     "Structural work underway. External crane booked."),
    ("M-018", "G3", "All equipment installation and utility hookup complete", "ALL", "2025-10-13", "2025-10-13", None, "T. Okonkwo", "NOT STARTED", 0.00, "M-015",
     "4 wks install + 2 wks utility hookup per platform; parallel paths planned"),
    ("M-019", "G4", "Process qualification (PQ) initiated — first tool", "EQ-014", "2025-10-27", "2025-10-27", None, "M. Chen", "NOT STARTED", 0.00, "M-018",
     "EQ-014 RTP first to PQ; edge ring data from FAT will accelerate PQ"),
    ("M-020", "G4", "Process qualification (PQ) complete — all tools", "ALL", "2025-11-24", "2025-11-24", None, "M. Chen", "NOT STARTED", 0.00, "M-019",
     "5-week PQ phase; yield >94% and uptime >90% required"),
    ("M-021", "G5", "Manufacturing handover and production release", "ALL", "2025-12-08", "2025-12-08", None, "A. Novak", "NOT STARTED", 0.00, "M-020",
     "SOP training, spare parts stocked, maintenance schedule published"),
]

GATE_HEADERS = ["Gate", "Gate Name", "Target Date", "Actual/Forecast Date", "Gate Status", "Entry Criteria Met",
                "Approver", "Approval Date", "Open Blockers (count)", "Decision", "Notes"]
MS_HEADERS = ["Milestone ID", "Gate", "Milestone Description", "Equipment Ref", "Planned Date", "Forecast Date",
              "Actual Date", "Owner", "Status", "% Complete", "Predecessor", "Notes"]


def build(wb):
    ws = wb.create_sheet("S25_Milestone_Gate_Tracker")
    set_tab_color(ws, 5)
    row = title_block(ws, 5, "S25", "Program Milestone & Gate Review Tracker — Greenfield Expansion Phase II",
                       "Gate-controlled program: G0 Concept -> G1 Definition -> G2 Execution -> G3 Commissioning -> G4 Qualification -> G5 Production Release | "
                       "All gate entry criteria must be GREEN before approval; AMBER items require documented acceptance; RED items are blockers.",
                       n_cols=11)

    row = section_header(ws, row, 1, "GATE REVIEW STATUS SUMMARY", 11, 5)
    header_row = write_headers(ws, row, 1, GATE_HEADERS, 5)
    gate_first = row + 1
    r = gate_first
    for (g, name, target, actual, status, crit, appr, apdate, blockers, decision, notes) in GATES:
        ws.cell(row=r, column=1, value=g)
        ws.cell(row=r, column=2, value=name)
        ws.cell(row=r, column=3, value=target)
        ws.cell(row=r, column=4, value=actual)
        stc = ws.cell(row=r, column=5, value=status)
        stc.fill = PatternFill("solid", fgColor=RAG_GREEN if status == "APPROVED" else (RAG_AMBER if status == "IN PROGRESS" else "F2F2F2"))
        cm = ws.cell(row=r, column=6, value=crit); cm.number_format = PCT1
        ws.cell(row=r, column=7, value=appr)
        ws.cell(row=r, column=8, value=apdate)
        ws.cell(row=r, column=9, value=blockers).font = BLUE_INPUT
        dc = ws.cell(row=r, column=10, value=decision)
        dc.fill = PatternFill("solid", fgColor=RAG_GREEN if decision == "GO" else (RAG_AMBER if "CONDITIONAL" in decision else "F2F2F2"))
        nc = ws.cell(row=r, column=11, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 12):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    gate_last = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "DETAILED PROGRAM MILESTONES", 12, 5)
    header_row2 = write_headers(ws, row, 1, MS_HEADERS, 5)
    ms_first = row + 1
    r = ms_first
    for (mid, gate, desc, eq, plan, fcast, actual, owner, status, pct, pred, notes) in MILESTONES:
        ws.cell(row=r, column=1, value=mid)
        ws.cell(row=r, column=2, value=gate)
        ws.cell(row=r, column=3, value=desc)
        ws.cell(row=r, column=4, value=eq)
        ws.cell(row=r, column=5, value=plan)
        ws.cell(row=r, column=6, value=fcast)
        ws.cell(row=r, column=7, value=actual if actual else "—")
        ws.cell(row=r, column=8, value=owner)
        stc = ws.cell(row=r, column=9, value=status)
        if status == "COMPLETE":
            stc.fill = PatternFill("solid", fgColor=RAG_GREEN)
        elif status == "AT RISK":
            stc.fill = PatternFill("solid", fgColor=RAG_RED)
        elif status == "IN PROGRESS":
            stc.fill = PatternFill("solid", fgColor=RAG_AMBER)
        else:
            stc.fill = PatternFill("solid", fgColor="F2F2F2")
        pc = ws.cell(row=r, column=10, value=pct); pc.number_format = PCT1; pc.font = BLUE_INPUT
        ws.cell(row=r, column=11, value=pred)
        nc = ws.cell(row=r, column=12, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 13):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    ms_last = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "PROGRAM PROGRESS SUMMARY", 2, 5)
    stats = [
        ("Total Milestones", f"=COUNTA(A{ms_first}:A{ms_last})", CUR0),
        ("Milestones Complete", f'=COUNTIF(I{ms_first}:I{ms_last},"COMPLETE")', CUR0),
        ("Milestones In Progress", f'=COUNTIF(I{ms_first}:I{ms_last},"IN PROGRESS")', CUR0),
        ("Milestones At Risk or Blocked", f'=COUNTIF(I{ms_first}:I{ms_last},"AT RISK")', CUR0),
        ("Overall Program %", f"=AVERAGE(J{ms_first}:J{ms_last})", PCT1),
        ("Gates Complete / Approved", f'=COUNTIF(E{gate_first}:E{gate_last},"APPROVED")', CUR0),
        ("Open Blockers Across All Gates", f"=SUM(I{gate_first}:I{gate_last})", CUR0),
    ]
    stat_rows = {}
    stat_keys = ["total_milestones", "milestones_complete", "milestones_in_progress",
                 "milestones_at_risk", "overall_program_pct", "gates_approved", "open_blockers"]
    for key, (label, formula, fmt) in zip(stat_keys, stats):
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        stat_rows[key] = row
        row += 1

    autosize(ws, {1: 11, 2: 34, 3: 13, 4: 13, 5: 13, 6: 12, 7: 22, 8: 12, 9: 12, 10: 10, 11: 55})
    freeze_below(ws, gate_first)
    return {
        "sheet": ws.title, "ms_first": ms_first, "ms_last": ms_last,
        "gate_first": gate_first, "gate_last": gate_last,
        "overall_program_pct_cell": f"B{stat_rows['overall_program_pct']}",
        "open_blockers_cell": f"B{stat_rows['open_blockers']}",
        "gates_approved_cell": f"B{stat_rows['gates_approved']}",
        "milestones_at_risk_cell": f"B{stat_rows['milestones_at_risk']}",
    }
