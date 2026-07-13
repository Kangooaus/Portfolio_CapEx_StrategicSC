from gen_common import *

DIMENSIONS = [
    ("Financial Return (NPV / IRR)", 0.25, 5, 3, "Greenfield's $9.5M NPV and 14.2% IRR dwarf Riverside's $1.85M/16.8% in absolute terms"),
    ("Strategic Fit / Business Priority", 0.20, 5, 3, "Greenfield is core capacity for the primary revenue driver; Riverside is an efficiency play"),
    ("Supply Chain / Execution Risk (higher score = lower risk)", 0.15, 3, 4, "Greenfield carries a HIGH-tier single-source pump risk; Riverside's risk profile is materially lighter"),
    ("Schedule Readiness / Time to Value", 0.15, 4, 2, "Greenfield is already at G2 execution; Riverside is still FEL-2, pre-AR"),
    ("Capital Efficiency (impact per $ requested)", 0.15, 3, 4, "Riverside's smaller ask and 3.1-yr payback are more capital-efficient than Greenfield's $16M ask"),
    ("Organizational Readiness", 0.10, 5, 3, "Greenfield has a dedicated, established program team; Riverside's PM and team are still standing up"),
]


def build(wb, s33):
    ws = wb.create_sheet("S35_Portfolio_Prioritization")
    set_tab_color(ws, 6)
    row = title_block(ws, 6, "S35", "Portfolio Prioritization — Capital Allocation Decision Framework",
                       "Portfolio Director: Sourabh Tarodekar | Weighted scorecard used to rank active + proposed programs "
                       "each planning cycle | Same weighting methodology as S13_Scenario_Analysis, applied program-vs-program "
                       "instead of scenario-vs-scenario", n_cols=9)

    row = section_header(ws, row, 1, "SCORING DIMENSION WEIGHTS & RATIONALE", 9, 6)
    headers = ["Dimension", "Weight", "PRG-001 Score (1-5)", "PRG-002 Score (1-5)", "Wtd PRG-001", "Wtd PRG-002",
               "Rationale"]
    row = write_headers(ws, row, 1, headers, 6)
    first_row = row
    r = row
    for dim, wt, s1, s2, rationale in DIMENSIONS:
        ws.cell(row=r, column=1, value=dim)
        wc = ws.cell(row=r, column=2, value=wt); wc.number_format = PCT1; wc.font = BLUE_INPUT
        ws.cell(row=r, column=3, value=s1).font = BLUE_INPUT
        ws.cell(row=r, column=4, value=s2).font = BLUE_INPUT
        w1 = ws.cell(row=r, column=5, value=f"=B{r}*C{r}"); w1.number_format = CUR2
        w2 = ws.cell(row=r, column=6, value=f"=B{r}*D{r}"); w2.number_format = CUR2
        ws.cell(row=r, column=7, value=rationale).alignment = LEFT_WRAP
        for c in range(1, 8):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1

    ws.cell(row=r, column=1, value="TOTAL WEIGHTED SCORE").font = BOLD
    tw = ws.cell(row=r, column=2, value=f"=SUM(B{first_row}:B{last_row})"); tw.number_format = PCT1; tw.font = BOLD
    ts1 = ws.cell(row=r, column=5, value=f"=SUM(E{first_row}:E{last_row})"); ts1.number_format = CUR2; ts1.font = BOLD
    ts2 = ws.cell(row=r, column=6, value=f"=SUM(F{first_row}:F{last_row})"); ts2.number_format = CUR2; ts2.font = BOLD
    for c in range(1, 8):
        ws.cell(row=r, column=c).border = BORDER_ALL
        ws.cell(row=r, column=c).fill = zone_fill_light(6)
    total_row = r
    row = r + 2

    row = section_header(ws, row, 1, "RECOMMENDED SEQUENCING", 2, 6)
    ws.cell(row=row, column=1, value="#1 Ranked Program").border = BORDER_ALL
    rank1 = ws.cell(row=row, column=2, value=f'=IF(E{total_row}>=F{total_row},"PRG-001 — Greenfield Expansion Phase II","PRG-002 — Riverside Automation Upgrade Phase I")')
    rank1.font = BOLD
    rank1.border = BORDER_ALL
    row += 1
    ws.cell(row=row, column=1, value="#1 Weighted Score").border = BORDER_ALL
    c = ws.cell(row=row, column=2, value=f"=MAX(E{total_row},F{total_row})"); c.number_format = CUR2; c.border = BORDER_ALL
    row += 2

    row = section_header(ws, row, 1, "DECISION SUMMARY", 9, 6)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=9)
    ws.cell(row=row, column=1, value=(
        "Greenfield Expansion Phase II ranks #1 (4.25/5.0) and remains the portfolio's priority commitment — it is already "
        "AR-approved and in execution, and no action changes that. Riverside Automation Upgrade Phase I ranks #2 (3.15/5.0): "
        "recommend continuing FEL-2 feasibility work and targeting AR submission once Greenfield's peak capital draw "
        "(Q3-2025, per S14_CashFlow_Model) has passed, so the two programs' spend curves don't compete for the same "
        "capital window. Riverside's lower risk profile and faster payback make it an attractive next-in-queue candidate "
        "once schedule and organizational readiness catch up to Greenfield's."
    )).alignment = LEFT_WRAP
    ws.row_dimensions[row].height = 75

    autosize(ws, {1: 34, 2: 9, 3: 15, 4: 15, 5: 12, 6: 12, 7: 50, 8: 10, 9: 10})
    freeze_below(ws, first_row)
    return {"sheet": ws.title, "total_row": total_row}
