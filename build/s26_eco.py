from gen_common import *

# ECOID, Title, Originator, OriginType, Equip, Desc, Reason, Cost, SchedImpact, QualityImpact, Requal, Status, Approval, Submitted, Impl, LinkedVDC
ECOS = [
    ("ECO-001", "Gas Cabinet Safety Interlock Upgrade", "Facilities / Safety", "Regulatory", "EQ-007",
     "Add secondary pressure interlock and emergency shutoff valve per updated NFPA 72 guidance",
     "Regulatory compliance — permit condition", 28500, 2, "No yield impact; safety-critical improvement",
     "YES — re-FAT on gas cabinet", "IMPLEMENTED", "2025-03-10", "2025-03-24", "2025-05-15", "—"),
    ("ECO-002", "TEL Furnace Recipe Parameter Change", "Process Engineering", "Customer-Driven", "EQ-004",
     "Update oxidation time profile on Recipe Set B3 to achieve customer-specified film uniformity +/-1.5%",
     "Customer quality requirement tightened for Phase III product", 12000, 1, "Yield improvement expected +0.5% on PF-A",
     "YES — PQ re-run for Recipe B3", "IMPLEMENTED", "2025-04-02", "2025-04-08", "2025-07-20", "VDC-003"),
    ("ECO-003", "RTP Edge Ring Material Substitution", "Process Engineering / AMAT", "Internal Engineering", "EQ-014",
     "Replace SiC edge ring with high-purity CVD SiC — improved thermal uniformity at >900C",
     "Process optimization — reduce edge exclusion zone", 15000, 0, "Yield improvement +0.8% at wafer edge",
     "YES — thermal profile re-validation", "IMPLEMENTED", "2025-02-15", "2025-02-28", "2025-06-10", "VDC-001"),
    ("ECO-004", "MES Integration Protocol Revision", "Controls / IT-OT", "Internal Engineering", "EQ-005/009/010",
     "Update SCADA-to-MES data handshake to use REST API v2.1 (replace deprecated SOAP endpoints)",
     "IT/OT architecture upgrade — eliminates latency bug", 8000, 1, "No yield impact; +15ms improvement in alarm response",
     "NO — software change only", "IMPLEMENTED", "2025-05-10", "2025-05-17", "2025-07-01", "—"),
    ("ECO-005", "Chiller Glycol Concentration Adjustment", "Facilities Engineering", "Internal Engineering", "EQ-012",
     "Increase inhibited glycol concentration from 30% to 35% to reduce corrosion in stainless loop",
     "Preventive — loop inspection found minor oxidation at fittings", 3500, 0, "No yield impact; improved system longevity",
     "NO", "IMPLEMENTED", "2025-06-01", "2025-06-05", "2025-06-15", "—"),
    ("ECO-006", "Dry Screw Pump N2 Purge Line Upgrade", "Engineering / Edwards", "Internal Engineering", "EQ-001/013",
     "Increase N2 purge flow from 8 L/min to 12 L/min to reduce pump seal degradation rate",
     "Reliability improvement — seal MTBF extended by ~20%", 18000, 1, "No yield impact; MTBF improvement 8,760 -> 10,500 hrs",
     "NO — purge line change only", "IN REVIEW", "2025-07-12", "Pending", "TBC", "—"),
    ("ECO-007", "DCS Cybersecurity Firmware Update", "Controls / InfoSec", "Regulatory", "EQ-009",
     "Apply Siemens TIA Portal firmware patch v19.0.3 per ICS-CERT advisory ICSA-2025-089",
     "Security patch — critical vulnerability mitigation", 5000, 0, "No yield impact; mandatory security update",
     "NO — firmware only; controlled change", "IN REVIEW", "2025-07-20", "Pending", "2025-08-15 target", "—"),
    ("ECO-008", "AMR Fleet Route Optimization v2", "Operations / MiR", "Internal Engineering", "EQ-015",
     "Implement MiR Fleet Manager route algorithm Phase 2 to reduce carrier wait time by ~18%",
     "Operational efficiency — program improvement", 6000, 0, "No yield impact; +18% throughput improvement for AMR",
     "NO — software update", "IMPLEMENTED", "2025-08-01", "2025-08-05", "2025-09-01", "—"),
    ("ECO-009", "Bulk Gas Vessel Pressure Relief Resetting", "Safety / Linde", "Regulatory", "EQ-008",
     "Recalibrate PRV setpoints from 320 PSI to 300 PSI per updated site pressure vessel code",
     "Regulatory requirement — insurance inspection finding", 4200, 0, "No yield impact; safety compliance",
     "YES — pressure test re-cert required", "IN REVIEW", "2025-08-10", "Pending", "2025-09-15 target", "VDC-005"),
    ("ECO-010", "Furnace Zone Controller Firmware Upgrade", "Process Engineering / Thermco", "Internal Engineering", "EQ-003",
     "Upgrade Thermco zone controller firmware v4.1->v4.3 for improved PID auto-tune algorithm",
     "Process stability improvement — temperature uniformity +/-0.3C better", 7000, 0, "Yield improvement expected +0.2%",
     "YES — process re-qualification run required", "DRAFT", "2025-09-05", "Pending", "TBC", "—"),
]

HEADERS = ["ECO ID", "ECO Title", "Originator", "Origin Type", "Affected Equip", "Change Description", "Reason",
           "Cost Impact (USD)", "Schedule Impact (wks)", "Quality/Yield Impact", "Requalif. Required?",
           "ECO Status", "Design Auth. Approval Date", "Submitted Date", "Impl. Date", "Linked VDC"]


def build(wb):
    ws = wb.create_sheet("S26_Engineering_Change_Orders")
    set_tab_color(ws, 5)
    row = title_block(ws, 5, "S26", "Engineering Change Orders (ECO) Register — Phase II Program",
                       "Formal ECO register for all design changes — internal, customer-driven & regulatory | "
                       "Owner: Sourabh Tarodekar | Related VDCs tracked in S27_Vendor_Design_Changes", n_cols=15)
    header_row = write_headers(ws, row, 1, HEADERS, 5)
    first_row = header_row
    r = header_row
    for (eid, title, orig, otype, eq, desc, reason, cost, sched, qual, requal, status, apdate, submit, impl, vdc) in ECOS:
        ws.cell(row=r, column=1, value=eid)
        ws.cell(row=r, column=2, value=title)
        ws.cell(row=r, column=3, value=orig)
        ws.cell(row=r, column=4, value=otype)
        ws.cell(row=r, column=5, value=eq)
        ws.cell(row=r, column=6, value=desc).alignment = LEFT_WRAP
        ws.cell(row=r, column=7, value=reason).alignment = LEFT_WRAP
        cc = ws.cell(row=r, column=8, value=cost); cc.number_format = USD0; cc.font = BLUE_INPUT
        ws.cell(row=r, column=9, value=sched).font = BLUE_INPUT
        ws.cell(row=r, column=10, value=qual).alignment = LEFT_WRAP
        ws.cell(row=r, column=11, value=requal)
        stc = ws.cell(row=r, column=12, value=status)
        if status == "IMPLEMENTED":
            stc.fill = PatternFill("solid", fgColor=RAG_GREEN)
        elif status == "IN REVIEW":
            stc.fill = PatternFill("solid", fgColor=RAG_AMBER)
        else:
            stc.fill = PatternFill("solid", fgColor="F2F2F2")
        ws.cell(row=r, column=13, value=apdate)
        ws.cell(row=r, column=14, value=submit)
        ws.cell(row=r, column=15, value=impl)
        ws.cell(row=r, column=16, value=vdc)
        for c in range(1, 17):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    last_row = r - 1
    row = r + 2

    row = section_header(ws, row, 1, "ECO SUMMARY", 2, 5)
    stats = [
        ("Total ECOs Raised", f"=COUNTA(A{first_row}:A{last_row})", CUR0),
        ("Implemented / Closed", f'=COUNTIF(L{first_row}:L{last_row},"IMPLEMENTED")', CUR0),
        ("In Review", f'=COUNTIF(L{first_row}:L{last_row},"IN REVIEW")', CUR0),
        ("Total Cost Impact (USD)", f"=SUM(H{first_row}:H{last_row})", USD0),
        ("Requalification Required (count of YES)", f'=COUNTIF(K{first_row}:K{last_row},"YES*")', CUR0),
    ]
    for label, formula, fmt in stats:
        ws.cell(row=row, column=1, value=label).border = BORDER_ALL
        c = ws.cell(row=row, column=2, value=formula)
        c.font = BOLD
        c.number_format = fmt
        c.border = BORDER_ALL
        row += 1

    autosize(ws, {1: 9, 2: 30, 3: 22, 4: 16, 5: 15, 6: 42, 7: 34, 8: 12, 9: 12, 10: 34, 11: 26, 12: 13, 13: 15, 14: 12, 15: 18, 16: 10})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
