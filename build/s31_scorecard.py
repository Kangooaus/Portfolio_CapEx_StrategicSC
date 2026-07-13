from gen_common import *

WEIGHTS = [
    ("Delivery Performance (On-Time %)", 0.25, "Historical on-time delivery rate vs committed dates"),
    ("Quality (Defect Rate / FAT Pass Rate)", 0.20, "First-pass FAT acceptance rate; incoming inspection defect rate"),
    ("Commercial (Pricing Competitiveness)", 0.20, "Benchmark vs market; responsiveness; payment terms"),
    ("Technical Capability (Spec Compliance)", 0.25, "Meets or exceeds technical specification; engineering support quality"),
    ("Program Support (Communication / PM)", 0.10, "Responsiveness; dedicated PM; escalation handling"),
]

# Supplier, EqRef, Region, QualStage, Delivery, Quality, Commercial, Technical, Support, Status, LastAudit, NextReview, Notes
SUPPLIERS = [
    ("Edwards Vacuum", "EQ-001", "UK", "AVL — Approved", 4, 4, 3, 4, 4, "APPROVED", "2025-Q1", "2025-Q3",
     "Reliable supplier; post-Brexit logistics occasionally impacts lead time; alt-vendor qual complete"),
    ("Pfeiffer Vacuum", "EQ-002", "DE", "AVL — Conditional", 3, 5, 3, 5, 3, "CONDITIONAL", "2024-Q3", "2025-Q2",
     "Single-source; HIGH supply risk. Conditional approval pending Shimadzu alt qualification."),
    ("Thermco Systems", "EQ-003", "USA", "AVL — Preferred", 5, 5, 4, 5, 5, "PREFERRED", "2024-Q4", "2025-Q4",
     "Best-in-class performance; strong PM support; BTU validated as alt; no concerns"),
    ("Tokyo Electron Ltd (TEL)", "EQ-004", "JP", "AVL — Preferred", 4, 5, 3, 5, 4, "PREFERRED", "2024-Q3", "2025-Q3",
     "Premium supplier; higher commercial cost justified by TCO model; JPY FX hedged"),
    ("Brooks Automation", "EQ-005", "USA", "AVL — Approved", 4, 4, 4, 4, 4, "APPROVED", "2025-Q1", "2025-Q3",
     "Strong delivery and quality; MES integration complexity is program risk not supplier risk"),
    ("Daifuku", "EQ-006", "JP", "AVL — Conditional", 3, 4, 3, 4, 3, "CONDITIONAL", "2024-Q4", "2025-Q2",
     "Single-source for overhead track; commercial score impacted by $85K change order risk"),
    ("Air Liquide Engineering", "EQ-007", "FR", "Qualification In Progress", 3, 3, 3, 4, 3, "IN QUALIFICATION", "N/A", "2025-Q2",
     "Quote still under negotiation; hazmat permit risk reduces score; full audit scheduled Q2"),
    ("Linde Engineering", "EQ-008", "DE", "AVL — Approved", 4, 4, 4, 4, 4, "APPROVED", "2024-Q3", "2025-Q4",
     "Strong supplier; existing site gas supply contract provides leverage"),
    ("Siemens AG", "EQ-009", "DE", "AVL — Preferred", 5, 5, 4, 5, 5, "PREFERRED", "2024-Q2", "2025-Q4",
     "Strategic preferred supplier; highest reliability score in portfolio"),
    ("Inductive Automation", "EQ-010", "USA", "AVL — Approved", 5, 5, 5, 4, 4, "APPROVED", "2024-Q4", "2025-Q4",
     "Software vendor; excellent support; low supply risk"),
    ("ABB Ltd", "EQ-011", "CH", "AVL — Approved", 4, 4, 4, 4, 4, "APPROVED", "2024-Q3", "2025-Q4",
     "Established supplier; transformer lead time extended but within program tolerance"),
    ("Daikin Applied", "EQ-012", "JP", "AVL — Approved", 4, 4, 3, 4, 4, "APPROVED", "2024-Q4", "2025-Q3",
     "Solid supplier; glycol loop interface must be finalized before FAT — see CR-012"),
    ("Busch Vacuum", "EQ-013", "DE", "AVL — Approved", 4, 4, 4, 4, 4, "APPROVED", "2024-Q3", "2025-Q4",
     "Strong alt to Edwards for pump systems; validated as secondary source"),
    ("Applied Materials (AMAT)", "EQ-014", "USA", "AVL — Preferred", 4, 5, 3, 5, 5, "PREFERRED", "2024-Q2", "2025-Q4",
     "Strategic OEM relationship; highest-value PO in program; excellent technical support"),
    ("Mobile Industrial Robots (MiR)", "EQ-015", "DK", "AVL — Approved", 4, 4, 4, 4, 3, "APPROVED", "2025-Q1", "2025-Q3",
     "Strong fleet management platform; PM support slightly below average"),
    ("Shimadzu Corp (Alt EQ-002)", "EQ-002", "JP", "Qualification In Progress", None, None, None, 3, None, "IN QUALIFICATION", "N/A", "2025-Q3",
     "Initiated as alt to Pfeiffer per CR-007; TMP-3203L under technical evaluation; 90-day qual program"),
    ("BTU International (Alt EQ-003)", "EQ-003", "USA", "AVL — Approved", 4, 4, 4, 4, 4, "APPROVED", "2024-Q2", "2025-Q4",
     "Pre-qualified as secondary to Thermco; compatible process performance; available as backup"),
    ("Matheson Gas (Alt EQ-007)", "EQ-007", "USA", "RFQ Issued", None, None, 3, 3, None, "MONITORING", "N/A", "2025-Q2",
     "RFQ issued as alternative to Air Liquide; pricing and delivery terms under review"),
]

HEADERS = ["Supplier", "Equip Ref", "Region", "Qual Stage", "Delivery (1-5)", "Quality (1-5)", "Commercial (1-5)",
           "Technical (1-5)", "Program Support (1-5)", "Composite Weighted Score", "Supplier Status",
           "Last Audit Date", "Next Review Date", "Qualification Notes"]


def build(wb):
    ws = wb.create_sheet("S31_Vendor_Scorecard")
    set_tab_color(ws, 5)
    row = title_block(ws, 5, "S31", "Vendor Scorecard & Qualification Status — CapEx Equipment Suppliers",
                       "Scores suppliers on delivery, quality, commercial, technical, and support dimensions | "
                       "Qualification stage tracks RFI -> RFQ -> AVL (Approved Vendor List) | Inputs in BLUE", n_cols=14)

    row = section_header(ws, row, 1, "SCORING DIMENSION WEIGHTS", 3, 5)
    row = write_headers(ws, row, 1, ["Dimension", "Weight", "Description"], 5)
    for dim, wt, desc in WEIGHTS:
        ws.cell(row=row, column=1, value=dim)
        c = ws.cell(row=row, column=2, value=wt); c.number_format = PCT1; c.font = BLUE_INPUT
        ws.cell(row=row, column=3, value=desc).alignment = LEFT_WRAP
        for c in range(1, 4):
            ws.cell(row=row, column=c).border = BORDER_ALL
        row += 1
    row += 1

    row = section_header(ws, row, 1, "SUPPLIER SCORECARD & QUALIFICATION MATRIX", 14, 5)
    header_row = write_headers(ws, row, 1, HEADERS, 5)
    first_row = header_row
    r = header_row
    for (sup, eq, region, stage, d, q, c, t, s, status, audit, nextrev, notes) in SUPPLIERS:
        ws.cell(row=r, column=1, value=sup)
        ws.cell(row=r, column=2, value=eq)
        ws.cell(row=r, column=3, value=region)
        ws.cell(row=r, column=4, value=stage)
        for i, v in enumerate([d, q, c, t, s]):
            cc = ws.cell(row=r, column=5 + i, value=v if v is not None else "N/A")
            if v is not None:
                cc.font = BLUE_INPUT
        if all(v is not None for v in [d, q, c, t, s]):
            score = ws.cell(row=r, column=10, value=f"=0.25*E{r}+0.2*F{r}+0.2*G{r}+0.25*H{r}+0.1*I{r}")
            score.number_format = CUR2
        else:
            ws.cell(row=r, column=10, value="—")
        stc = ws.cell(row=r, column=11, value=status)
        if status == "PREFERRED":
            stc.fill = PatternFill("solid", fgColor="A9D18E")
        elif status == "APPROVED":
            stc.fill = PatternFill("solid", fgColor=RAG_GREEN)
        elif status == "CONDITIONAL":
            stc.fill = PatternFill("solid", fgColor=RAG_AMBER)
        elif status == "IN QUALIFICATION":
            stc.fill = PatternFill("solid", fgColor="DDEBF7")
        elif status == "MONITORING":
            stc.fill = PatternFill("solid", fgColor="FFF2CC")
        ws.cell(row=r, column=12, value=audit)
        ws.cell(row=r, column=13, value=nextrev)
        nc = ws.cell(row=r, column=14, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 15):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "VENDOR QUALIFICATION SUMMARY", 2, 5)
    stats = [
        ("Total Suppliers Tracked", f"=COUNTA(A{first_row}:A{last_row})", CUR0),
        ("Preferred Suppliers (AVL)", f'=COUNTIF(K{first_row}:K{last_row},"PREFERRED")', CUR0),
        ("Approved Suppliers (AVL)", f'=COUNTIF(K{first_row}:K{last_row},"APPROVED")', CUR0),
        ("Conditional / Monitoring", f'=COUNTIF(K{first_row}:K{last_row},"CONDITIONAL")+COUNTIF(K{first_row}:K{last_row},"MONITORING")', CUR0),
        ("In Qualification", f'=COUNTIF(K{first_row}:K{last_row},"IN QUALIFICATION")', CUR0),
        ("Avg Composite Score (Active AVL)", f'=AVERAGEIF(J{first_row}:J{last_row},">0")', CUR2),
    ]
    for label, formula, fmt in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 26, 2: 10, 3: 8, 4: 22, 5: 11, 6: 11, 7: 12, 8: 11, 9: 14, 10: 15, 11: 15, 12: 12, 13: 13, 14: 50})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
