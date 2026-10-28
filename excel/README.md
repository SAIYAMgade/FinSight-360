# FinSight 360: Executive Excel Reporting Workbook

## 1. Overview
The **FinSight 360 Executive Management Workbook** (`excel/FinSight_360_Executive_Report.xlsx`) is an institutional-grade spreadsheet model built for the Chief Risk Officer (CRO), Credit Committee, and Portfolio Review Team.

It transforms 396,030 individual loan records and automated validation audits into structured, formatted executive sheets designed for decision-making.

---

## 2. Workbook Structure & Tab Navigation

| Sheet Tab | Title | Core Contents | Intended Audience |
| :--- | :--- | :--- | :--- |
| **`Executive_Summary`** | Strategic Portfolio Briefing | High-level KPIs, baseline default rate (19.61%), executive commentary, and navigation index. | Board of Directors, CRO, CEO |
| **`Portfolio_Analysis`** | Portfolio Volume & Purpose | Terminal loan status profile (`Fully Paid` vs `Charged Off`), loan term structure (36m vs 60m), and loan purpose breakdown. | Portfolio Managers, ALCO |
| **`Credit_Risk_Analysis`** | Credit Risk Diagnostics | Underwriting risk grade matrix (A to G), DTI leverage bands, and income tiers. | Credit Risk Analysts, Underwriters |
| **`Trends_and_Vintages`** | Origination Trends | Annual origination volumes (2007–2016), YoY volume growth (%), and vintage default rate maturation. | Strategic Planning, Finance |
| **`Data_Quality`** | Automated Audit Log | Full 12-rule validation scorecard, severity flags, failure rates, and color-coded compliance status. | Data Governance, Compliance |
| **`Data_Dictionary`** | Analytical Schema Reference | Field names, source origins, data types, and transformation logic. | Analytics Engineers, Auditors |

---

## 3. Spreadsheet Design Standards & Best Practices
- **Visual Hierarchy**: Deep Navy (`#1E3A8A`) section headers with crisp white text; light slate sub-headers (`#F1F5F9`).
- **Accounting Number Formatting**:
  - Currency: `$#,##0` (e.g., `$5,589,522,775`)
  - Percentages: `0.00%` (e.g., `19.61%`)
  - Facility Counts: `#,##0` (e.g., `396,030`)
- **Interactive Usability**:
  - Frozen top panes (`Freeze Panes`) enabled across all analytical sheets so column headers remain visible while scrolling.
  - Native Excel formulas (`SUM`, `AVERAGE`) used on totals rows to maintain audit transparency.
  - No external workbook links or broken `#REF!` dependencies.
- **Automated Generation**:
  - Programmatically generated via `scripts/build_excel_report.py`.
  - Can be refreshed on updated data runs with a single command:
    ```bash
    python scripts/build_excel_report.py
    ```
