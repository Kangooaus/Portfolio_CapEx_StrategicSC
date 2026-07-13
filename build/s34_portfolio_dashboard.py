from gen_common import *


def build(wb, s33):
    ws = wb.create_sheet("S34_Portfolio_Dashboard")
    set_tab_color(ws, 6)
    row = title_block(ws, 6, "S34", "PORTFOLIO EXECUTIVE DASHBOARD — ALL PROGRAMS",
                       "Portfolio Director: Sourabh Tarodekar · Aggregates every active/proposed program in S33_Portfolio_Register · "
                       "All values linked live", n_cols=10)

    def q(cell):
        return f"'{s33['sheet']}'!{cell}"

    def tile(r, c, label, formula, fmt, sublabel):
        ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + 1)
        lc = ws.cell(row=r, column=c, value=label)
        lc.font = Font(bold=True, size=9, color="FFFFFF")
        lc.fill = zone_fill(6)
        lc.alignment = CENTER
        ws.merge_cells(start_row=r + 1, start_column=c, end_row=r + 1, end_column=c + 1)
        vc = ws.cell(row=r + 1, column=c, value=formula)
        vc.font = Font(bold=True, size=16, color="0E6655")
        vc.number_format = fmt
        vc.alignment = CENTER
        vc.fill = PatternFill("solid", fgColor="F2F2F2")
        ws.merge_cells(start_row=r + 2, start_column=c, end_row=r + 2, end_column=c + 1)
        sc = ws.cell(row=r + 2, column=c, value=sublabel)
        sc.font = Font(size=8, italic=True, color="666666")
        sc.alignment = CENTER
        ws.row_dimensions[r + 1].height = 26
        for rr in (r, r + 1, r + 2):
            for cc in (c, c + 1):
                ws.cell(row=rr, column=cc).border = BORDER_ALL

    row = section_header(ws, row, 1, "PORTFOLIO KEY PERFORMANCE INDICATORS", 10, 6)
    tile(row, 1, "ACTIVE + PROPOSED PROGRAMS", f"={q(s33['program_count_cell'])}", CUR0, "S33 — Portfolio Register")
    tile(row, 3, "TOTAL PORTFOLIO CAPEX", f"={q(s33['total_capex_cell'])}", USD0, "Sum across all programs")
    tile(row, 5, "TOTAL APPROVED/EST. BUDGET", f"={q(s33['total_budget_cell'])}", USD0, "Incl. contingency + reserves")
    tile(row, 7, "BLENDED SUPPLY CHAIN RISK", f"={q(s33['blended_risk_cell'])}", CUR2, "Avg across all programs")
    tile(row, 9, "TOTAL EQUIPMENT PLATFORMS", f"={q(s33['total_platforms_cell'])}", CUR0, "All programs combined")
    row += 4

    row = section_header(ws, row, 1, "PROGRAM-BY-PROGRAM COMPARISON", 9, 6)
    headers = ["Program", "Phase / Status", "CapEx (USD)", "% of Portfolio CapEx", "Approved/Est. Budget (USD)",
               "IRR", "Risk Score", "Equipment Platforms", "Payback (yrs)"]
    header_row = write_headers(ws, row, 1, headers, 6)
    r = header_row
    for prog_row in (s33["prg1_row"], s33["prg2_row"]):
        ws.cell(row=r, column=1, value=f"={q('B' + str(prog_row))}")
        ws.cell(row=r, column=2, value=f"={q('G' + str(prog_row))}")
        cc = ws.cell(row=r, column=3, value=f"={q('H' + str(prog_row))}"); cc.number_format = USD0
        pc = ws.cell(row=r, column=4, value=f"=C{r}/{q(s33['total_capex_cell'])}"); pc.number_format = PCT1
        bc = ws.cell(row=r, column=5, value=f"={q('J' + str(prog_row))}"); bc.number_format = USD0
        ic = ws.cell(row=r, column=6, value=f"={q('K' + str(prog_row))}"); ic.number_format = PCT1
        rc = ws.cell(row=r, column=7, value=f"={q('N' + str(prog_row))}"); rc.number_format = CUR2
        plc = ws.cell(row=r, column=8, value=f"={q('O' + str(prog_row))}")
        pbc = ws.cell(row=r, column=9, value=f"={q('M' + str(prog_row))}"); pbc.number_format = CUR2
        for c in range(1, 10):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    comp_last = r - 1
    ws.cell(row=r, column=1, value="PORTFOLIO TOTAL").font = BOLD
    tc = ws.cell(row=r, column=3, value=f"=SUM(C{header_row}:C{comp_last})"); tc.number_format = USD0; tc.font = BOLD
    ws.cell(row=r, column=4, value=1).number_format = PCT1
    ws.cell(row=r, column=4).font = BOLD
    tb = ws.cell(row=r, column=5, value=f"=SUM(E{header_row}:E{comp_last})"); tb.number_format = USD0; tb.font = BOLD
    ravg = ws.cell(row=r, column=7, value=f"=AVERAGE(G{header_row}:G{comp_last})"); ravg.number_format = CUR2; ravg.font = BOLD
    tpl = ws.cell(row=r, column=8, value=f"=SUM(H{header_row}:H{comp_last})"); tpl.font = BOLD
    for c in range(1, 10):
        ws.cell(row=r, column=c).border = BORDER_ALL
        ws.cell(row=r, column=c).fill = zone_fill_light(6)
    row = r + 2

    row = section_header(ws, row, 1, "PORTFOLIO NOTES", 10, 6)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=10)
    ws.cell(row=row, column=1, value=(
        "PRG-001 (Greenfield Expansion Phase II) is fully approved and in execution — every figure above is live-linked "
        "to its 33-sheet model (S00-S32). PRG-002 (Riverside Automation Upgrade Phase I) is at FEL-2 (feasibility); its "
        "equipment, supplier, and risk data are live-linked to S02/S03/S16, but its IRR/NPV/payback are Finance's FEL-2 "
        "planning estimates pending a full TCO build-out ahead of AR submission. See S35_Portfolio_Prioritization for the "
        "capital allocation decision framework across both programs."
    )).alignment = LEFT_WRAP
    ws.row_dimensions[row].height = 60

    autosize(ws, {1: 14, 2: 26, 3: 14, 4: 14, 5: 16, 6: 16, 7: 16, 8: 12, 9: 16, 10: 16})
    freeze_below(ws, 1)
    return {"sheet": ws.title}
