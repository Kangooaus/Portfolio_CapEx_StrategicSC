from gen_common import *

# EqID, Category, Tool, Throughput(u/hr or None), Qty, OpHrs, HasThroughput
CAP_ROWS = [
    ("EQ-001", "Vacuum Pump System", "Dry Screw Vacuum Pump", None, 4, 8320),
    ("EQ-002", "Vacuum Pump System", "Turbomolecular Pump Assembly", None, 3, 8320),
    ("EQ-003", "High-Temp Furnace", "Tube Furnace System – 8-zone", 24, 2, 8320),
    ("EQ-004", "High-Temp Furnace", "Batch Oxidation Furnace", 18, 2, 8320),
    ("EQ-005", "Robotics / Automation", "SCARA Wafer Transfer Robot", None, 6, 8320),
    ("EQ-006", "Robotics / Automation", "Overhead Track Conveyor", None, 1, 8320),
    ("EQ-007", "Gas Handling System", "Process Gas Cabinet", None, 4, 8320),
    ("EQ-009", "PLC Control System", "DCS – Siemens S7-1500", None, 5, 8320),
    ("EQ-011", "Facility Infra", "Dry-Type Transformer", None, 2, 8760),
    ("EQ-012", "Facility Infra – Cooling", "Process Chiller System", None, 3, 8760),
    ("EQ-013", "Vacuum Pump System", "Roots Blower Booster", None, 6, 8320),
    ("EQ-014", "High-Temp Furnace", "RTP – Rapid Thermal Processor", 32, 2, 8320),
    ("EQ-015", "Robotics / Automation", "AMR Fleet (x10)", None, 1, 8320),
]

HEADERS = ["Equipment ID", "Equipment Category", "Tool Type", "Throughput (units/hr)", "Quantity",
           "Op Hours/Year", "Effective Uptime (%)", "Annual Capacity (units/yr)", "Baseline Demand (units/yr)",
           "Capacity Cushion (units)", "Tool Contribution to Portfolio Cap (%)", "Surge Demand (+20%, units/yr)",
           "Surge Contribution (%)", "Bottleneck Flag"]


def build(wb, named):
    ws = wb.create_sheet("S10_Capacity_Planning")
    set_tab_color(ws, 2)
    row = title_block(ws, 2, "S10", "Capacity Planning Model — Annual Production Capacity Supported by Equipment Portfolio",
                       "Inputs from S02_Equipment_Portfolio and S01_Disclaimer_Assumptions | Identifies bottlenecks | "
                       "Models +20% demand surge scenario", n_cols=14)

    uptime = cellref(named, "Equipment Uptime Target")
    maint_dt = cellref(named, "Planned Maintenance Downtime")
    yield_a = cellref(named, "Process Yield Assumption")

    row = section_header(ws, row, 1, "CAPACITY MODEL PARAMETERS", 4, 2)
    row = write_headers(ws, row, 1, ["Parameter", "Value", "Unit", "Source"], 2)
    ws.cell(row=row, column=1, value="Equipment Uptime (%)")
    c = ws.cell(row=row, column=2, value=f"={uptime}"); c.number_format = PCT1; c.font = GREEN_LINK
    ws.cell(row=row, column=4, value="S01 — 92% target")
    row += 1
    ws.cell(row=row, column=1, value="Planned Maint Downtime (%)")
    c = ws.cell(row=row, column=2, value=f"={maint_dt}"); c.number_format = PCT1; c.font = GREEN_LINK
    ws.cell(row=row, column=4, value="S01 — 4% allocated")
    row += 1
    eff_uptime_row = row
    ws.cell(row=row, column=1, value="Effective Uptime (%)")
    c = ws.cell(row=row, column=2, value=f"=B{row-2}-B{row-1}"); c.number_format = PCT1
    ws.cell(row=row, column=4, value="Uptime minus Planned Maint (formula)")
    row += 1
    yield_row = row
    ws.cell(row=row, column=1, value="Process Yield (%)")
    c = ws.cell(row=row, column=2, value=f"={yield_a}"); c.number_format = PCT1; c.font = GREEN_LINK
    ws.cell(row=row, column=4, value="S01 — 96% yield")
    row += 1
    ws.cell(row=row, column=1, value="Baseline Demand (units/yr)")
    baseline_demand_row = row
    c = ws.cell(row=row, column=2, value=750000); c.number_format = CUR0; c.font = BLUE_INPUT
    ws.cell(row=row, column=4, value="Engineering baseline — current program requirement")
    row += 1
    ws.cell(row=row, column=1, value="Surge Scenario (+20%) Demand (units/yr)")
    surge_demand_row = row
    c = ws.cell(row=row, column=2, value=f"=B{baseline_demand_row}*1.2"); c.number_format = CUR0
    ws.cell(row=row, column=4, value="Stress test: 20% volume increase")
    row += 2

    row = section_header(ws, row, 1, "EQUIPMENT CAPACITY MODEL — BASELINE vs SURGE SCENARIO", 14, 2)
    header_row = write_headers(ws, row, 1, HEADERS, 2)
    first_row = header_row
    r = header_row
    process_tool_rows = []
    for (eid, cat, tool, thr, qty, ophrs) in CAP_ROWS:
        ws.cell(row=r, column=1, value=eid)
        ws.cell(row=r, column=2, value=cat)
        ws.cell(row=r, column=3, value=tool)
        tc = ws.cell(row=r, column=4, value=thr if thr else "N/A")
        if thr:
            tc.font = BLUE_INPUT
        ws.cell(row=r, column=5, value=qty).font = BLUE_INPUT
        ws.cell(row=r, column=6, value=ophrs).font = BLUE_INPUT
        eu = ws.cell(row=r, column=7, value=f"=$B${eff_uptime_row}"); eu.number_format = PCT1
        if thr:
            process_tool_rows.append(r)
            cap = ws.cell(row=r, column=8, value=f"=D{r}*E{r}*F{r}*G{r}*$B${yield_row}")
            cap.number_format = CUR0
            dem = ws.cell(row=r, column=9, value=f"=$B${baseline_demand_row}")
            dem.number_format = CUR0
            cush = ws.cell(row=r, column=10, value=f"=H{r}-I{r}")
            cush.number_format = CUR0
            contrib = ws.cell(row=r, column=11, value=f"=I{r}/H{r}")
            contrib.number_format = PCT1
            surge = ws.cell(row=r, column=12, value=f"=$B${surge_demand_row}")
            surge.number_format = CUR0
            surgec = ws.cell(row=r, column=13, value=f"=L{r}/H{r}")
            surgec.number_format = PCT1
            ws.cell(row=r, column=14, value="⚠ BOTTLENECK (portfolio-level surge >72% utilization)")
        else:
            for cc in range(8, 14):
                ws.cell(row=r, column=cc, value="—")
            ws.cell(row=r, column=14, value="SUPPORT EQUIPMENT")
        for c in range(1, 15):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "CAPACITY SUMMARY & BOTTLENECK ANALYSIS", 2, 2)
    total_cap_row = row
    ws.cell(row=row, column=1, value="Total Annual Capacity (Process Tools Only)")
    hrows = ",".join(f"H{x}" for x in process_tool_rows)
    c = ws.cell(row=row, column=2, value=f"=SUM({hrows})" if len(process_tool_rows) > 1 else f"={hrows}")
    c.number_format = CUR0; c.font = BOLD
    row += 1
    ws.cell(row=row, column=1, value="Baseline Demand")
    c = ws.cell(row=row, column=2, value=f"=B{baseline_demand_row}"); c.number_format = CUR0
    row += 1
    cushion_row = row
    ws.cell(row=row, column=1, value="Baseline Capacity Cushion")
    c = ws.cell(row=row, column=2, value=f"=B{total_cap_row}-B{row-1}"); c.number_format = CUR0
    row += 1
    ws.cell(row=row, column=1, value="Baseline Utilization")
    c = ws.cell(row=row, column=2, value=f"=B{total_cap_row-2}/B{total_cap_row}"); c.number_format = PCT1
    row += 1
    ws.cell(row=row, column=1, value="Surge Demand (+20%)")
    c = ws.cell(row=row, column=2, value=f"=B{surge_demand_row}"); c.number_format = CUR0
    row += 1
    ws.cell(row=row, column=1, value="Bottleneck Equipment (Surge)")
    ws.cell(row=row, column=2, value="Batch Oxidation Furnace (EQ-004) — lowest individual Annual Capacity among process tools")
    row += 1
    ws.cell(row=row, column=1, value="Max Surge Utilization")
    c = ws.cell(row=row, column=2, value=f"=B{surge_demand_row}/B{total_cap_row}"); c.number_format = PCT1
    row += 1

    autosize(ws, {1: 12, 2: 22, 3: 30, 4: 14, 5: 8, 6: 12, 7: 12, 8: 14, 9: 14, 10: 13, 11: 15, 12: 15, 13: 13, 14: 40})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title, "total_capacity_cell": f"B{total_cap_row}", "cushion_cell": f"B{cushion_row}"}
