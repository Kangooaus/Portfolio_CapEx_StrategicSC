from gen_common import *

PARAMS_A = dict(purchase=680000, qty=2, install=52000, energy_kwh=110, ophrs=8320,
                maint_rate=0.045, mtbf=4200, mttr=6, spares=18000, life=15, residual=0.05)
PARAMS_B = dict(purchase=520000, qty=2, install=38000, energy_kwh=98, ophrs=8320,
                maint_rate=0.055, mtbf=2800, mttr=10, spares=28000, life=12, residual=0.03)


def build(wb, named):
    ws = wb.create_sheet("S05_TCO_Downtime_Model")
    set_tab_color(ws, 1)
    row = title_block(ws, 1, "S05", "Total Cost of Ownership (TCO) & Downtime Risk Model — 10-Year Lifecycle Analysis",
                       "Compares Supplier A (Premium — TEL/AMAT-type) vs Supplier B (Value — domestic alternative) across purchase, "
                       "energy, maintenance, downtime, and lifecycle NPV | Discount Rate from S01_Disclaimer_Assumptions", n_cols=13)

    wacc = cellref(named, "Discount Rate (WACC)")
    infl = cellref(named, "Inflation Rate")
    energy_price = cellref(named, "Energy Price – Electricity")
    prod_value = cellref(named, "Production Value per Hour")

    row = section_header(ws, row, 1, "MODEL PARAMETERS (linked from S01_Disclaimer_Assumptions)", 2, 1)
    ws.cell(row=row, column=1, value="Discount Rate (WACC)")
    c = ws.cell(row=row, column=2, value=f"={wacc}"); c.number_format = PCT1; c.font = GREEN_LINK
    row += 1
    ws.cell(row=row, column=1, value="Project Horizon (Years)")
    c = ws.cell(row=row, column=2, value=10)
    row += 1
    ws.cell(row=row, column=1, value="Energy Price (USD/kWh)")
    c = ws.cell(row=row, column=2, value=f"={energy_price}"); c.number_format = USD2; c.font = GREEN_LINK
    row += 1
    ws.cell(row=row, column=1, value="Production Value per Hour (USD/hr)")
    c = ws.cell(row=row, column=2, value=f"={prod_value}"); c.number_format = USD0; c.font = GREEN_LINK
    row += 1
    ws.cell(row=row, column=1, value="Inflation Rate")
    c = ws.cell(row=row, column=2, value=f"={infl}"); c.number_format = PCT1; c.font = GREEN_LINK
    row += 2

    row = section_header(ws, row, 1, "EQUIPMENT COMPARISON — SUPPLIER A (PREMIUM) vs SUPPLIER B (VALUE)", 5, 1)
    row = write_headers(ws, row, 1, ["Cost Parameter", "Supplier A (Premium)", "Supplier B (Value)", "Delta (B-A)", "Notes"], 1)
    comp_rows = [
        ("Purchase Price (per unit, USD)", PARAMS_A["purchase"], PARAMS_B["purchase"], USD0,
         "Supplier A = TEL EQ-004 type; Supplier B = domestic alternative"),
        ("Quantity", PARAMS_A["qty"], PARAMS_B["qty"], CUR0, "Equal quantity for fair comparison"),
        ("Installation Cost (per unit, USD)", PARAMS_A["install"], PARAMS_B["install"], USD0,
         "Supplier A requires specialized installation crew (JPY contract)"),
        ("Energy Consumption (kWh/hr)", PARAMS_A["energy_kwh"], PARAMS_B["energy_kwh"], CUR0,
         "Supplier A higher thermal efficiency spec; Supplier B 11% higher power draw"),
        ("Operational Hours (Annual)", PARAMS_A["ophrs"], PARAMS_B["ophrs"], CUR0, "Both operate on identical shift schedule"),
        ("Maintenance Rate (% of purchase)", PARAMS_A["maint_rate"], PARAMS_B["maint_rate"], PCT1,
         "Supplier A lower maint rate; Supplier B higher due to older platform design"),
        ("Expected MTBF (hrs)", PARAMS_A["mtbf"], PARAMS_B["mtbf"], CUR0, "Mean Time Between Failures; Supplier A more robust platform"),
        ("Expected MTTR (hrs)", PARAMS_A["mttr"], PARAMS_B["mttr"], CUR0, "Mean Time To Repair; Supplier A has faster FSE response SLA"),
        ("Spare Parts Annual Cost (USD)", PARAMS_A["spares"], PARAMS_B["spares"], USD0,
         "Supplier A proprietary spares expensive but fewer events; B more frequent"),
        ("Expected Equipment Lifetime (yrs)", PARAMS_A["life"], PARAMS_B["life"], CUR0, "Supplier A longer qualified life; Supplier B 12 yr basis"),
        ("Residual Value at End of Life (%)", PARAMS_A["residual"], PARAMS_B["residual"], PCT1,
         "Estimated salvage/residual as % of purchase price"),
    ]
    for label, a, b, fmt, note in comp_rows:
        ws.cell(row=row, column=1, value=label)
        ca = ws.cell(row=row, column=2, value=a); ca.number_format = fmt; ca.font = BLUE_INPUT
        cb = ws.cell(row=row, column=3, value=b); cb.number_format = fmt; cb.font = BLUE_INPUT
        cd = ws.cell(row=row, column=4, value=f"=C{row}-B{row}"); cd.number_format = fmt
        cn = ws.cell(row=row, column=5, value=note); cn.alignment = LEFT_WRAP
        for c in range(1, 6):
            ws.cell(row=row, column=c).border = BORDER_ALL
        row += 1
    row += 1

    # 10-year lifecycle model
    year_headers = [f"Y{i}" for i in range(1, 11)]
    row = section_header(ws, row, 1, "10-YEAR LIFECYCLE COST MODEL", 13, 1)
    row = write_headers(ws, row, 1, ["Cost Component / Supplier"] + year_headers + ["10-Yr Total", "NPV (10-Yr)"], 1)

    def year_cols():
        return [chr(ord('B') + i) for i in range(10)]  # B..K

    cols = year_cols()

    def write_flat_row(row, label, y1_formula, escalate=True, is_flat_value=False):
        ws.cell(row=row, column=1, value=label)
        for i, col in enumerate(cols):
            if i == 0:
                f = y1_formula
            else:
                prev = cols[i - 1]
                if escalate:
                    f = f"={prev}{row}*(1+{infl})"
                else:
                    f = f"={prev}{row}"
            c = ws.cell(row=row, column=2 + i, value=f)
            c.number_format = USD0
        total_col = chr(ord('B') + 10)  # L
        npv_col = chr(ord('B') + 11)  # M
        tot = ws.cell(row=row, column=12, value=f"=SUM(B{row}:K{row})"); tot.number_format = USD0
        npv = ws.cell(row=row, column=13, value=f"=NPV({wacc},B{row}:K{row})"); npv.number_format = USD0
        for c in range(1, 14):
            ws.cell(row=row, column=c).border = BORDER_ALL
        return row + 1

    # Purchase cost (one-time year1)
    row = section_header(ws, row, 1, "1. Purchase Cost (total)", 13, 1); ws.cell(row=row-1, column=1).font = BOLD
    row_purchase_a = row
    row = write_flat_row(row, "Supplier A", f"={PARAMS_A['purchase']}*{PARAMS_A['qty']}", escalate=False)
    for i, col in enumerate(cols[1:], start=1):
        ws.cell(row=row_purchase_a, column=2 + i, value=0).number_format = USD0
    row_purchase_b = row
    row = write_flat_row(row, "Supplier B", f"={PARAMS_B['purchase']}*{PARAMS_B['qty']}", escalate=False)
    for i, col in enumerate(cols[1:], start=1):
        ws.cell(row=row_purchase_b, column=2 + i, value=0).number_format = USD0

    row = section_header(ws, row, 1, "2. Installation Cost (total)", 13, 1); ws.cell(row=row-1, column=1).font = BOLD
    row_install_a = row
    row = write_flat_row(row, "Supplier A", f"={PARAMS_A['install']}*{PARAMS_A['qty']}", escalate=False)
    for i in range(1, 10):
        ws.cell(row=row_install_a, column=2 + i, value=0).number_format = USD0
    row_install_b = row
    row = write_flat_row(row, "Supplier B", f"={PARAMS_B['install']}*{PARAMS_B['qty']}", escalate=False)
    for i in range(1, 10):
        ws.cell(row=row_install_b, column=2 + i, value=0).number_format = USD0

    row = section_header(ws, row, 1, "3. Annual Energy Cost (escalates with inflation from Year 2)", 13, 1); ws.cell(row=row-1, column=1).font = BOLD
    row_energy_a = row
    row = write_flat_row(row, "Supplier A", f"={PARAMS_A['energy_kwh']}*{PARAMS_A['qty']}*{PARAMS_A['ophrs']}*{energy_price}")
    row_energy_b = row
    row = write_flat_row(row, "Supplier B", f"={PARAMS_B['energy_kwh']}*{PARAMS_B['qty']}*{PARAMS_B['ophrs']}*{energy_price}")

    row = section_header(ws, row, 1, "4. Annual Maintenance Cost (% of purchase; escalates with inflation)", 13, 1); ws.cell(row=row-1, column=1).font = BOLD
    row_maint_a = row
    row = write_flat_row(row, "Supplier A", f"={PARAMS_A['purchase']}*{PARAMS_A['qty']}*{PARAMS_A['maint_rate']}")
    row_maint_b = row
    row = write_flat_row(row, "Supplier B", f"={PARAMS_B['purchase']}*{PARAMS_B['qty']}*{PARAMS_B['maint_rate']}")

    row = section_header(ws, row, 1, "5. Annual Spare Parts Cost (escalates with inflation)", 13, 1); ws.cell(row=row-1, column=1).font = BOLD
    row_spares_a = row
    row = write_flat_row(row, "Supplier A", f"={PARAMS_A['spares']}")
    row_spares_b = row
    row = write_flat_row(row, "Supplier B", f"={PARAMS_B['spares']}")

    row = section_header(ws, row, 1, "6. Downtime Cost (Annual) — (Op Hrs ÷ MTBF) × MTTR × Production Value/hr", 13, 1); ws.cell(row=row-1, column=1).font = BOLD
    row_down_a = row
    dt_a_formula = f"=({PARAMS_A['ophrs']}/{PARAMS_A['mtbf']})*{PARAMS_A['mttr']}*{prod_value}"
    row = write_flat_row(row, "Supplier A", dt_a_formula, escalate=False)
    for i in range(1, 10):
        ws.cell(row=row_down_a, column=2 + i, value=dt_a_formula).number_format = USD0
    row_down_b = row
    dt_b_formula = f"=({PARAMS_B['ophrs']}/{PARAMS_B['mtbf']})*{PARAMS_B['mttr']}*{prod_value}"
    row = write_flat_row(row, "Supplier B", dt_b_formula, escalate=False)
    for i in range(1, 10):
        ws.cell(row=row_down_b, column=2 + i, value=dt_b_formula).number_format = USD0
    row += 1

    # TOTAL COST OF OWNERSHIP SUMMARY
    row = section_header(ws, row, 1, "TOTAL COST OF OWNERSHIP SUMMARY", 13, 1)
    row = write_headers(ws, row, 1, ["Supplier"] + year_headers + ["10-Yr Total", "NPV (10-Yr)"], 1)
    row_tco_a = row
    ws.cell(row=row, column=1, value="A (Premium)")
    for i, col in enumerate(cols):
        c = ws.cell(row=row, column=2 + i,
                     value=f"={col}{row_purchase_a}+{col}{row_install_a}+{col}{row_energy_a}+{col}{row_maint_a}+{col}{row_spares_a}+{col}{row_down_a}")
        c.number_format = USD0
    ws.cell(row=row, column=12, value=f"=SUM(B{row}:K{row})").number_format = USD0
    ws.cell(row=row, column=13, value=f"=NPV({wacc},B{row}:K{row})").number_format = USD0
    for c in range(1, 14):
        ws.cell(row=row, column=c).border = BORDER_ALL
    row += 1
    row_tco_b = row
    ws.cell(row=row, column=1, value="B (Value)")
    for i, col in enumerate(cols):
        c = ws.cell(row=row, column=2 + i,
                     value=f"={col}{row_purchase_b}+{col}{row_install_b}+{col}{row_energy_b}+{col}{row_maint_b}+{col}{row_spares_b}+{col}{row_down_b}")
        c.number_format = USD0
    ws.cell(row=row, column=12, value=f"=SUM(B{row}:K{row})").number_format = USD0
    ws.cell(row=row, column=13, value=f"=NPV({wacc},B{row}:K{row})").number_format = USD0
    for c in range(1, 14):
        ws.cell(row=row, column=c).border = BORDER_ALL
    row += 1
    row_tco_delta = row
    ws.cell(row=row, column=1, value="TCO DELTA (B Savings vs A)").font = BOLD
    for i, col in enumerate(cols):
        c = ws.cell(row=row, column=2 + i, value=f"={col}{row_tco_a}-{col}{row_tco_b}")
        c.number_format = USD0
        c.font = BOLD
    ws.cell(row=row, column=12, value=f"=L{row_tco_a}-L{row_tco_b}").number_format = USD0
    ws.cell(row=row, column=13, value=f"=M{row_tco_a}-M{row_tco_b}").number_format = USD0
    for c in range(1, 14):
        ws.cell(row=row, column=c).border = BORDER_ALL
        ws.cell(row=row, column=c).fill = zone_fill_light(1)
    row += 2

    autosize(ws, {1: 32})
    for c in range(2, 14):
        ws.column_dimensions[get_column_letter(c)].width = 13
    freeze_below(ws, 1)

    return {"sheet": ws.title, "tco_a_row": row_tco_a, "tco_b_row": row_tco_b, "tco_delta_row": row_tco_delta}
