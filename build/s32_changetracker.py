from gen_common import *

# ChangeID, RaisedDate, EqRef, Category, Desc, Reason, Cost(or None), SchedImpact, Risk, RaisedBy, ApprovedBy, Status, Notes
CHANGES = [
    ("CR-001", "2025-03-17", "EQ-004", "Installation Scope",
     "Add external 50-tonne crane hire and structural floor reinforcement for EQ-004 batch furnace installation",
     "Site walk revealed existing 3.5T facility crane is insufficient for 4,800 kg TEL furnace. Structural analysis confirmed floor reinforcement required.",
     62000, 1, "LOW", "T. Okonkwo (Facilities)", "PM — Sourabh Tarodekar", "APPROVED — IMPLEMENTED",
     "Crane booked. Structural work complete Week 14. Cost added to EQ-004 install line item."),
    ("CR-002", "2025-03-19", "EQ-001", "Facility Infrastructure",
     "Install new 100A dedicated electrical sub-panel and 35m cable run for EQ-001 vacuum pump set",
     "Existing electrical panel headroom 45 kW — insufficient for 4-pump set requiring 74 kW. Identified during site walk.",
     22000, 0, "LOW", "T. Okonkwo (Facilities)", "PM — Sourabh Tarodekar", "APPROVED — IMPLEMENTED",
     "Sub-panel installed Week 28-29. Electrical test passed. No schedule impact to EQ-001 delivery."),
    ("CR-003", "2025-03-24", "EQ-007", "Regulatory / Compliance",
     "Engage regulatory consultant for expedited hazmat permit for EQ-007 toxic gas cabinet",
     "Standard permit lead time 8-12 weeks exceeds program schedule allowance of 6 weeks. Permit is on critical path.",
     8500, 0, "HIGH", "D. Walsh (EHS)", "PM — Sourabh Tarodekar", "APPROVED — PENDING",
     "Consultant engaged 2025-03-25. Permit application filed. Estimated approval 2025-05-30. Monitor weekly."),
    ("CR-004", "2025-04-14", "EQ-003", "Technical Specification",
     "Add helium leak test to EQ-003 tube furnace FAT protocol per site safety standard SHE-042",
     "Quality review identified omission of He leak test in Thermco-supplied FAT protocol. SHE-042 mandates He leak testing.",
     None, 0, "LOW", "K. Tanaka (Quality)", "Quality Director", "APPROVED — IMPLEMENTED",
     "FAT protocol updated and approved by Quality 2025-04-18. No cost or schedule impact."),
    ("CR-005", "2025-04-21", "EQ-014", "Process Specification",
     "Add edge ring qualification lot (25 wafers) to EQ-014 AMAT RTP FAT protocol",
     "Process engineering identified edge-to-center non-uniformity risk at high ramp rates (>150C/s).",
     None, 0, "MODERATE", "M. Chen (Process Eng.)", "Director of Engineering", "APPROVED — IMPLEMENTED",
     "Protocol updated. 25-wafer edge ring lot included in FAT scope. No cost impact — AMAT absorbs wafer cost."),
    ("CR-006", "2025-05-05", "EQ-006", "Schedule Change",
     "Freeze Daifuku overhead conveyor layout by Week 6 — activate change control for any post-freeze deviation",
     "Daifuku contract specifies 4-week delay + $85K re-engineering fee for any layout change after civil interface freeze.",
     None, 0, "MODERATE", "Sourabh Tarodekar (PM)", "PM — Sourabh Tarodekar", "APPROVED — IMPLEMENTED",
     "Freeze notice issued 2025-05-07. Layout confirmed by all teams. Change control process active."),
    ("CR-007", "2025-05-05", "EQ-002", "Supplier Change",
     "Initiate parallel qualification of Shimadzu TMP-3203L as alternative to Pfeiffer EQ-002 turbomolecular pump",
     "EQ-002 is single-source with Pfeiffer. Risk accepted with condition of parallel alt vendor qualification.",
     45000, 0, "HIGH", "S. Kim (Supply Chain)", "VP Supply Chain", "UNDER REVIEW",
     "Shimadzu evaluation plan drafted. Test units requested. Qualification target: 90 days from Week 10 start."),
    ("CR-008", "2025-05-05", "EQ-004", "Technical Specification",
     "Execute JPY/USD forward currency hedge for EQ-004 TEL batch furnace ($1.36M JPY-denominated)",
     "EQ-004 invoiced in JPY. Finance modelled adverse scenario at 142 JPY/USD — $64K additional cost.",
     None, 0, "LOW", "R. Patel (Finance)", "CFO", "APPROVED — IMPLEMENTED",
     "Forward contract executed 2025-05-08. Rate locked at 149.0 JPY/USD through Q4-2025."),
    ("CR-009", "2025-05-12", "EQ-009", "Software / Integration",
     "Add IT/OT DMZ network infrastructure to CapEx scope to support SCADA cybersecurity compliance",
     "IT/OT review identified requirement for demilitarised zone (DMZ) per InfoSec policy OT-SEC-003.",
     45000, 0, "MODERATE", "P. Singh (IT/OT)", "PM — Sourabh Tarodekar", "UNDER REVIEW",
     "Network design spec in progress. Decision required by Week 15 to avoid impact to SCADA commissioning."),
    ("CR-010", "2025-05-12", "EQ-005", "Software / Integration",
     "Engage Brooks Automation software engineer on-site from Week 32 for MES/SEMI E30 software customisation",
     "Manufacturing review confirmed SEMI E30 compliance required for fab MES interface.",
     28000, 0, "MODERATE", "A. Novak (Manufacturing)", "Director of Engineering", "APPROVED — PENDING",
     "Brooks SE engagement confirmed. MES command set document due Week 28. T&E budget allocated."),
    ("CR-011", "2025-05-19", "EQ-013", "Technical Specification",
     "Update EQ-013 Roots blower installation sequence — must install after EQ-001 dry screw pumps",
     "Engineering review confirmed Roots blower (EQ-013) must be installed downstream of dry screw pumps (EQ-001).",
     None, 0, "LOW", "M. Chen (Process Eng.)", "Director of Engineering", "APPROVED — IMPLEMENTED",
     "Deployment timeline (S09) updated. Install sequence constraint documented in engineering notes."),
    ("CR-012", "2025-05-19", "EQ-012", "Facility Infrastructure",
     "Finalize glycol loop design for EQ-012 process chiller — complete engineering package by Week 14",
     "Mechanical engineering review confirmed glycol loop interface design must be finalized before Daikin FAT drawings.",
     None, 1, "MODERATE", "T. Okonkwo (Facilities)", "PM — Sourabh Tarodekar", "UNDER REVIEW",
     "Mechanical engineering team completing glycol loop design. Review meeting scheduled Week 13."),
]

HEADERS = ["Change ID", "Raised Date", "Equipment Ref", "Change Category", "Change Description", "Reason / Trigger",
           "Cost Impact (USD)", "Schedule Impact (wks)", "Quality/Tech Risk", "Raised By", "Approved By",
           "Change Status", "Implementation Notes"]


def build(wb, ar_contingency_ref):
    ws = wb.create_sheet("S32_Change_Tracker")
    set_tab_color(ws, 5)
    row = title_block(ws, 5, "S32", "Engineering Change Management Tracker — CapEx Phase II Program",
                       "All scope, technical, or budget changes must be logged here | Approved changes flow to AR update and decision log | "
                       "Owner accountable for implementation", n_cols=13)
    header_row = write_headers(ws, row, 1, HEADERS, 5)
    first_row = header_row
    r = header_row
    for (cid, rdate, eq, cat, desc, reason, cost, sched, risk, raisedby, apprby, status, notes) in CHANGES:
        ws.cell(row=r, column=1, value=cid)
        ws.cell(row=r, column=2, value=rdate)
        ws.cell(row=r, column=3, value=eq)
        ws.cell(row=r, column=4, value=cat)
        ws.cell(row=r, column=5, value=desc).alignment = LEFT_WRAP
        ws.cell(row=r, column=6, value=reason).alignment = LEFT_WRAP
        cc = ws.cell(row=r, column=7, value=cost if cost is not None else "-")
        if cost is not None:
            cc.number_format = USD0
            cc.font = BLUE_INPUT
        ws.cell(row=r, column=8, value=sched).font = BLUE_INPUT
        rc = ws.cell(row=r, column=9, value=risk)
        f = rag_fill(risk)
        if f:
            rc.fill = f
        ws.cell(row=r, column=10, value=raisedby)
        ws.cell(row=r, column=11, value=apprby)
        stc = ws.cell(row=r, column=12, value=status)
        if "IMPLEMENTED" in status:
            stc.fill = PatternFill("solid", fgColor=RAG_GREEN)
        elif "PENDING" in status:
            stc.fill = PatternFill("solid", fgColor="DDEBF7")
        elif "REVIEW" in status:
            stc.fill = PatternFill("solid", fgColor=RAG_AMBER)
        nc = ws.cell(row=r, column=13, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 14):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "CHANGE IMPACT SUMMARY", 2, 5)
    stats = [
        ("Total Change Requests Logged", f"=COUNTA(A{first_row}:A{last_row})", CUR0),
        ("Approved and Implemented", f'=COUNTIF(L{first_row}:L{last_row},"APPROVED — IMPLEMENTED")', CUR0),
        ("Approved Pending Implementation", f'=COUNTIF(L{first_row}:L{last_row},"APPROVED — PENDING")', CUR0),
        ("Total Under Review", f'=COUNTIF(L{first_row}:L{last_row},"UNDER REVIEW")', CUR0),
        ("Cumulative Cost Impact (USD)", f'=SUMIF(G{first_row}:G{last_row},">0")', USD0),
        ("Schedule Impact (wks)", f"=SUM(H{first_row}:H{last_row})", CUR0),
        ("HIGH or CRITICAL Budget Risk", f'=COUNTIF(I{first_row}:I{last_row},"HIGH")+COUNTIF(I{first_row}:I{last_row},"CRITICAL")', CUR0),
    ]
    cum_cost_row = None
    for i, (label, formula, fmt) in enumerate(stats):
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        if label.startswith("Cumulative"):
            cum_cost_row = row
        row += 1
    ws.cell(row=row, column=1, value="Contingency Reserve Used (vs S12 AR Contingency Reserve)").border = BORDER_ALL
    c = ws.cell(row=row, column=2, value=f"=B{cum_cost_row}/'{ar_contingency_ref[0]}'!{ar_contingency_ref[1]}")
    c.number_format = PCT1
    c.font = BOLD
    c.border = BORDER_ALL

    autosize(ws, {1: 9, 2: 12, 3: 10, 4: 20, 5: 44, 6: 44, 7: 12, 8: 12, 9: 12, 10: 20, 11: 22, 12: 20, 13: 48})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
