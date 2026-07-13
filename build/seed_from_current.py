"""
seed_from_current.py — ONE-TIME migration.

Transcribes today's hardcoded data (the EQUIPMENT/SUPPLIERS/RISK_ITEMS
literals in s02/s03/s16, the assumptions sections in s01, and the program
metadata scattered across s33_portfolio_register.py and
assets/js/programs-data.js) into capex_portfolio.db.

After Phase 2 rewires the sheet generators to read from db.py, the source
literals this script transcribes become dead code and get deleted from
s02/s03/s16 — this script is what makes that deletion safe: everything
those lists held is preserved in the database first.

Safe to re-run: every insert is an upsert (ON CONFLICT DO UPDATE), so
running this twice just re-syncs to the same values.
"""
import db

PROGRAMS = [
    dict(program_ref="PRG-001", name="Greenfield Expansion Phase II", short_name="Greenfield Phase II",
         sponsor="Sourabh Tarodekar (Portfolio Director)", program_manager="Sourabh Tarodekar",
         business_unit="Semiconductor & Advanced Process Division",
         phase="G2 — Equipment Build & FAT (Execution)", status="APPROVED — IN EXECUTION",
         phase_tag="IN EXECUTION", phase_tag_class="st-green", has_execution_history=1,
         ar_reference="AR-2025-0082", period="Q2–Q4 2025",
         equip_cost=12525000, install_cost=1345000, contingency=1387000, fx_reserve=485000,
         nre=320000, total_ar_budget=16062000, irr=0.142, npv=9520000, payback_yrs=4.2,
         is_estimate=0, sort_order=1, notes="Full 33-sheet model; financials/schedule/risk fully linked in Excel."),
    dict(program_ref="PRG-002", name="Riverside Automation Upgrade Phase I", short_name="Riverside Phase I",
         sponsor="Sourabh Tarodekar (Portfolio Director)", program_manager="Elena Vargas",
         business_unit="Packaging & Distribution Operations",
         phase="FEL-2 — Feasibility (Pre-Execution)", status="PROPOSED — AWAITING AR APPROVAL",
         phase_tag="PRE-EXECUTION", phase_tag_class="st-amber", has_execution_history=0,
         ar_reference="Pending — targeting Q4-2025 submission", period="FEL-2 planning, 2025",
         equip_cost=2101000, install_cost=281000, contingency=238200, fx_reserve=42000,
         nre=95000, total_ar_budget=2757200, irr=0.168, npv=1850000, payback_yrs=3.1,
         is_estimate=1, sort_order=2, notes="Equipment/supplier/risk data real; IRR/NPV/payback are FEL-2 estimates."),
]

# (equip_id, category, tool_type, supplier, region, currency, unit_cost, qty,
#  install_cost_unit, life_yrs, energy_kwh_hr, maint_rate_pct, throughput_uhr, op_hrs_yr, notes)
EQUIPMENT_PRG1 = [
    ("EQ-001", "Vacuum Pump System", "Dry Screw Vacuum Pump – 250 m³/hr", "Edwards Vacuum", "UK", "EUR", 185000, 4, 22000, 12, 18.5, 0.06, 0, 8320,
     "Requires N2 purge line; facility electrical upgrade needed prior to installation"),
    ("EQ-002", "Vacuum Pump System", "Turbomolecular Pump Assembly – 2000 L/s", "Pfeiffer Vacuum", "DE", "EUR", 310000, 3, 28000, 10, 12.0, 0.05, 0, 8320,
     "Single-source supplier; no qualified alt vendor as of Q1-2025; lead time under review"),
    ("EQ-003", "High-Temp Furnace", "Tube Furnace System – 1200°C / 8-zone", "Thermco Systems", "USA", "USD", 520000, 2, 45000, 15, 95.0, 0.04, 24, 8320,
     "FAT to be conducted at supplier site in Austin, TX; includes process recipe transfer"),
    ("EQ-004", "High-Temp Furnace", "Batch Oxidation Furnace – 1100°C", "Tokyo Electron Ltd", "JP", "JPY", 680000, 2, 52000, 15, 110.0, 0.045, 18, 8320,
     "JPY-denominated; FX hedge required; import duty ~3.2%; installation requires crane lift"),
    ("EQ-005", "Robotics / Automation", "6-Axis Wafer Transfer Robot – SCARA", "Brooks Automation", "USA", "USD", 275000, 6, 18000, 10, 4.2, 0.05, 120, 8320,
     "Software integration with fab MES required; vendor to supply integration team on-site"),
    ("EQ-006", "Robotics / Automation", "Overhead Track Conveyor – 50m loop", "Daifuku", "JP", "JPY", 420000, 1, 85000, 12, 22.0, 0.04, 0, 8320,
     "Single installation; civil works for track mounts included in install cost estimate"),
    ("EQ-007", "Gas Handling System", "Process Gas Cabinet – 6-zone manifold", "Air Liquide Engineering", "FR", "EUR", 195000, 4, 32000, 12, 0.8, 0.06, 0, 8320,
     "Hazmat classified; requires local regulatory permit; supplier quote under negotiation"),
    ("EQ-008", "Gas Handling System", "Bulk Gas Storage & Delivery – N2/O2/Ar", "Linde Engineering", "DE", "EUR", 340000, 1, 120000, 20, 2.5, 0.03, 0, 8320,
     "Facility infrastructure tie-in; utility coordination required with site civil team"),
    ("EQ-009", "PLC Control System", "Distributed Control System – Siemens S7-1500", "Siemens AG", "DE", "EUR", 165000, 5, 15000, 10, 1.2, 0.07, 0, 8320,
     "Software license included; annual subscription renewal at $12K/system; cybersecurity review pending"),
    ("EQ-010", "PLC Control System", "SCADA Integration Platform – Ignition", "Inductive Automation", "USA", "USD", 85000, 3, 8000, 8, 0.5, 0.08, 0, 8320,
     "Server hardware separate line item; IT/OT network segmentation required by InfoSec"),
    ("EQ-011", "Facility Infra – Power", "Dry-Type Transformer – 2 MVA / 480V", "ABB Ltd", "CH", "USD", 210000, 2, 35000, 25, 0.0, 0.02, 0, 8760,
     "Component reused from prior program (legacy); refurbishment cost included in install"),
    ("EQ-012", "Facility Infra – Cooling", "Process Chiller System – 200 kW", "Daikin Applied", "JP", "JPY", 295000, 3, 40000, 15, 68.0, 0.05, 0, 8760,
     "Glycol loop design pending; coordinate with mechanical engineering; JPY FX risk noted"),
    ("EQ-013", "Vacuum Pump System", "Roots Blower Booster – 500 m³/hr", "Busch Vacuum", "DE", "EUR", 125000, 6, 14000, 10, 28.0, 0.06, 0, 8320,
     "Paired with EQ-001 dry screw pumps; interdependent installation sequence required"),
    ("EQ-014", "High-Temp Furnace", "RTP – Rapid Thermal Processor", "Applied Materials", "USA", "USD", 875000, 2, 60000, 12, 85.0, 0.04, 32, 8320,
     "Highest unit cost item; finance approval gate required before PO issuance; AR pending"),
    ("EQ-015", "Robotics / Automation", "AMR Fleet – Autonomous Mobile Robots (×10)", "Mobile Industrial Robots (MiR)", "DK", "EUR", 380000, 1, 45000, 8, 6.0, 0.06, 0, 8320,
     "Fleet management software license included; Wi-Fi infrastructure upgrade required"),
]

EQUIPMENT_PRG2 = [
    ("RV-001", "Robotics / Automation", "Palletizing Robot – 6-Axis, 40kg payload", "Fanuc America", "USA", "USD", 165000, 2, 20000, 10, 3.8, 0.05, 0, 6240,
     "Replaces manual end-of-line palletizing; guarding and safety scanner included in install"),
    ("RV-002", "Packaging Automation", "Case Packer / Cartoning System", "Krones AG", "DE", "EUR", 410000, 1, 55000, 12, 14.0, 0.05, 0, 6240,
     "Single-source specialized cartoning technology; no qualified alt vendor identified"),
    ("RV-003", "Robotics / Automation", "AGV Fleet – Tow/Unit Load (×6)", "Fetch Robotics", "USA", "USD", 85000, 6, 8000, 8, 1.1, 0.06, 0, 6240,
     "Fleet management software license included; warehouse Wi-Fi survey required pre-deployment"),
    ("RV-004", "Quality / Automation", "Vision Inspection System (×3)", "Cognex Corporation", "USA", "USD", 62000, 3, 6000, 8, 0.6, 0.04, 0, 6240,
     "In-line case/label inspection; integrates with existing MES via OPC-UA"),
    ("RV-005", "PLC Control System", "Warehouse Control System Integration", "Rockwell Automation", "USA", "USD", 145000, 1, 25000, 10, 1.0, 0.06, 0, 6240,
     "Integrates AGV fleet, conveyor, and WMS; software license + 1yr support included"),
    ("RV-006", "Material Handling", "Conveyor & Sortation System", "Dematic Corp", "USA", "USD", 520000, 1, 95000, 15, 26.0, 0.04, 0, 6240,
     "Longest lead item; civil floor anchoring required; phased cutover to avoid line downtime"),
]

# (supplier, component_type, equip_ref, region, currency, std_lt, current_lt, reliability, single_source, alt_available, notes)
SUPPLIERS_PRG1 = [
    ("Edwards Vacuum", "Dry Screw Vacuum Pumps", "EQ-001", "UK", "EUR", 14, 18, 82, 0, 1,
     "Reliability impacted by post-Brexit logistics; alt vendor pre-qual in progress with Busch"),
    ("Pfeiffer Vacuum", "Turbomolecular Pumps", "EQ-002", "DE", "EUR", 16, 26, 88, 1, 0,
     "CRITICAL – single source; no qualified alternative; EQ-002 delivery risk HIGH; escalate to program director"),
    ("Thermco Systems", "High-Temp Tube Furnaces", "EQ-003", "USA", "USD", 18, 20, 91, 0, 1,
     "Preferred supplier; strong historical performance; alt supplier (BTU International) pre-qualified"),
    ("Tokyo Electron Ltd (TEL)", "Batch Oxidation Furnaces", "EQ-004", "JP", "JPY", 20, 28, 85, 0, 1,
     "JPY currency risk; FX hedge executed Q4-2024; alt: Kokusai Electric pre-qualified"),
    ("Brooks Automation", "Wafer Transfer Robots (SCARA)", "EQ-005", "USA", "USD", 12, 14, 90, 0, 1,
     "Software integration complexity is primary risk; not supply risk; support SLA confirmed"),
    ("Daifuku", "Overhead Conveyor Track System", "EQ-006", "JP", "JPY", 22, 30, 83, 1, 0,
     "Single source for overhead track design; civil interface drawings required 8 wks prior to FAT"),
    ("Air Liquide Engineering", "Process Gas Cabinets", "EQ-007", "FR", "EUR", 16, 22, 79, 0, 1,
     "Quote under negotiation; delivery risk moderate; Matheson Gas alt supplier evaluated"),
    ("Linde Engineering", "Bulk Gas Storage & Delivery", "EQ-008", "DE", "EUR", 24, 32, 86, 0, 1,
     "Long procurement cycle; requires site permit coordination; 32-wk lead time confirmed by supplier"),
    ("Siemens AG", "Distributed Control Systems", "EQ-009", "DE", "EUR", 10, 14, 92, 0, 1,
     "Strong supply reliability; cybersecurity review adds 3-wk internal approval cycle"),
    ("Inductive Automation", "SCADA Platform Licenses", "EQ-010", "USA", "USD", 4, 5, 95, 0, 1,
     "Software license only; low supply risk; primary risk is IT/OT integration complexity"),
    ("ABB Ltd", "Dry-Type Transformers", "EQ-011", "CH", "USD", 14, 20, 87, 0, 1,
     "Component partially reused from prior program; new units on 20-wk market lead time"),
    ("Daikin Applied", "Process Chiller Systems", "EQ-012", "JP", "JPY", 16, 20, 89, 0, 1,
     "Glycol loop interface drawings required prior to FAT; JPY exposure monitored"),
    ("Busch Vacuum", "Roots Blower Boosters", "EQ-013", "DE", "EUR", 12, 15, 88, 0, 1,
     "Paired supply with Edwards EQ-001; coordinated delivery schedule required"),
    ("Applied Materials", "Rapid Thermal Processors (RTP)", "EQ-014", "USA", "USD", 20, 24, 90, 0, 1,
     "Highest value item; supplier requires 30% deposit at PO; finance pre-approval required"),
    ("Mobile Industrial Robots (MiR)", "AMR Fleet – 10 Units", "EQ-015", "DK", "EUR", 14, 18, 84, 0, 1,
     "Fleet SW license bundled; Wi-Fi site survey required 6 wks pre-installation"),
]

SUPPLIERS_PRG2 = [
    ("Fanuc America", "Palletizing Robots", "RV-001", "USA", "USD", 10, 12, 91, 0, 1,
     "Deep bench of qualified integrators; low supply risk; standard robot platform"),
    ("Krones AG", "Case Packer / Cartoning Systems", "RV-002", "DE", "EUR", 20, 24, 86, 1, 0,
     "Single-source specialized cartoning technology; no qualified alternative identified"),
    ("Fetch Robotics", "AGV Fleet Units", "RV-003", "USA", "USD", 8, 9, 93, 0, 1,
     "Mature AGV platform; Locus Robotics evaluated as viable alternate"),
    ("Cognex Corporation", "Vision Inspection Systems", "RV-004", "USA", "USD", 6, 7, 95, 0, 1,
     "Commodity machine-vision hardware; Keyence pre-qualified as alternate"),
    ("Rockwell Automation", "Warehouse Control System", "RV-005", "USA", "USD", 8, 9, 94, 0, 1,
     "Strong integrator relationship; low supply risk; standard PlantPAx platform"),
    ("Dematic Corp", "Conveyor & Sortation Systems", "RV-006", "USA", "USD", 16, 20, 88, 0, 1,
     "Complex site-specific integration; Honeywell Intelligrated evaluated as alternate"),
]

# (equip_ref, supplier, component, std_lead, current_lead, delay_prob, sched_impact,
#  replace_difficulty, single_source, buffer_stock, mitigation, status)
RISK_ITEMS_PRG1 = [
    ("EQ-001", "Edwards Vacuum", "Dry Screw Pump – Complete Unit", 14, 18, 0.35, 3, 2, 0, 0,
     "Expedite order; confirm delivery schedule with supplier weekly; pre-qualify Busch as alt", "IN PROGRESS"),
    ("EQ-002", "Pfeiffer Vacuum", "Turbomolecular Pump – Complete Unit", 16, 26, 0.55, 5, 5, 1, 0,
     "CRITICAL PATH: Escalate to VP Supply Chain; evaluate rebuilt unit as bridge; initiate alt vendor qual", "ESCALATED"),
    ("EQ-002", "Pfeiffer Vacuum", "Turbomolecular Controller Electronics", 12, 18, 0.45, 4, 5, 1, 0,
     "Controller firmware proprietary; no drop-in alt; request safety stock commitment from supplier", "ESCALATED"),
    ("EQ-003", "Thermco Systems", "Tube Furnace – Hot Zone Assembly", 18, 20, 0.20, 4, 3, 0, 0,
     "BTU International validated as alt; maintain contact; include alt option in RFQ", "MONITORED"),
    ("EQ-003", "Thermco Systems", "8-Zone Heating Element Set", 10, 12, 0.15, 3, 2, 0, 1,
     "2-set buffer stock maintained; supplier reliability high; no immediate action required", "OK"),
    ("EQ-004", "Tokyo Electron (TEL)", "Batch Furnace – Complete System", 20, 28, 0.40, 5, 4, 0, 0,
     "JPY FX hedge confirmed; increase FAT scope to 3 weeks; dedicated TEL PM assigned", "IN PROGRESS"),
    ("EQ-004", "Tokyo Electron (TEL)", "Process Recipe Transfer Package", None, None, 0.30, 4, 4, 1, 0,
     "Non-tangible risk: recipe IP held by TEL; require contractual data transfer clause at PO stage", "LEGAL REVIEW"),
    ("EQ-005", "Brooks Automation", "SCARA Robot – Mechanical Assembly", 12, 14, 0.15, 3, 3, 0, 0,
     "Brooks delivery historically reliable; no action required; standard monitoring", "OK"),
    ("EQ-005", "Brooks Automation", "MES Software Integration Module", None, None, 0.45, 4, 4, 1, 0,
     "Integration complexity risk — not supply risk; assign Brooks SW engineer on-site 4 wks pre-FAT", "IN PROGRESS"),
    ("EQ-006", "Daifuku", "Overhead Track System – Civil Interface", 22, 30, 0.50, 4, 5, 1, 0,
     "Civil drawings required 8 wks pre-install; freeze layout by Week 6; no alt track supplier", "ESCALATED"),
    ("EQ-007", "Air Liquide Eng.", "Gas Cabinet – Complete Assembly", 16, 22, 0.40, 3, 3, 0, 0,
     "Quote under negotiation; delay increases if PO not placed by target date; expedite sourcing decision", "IN PROGRESS"),
    ("EQ-007", "Air Liquide Eng.", "Hazmat Permit – Regulatory", None, None, 0.35, 5, 5, 1, 0,
     "Permit lead time 8-12 wks; submit application immediately; failure impacts entire gas system install", "ACTION REQ'D"),
    ("EQ-008", "Linde Engineering", "Bulk Gas Storage Vessel", 24, 32, 0.35, 4, 3, 0, 0,
     "Long-lead vessel; PO must be placed by program Week 4; civil pad work parallel path", "IN PROGRESS"),
    ("EQ-009", "Siemens AG", "S7-1500 PLC Hardware Set", 10, 14, 0.15, 2, 2, 0, 1,
     "Strong supply reliability; buffer stock of 1 spare CPU maintained; low risk", "OK"),
    ("EQ-009", "Siemens AG", "Cybersecurity Compliance Review", None, None, 0.25, 3, 3, 1, 0,
     "Internal InfoSec review adds 3 wks; submit documentation package 6 wks pre-installation", "IN PROGRESS"),
    ("EQ-011", "ABB Ltd", "2 MVA Dry-Type Transformer", 14, 20, 0.25, 4, 3, 0, 0,
     "Reuse of legacy unit partially mitigates; new unit on order; monitor delivery", "MONITORED"),
    ("EQ-012", "Daikin Applied", "Chiller – Complete Package", 16, 20, 0.20, 3, 2, 0, 0,
     "Glycol loop interface design must be finalized prior to FAT; coordinate with mechanical team", "IN PROGRESS"),
    ("EQ-014", "Applied Materials", "RTP Tool – Complete System", 20, 24, 0.25, 5, 4, 0, 0,
     "Highest-value item; AMAT requires 30% deposit at PO; finance pre-approval gate required", "ACTION REQ'D"),
    ("EQ-015", "MiR (Mobile Industrial Robots)", "AMR Fleet – 10 Units", 14, 18, 0.30, 2, 2, 0, 0,
     "Wi-Fi infrastructure survey required 6 wks pre-delivery; coordinate with IT/OT team", "MONITORED"),
]

RISK_ITEMS_PRG2 = [
    ("RV-001", "Fanuc America", "Palletizing Robot – Complete Unit", 10, 12, 0.15, 2, 2, 0, 0,
     "Standard robot platform; low risk; monitor delivery per standard cadence", "OK"),
    ("RV-002", "Krones AG", "Cartoning System – Complete Unit", 20, 24, 0.30, 4, 4, 1, 0,
     "Single-source specialized tech; no qualified alt; monitor delivery weekly during build", "IN PROGRESS"),
    ("RV-003", "Fetch Robotics", "AGV Fleet – Complete Units", 8, 9, 0.10, 2, 1, 0, 0,
     "Mature platform; low supply risk; standard monitoring", "OK"),
    ("RV-004", "Cognex Corporation", "Vision Inspection – Complete Units", 6, 7, 0.10, 2, 1, 0, 1,
     "Commodity vision hardware; Keyence pre-qualified alt on file", "OK"),
    ("RV-005", "Rockwell Automation", "WCS Integration – Software/Hardware", 8, 9, 0.20, 3, 2, 0, 0,
     "Standard PlantPAx platform; integrator has strong track record", "MONITORED"),
    ("RV-006", "Dematic Corp", "Conveyor & Sortation – Complete System", 16, 20, 0.25, 3, 3, 0, 0,
     "Complex site-specific integration; phased cutover plan mitigates schedule risk", "MONITORED"),
]

# (section, parameter, value, unit, source, date_validated, notes)
# `value` may be a number (stored in assumptions.value) or a string (stored in
# assumptions.value_text) — seed() below routes each to the right column.
ASSUMPTIONS = [
    ("ENERGY & UTILITIES", "Energy Price – Electricity", 0.110, "USD/kWh", "EIA Industrial Rate Survey – US Avg 2024", "2025-01",
     "Used in Annual Energy Cost calculations across S02, S05 TCO model"),
    ("ENERGY & UTILITIES", "Natural Gas Price", 4.800, "USD/MMBtu", "EIA Natural Gas Industrial Price – 2024", "2025-01",
     "Used for high-temp furnace operating cost estimation"),
    ("ENERGY & UTILITIES", "Cooling Water Cost", 0.018, "USD/gallon", "Site Utility Rate Schedule Rev C", "2025-01",
     "Applicable to chiller and process cooling loads"),
    ("ENERGY & UTILITIES", "N2 Bulk Gas Cost", 0.045, "USD/scf", "Site Utility Rate Schedule Rev C", "2025-01",
     "Applicable to gas handling system operating cost"),
    ("FINANCIAL & DISCOUNT ASSUMPTIONS", "Discount Rate (WACC)", 0.08, "—", "Finance Department; WACC model approved Q4-2024", "2025-01",
     "Used in NPV calculations; 8% reflects blended cost of capital"),
    ("FINANCIAL & DISCOUNT ASSUMPTIONS", "Project Horizon", 10, "Years", "Standard CapEx lifecycle policy", "2025-01",
     "All TCO and NPV models use 10-year horizon"),
    ("FINANCIAL & DISCOUNT ASSUMPTIONS", "Tax Rate (Effective)", 0.21, "—", "US Federal + State blended estimate", "2025-01",
     "Applied in AR payback model for after-tax IRR"),
    ("FINANCIAL & DISCOUNT ASSUMPTIONS", "CapEx Depreciation Method", "MACRS 7-yr", "—", "Finance / Tax Counsel guidance", "2025-01",
     "Per AR Summary financial justification"),
    ("FINANCIAL & DISCOUNT ASSUMPTIONS", "Inflation Rate", 0.025, "—", "Corporate finance planning assumption", "2025-01",
     "Used to escalate Year 2-10 OpEx in TCO model"),
    ("LABOR RATES", "Fabrication Shop Rate", 95.00, "USD/hr", "Supplier benchmarking; 2024 MW industrial rate", "2025-01",
     "Used in Should-Cost labor model (S04)"),
    ("LABOR RATES", "Engineering Labor Rate", 120.00, "USD/hr", "Internal engineering rate card Rev 2024", "2025-01",
     "Used in NRE and program labor estimates"),
    ("LABOR RATES", "Installation Labor Rate", 85.00, "USD/hr", "Facilities contractor rate card", "2025-01",
     "Used in on-site installation cost estimates"),
    ("LABOR RATES", "Field Service Rate (Supplier)", 175.00, "USD/hr", "Supplier FSE rate benchmark", "2025-01",
     "Used in downtime / MTTR cost modelling"),
    ("EQUIPMENT PERFORMANCE", "Equipment Uptime Target", 0.92, "—", "Program engineering specification", "2025-01",
     "92% uptime = 608 downtime hrs/yr basis for MTBF model"),
    ("EQUIPMENT PERFORMANCE", "Planned Maintenance Downtime", 0.04, "—", "Maintenance planning schedule", "2025-01",
     "4% of annual hours allocated to preventive maintenance"),
    ("EQUIPMENT PERFORMANCE", "Process Yield Assumption", 0.96, "—", "Engineering process spec", "2025-01",
     "Used in capacity model to calculate effective throughput"),
    ("EQUIPMENT PERFORMANCE", "Production Value per Hour", 4500.00, "USD/hr", "Finance — fully-loaded production cost model", "2025-01",
     "Downtime Cost = Value/hr × MTTR hrs"),
    ("SUPPLIER COST MODEL INPUTS", "Supplier Margin – Low", 0.15, "—", "Benchmarking; competitive-bid suppliers", "2025-01",
     "Lower bound; applied to multi-source components"),
    ("SUPPLIER COST MODEL INPUTS", "Supplier Margin – High", 0.25, "—", "Benchmarking; sole-source suppliers", "2025-01",
     "Upper bound; applied to single-source components"),
    ("SUPPLIER COST MODEL INPUTS", "Material Scrap Factor – Low", 0.05, "—", "Engineering; precision machined parts", "2025-01",
     "5% scrap on raw material purchases"),
    ("SUPPLIER COST MODEL INPUTS", "Material Scrap Factor – High", 0.08, "—", "Engineering; cast / welded assemblies", "2025-01",
     "8% scrap on complex fabrications"),
    ("SUPPLIER COST MODEL INPUTS", "Material Price – Steel (304 SS)", 3.800, "USD/kg", "Metal bulletin Q1-2025", "2025-01",
     "Used in vacuum chamber and furnace body cost estimates"),
    ("SUPPLIER COST MODEL INPUTS", "Material Price – Aluminum", 4.200, "USD/kg", "Metal bulletin Q1-2025", "2025-01",
     "Used in robotics frame and structural components"),
    ("SUPPLIER COST MODEL INPUTS", "Material Price – Copper", 9.500, "USD/kg", "COMEX spot Q1-2025", "2025-01",
     "Used in transformer winding and electrical bus cost estimates"),
    ("DEPLOYMENT TIMELINE ASSUMPTIONS", "Supplier Manufacturing Duration", 20, "Weeks", "Program schedule baseline Rev 1.0", "2025-01",
     "Range: 16–24 wks depending on equipment complexity"),
    ("DEPLOYMENT TIMELINE ASSUMPTIONS", "Factory Acceptance Testing (FAT)", 2, "Weeks", "Standard FAT protocol – all equipment", "2025-01",
     "2 weeks minimum; may extend for complex systems"),
    ("DEPLOYMENT TIMELINE ASSUMPTIONS", "International Shipping Duration", 3, "Weeks", "Freight forwarder estimate; ocean freight", "2025-01",
     "Air freight contingency +50% cost; used for risk scenario"),
    ("DEPLOYMENT TIMELINE ASSUMPTIONS", "On-Site Installation", 4, "Weeks", "Facilities project plan Rev A", "2025-01",
     "Per equipment platform; parallel installation possible"),
    ("DEPLOYMENT TIMELINE ASSUMPTIONS", "Utility Hookup", 2, "Weeks", "Facilities electrical + mechanical schedule", "2025-01",
     "Includes inspection and commissioning sign-off"),
    ("DEPLOYMENT TIMELINE ASSUMPTIONS", "Process Qualification (PQ)", 5, "Weeks", "Process engineering qualification plan", "2025-01",
     "Range: 4–6 wks; 5 wks used as baseline"),
    ("FX SENSITIVITY ASSUMPTIONS", "USD/EUR Exchange Rate (Baseline)", 1.09, "USD per EUR", "Bloomberg rates Q1-2025 average", "2025-01",
     "Baseline conversion rate for EUR-denominated equipment"),
    ("FX SENSITIVITY ASSUMPTIONS", "USD/JPY Exchange Rate (Baseline)", 149.5, "JPY per USD", "Bloomberg rates Q1-2025 average", "2025-01",
     "Baseline conversion rate for JPY-denominated equipment"),
    ("FX SENSITIVITY ASSUMPTIONS", "EUR Sensitivity – Adverse", 1.15, "USD per EUR", "FX stress scenario +6%", "2025-01",
     "1% move in EUR/USD = ~$85K portfolio cost impact"),
    ("FX SENSITIVITY ASSUMPTIONS", "EUR Sensitivity – Favorable", 1.03, "USD per EUR", "FX stress scenario -6%", "2025-01",
     "Favorable scenario used in S13 Scenario Analysis"),
    ("FX SENSITIVITY ASSUMPTIONS", "JPY Sensitivity – Adverse", 142.00, "JPY per USD", "FX stress scenario (JPY strengthens)", "2025-01",
     "Stronger JPY = higher USD cost for JPY equipment"),
    ("FX SENSITIVITY ASSUMPTIONS", "JPY Sensitivity – Favorable", 157.00, "JPY per USD", "FX stress scenario (JPY weakens)", "2025-01",
     "Weaker JPY = lower USD cost for JPY equipment"),
]


def seed():
    db.init_schema()
    conn = db.get_connection()

    for row in PROGRAMS:
        db.upsert_program(row, conn=conn)

    for i, e in enumerate(EQUIPMENT_PRG1):
        db.upsert_equipment(dict(zip(
            ["equip_id", "category", "tool_type", "supplier", "region", "currency", "unit_cost", "qty",
             "install_cost_unit", "life_yrs", "energy_kwh_hr", "maint_rate_pct", "throughput_uhr",
             "op_hrs_yr", "notes"], e), program_ref="PRG-001", sort_order=i), conn=conn)
    for i, e in enumerate(EQUIPMENT_PRG2):
        db.upsert_equipment(dict(zip(
            ["equip_id", "category", "tool_type", "supplier", "region", "currency", "unit_cost", "qty",
             "install_cost_unit", "life_yrs", "energy_kwh_hr", "maint_rate_pct", "throughput_uhr",
             "op_hrs_yr", "notes"], e), program_ref="PRG-002", sort_order=i), conn=conn)

    conn.execute("DELETE FROM suppliers")  # suppliers has no natural unique key; reseed clean
    for i, s in enumerate(SUPPLIERS_PRG1):
        db.upsert_supplier(dict(zip(
            ["supplier_name", "component_type", "equip_ref", "region", "currency", "std_lt_wks",
             "current_lt_wks", "reliability", "single_source", "alt_supplier_available", "notes"], s),
            program_ref="PRG-001", sort_order=i), conn=conn)
    for i, s in enumerate(SUPPLIERS_PRG2):
        db.upsert_supplier(dict(zip(
            ["supplier_name", "component_type", "equip_ref", "region", "currency", "std_lt_wks",
             "current_lt_wks", "reliability", "single_source", "alt_supplier_available", "notes"], s),
            program_ref="PRG-002", sort_order=i), conn=conn)

    conn.execute("DELETE FROM risk_items")
    for i, r in enumerate(RISK_ITEMS_PRG1):
        db.upsert_risk_item(dict(zip(
            ["equip_ref", "supplier", "component", "std_lead", "current_lead", "delay_prob",
             "sched_impact", "replace_difficulty", "single_source", "buffer_stock", "mitigation", "status"], r),
            program_ref="PRG-001", sort_order=i), conn=conn)
    for i, r in enumerate(RISK_ITEMS_PRG2):
        db.upsert_risk_item(dict(zip(
            ["equip_ref", "supplier", "component", "std_lead", "current_lead", "delay_prob",
             "sched_impact", "replace_difficulty", "single_source", "buffer_stock", "mitigation", "status"], r),
            program_ref="PRG-002", sort_order=i), conn=conn)

    conn.execute("DELETE FROM assumptions")
    for i, a in enumerate(ASSUMPTIONS):
        row = dict(zip(["section", "parameter", "value", "unit", "source", "date_validated", "notes"], a))
        if isinstance(row["value"], str):
            row["value_text"] = row["value"]
            row["value"] = None
        db.upsert_assumption(dict(row, program_ref=None, sort_order=i), conn=conn)

    conn.commit()
    conn.close()

    print("Seed complete.")
    print("Programs:", len(PROGRAMS))
    print("Equipment rows:", len(EQUIPMENT_PRG1) + len(EQUIPMENT_PRG2))
    print("Supplier rows:", len(SUPPLIERS_PRG1) + len(SUPPLIERS_PRG2))
    print("Risk item rows:", len(RISK_ITEMS_PRG1) + len(RISK_ITEMS_PRG2))
    print("Assumption rows:", len(ASSUMPTIONS))


if __name__ == "__main__":
    seed()
