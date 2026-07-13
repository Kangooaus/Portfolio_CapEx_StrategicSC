from gen_common import *
from openpyxl.formatting.rule import CellIsRule
import db

HEADERS = ["Equip Ref", "Supplier", "Component / Sub-System", "Std Lead (wks)", "Current Lead (wks)",
           "Delay Prob. (0-1)", "Sched. Impact (1-5)", "Replace Difficulty (1-5)", "Composite Risk Score",
           "Risk Tier", "Single Source?", "Buffer Stock?", "Mitigation Action", "Status", "Program ID"]


def _write_risk_rows(ws, r, rows, program_id):
    """rows: list of dicts from db.list_risk_items()."""
    for ri in rows:
        eq, sup, comp = ri["equip_ref"], ri["supplier"], ri["component"]
        stdlt, curlt = ri["std_lead"], ri["current_lead"]
        prob, sched, repl = ri["delay_prob"], ri["sched_impact"], ri["replace_difficulty"]
        single = "YES" if ri["single_source"] == "Yes" else "No"
        buf = ri["buffer_stock"]
        mit, status = ri["mitigation"], ri["status"]
        ws.cell(row=r, column=1, value=eq)
        ws.cell(row=r, column=2, value=sup)
        ws.cell(row=r, column=3, value=comp)
        ws.cell(row=r, column=4, value=stdlt if stdlt else "N/A").font = BLUE_INPUT
        ws.cell(row=r, column=5, value=curlt if curlt else "N/A").font = BLUE_INPUT
        ws.cell(row=r, column=6, value=prob).number_format = PCT1
        ws.cell(row=r, column=6).font = BLUE_INPUT
        ws.cell(row=r, column=7, value=sched).font = BLUE_INPUT
        ws.cell(row=r, column=8, value=repl).font = BLUE_INPUT
        score = ws.cell(row=r, column=9, value=f"=F{r}*G{r}*H{r}")
        score.number_format = CUR2
        ws.cell(row=r, column=10,
                value=f'=IF(OR(K{r}="YES",I{r}>20),IF(I{r}>20,"CRITICAL",IF(K{r}="YES","CRITICAL","HIGH")),IF(I{r}>8,"HIGH",IF(I{r}>2,"MODERATE","LOW")))')
        ws.cell(row=r, column=11, value=single)
        ws.cell(row=r, column=12, value=buf)
        mc = ws.cell(row=r, column=13, value=mit); mc.alignment = LEFT_WRAP
        ws.cell(row=r, column=14, value=status)
        pid = ws.cell(row=r, column=15, value=program_id)
        pid.font = BLUE_INPUT
        pid.alignment = CENTER
        for c in range(1, 16):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    return r


def _summary_block(ws, row, first_row, last_row, title):
    row = section_header(ws, row, 1, title, 2, 3)
    stats = [
        ("Total Components Tracked", f"=COUNTA(A{first_row}:A{last_row})"),
        ("Single-Source Components", f'=COUNTIF(K{first_row}:K{last_row},"YES")'),
        ("Avg Composite Risk Score", f"=AVERAGE(I{first_row}:I{last_row})"),
        ("Max Risk Score (Worst Item)", f"=MAX(I{first_row}:I{last_row})"),
        ("CRITICAL Tier Items", f'=COUNTIF(J{first_row}:J{last_row},"CRITICAL")'),
        ("HIGH Tier Items", f'=COUNTIF(J{first_row}:J{last_row},"HIGH")'),
    ]
    stat_rows = {}
    keys = ["total", "single_source", "avg_risk", "max_risk", "critical_count", "high_count"]
    for key, (label, formula) in zip(keys, stats):
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.number_format = CUR2
        c.font = BOLD
        c.border = BORDER_ALL
        stat_rows[key] = row
        row += 1
    return row, stat_rows


def build(wb):
    ws = wb.create_sheet("S16_Supply_Chain_Risk")
    set_tab_color(ws, 3)
    row = title_block(ws, 3, "S16", "Supply Chain Risk & Lead-Time Analysis — CapEx Equipment Program",
                       "Risk Score = Delay Probability x Schedule Impact Score x Replacement Difficulty | "
                       "Heatmap tiers: LOW / MODERATE / HIGH / CRITICAL | Single-source components auto-flagged CRITICAL if Risk Score > 20 | "
                       "Program ID column enables portfolio-wide rollups",
                       n_cols=15)
    header_row = write_headers(ws, row, 1, HEADERS, 3)
    first_row = header_row
    r = header_row
    r = _write_risk_rows(ws, r, db.list_risk_items(program_ref="PRG-001"), "PRG-001")
    last_row = r - 1
    row = r + 2

    ws.conditional_formatting.add(f"J{first_row}:J{last_row}",
                                   CellIsRule(operator="equal", formula=['"CRITICAL"'], fill=PatternFill("solid", fgColor=RAG_RED)))
    ws.conditional_formatting.add(f"J{first_row}:J{last_row}",
                                   CellIsRule(operator="equal", formula=['"HIGH"'], fill=PatternFill("solid", fgColor="FFD9B3")))
    ws.conditional_formatting.add(f"J{first_row}:J{last_row}",
                                   CellIsRule(operator="equal", formula=['"MODERATE"'], fill=PatternFill("solid", fgColor=RAG_AMBER)))
    ws.conditional_formatting.add(f"J{first_row}:J{last_row}",
                                   CellIsRule(operator="equal", formula=['"LOW"'], fill=PatternFill("solid", fgColor=RAG_GREEN)))

    row = section_header(ws, row, 1, "SUPPLY CHAIN RISK HEATMAP SUMMARY — PRG-001 Greenfield Expansion Phase II", 4, 3)
    row = write_headers(ws, row, 1, ["Risk Tier", "Count", "% of Items", "Action Required"], 3)
    for tier, action in [
        ("CRITICAL", "Immediate VP-level escalation; daily status; dedicated mitigation team"),
        ("HIGH", "Weekly executive review; mitigation plan required within 5 business days"),
        ("MODERATE", "Bi-weekly review; mitigation plan in place; monitor for deterioration"),
        ("LOW", "Standard monitoring; quarterly supplier check-in sufficient"),
    ]:
        ws.cell(row=row, column=1, value=tier)
        ws.cell(row=row, column=2, value=f'=COUNTIF(J{first_row}:J{last_row},A{row})')
        pct = ws.cell(row=row, column=3, value=f"=B{row}/{last_row - first_row + 1}"); pct.number_format = PCT1
        ws.cell(row=row, column=4, value=action).alignment = LEFT_WRAP
        f = rag_fill(tier)
        if f:
            ws.cell(row=row, column=1).fill = f
        for c in range(1, 5):
            ws.cell(row=row, column=c).border = BORDER_ALL
        row += 1
    row += 1

    row, prg1_stats = _summary_block(ws, row, first_row, last_row, "AGGREGATE RISK STATISTICS — PRG-001 Greenfield Expansion Phase II")
    row += 1

    # --- Program 2 block ---
    row = section_header(ws, row, 1, "PRG-002 RISK REGISTER — Riverside Automation Upgrade Phase I", 15, 3)
    prg2_header_row = write_headers(ws, row, 1, HEADERS, 3)
    prg2_first_row = prg2_header_row
    r = prg2_header_row
    r = _write_risk_rows(ws, r, db.list_risk_items(program_ref="PRG-002"), "PRG-002")
    prg2_last_row = r - 1
    row = r + 1

    ws.conditional_formatting.add(f"J{prg2_first_row}:J{prg2_last_row}",
                                   CellIsRule(operator="equal", formula=['"CRITICAL"'], fill=PatternFill("solid", fgColor=RAG_RED)))
    ws.conditional_formatting.add(f"J{prg2_first_row}:J{prg2_last_row}",
                                   CellIsRule(operator="equal", formula=['"HIGH"'], fill=PatternFill("solid", fgColor="FFD9B3")))
    ws.conditional_formatting.add(f"J{prg2_first_row}:J{prg2_last_row}",
                                   CellIsRule(operator="equal", formula=['"MODERATE"'], fill=PatternFill("solid", fgColor=RAG_AMBER)))
    ws.conditional_formatting.add(f"J{prg2_first_row}:J{prg2_last_row}",
                                   CellIsRule(operator="equal", formula=['"LOW"'], fill=PatternFill("solid", fgColor=RAG_GREEN)))

    row, prg2_stats = _summary_block(ws, row, prg2_first_row, prg2_last_row, "AGGREGATE RISK STATISTICS — PRG-002 Riverside Automation Upgrade Phase I")

    autosize(ws, {1: 9, 2: 22, 3: 32, 4: 10, 5: 11, 6: 11, 7: 10, 8: 12, 9: 13, 10: 10, 11: 10, 12: 10, 13: 50, 14: 13, 15: 12})
    freeze_below(ws, header_row + 1)
    return {
        "sheet": ws.title, "first_row": first_row, "last_row": last_row,
        "program_id_col": "O",
        "prg2_first_row": prg2_first_row, "prg2_last_row": prg2_last_row,
        "prg1_avg_risk_cell": f"B{prg1_stats['avg_risk']}",
        "prg1_single_source_cell": f"B{prg1_stats['single_source']}",
        "prg2_avg_risk_cell": f"B{prg2_stats['avg_risk']}",
        "prg2_single_source_cell": f"B{prg2_stats['single_source']}",
        "prg2_total_cell": f"B{prg2_stats['total']}",
    }
