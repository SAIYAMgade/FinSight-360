# FinSight 360: Power BI Dashboard & BI Modeling Architecture

## 1. Overview
Power BI serves as the primary Business Intelligence deliverable for **FinSight 360**, presenting an executive-ready, interactive command center for bank executives, portfolio managers, and credit risk committees.

The report is structured into three purpose-built analytical pages:
1. **Executive Portfolio Overview**: Macro portfolio scale, origination trends, terminal status distribution, and high-level risk allocations.
2. **Credit Risk Segmentation**: Deep-dive risk diagnostics examining observed default rates across underwriting grades, loan purposes, income tiers, and leverage bands.
3. **Portfolio Vintages & Data Quality**: Origination vintage maturation tracking, interest rate pricing dispersion, and an automated data quality audit scorecard.

---

## 2. Power BI Architecture & Data Connectivity
Power BI Desktop connects to the FinSight 360 analytical layers using either of two supported modes:

### Mode A: Direct Database Connectivity (PostgreSQL / SQLite)
- **PostgreSQL**: Connect via native PostgreSQL connector to `localhost:5432/finsight360`. Import tables `fact_loans`, `dim_risk_grade`, `dim_loan_purpose`, `dim_date`, and `dq_audit_log`.
- **ODBC**: Connect via SQLite3 ODBC Driver to `data/processed/finsight360.db`.

### Mode B: Direct Analytical Files (CSV / Parquet)
For zero-dependency deployment and standalone evaluation without running database services, import the curated analytical exports from `powerbi/data_exports/`:
- `fact_loans.csv`: Core loan transactions and performance attributes.
- `dim_risk_grade.csv`: Underwriting grade lookup and risk tier groupings.
- `dim_loan_purpose.csv`: Categorized loan purpose definitions.
- `dim_date.csv`: Continuous calendar dimension covering all origination vintages.
- `dq_audit_log.csv`: Automated data quality check results.

---

## 3. Key Design Principles & Color Palette
- **Institutional Banking Color Palette**:
  - Primary Navy (`#1E3A8A`): Used for primary headers, baseline bars, and total volumes.
  - Success / Performing Teal (`#0D9488`): Used for `Fully Paid` facilities and low-risk prime tiers.
  - Credit Risk / Charge-Off Crimson (`#BE123C`): Used for `Charged Off` loans, default rates, and severe data quality alerts.
  - Caution Amber (`#D97706`): Used for warning thresholds and intermediate risk grades.
  - Background Canvas (`#F8FAFC`): Clean off-white background with white visual card containers.
- **Cognitive Clarity**: Restrained visual density; every visual answers a specific business question. Avoids saturated rainbow fills or truncated axes.
- **Denominator Discipline**: All rates handle blanks and zeros via explicit DAX `DIVIDE()` logic.

---

## 4. Supporting Documentation Links
- [Data Model Specification](file:///c:/Users/saiya/Desktop/360/powerbi/data_model.md)
- [DAX Measures Library](file:///c:/Users/saiya/Desktop/360/powerbi/dax_measures.md)
- [Dashboard Specification & Wireframes](file:///c:/Users/saiya/Desktop/360/powerbi/dashboard_specification.md)
- [Actual Dashboard Visual Screenshots](file:///c:/Users/saiya/Desktop/360/reports/screenshots/)
