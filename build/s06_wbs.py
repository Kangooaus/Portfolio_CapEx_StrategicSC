from gen_common import *

# WBS Code, Level, Name, Function, Duration, Start, End, Deliverable
WBS = [
    ("1.0", 1, "GREENFIELD EXPANSION PHASE II — PROGRAM", "Program Management", 46, 1, 46, "Full program from AR approval to production release"),
    ("1.1", 2, "PROGRAM MANAGEMENT", "Program Management", 46, 1, 46, "Program governance and control"),
    ("1.1.1", 3, "Program kick-off & AR execution", "PM / Finance", 1, 1, 1, "AR signed, cost centre open, PO authority issued"),
    ("1.1.2", 3, "Stakeholder communication plan", "PM / Eng Leadership", 1, 1, 2, "RACI matrix, communication cadence agreed"),
    ("1.1.3", 3, "Program schedule baseline", "PM / Scheduling", 1, 1, 2, "CPM schedule issued, baseline locked"),
    ("1.1.4", 3, "Weekly program review cadence", "PM", 45, 2, 46, "Weekly status reports issued throughout program"),
    ("1.1.5", 3, "Lessons learned & close-out report", "PM", 1, 46, 46, "Program close-out document issued"),
    ("1.2", 2, "SOURCING & PROCUREMENT", "Supply Chain / Sourcing", 14, 1, 14, "All long-lead POs placed; contracts executed"),
    ("1.2.1", 3, "RFQ issue — long-lead equipment (EQ-002,004,008,014)", "Sourcing", 1, 1, 1, "RFQs issued to shortlisted suppliers"),
    ("1.2.2", 3, "Supplier commercial evaluation & BAFO", "Sourcing", 2, 1, 3, "Bid tabulations complete; BAFO received"),
    ("1.2.3", 3, "Negotiation & contract award — EQ-014 (AMAT RTP)", "Sourcing / Legal", 2, 2, 4, "PO issued; 30% deposit paid"),
    ("1.2.4", 3, "Negotiation & contract award — EQ-002 (Pfeiffer TMP)", "Sourcing / Legal", 2, 2, 4, "PO issued; FX hedge confirmed"),
    ("1.2.5", 3, "Negotiation & contract award — EQ-004 (TEL Furnace)", "Sourcing / Legal", 2, 2, 4, "PO issued; JPY hedge executed"),
    ("1.2.6", 3, "Negotiation & contract award — remaining equipment", "Sourcing", 2, 3, 5, "All remaining POs placed"),
    ("1.2.7", 3, "FX forward contract execution — EUR & JPY", "Finance / Treasury", 1, 3, 4, "Hedge contracts in place before PO placement"),
    ("1.2.8", 3, "Import/export documentation package", "Logistics / Trade Compliance", 2, 4, 6, "HS codes filed; import bonds arranged"),
    ("1.2.9", 3, "Shimadzu alt-source qualification initiation (EQ-002)", "Sourcing / Engineering", 8, 4, 12, "Alt vendor qual program started; TMP-3203L under test"),
    ("1.3", 2, "ENGINEERING", "Engineering / Process", 20, 1, 20, "Design freeze; FAT specifications issued"),
    ("1.3.1", 3, "Equipment technical specification review", "Process / Mech Eng", 2, 1, 3, "Supplier specs signed off; deviation log issued"),
    ("1.3.2", 3, "FAT protocol development — all equipment", "Process Engineering", 3, 2, 5, "FAT protocols issued; supplier acceptance"),
    ("1.3.3", 3, "Utility design package — electrical, gas, cooling", "Facilities Engineering", 4, 2, 6, "Utility design drawings issued for civil/mech"),
    ("1.3.4", 3, "Site layout & equipment placement plan", "Facilities / Mech Eng", 3, 3, 6, "Final floor plan approved; civil works can start"),
    ("1.3.5", 3, "Integration spec — MES/SCADA/DCS", "Controls / IT-OT", 4, 3, 7, "Integration design spec issued and approved"),
    ("1.3.6", 3, "Process recipe transfer — TEL EQ-004", "Process Engineering / TEL", 3, 5, 8, "Contractual recipe transfer clause executed; recipes received"),
    ("1.3.7", 3, "Cybersecurity review — Siemens DCS", "InfoSec / Engineering", 3, 5, 8, "Cybersecurity approval issued for OT network connection"),
    ("1.3.8", 3, "Engineering change order management", "Engineering", "ongoing", 1, 46, "ECO register maintained throughout program"),
    ("1.4", 2, "SUPPLIER FABRICATION & FAT", "Supply Chain / Engineering", 26, 1, 27, "All equipment at FAT complete; ready to ship"),
    ("1.4.1", 3, "EQ-014 (AMAT RTP) — manufacturing & FAT", "AMAT / Engineering", 24, 1, 25, "RTP units pass FAT; shipping released"),
    ("1.4.2", 3, "EQ-002 (Pfeiffer TMP) — manufacturing & FAT [CRITICAL PATH]", "Pfeiffer / Engineering", 26, 1, 27, "CRITICAL PATH: TMPs pass FAT; shipping released"),
    ("1.4.3", 3, "EQ-004 (TEL Batch Furnace) — manufacturing & FAT", "TEL / Engineering", 28, 1, 29, "Batch furnace FAT complete; JPY invoice settled"),
    ("1.4.4", 3, "EQ-003 (Thermco Tube Furnace) — manufacturing & FAT", "Thermco / Engineering", 20, 2, 22, "Tube furnace FAT at Austin TX; recipe transfer"),
    ("1.4.5", 3, "EQ-005 (Brooks SCARA) — manufacturing & FAT", "Brooks / Engineering", 14, 3, 17, "Robot units FAT complete; MES integration tested"),
    ("1.4.6", 3, "EQ-008 (Linde Bulk Gas) — manufacturing", "Linde / Facilities", 32, 1, 33, "Longest LT: bulk vessel shipped on schedule"),
    ("1.4.7", 3, "Remaining equipment — manufacturing & FAT", "Various suppliers", "10-18", 2, 20, "All units pass FAT; no open NCRs"),
    ("1.5", 2, "LOGISTICS", "Supply Chain / Logistics", 8, 15, 28, "All equipment delivered to site; no customs holds"),
    ("1.5.1", 3, "International freight booking — JPY equipment", "Logistics", 2, 15, 17, "TEL, Daikin, Daifuku freight booked; sea freight"),
    ("1.5.2", 3, "International freight booking — EUR equipment", "Logistics", 2, 15, 17, "EUR equipment freight arranged; road/air options"),
    ("1.5.3", 3, "Customs clearance — all international equipment", "Trade Compliance", 2, 17, 24, "Customs cleared; duty paid; no holds"),
    ("1.5.4", 3, "Final delivery & receipt inspection — site", "Logistics / Engineering", 3, 18, 28, "All equipment received, inspected; CRs raised if needed"),
    ("1.6", 2, "SITE READINESS", "Facilities / Civil", 20, 1, 20, "All utilities ready; floor loading confirmed; permits"),
    ("1.6.1", 3, "Structural floor reinforcement — EQ-004 zone", "Civil Engineering", 6, 3, 9, "Floor certified for 680kg/m² furnace load"),
    ("1.6.2", 3, "Electrical infrastructure — transformers & feeds", "Electrical Engineering", 10, 2, 12, "480V feeds complete; EQ-011 energized"),
    ("1.6.3", 3, "Cooling loop installation — glycol system", "Mechanical Engineering", 8, 4, 12, "Glycol loop pressure-tested; chiller tie-in complete"),
    ("1.6.4", 3, "Gas system infrastructure — hazmat permit", "Facilities / Regulatory", 12, 1, 13, "Hazmat permit received; gas lines installed"),
    ("1.6.5", 3, "Wi-Fi infrastructure upgrade — AMR/OT network", "IT/OT Engineering", 6, 6, 12, "Wi-Fi survey complete; AP installed; throughput confirmed"),
    ("1.6.6", 3, "Clean room / ESD zone preparation", "Facilities", 4, 8, 12, "ESD flooring installed; HVAC certified; gown area ready"),
    ("1.7", 2, "INSTALLATION & COMMISSIONING", "Installation / Engineering", 14, 19, 33, "All equipment mechanically installed; utilities connected"),
    ("1.7.1", 3, "EQ-014 RTP installation", "Installation Team", 2, 20, 22, "RTP installed; electrical connected; safety interlocks tested"),
    ("1.7.2", 3, "EQ-003/004 furnace installation", "Installation Team", 3, 20, 23, "Furnaces installed; N2 purge connected; crane lift complete"),
    ("1.7.3", 3, "EQ-005 robot installation & MES integration", "Installation / IT", 3, 20, 23, "Robots calibrated; MES endpoints mapped; integration tested"),
    ("1.7.4", 3, "EQ-006 overhead conveyor installation", "Daifuku / Civil", 4, 21, 25, "Track mounts installed; conveyor commissioned; safety scan"),
    ("1.7.5", 3, "Utility tie-in — all equipment", "Facilities / Engineering", 4, 22, 26, "All utilities connected; interlock logic verified"),
    ("1.7.6", 3, "EQ-002 TMP installation [CRITICAL PATH]", "Installation / Pfeiffer", 2, 28, 30, "TMPs installed; roughing pumps connected; leak test"),
    ("1.7.7", 3, "EQ-008 bulk gas delivery final installation", "Linde / Facilities", 2, 30, 32, "Bulk vessel on-site; gas distribution connected; permit closed"),
    ("1.8", 2, "PROCESS QUALIFICATION & PRODUCTION RELEASE", "Process Engineering", 14, 33, 46, "All 15 platforms process-qualified; G5 production release"),
    ("1.8.1", 3, "G4 qualification — EQ-014 RTP", "Process Eng / AMAT", 3, 33, 36, "RTP qualification wafers meet spec; PQ report issued"),
    ("1.8.2", 3, "G4 qualification — EQ-003/004 furnaces", "Process Eng / Thermco / TEL", 4, 34, 38, "Furnace temperature uniformity and oxidation rates certified"),
    ("1.8.3", 3, "G4 qualification — EQ-005 robots & MES", "Process Eng / Brooks", 3, 35, 38, "Robot repeatability ±0.1mm; MES integration validated"),
    ("1.8.4", 3, "G4 qualification — all remaining equipment", "Process Engineering", 3, 36, 39, "All 15 platforms in qualified state"),
    ("1.8.5", 3, "SOP documentation & operator training", "Process Eng / Training", 3, 38, 41, "SOPs issued; all operators trained and signed off"),
    ("1.8.6", 3, "Spare parts receipt & inventory loading", "Supply Chain / Maintenance", 2, 38, 40, "Critical spares stocked; CMMS loaded; reorder triggers set"),
    ("1.8.7", 3, "G5 production release — handover to Operations", "PM / Process Eng / Ops", 2, 44, 46, "Formal handover complete; program closed"),
]

HEADERS = ["WBS Code", "Level", "Workstream / Work Package", "Responsible Function",
           "Duration Est (wks)", "Start Wk", "End Wk", "Deliverable / Exit Criterion"]


def build(wb):
    ws = wb.create_sheet("S06_WBS")
    set_tab_color(ws, 2)
    row = title_block(ws, 2, "S06", "Work Breakdown Structure (WBS) — Greenfield Expansion Phase II",
                       "Program: Greenfield Expansion Phase II | Owner: Sourabh Tarodekar | Status: Active | All dates 2025 | "
                       "WBS hierarchy: Level 1 = Program | Level 2 = Workstream | Level 3 = Work Package | "
                       "WBS codes used as Activity IDs in S07_CPM_Master_Schedule", n_cols=8)
    header_row = write_headers(ws, row, 1, HEADERS, 2)
    r = header_row
    for code, level, name, func, dur, start, end, deliv in WBS:
        c1 = ws.cell(row=r, column=1, value=code)
        c2 = ws.cell(row=r, column=2, value=level)
        c3 = ws.cell(row=r, column=3, value=("    " * (level - 1)) + name)
        if level <= 2:
            c3.font = BOLD
            for cc in (1, 2, 3, 4, 5, 6, 7, 8):
                ws.cell(row=r, column=cc).fill = zone_fill_light(2)
        ws.cell(row=r, column=4, value=func)
        ws.cell(row=r, column=5, value=dur)
        ws.cell(row=r, column=6, value=start)
        ws.cell(row=r, column=7, value=end)
        nc = ws.cell(row=r, column=8, value=deliv)
        nc.alignment = LEFT_WRAP
        for c in range(1, 9):
            ws.cell(row=r, column=c).border = BORDER_ALL
        r += 1
    autosize(ws, {1: 8, 2: 7, 3: 48, 4: 24, 5: 12, 6: 9, 7: 8, 8: 50})
    freeze_below(ws, header_row + 1)
    return {"sheet": ws.title}
