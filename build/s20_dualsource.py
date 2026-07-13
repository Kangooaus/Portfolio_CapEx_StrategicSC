from gen_common import *

# Commodity, PrimarySupplier, EquipRef, AltSupplier, QualStatus, RiskReduction, TargetCompletion, Notes
DUAL_SOURCE = [
    ("Turbomolecular Pumps", "Pfeiffer Vacuum", "EQ-002", "Shimadzu Corp (TMP-3203L)", "IN QUALIFICATION",
     "Eliminates single-source CRITICAL risk on program's highest-risk item", "2025-Q3",
     "90-day qualification program initiated per CR-007; test units requested"),
    ("Dry Screw Vacuum Pumps", "Edwards Vacuum", "EQ-001", "Busch Vacuum", "AVL — QUALIFIED",
     "Already-qualified alt reduces post-Brexit logistics exposure", "COMPLETE",
     "Busch already supplies EQ-013; cross-qualified as backup to Edwards"),
    ("High-Temp Tube Furnaces", "Thermco Systems", "EQ-003", "BTU International", "AVL — QUALIFIED",
     "Reduces exposure to single furnace OEM for core process step", "COMPLETE",
     "BTU pre-qualified; compatible process performance confirmed"),
    ("Batch Oxidation Furnaces", "Tokyo Electron Ltd", "EQ-004", "Kokusai Electric", "PRE-QUALIFIED",
     "Mitigates JPY/TEL concentration risk on second-largest CapEx line", "2025-Q4 (monitoring)",
     "Pre-qualified but not activated; TEL relationship strategic, monitored not urgent"),
    ("Process Gas Cabinets", "Air Liquide Engineering", "EQ-007", "Matheson Gas", "RFQ ISSUED",
     "Provides commercial leverage during active EQ-007 negotiation", "2025-Q2",
     "RFQ issued in parallel with Air Liquide negotiation; pricing/delivery under review"),
    ("Bulk Gas Storage & Delivery", "Linde Engineering", "EQ-008", "Air Products", "RFQ ISSUED",
     "Commercial leverage; long lead-time category benefits from dual-source", "2025-Q3",
     "Used as competitive tension during Linde negotiation (closed favorably)"),
    ("SCARA Robots", "Brooks Automation", "EQ-005", "Kawasaki Robotics", "TECHNICAL EVAL",
     "Reduces dependency on single robotics OEM for material handling", "2025-Q4",
     "Technical evaluation only; no immediate qualification driver — moderate priority"),
    ("Roots Blower Boosters", "Busch Vacuum", "EQ-013", "Edwards Vacuum", "AVL — QUALIFIED",
     "Mutual cross-qualification with EQ-001 Edwards / EQ-013 Busch pairing", "COMPLETE",
     "Edwards and Busch mutually qualified as alternates across both platforms"),
]

HEADERS = ["Commodity", "Primary Supplier", "Equip Ref", "Alternate Supplier", "Qualification Status",
           "Risk Reduction Rationale", "Target Completion", "Notes"]


def build(wb):
    ws = wb.create_sheet("S20_Dual_MultiSource_Strategy")
    set_tab_color(ws, 4)
    row = title_block(ws, 4, "S20", "Dual / Multi-Source Strategy — Qualification Status & Risk Reduction",
                       "Program: Greenfield Expansion Phase II | Owner: Sourabh Tarodekar / Strategic Sourcing | "
                       "8 commodities with active or completed dual-source programs | Directly reduces S16 supply chain risk exposure",
                       n_cols=8)
    header_row = write_headers(ws, row, 1, HEADERS, 4)
    first_row = header_row
    r = header_row
    for (comm, prim, eq, alt, status, rationale, target, notes) in DUAL_SOURCE:
        ws.cell(row=r, column=1, value=comm)
        ws.cell(row=r, column=2, value=prim)
        ws.cell(row=r, column=3, value=eq)
        ws.cell(row=r, column=4, value=alt)
        stc = ws.cell(row=r, column=5, value=status)
        if "QUALIFIED" in status:
            stc.fill = PatternFill("solid", fgColor=RAG_GREEN)
        elif status in ("IN QUALIFICATION", "PRE-QUALIFIED"):
            stc.fill = PatternFill("solid", fgColor=RAG_AMBER)
        else:
            stc.fill = PatternFill("solid", fgColor="DDEBF7")
        ws.cell(row=r, column=6, value=rationale).alignment = LEFT_WRAP
        ws.cell(row=r, column=7, value=target)
        nc = ws.cell(row=r, column=8, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 9):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "DUAL-SOURCE PROGRAM IMPACT SUMMARY", 2, 4)
    stats = [
        ("Commodities with Dual-Source Program", f"=COUNTA(A{first_row}:A{last_row})", CUR0),
        ("Qualified / AVL-Ready Alternates", f'=COUNTIF(E{first_row}:E{last_row},"AVL — QUALIFIED")', CUR0),
        ("Active Qualification Programs", f'=COUNTIF(E{first_row}:E{last_row},"IN QUALIFICATION")+COUNTIF(E{first_row}:E{last_row},"PRE-QUALIFIED")', CUR0),
        ("RFQ / Early-Stage Programs", f'=COUNTIF(E{first_row}:E{last_row},"RFQ ISSUED")+COUNTIF(E{first_row}:E{last_row},"TECHNICAL EVAL")', CUR0),
    ]
    for label, formula, fmt in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 24, 2: 20, 3: 10, 4: 24, 5: 18, 6: 44, 7: 16, 8: 46})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
