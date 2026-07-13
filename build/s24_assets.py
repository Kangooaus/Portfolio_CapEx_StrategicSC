from gen_common import *

# AssetTag, EqRef, Desc, Serial, Qty, Location, Status, PurchaseDate, InstallDate, CommissDate, RemLife, ReplaceYear, ReplaceCost, Warranty, Support, Notes
ASSETS = [
    ("AST-001", "EQ-001", "Dry Screw Vacuum Pump (x4)", "VSP-2025-001/004", 4, "Bay A — Vacuum Zone", "IN PRODUCTION",
     "2025-02-15", "2025-09-01", "2025-11-15", 10, 2035, 890000, "2025-Q4 (see contract)", "Edwards Annual PM",
     "Post-Brexit logistics; Busch backup activated"),
    ("AST-002", "EQ-002", "Turbomolecular Pump (x3)", "TMP-2025-101/103", 3, "Bay A — Vacuum Zone", "IN PRODUCTION",
     "2025-02-20", "2025-11-01", "2025-12-15", 8, 2033, 1200000, "2025-Q4 (see contract)", "Pfeiffer 24/7 support",
     "CRITICAL path item; bearing safety stock maintained"),
    ("AST-003", "EQ-003", "Tube Furnace System (x2)", "THF-2025-201/202", 2, "Bay B — Thermal Zone", "IN PRODUCTION",
     "2025-01-20", "2025-09-15", "2025-11-20", 13, 2038, 1350000, "2025-Q4 (see contract)", "Thermco 3yr full service",
     "FAT completed Austin TX; recipe transfer done"),
    ("AST-004", "EQ-004", "Batch Oxidation Furnace (x2)", "BOF-2025-301/302", 2, "Bay B — Thermal Zone", "QUALIFIED — PQ in progress",
     "2025-02-10", "2025-11-15", "Pending", 13, 2038, 1700000, "2025-Q4 (see contract)", "TEL 3yr comprehensive",
     "JPY FX hedged; structural reinforcement complete"),
    ("AST-005", "EQ-005", "SCARA Robot (x6)", "SCR-2025-401/406", 6, "Bay C — Robotics Zone", "IN PRODUCTION",
     "2025-01-15", "2025-09-01", "2025-11-10", 8, 2033, 2200000, "2025-Q4 (see contract)", "Brooks MES+mech 2yr",
     "MES integration verified; OEE above plan"),
    ("AST-006", "EQ-006", "Overhead Conveyor (x1 system)", "OTC-2025-501", 1, "Bays A-C — Overhead Track", "INSTALLED — commissioning",
     "2025-02-20", "2025-11-20", "Pending", 10, 2035, 560000, "2025-Q4 (see contract)", "Daifuku civil+mech 2yr",
     "Civil interface complete; Wi-Fi nav calibration in progress"),
    ("AST-007", "EQ-007", "Process Gas Cabinet (x4)", "PGC-2025-601/604", 4, "Bay D — Gas Room", "IN PRODUCTION",
     "2025-02-28", "2025-10-01", "2025-11-30", 10, 2035, 1040000, "2025-Q4 (see contract)", "Air Liquide annual cert",
     "Hazmat permit closed; MFC calibration schedule active"),
    ("AST-008", "EQ-008", "Bulk Gas Storage (x1 system)", "BGS-2025-701", 1, "External — Tank Farm", "IN PRODUCTION",
     "2025-02-20", "2025-11-10", "2025-12-01", 18, 2043, 450000, "2025-Q4 (see contract)", "Linde site contract",
     "32-wk LT; on-site Linde maintenance contract"),
    ("AST-009", "EQ-009", "DCS — Siemens S7-1500 (x5)", "DCS-2025-801/805", 5, "Control Room", "IN PRODUCTION",
     "2025-01-28", "2025-09-01", "2025-11-01", 8, 2033, 1100000, "2025-Q4 (see contract)", "Siemens Gold Support",
     "Cybersecurity audit Month 4; LTA pricing locked"),
    ("AST-010", "EQ-010", "SCADA Platform (x3 licenses)", "SCA-2025-901/903", 3, "Control Room (virtual)", "IN PRODUCTION",
     "2025-02-05", "2025-09-01", "2025-11-01", 6, 2031, 330000, "2025-Q4 (see contract)", "Inductive Auto subscription",
     "Annual license renewal; IT/OT integration stable"),
    ("AST-011", "EQ-011", "Dry-Type Transformer (x2)", "TRF-2025-1001/1002", 2, "Electrical Room", "IN PRODUCTION",
     "2025-02-01", "2025-08-15", "2025-10-01", 23, 2048, 560000, "2050-02-01", "ABB manufacturer warranty",
     "Reused partial from prior program; new units installed"),
    ("AST-012", "EQ-012", "Process Chiller (x3)", "PCH-2025-1101/1103", 3, "Mechanical Room", "IN PRODUCTION",
     "2025-01-30", "2025-09-15", "2025-11-20", 13, 2038, 1150000, "2025-Q4 (see contract)", "Daikin annual PM",
     "Glycol loop stable; JPY FX hedged"),
    ("AST-013", "EQ-013", "Roots Blower Booster (x6)", "RBB-2025-1201/1206", 6, "Bay A — Vacuum Zone", "IN PRODUCTION",
     "2025-01-28", "2025-09-01", "2025-11-15", 8, 2033, 975000, "2025-Q4 (see contract)", "Busch annual PM",
     "Paired with EQ-001; coordinated maintenance schedule"),
    ("AST-014", "EQ-014", "RTP Tool (x2)", "RTP-2025-1301/1302", 2, "Bay B — Thermal Zone", "IN PRODUCTION",
     "2025-02-01", "2025-10-20", "2025-12-01", 10, 2035, 2300000, "2025-Q4 (see contract)", "AMAT comprehensive 3yr",
     "Highest-value asset; AMAT dedicated FSE on-site Q4-2025"),
    ("AST-015", "EQ-015", "AMR Fleet (x10 robots)", "AMR-2025-1401/1410", 10, "All Bays — Fleet routing", "IN PRODUCTION",
     "2025-02-05", "2025-09-15", "2025-11-15", 6, 2031, 500000, "2025-Q4 (see contract)", "MiR fleet management sub",
     "Wi-Fi integration stable; Phase 2 routing optimization pending"),
]

HEADERS = ["Asset Tag", "Equip Ref", "Asset Description", "Serial # (Synthetic)", "Qty", "Location (Zone/Bay)",
           "Current Status", "Purchase Date", "Install Date", "Commiss. Date", "Remaining Lifetime (yrs)",
           "Replace Target Year", "Replacement Cost Est. (USD)", "Warranty Expiry", "Support Contract", "Notes"]


def build(wb):
    ws = wb.create_sheet("S24_Asset_Tracking")
    set_tab_color(ws, 4)
    row = title_block(ws, 4, "S24", "Asset Tracking Register — Equipment Fleet Lifecycle & Physical Status",
                       "Tracks all 45 physical assets by serial/tag, location, lifecycle state, maintenance & warranty | "
                       "Owner: Sourabh Tarodekar | Register is platform-level (15 rows); Qty column expands to 45 physical units total | "
                       "Feeds S29 ROI Tracker and S25 Milestone Gate Tracker", n_cols=16)
    header_row = write_headers(ws, row, 1, HEADERS, 4)
    first_row = header_row
    r = header_row
    for (tag, eq, desc, serial, qty, loc, status, pdate, idate, cdate, life, ryear, rcost, warr, supp, notes) in ASSETS:
        ws.cell(row=r, column=1, value=tag)
        ws.cell(row=r, column=2, value=eq)
        ws.cell(row=r, column=3, value=desc)
        ws.cell(row=r, column=4, value=serial)
        ws.cell(row=r, column=5, value=qty).font = BLUE_INPUT
        ws.cell(row=r, column=6, value=loc)
        stc = ws.cell(row=r, column=7, value=status)
        if status == "IN PRODUCTION":
            stc.fill = PatternFill("solid", fgColor=RAG_GREEN)
        else:
            stc.fill = PatternFill("solid", fgColor=RAG_AMBER)
        ws.cell(row=r, column=8, value=pdate)
        ws.cell(row=r, column=9, value=idate)
        ws.cell(row=r, column=10, value=cdate)
        ws.cell(row=r, column=11, value=life).font = BLUE_INPUT
        ws.cell(row=r, column=12, value=ryear).font = BLUE_INPUT
        rc = ws.cell(row=r, column=13, value=rcost); rc.number_format = USD0; rc.font = BLUE_INPUT
        ws.cell(row=r, column=14, value=warr)
        ws.cell(row=r, column=15, value=supp)
        nc = ws.cell(row=r, column=16, value=notes); nc.alignment = LEFT_WRAP
        for c in range(1, 17):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "FLEET SUMMARY", 2, 4)
    stats = [
        ("Total Assets Tracked (sum of Qty)", f"=SUM(E{first_row}:E{last_row})", CUR0),
        ("Equipment Platforms", f"=COUNTA(A{first_row}:A{last_row})", CUR0),
        ("Assets In Production (platforms)", f'=COUNTIF(G{first_row}:G{last_row},"IN PRODUCTION")', CUR0),
        ("Total Replacement Value (Portfolio, USD)", f"=SUM(M{first_row}:M{last_row})", USD0),
        ("Average Remaining Lifetime (yrs)", f"=AVERAGE(K{first_row}:K{last_row})", CUR2),
    ]
    for label, formula, fmt in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 9, 2: 9, 3: 26, 4: 18, 5: 6, 6: 22, 7: 22, 8: 12, 9: 12, 10: 12, 11: 11, 12: 11, 13: 15, 14: 18, 15: 22, 16: 46})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
