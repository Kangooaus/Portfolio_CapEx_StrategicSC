from gen_common import *

MILESTONES = [
    ("M01", "AR Approved — Phase II", "G0/G1", "2025-04-07", "APPROVED", "Sourabh Tarodekar",
     "Long-lead PO authority granted; cost centre CC-4421 open"),
    ("M02", "All Long-Lead POs Placed", "G1", "2025-04-28", "COMPLETE", "Sourcing",
     "EQ-002,004,008,014 POs placed; FX hedges executed"),
    ("M03", "Site Layout Frozen", "—", "2025-04-14", "APPROVED", "Facilities",
     "Civil works can proceed; no further layout changes"),
    ("M04", "Hazmat Permit Submitted", "—", "2025-04-14", "IN PROGRESS", "Regulatory",
     "Permit application filed; 12-wk processing time"),
    ("M05", "All Equipment POs Placed", "G1", "2025-05-12", "COMPLETE", "Sourcing",
     "Full PO portfolio placed; supplier schedule confirmed"),
    ("M06", "Site Utilities Complete (Elec + Cool)", "—", "2025-08-11", "ON TRACK", "Facilities",
     "Electrical feeds + glycol loop ready before delivery"),
    ("M07", "Hazmat Permit Received", "—", "2025-07-07", "ON TRACK", "Regulatory",
     "CRITICAL — blocks gas system install if delayed"),
    ("M08", "EQ-014 AMAT RTP FAT Complete", "G2", "2025-09-22", "ON TRACK", "Engineering",
     "First FAT complete; highest-value item"),
    ("M09", "EQ-002 Pfeiffer TMP FAT Complete", "G2", "2025-10-20", "CRITICAL PATH", "Engineering / Pfeiffer",
     "CRITICAL PATH — no float; monitor weekly"),
    ("M10", "All Equipment Delivered to Site", "G3", "2025-10-27", "ON TRACK", "Logistics",
     "All 15 platforms on-site; receipt inspection complete"),
    ("M11", "All Equipment Installed", "G3", "2025-11-10", "ON TRACK", "Installation",
     "Mechanical install + utility tie-in complete"),
    ("M12", "G4 Process Qualification Start", "G4", "2025-11-10", "PLANNED", "Process Eng",
     "PQ begins; first tools: EQ-014 RTP, EQ-003 Furnace"),
    ("M13", "Full Process Qualification Complete", "G4", "2025-12-01", "PLANNED", "Process Eng",
     "All 15 platforms in qualified state; PQ reports issued"),
    ("M14", "Operator Training Complete", "—", "2025-12-08", "PLANNED", "Training / Ops",
     "All operators trained + certified on SOPs"),
    ("M15", "G5 Production Release", "G5", "2025-12-22", "PLANNED", "Sourabh Tarodekar",
     "Formal handover to Operations; program closed"),
]

HEADERS = ["#", "Milestone", "Gate", "Target Date", "Status", "Owner", "Notes"]

GATES = [
    ("G0+G1", "Apr-25", "Approved"),
    ("G2", "Aug-25", "FAT Complete"),
    ("G3", "Oct-25", "Install"),
    ("G4", "Nov-25", "PQ Start"),
    ("G5", "Dec-25", "Production Release"),
]


def build(wb):
    ws = wb.create_sheet("S08_Program_Milestone_Roadmap")
    set_tab_color(ws, 2)
    row = title_block(ws, 2, "S08", "Program Milestone Roadmap — Greenfield Expansion Phase II",
                       "Phase-gate roadmap from AR approval to production release | Owner: Sourabh Tarodekar | "
                       "All dates Apr-Dec 2025 | Gates: G0 (Concept) -> G5 (Production Release)", n_cols=7)

    row = section_header(ws, row, 1, "PROGRAM GATES", 3, 2)
    row = write_headers(ws, row, 1, ["Gate", "Month", "Status Label"], 2)
    for g, m, s in GATES:
        ws.cell(row=row, column=1, value=g)
        ws.cell(row=row, column=2, value=m)
        ws.cell(row=row, column=3, value=s)
        for c in range(1, 4):
            ws.cell(row=row, column=c).border = BORDER_ALL
        row += 1
    row += 1

    row = section_header(ws, row, 1, "KEY PROGRAM MILESTONES", 7, 2)
    header_row = write_headers(ws, row, 1, HEADERS, 2)
    first_row = header_row
    r = header_row
    for (mid, name, gate, date, status, owner, notes) in MILESTONES:
        ws.cell(row=r, column=1, value=mid)
        ws.cell(row=r, column=2, value=name)
        ws.cell(row=r, column=3, value=gate)
        ws.cell(row=r, column=4, value=date)
        sc = ws.cell(row=r, column=5, value=status)
        if status in ("COMPLETE", "APPROVED"):
            sc.fill = PatternFill("solid", fgColor=RAG_GREEN)
        elif status in ("IN PROGRESS", "CRITICAL PATH"):
            sc.fill = PatternFill("solid", fgColor=RAG_AMBER if status == "IN PROGRESS" else RAG_RED)
        elif status == "ON TRACK":
            sc.fill = PatternFill("solid", fgColor="DDEBF7")
        elif status == "PLANNED":
            sc.fill = PatternFill("solid", fgColor="F2F2F2")
        ws.cell(row=r, column=6, value=owner)
        nc = ws.cell(row=r, column=7, value=notes)
        nc.alignment = LEFT_WRAP
        for c in range(1, 8):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1

    autosize(ws, {1: 6, 2: 34, 3: 8, 4: 12, 5: 15, 6: 22, 7: 55})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title, "first_row": first_row, "last_row": last_row}
