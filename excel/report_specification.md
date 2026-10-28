# FinSight 360: Excel Report Technical Specification

This document details the layout structure, cell ranges, formula logic, and conditional formatting rules implemented in `FinSight_360_Executive_Report.xlsx`.

---

## 1. Sheet 1: `Executive_Summary`
- **Cell Range**: `A1:D33`
- **Header**: Merged title spanning A1:D2.
- **KPI Block (`A4:D17`)**:
  - `A5:D5`: Table Header (`Metric Name`, `Portfolio Value`, `Unit / Format`, `Analytical Interpretation`).
  - Values populated from verified portfolio calculations.
- **Executive Findings (`A19:A24`)**:
  - Bulleted management takeaways highlighting grade monotonicity, 60-month term risk, and high-leverage DTI concentrations.
- **Navigation Block (`A26:B32`)**:
  - Index directing users to corresponding analytical tabs.

---

## 2. Sheet 2: `Portfolio_Analysis`
- **Table 2A: Terminal Loan Status (`A3:F8`)**:
  - `A4:F4`: Header Row.
  - Rows 5 & 6: `Fully Paid` and `Charged Off` metrics.
  - Row 7: Total Row using Excel native formulas:
    - `B7`: `=SUM(B5:B6)` (Total Count = 396,030)
    - `C7`: `=SUM(C5:C6)` (Share = 100.00%)
    - `D7`: `=SUM(D5:D6)` (Total Exposure = $5,589,522,775)
    - `E7`: `=SUM(E5:E6)` (Exposure Share = 100.00%)
    - `F7`: `=AVERAGE(F5:F6)`
- **Table 2B: Loan Purpose Breakdown (`A10:H25`)**:
  - 14 distinct loan purposes ranked descending by funded exposure.
  - Metrics: Count, Exposure Share (%), Total Funded ($), Average Ticket ($), Average Rate (%), Charged Off Count, Default Rate (%).

---

## 3. Sheet 3: `Credit_Risk_Analysis`
- **Table 3A: Underwriting Grade Matrix (`A3:H12`)**:
  - Grades `A` through `G`.
  - Column 8: `Observed Default Rate (%)` highlighted in bold Crimson text for grades exceeding 20.00%.
- **Table 3B: DTI Leverage Performance (`A14:F21`)**:
  - Closed leverage brackets (`< 10%`, `10-15%`, `15-20%`, `20-25%`, `25-30%`, `30%+`).
  - Evaluates default rate escalation as borrower debt service burden increases.

---

## 4. Sheet 4: `Trends_and_Vintages`
- **Table 4A: Annual Origination Trends (`A3:H14`)**:
  - 10 distinct origination years (2007 through 2016).
  - Column 4 (`YoY Volume Growth`): Percentage change over preceding vintage year.
  - Column 8 (`Vintage Default Rate`): Reflects ultimate cohort maturation and loss emergence.

---

## 5. Sheet 5: `Data_Quality`
- **Table 5A: Automated Audit Log (`A3:H17`)**:
  - 12 automated checks from `DataQualityValidator`.
  - **Conditional Formatting Rules**:
    - `PASS`: Soft green fill (`#DCFCE7`), dark green text.
    - `WARNING`: Soft amber fill (`#FEF3C7`), dark amber text.
    - `FAIL`: Soft red fill (`#FEE2E2`), dark red text.

---

## 6. Sheet 6: `Data_Dictionary`
- **Table 6A: Analytical Schema Reference (`A3:D29`)**:
  - 25 core analytical attributes documented with exact data type and business logic mapping.
