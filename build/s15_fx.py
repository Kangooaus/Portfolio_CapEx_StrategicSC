from gen_common import *

# eq_idx (1-based EQ number), Description, Currency, Hedge Status, Hedge Rate, Notes
FX_ITEMS = [
    (1, "Dry Screw Vacuum Pump (x4)", "EUR", "HEDGED", 1.085, "Forward contract executed; rate locked at 1.085 through Q3-2025"),
    (2, "Turbomolecular Pump (x3)", "EUR", "HEDGED", 1.090, "Forward contract at baseline rate; expires Q3-2025"),
    (4, "Batch Oxidation Furnace — TEL (x2)", "JPY", "HEDGED", 149.0, "Forward contract at 149.0 JPY/USD; DEC-003 + CR-008 reference"),
    (6, "Overhead Conveyor — Daifuku", "JPY", "HEDGED", 149.0, "Hedged as part of JPY program-wide forward contract"),
    (7, "Gas Handling Cabinet (x4)", "EUR", "OPEN", None, "Quote under negotiation; PO not yet placed; unhedged exposure"),
    (8, "Bulk Gas Storage — Linde", "EUR", "HEDGED", 1.090, "Hedged at PO placement; long-lead item requires early hedge"),
    (9, "DCS — Siemens S7-1500 (x5)", "EUR", "HEDGED", 1.090, "Hedged with EUR program forward; expires Q2-2025"),
    (12, "Process Chiller — Daikin (x3)", "JPY", "HEDGED", 149.0, "Included in JPY hedge package; Daikin invoice in JPY"),
    (13, "Roots Blower Booster (x6)", "EUR", "HEDGED", 1.085, "Forward at 1.085; coordinated with EQ-001 Edwards delivery schedule"),
    (15, "AMR Fleet — MiR (x10)", "EUR", "HEDGED", 1.090, "Hedged at PO placement; forward expires Q3-2025"),
]

HEADERS = ["Equip ID", "Tool Description", "Ccy", "Contract Value (Local Ccy)", "Baseline FX Rate",
           "Baseline USD Cost", "Adverse FX Rate", "Adverse USD Cost", "Adverse Impact (USD)",
           "Favorable FX Rate", "Favorable USD Cost", "Hedge Status", "Hedge Rate", "Notes"]


def build(wb, s02_info, named):
    ws = wb.create_sheet("S15_FX_Exposure_Model")
    set_tab_color(ws, 3)
    row = title_block(ws, 3, "S15", "FX Exposure & Currency Risk Model — EUR / JPY Equipment Purchases",
                       "Program: Greenfield Expansion Phase II | ~40% of portfolio denominated in EUR or JPY | "
                       "All baseline/stress rates from S01_Disclaimer_Assumptions | Hedge status linked to cash flow schedule",
                       n_cols=14)

    eur_base = cellref(named, "USD/EUR Exchange Rate (Baseline)")
    eur_adv = cellref(named, "EUR Sensitivity – Adverse")
    eur_fav = cellref(named, "EUR Sensitivity – Favorable")
    jpy_base = cellref(named, "USD/JPY Exchange Rate (Baseline)")
    jpy_adv = cellref(named, "JPY Sensitivity – Adverse")
    jpy_fav = cellref(named, "JPY Sensitivity – Favorable")

    row = section_header(ws, row, 1, "FX RATE ASSUMPTIONS (Linked from S01_Disclaimer_Assumptions)", 5, 3)
    row = write_headers(ws, row, 1, ["Rate Parameter", "Baseline", "Adverse", "Favorable", "Notes"], 3)
    ws.cell(row=row, column=1, value="USD/EUR (baseline, USD per EUR)")
    for col, ref in zip((2, 3, 4), (eur_base, eur_adv, eur_fav)):
        c = ws.cell(row=row, column=col, value=f"={ref}"); c.number_format = CUR2; c.font = GREEN_LINK
    ws.cell(row=row, column=5, value="1% move in EUR/USD ~ $85K portfolio impact")
    row += 1
    ws.cell(row=row, column=1, value="USD/JPY (baseline, JPY per USD)")
    for col, ref in zip((2, 3, 4), (jpy_base, jpy_adv, jpy_fav)):
        c = ws.cell(row=row, column=col, value=f"={ref}"); c.number_format = CUR2; c.font = GREEN_LINK
    ws.cell(row=row, column=5, value="Stronger JPY (lower rate) = higher USD cost")
    row += 2

    eq_first = s02_info["first_data_row"]

    row = section_header(ws, row, 1, "EQUIPMENT-LEVEL FX EXPOSURE ANALYSIS", 14, 3)
    header_row = write_headers(ws, row, 1, HEADERS, 3)
    first_row = header_row
    r = header_row
    for (eqn, desc, ccy, hedge, hedge_rate, notes) in FX_ITEMS:
        eq_row = eq_first + eqn - 1
        eq_id = f"EQ-{eqn:03d}"
        ws.cell(row=r, column=1, value=eq_id)
        ws.cell(row=r, column=2, value=desc)
        ws.cell(row=r, column=3, value=ccy)
        if ccy == "EUR":
            contract = ws.cell(row=r, column=4,
                                value=f"='{s02_info['sheet']}'!I{eq_row}/{eur_base}")
            base_rate = ws.cell(row=r, column=5, value=f"={eur_base}")
            base_cost = ws.cell(row=r, column=6, value=f"=D{r}*E{r}")
            adv_rate = ws.cell(row=r, column=7, value=f"={eur_adv}")
            adv_cost = ws.cell(row=r, column=8, value=f"=D{r}*G{r}")
            fav_rate = ws.cell(row=r, column=10, value=f"={eur_fav}")
            fav_cost = ws.cell(row=r, column=11, value=f"=D{r}*J{r}")
        else:  # JPY
            contract = ws.cell(row=r, column=4,
                                value=f"='{s02_info['sheet']}'!I{eq_row}*{jpy_base}")
            base_rate = ws.cell(row=r, column=5, value=f"={jpy_base}")
            base_cost = ws.cell(row=r, column=6, value=f"=D{r}/E{r}")
            adv_rate = ws.cell(row=r, column=7, value=f"={jpy_adv}")
            adv_cost = ws.cell(row=r, column=8, value=f"=D{r}/G{r}")
            fav_rate = ws.cell(row=r, column=10, value=f"={jpy_fav}")
            fav_cost = ws.cell(row=r, column=11, value=f"=D{r}/J{r}")
        for cell in (contract,):
            cell.number_format = CUR0
            cell.font = GREEN_LINK
        for cell in (base_rate, adv_rate, fav_rate):
            cell.number_format = CUR2
        for cell in (base_cost, adv_cost, fav_cost):
            cell.number_format = USD0
        impact = ws.cell(row=r, column=9, value=f"=H{r}-F{r}"); impact.number_format = USD0
        hs = ws.cell(row=r, column=12, value=hedge)
        hs.fill = PatternFill("solid", fgColor=RAG_GREEN if hedge == "HEDGED" else RAG_AMBER)
        hr = ws.cell(row=r, column=13, value=hedge_rate if hedge_rate else "N/A")
        if hedge_rate:
            hr.number_format = CUR2
            hr.font = BLUE_INPUT
        nc = ws.cell(row=r, column=14, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 15):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    totals_row = r
    ws.cell(row=r, column=1, value="FX PORTFOLIO TOTALS").font = BOLD
    for col_letter in ["D", "F", "H", "I", "K"]:
        c = ws.cell(row=r, column=ord(col_letter) - 64, value=f"=SUM({col_letter}{first_row}:{col_letter}{last_row})")
        c.number_format = USD0
        c.font = BOLD
    for c in range(1, 15):
        ws.cell(row=r, column=c).border = BORDER_ALL
        ws.cell(row=r, column=c).fill = zone_fill_light(3)
    row = r + 2

    row = section_header(ws, row, 1, "FX EXPOSURE SUMMARY & HEDGE EFFECTIVENESS", 2, 3)
    stats = [
        ("Total EUR-Denominated Spend (baseline USD)",
         f'=SUMIF(C{first_row}:C{last_row},"EUR",F{first_row}:F{last_row})'),
        ("Total JPY-Denominated Spend (baseline USD)",
         f'=SUMIF(C{first_row}:C{last_row},"JPY",F{first_row}:F{last_row})'),
        ("Total Portfolio FX-Exposed Spend (baseline USD)", f"=F{totals_row}"),
        ("Adverse FX Impact (if fully unhedged)", f"=I{totals_row}"),
        ("Items Fully Hedged", f'=COUNTIF(L{first_row}:L{last_row},"HEDGED")'),
        ("Items with Open Unhedged Exposure", f'=COUNTIF(L{first_row}:L{last_row},"OPEN")'),
        ("FX Reserve in AR Budget (USD)", 485000),
        ("Net FX Risk After Reserve", None),  # filled after
    ]
    stat_start = row
    for label, formula in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula if formula is not None else 0)
        c.number_format = USD0
        c.font = BOLD
        c.border = BORDER_ALL
        if label.startswith("Items"):
            c.number_format = CUR0
        if label.startswith("FX Reserve"):
            c.font = BLUE_INPUT
        row += 1
    net_risk_row = row - 1
    ws.cell(row=net_risk_row, column=2, value=f"=I{totals_row}+B{stat_start+6}")

    autosize(ws, {1: 9, 2: 30, 3: 6, 4: 16, 5: 12, 6: 14, 7: 12, 8: 14, 9: 14, 10: 12, 11: 14, 12: 11, 13: 10, 14: 46})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
