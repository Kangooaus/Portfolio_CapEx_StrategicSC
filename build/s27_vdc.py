from gen_common import *

VDCS = [
    ("VDC-001", "ECO-003", "Applied Materials", "EQ-014", "CVD SiC edge ring material substitution (SiC density >=3.12 g/cm3 -> premium CVD SiC grade)",
     "Function", "Improved dimensional stability at high temp; supplier quality improvement", "2025-02-10", "YES",
     "LOW — dimensional spec maintained; thermal improvement expected", "ACCEPT — CONDITIONAL",
     "Re-validate thermal profile; confirm +/-1.5% uniformity spec met", "YES", "2025-02-28",
     "Triggered ECO-003; AMAT FSE on-site for re-validation"),
    ("VDC-002", "—", "Pfeiffer Vacuum", "EQ-002", "Magnet assembly supplier change — from EU Tier-2 to Asian Tier-2 supplier (equivalent grade spec)",
     "Form", "Tier-2 supplier consolidation; cost reduction in Pfeiffer supply chain", "2025-03-05", "YES",
     "HIGH — magnetic performance critical to TMP speed/accuracy", "REJECT",
     "Pfeiffer to provide full equivalency test data; re-submit with material certs", "YES", "—",
     "REJECTED: insufficient test data provided. Pfeiffer re-submitting with test certs Q3-2025"),
    ("VDC-003", "ECO-002", "Tokyo Electron Ltd", "EQ-004", "PID zone controller firmware update v3.8 -> v4.0 — new thermal ramp algorithm",
     "Fit/Function", "TEL global platform update — improved uniformity for 65nm+ processes", "2025-03-20", "YES",
     "LOW-MOD — algorithm change; verified by TEL at factory on identical system", "ACCEPT — CONDITIONAL",
     "Run 3-wafer PQ qualification lot before production release", "YES", "2025-04-08",
     "TEL global platform upgrade; triggered ECO-002 for recipe B3 update"),
    ("VDC-004", "—", "Brooks Automation", "EQ-005", "SCARA servo drive firmware update v2.3 -> v2.5 — improved torque compensation",
     "Function", "Bug fix — eliminates 0.05mm positional drift under thermal load", "2025-04-01", "NO",
     "LOW — positional improvement; no form/fit change", "ACCEPT",
     "No requalification required; monitor 30-day performance after update", "NO", "2025-04-08",
     "Brooks minor update; no qualification re-trigger required"),
    ("VDC-005", "ECO-009", "Linde Engineering", "EQ-008", "Pressure relief valve manufacturer change (same setpoint; different brand — Leser -> Emerson)",
     "Form", "Leser discontinuing model; Emerson equivalent specification", "2025-05-15", "YES",
     "MOD — safety-critical component; must verify setpoint and certification", "ACCEPT — CONDITIONAL",
     "Provide Emerson PED certification and hydrostatic test report", "YES", "Pending",
     "Triggered ECO-009 for pressure re-certification; Emerson certs received; review in progress"),
    ("VDC-006", "—", "Siemens AG", "EQ-009", "TIA Portal software v18 -> v19 migration — new tag management structure",
     "Fit", "Siemens mandatory platform migration for security patch compatibility", "2025-06-10", "YES",
     "LOW — software change; backward compatible; Siemens certified", "ACCEPT",
     "Apply per cybersecurity ECO-007 schedule; backup current config before update", "NO", "2025-06-20",
     "Coordinated with ECO-007 cybersecurity update; Siemens migration guide followed"),
    ("VDC-007", "—", "Daikin Applied", "EQ-012", "Refrigerant change R-410A -> R-454B (HFO blend) — regulatory compliance",
     "Function", "ASHRAE 34 update and EU F-Gas regulation phase-down of HFC refrigerants", "2025-07-01", "YES",
     "MOD — different refrigerant chemistry; system pressure slightly lower; seals reviewed", "ACCEPT — CONDITIONAL",
     "Daikin to provide updated system performance data and seal compatibility certs", "NO", "Pending",
     "Regulatory-driven; R-454B lower GWP. Daikin submitting updated commissioning data."),
]

HEADERS = ["VDC ID", "Linked ECO", "Supplier", "Equip Ref", "Change Description", "Change Type", "Supplier Reason",
           "Notified Date", "Customer Approval Req?", "Risk Assessment", "Disposition", "Conditions",
           "Requalif. Req?", "Approval Date", "Notes"]


def build(wb):
    ws = wb.create_sheet("S27_Vendor_Design_Changes")
    set_tab_color(ws, 5)
    row = title_block(ws, 5, "S27", "Vendor Design Changes (VDC) Register — Supplier-Initiated Changes",
                       "Tracks all supplier-initiated design changes — approval, risk, disposition | Owner: Sourabh Tarodekar | "
                       "Linked ECOs in S26_Engineering_Change_Orders", n_cols=15)
    header_row = write_headers(ws, row, 1, HEADERS, 5)
    first_row = header_row
    r = header_row
    for (vid, eco, sup, eq, desc, ctype, reason, notified, custapp, risk, disp, cond, requal, apdate, notes) in VDCS:
        ws.cell(row=r, column=1, value=vid)
        ws.cell(row=r, column=2, value=eco)
        ws.cell(row=r, column=3, value=sup)
        ws.cell(row=r, column=4, value=eq)
        ws.cell(row=r, column=5, value=desc).alignment = LEFT_WRAP
        ws.cell(row=r, column=6, value=ctype)
        ws.cell(row=r, column=7, value=reason).alignment = LEFT_WRAP
        ws.cell(row=r, column=8, value=notified)
        ws.cell(row=r, column=9, value=custapp)
        ws.cell(row=r, column=10, value=risk).alignment = LEFT_WRAP
        dc = ws.cell(row=r, column=11, value=disp)
        if disp == "ACCEPT":
            dc.fill = PatternFill("solid", fgColor=RAG_GREEN)
        elif "CONDITIONAL" in disp:
            dc.fill = PatternFill("solid", fgColor=RAG_AMBER)
        elif disp == "REJECT":
            dc.fill = PatternFill("solid", fgColor=RAG_RED)
        ws.cell(row=r, column=12, value=cond).alignment = LEFT_WRAP
        ws.cell(row=r, column=13, value=requal)
        ws.cell(row=r, column=14, value=apdate)
        nc = ws.cell(row=r, column=15, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 16):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "VDC SUMMARY", 2, 5)
    stats = [
        ("Total VDCs Logged", f"=COUNTA(A{first_row}:A{last_row})", CUR0),
        ("Accepted (incl. Conditional)", f'=COUNTIF(K{first_row}:K{last_row},"ACCEPT*")', CUR0),
        ("Rejected", f'=COUNTIF(K{first_row}:K{last_row},"REJECT")', CUR0),
        ("Requalification Required", f'=COUNTIF(M{first_row}:M{last_row},"YES")', CUR0),
    ]
    for label, formula, fmt in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 9, 2: 11, 3: 20, 4: 10, 5: 44, 6: 11, 7: 40, 8: 12, 9: 12, 10: 36, 11: 18, 12: 40, 13: 11, 14: 12, 15: 46})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
