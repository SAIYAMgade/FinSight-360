# FinSight 360: DAX Measures Library & Formulation Guide

This document defines the formal DAX measures deployed in the FinSight 360 analytical model. Every measure is built with explicit denominator validation (`DIVIDE`), blank safety, and distinct identifier counts to eliminate calculation distortion.

---

## 1. Core Portfolio Sizing & Volume Measures

### Measure 01: `Total Loans`
Total count of evaluated loan facilities in the filtered context.
```dax
Total Loans = 
DISTINCTCOUNT(fact_loans[loan_id])
```
- **Format**: `#,##0`
- **Business Use**: Core volume KPI.

### Measure 02: `Total Original Loan Amount`
Total original funded principal volume across the portfolio.
```dax
Total Original Loan Amount = 
SUM(fact_loans[loan_amnt])
```
- **Format**: `$#,##0`
- **Business Use**: Total funded capital exposure.

### Measure 03: `Average Loan Amount`
Arithmetic mean of loan principal sizing.
```dax
Average Loan Amount = 
DIVIDE(
    [Total Original Loan Amount],
    [Total Loans],
    0
)
```
- **Format**: `$#,##0.00`
- **Business Use**: Facility ticket sizing tracking.

### Measure 04: `Average Interest Rate`
Average annualized nominal contract rate.
```dax
Average Interest Rate = 
AVERAGE(fact_loans[int_rate])
```
- **Format**: `0.00%`
- **Business Use**: Portfolio gross yield benchmark.

### Measure 05: `Average Debt to Income Ratio`
Arithmetic mean of borrower DTI leverage.
```dax
Average Debt to Income Ratio = 
AVERAGE(fact_loans[dti])
```
- **Format**: `0.00`
- **Business Use**: Financial leverage monitoring.

---

## 2. Repayment Status & Credit Risk Performance Measures

### Measure 06: `Fully Paid Loan Count`
Count of loans successfully paid in full by the borrower.
```dax
Fully Paid Loan Count = 
CALCULATE(
    [Total Loans],
    fact_loans[is_default] = 0
)
```
- **Format**: `#,##0`

### Measure 07: `Charged Off Loan Count`
Count of facilities written off as terminal credit losses.
```dax
Charged Off Loan Count = 
CALCULATE(
    [Total Loans],
    fact_loans[is_default] = 1
)
```
- **Format**: `#,##0`

### Measure 08: `Observed Default Rate`
The authoritative credit loss metric: share of completed facilities ending in charge-off.
```dax
Observed Default Rate = 
DIVIDE(
    [Charged Off Loan Count],
    [Total Loans],
    0
)
```
- **Format**: `0.00%`
- **Business Use**: Primary credit risk KPI for executive and regulatory reporting.

### Measure 09: `Defaulted Principal Exposure`
Dollar volume of funded principal associated with charged-off loans.
```dax
Defaulted Principal Exposure = 
CALCULATE(
    [Total Original Loan Amount],
    fact_loans[is_default] = 1
)
```
- **Format**: `$#,##0`
- **Business Use**: Cumulative capital at risk / charge-off volume.

### Measure 10: `Defaulted Exposure Share`
Percentage of total funded capital committed to defaulted loans.
```dax
Defaulted Exposure Share = 
DIVIDE(
    [Defaulted Principal Exposure],
    [Total Original Loan Amount],
    0
)
```
- **Format**: `0.00%`
- **Business Use**: Dollar-weighted portfolio loss rate.

---

## 3. Portfolio Allocation & Slicing Measures

### Measure 11: `Portfolio Exposure Share`
Share of total unfiltered portfolio exposure represented by the current active segment.
```dax
Portfolio Exposure Share = 
DIVIDE(
    [Total Original Loan Amount],
    CALCULATE([Total Original Loan Amount], ALL(fact_loans)),
    0
)
```
- **Format**: `0.00%`

### Measure 12: `Segment Risk Index`
Ratio of segment default rate to total portfolio baseline default rate (1.00 = portfolio average).
```dax
Segment Risk Index = 
VAR BaselineRate = CALCULATE([Observed Default Rate], ALL(fact_loans))
RETURN
DIVIDE(
    [Observed Default Rate],
    BaselineRate,
    1.0
)
```
- **Format**: `0.00`
- **Business Use**: Flagging segments with risk exceeding 1.25x baseline.

---

## 4. Vintage & Time-Intelligence Measures

### Measure 13: `Loan Count Previous Year`
Origination count for the corresponding prior calendar year.
```dax
Loan Count Previous Year = 
CALCULATE(
    [Total Loans],
    SAMEPERIODLASTYEAR(dim_date[full_date])
)
```
- **Format**: `#,##0`

### Measure 14: `Origination Volume YoY Growth`
Year-over-Year percentage change in funded origination capital.
```dax
Origination Volume YoY Growth = 
VAR CurrentVolume = [Total Original Loan Amount]
VAR PriorVolume = CALCULATE([Total Original Loan Amount], SAMEPERIODLASTYEAR(dim_date[full_date]))
RETURN
DIVIDE(
    CurrentVolume - PriorVolume,
    PriorVolume,
    BLANK()
)
```
- **Format**: `+0.00%;-0.00%;0.00%`

---

## 5. Data Quality & Audit Health Measures

### Measure 15: `Data Quality Rules Evaluated`
Count of automated validation rules executed.
```dax
Data Quality Rules Evaluated = 
COUNTROWS(dq_audit_log)
```
- **Format**: `#,##0`

### Measure 16: `Data Quality Failed Checks`
Count of critical rule failures.
```dax
Data Quality Failed Checks = 
CALCULATE(
    COUNTROWS(dq_audit_log),
    dq_audit_log[result] = "FAIL"
)
```
- **Format**: `#,##0`

### Measure 17: `Data Quality Warning Checks`
Count of warning alerts generated.
```dax
Data Quality Warning Checks = 
CALCULATE(
    COUNTROWS(dq_audit_log),
    dq_audit_log[result] = "WARNING"
)
```
- **Format**: `#,##0`

### Measure 18: `Data Quality Compliance Rate`
Overall data audit pass rate percentage.
```dax
Data Quality Compliance Rate = 
VAR PassCount = CALCULATE(COUNTROWS(dq_audit_log), dq_audit_log[result] = "PASS")
VAR TotalRules = COUNTROWS(dq_audit_log)
RETURN
DIVIDE(PassCount, TotalRules, 0)
```
- **Format**: `0.0%`
- **Business Use**: Executive governance confidence card.
