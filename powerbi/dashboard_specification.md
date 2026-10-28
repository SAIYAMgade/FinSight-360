# FinSight 360: Power BI Dashboard Visual & Layout Specification

This document provides visual engineering guidelines, visual card placements, field mappings, and interactive behavior for the three core report pages in Power BI Desktop.

---

## PAGE 1: EXECUTIVE PORTFOLIO OVERVIEW
**Purpose:** High-level strategic briefing on lending portfolio scale, funding trends, terminal outcome distribution, and capital deployment.

### 1. Header & Slicers (Top Ribbon)
- **Report Title**: `FinSight 360 | Executive Portfolio Command Center`
- **Subtitle**: `Portfolio Scale: 396,030 Closed Facilities | $5.59 Billion Origination Capital`
- **Slicers (Interactive Filters)**:
  - `Origination Year`: Dropdown / Between slider using `dim_date[year_num]`
  - `Loan Term`: Tile filter with `36 months` / `60 months`
  - `Risk Tier`: Multi-select dropdown using `dim_risk_grade[prime_status]`

### 2. Top KPI Cards Banner (Row 1)
| Card Title | Measure | Format | Styling / Visual Purpose |
| :--- | :--- | :--- | :--- |
| **Total Loans** | `[Total Loans]` | `396,030` | Core volume scale indicator |
| **Total Exposure** | `[Total Original Loan Amount]` | `$5.59B` | Total funded balance sheet exposure |
| **Average Loan Size** | `[Average Loan Amount]` | `$14,114` | Average facility ticket size |
| **Observed Default Rate** | `[Observed Default Rate]` | `19.61%` | Target benchmark credit loss rate |
| **Fully Paid Share** | `DIVIDE([Fully Paid Loan Count], [Total Loans])` | `80.39%` | Performing capital recovery rate |
| **Avg Contract Rate** | `[Average Interest Rate]` | `13.64%` | Nominal portfolio gross yield |

### 3. Visual Grid (Row 2 & Row 3)
- **Visual 1.1: Origination Volume Trend Over Time**
  - **Visual Type**: Clustered Column Chart
  - **X-Axis**: `dim_date[year_num]`
  - **Y-Axis**: `[Total Original Loan Amount]`
  - **Data Color**: Navy (`#1E3A8A`)
  - **Analytical Purpose**: Demonstrates post-2008 origination expansion and cycle growth.
- **Visual 1.2: Terminal Repayment Status Composition**
  - **Visual Type**: Donut Chart
  - **Legend**: `fact_loans[loan_status]`
  - **Values**: `[Total Loans]`
  - **Colors**: Fully Paid = Teal (`#0D9488`), Charged Off = Crimson (`#BE123C`)
  - **Data Labels**: Category + Percent of Total
- **Visual 1.3: Portfolio Exposure by Loan Purpose**
  - **Visual Type**: Horizontal Bar Chart (Sorted descending by exposure)
  - **Y-Axis**: `dim_loan_purpose[purpose]` (Top 8)
  - **X-Axis**: `[Total Original Loan Amount]`
  - **Color**: Slate Teal (`#0D9488`)
- **Visual 1.4: Capital Allocation by Underwriting Risk Grade**
  - **Visual Type**: Column Chart
  - **X-Axis**: `dim_risk_grade[grade]` (`A` to `G`)
  - **Y-Axis**: `[Total Original Loan Amount]`
  - **Color Gradient**: Teal (Grade A) to Deep Crimson (Grade G)

---

## PAGE 2: CREDIT RISK SEGMENTATION
**Purpose:** Diagnostic investigation into segment-level credit risk, identifying high-risk concentrations, leverage spikes, and pricing alignment.

### 1. Top Diagnostic Banner
- **Card 1**: `Total Defaulted Capital`: `$1.16 Billion` (`[Defaulted Principal Exposure]`)
- **Card 2**: `Defaulted Capital Share`: `20.73%` (`[Defaulted Exposure Share]`)
- **Card 3**: `High-Risk Segment Share`: `12.83%` (Grades E-G exposure share)

### 2. Analytical Visuals
- **Visual 2.1: Observed Default Rate by Risk Grade (%)**
  - **Visual Type**: Line Chart with Data Markers
  - **X-Axis**: `dim_risk_grade[grade]` (`A` to `G`)
  - **Y-Axis**: `[Observed Default Rate]`
  - **Reference Line**: Constant at `19.61%` (Portfolio Baseline)
  - **Key Finding**: Monotonic escalation from 6.29% (Grade A) to 45.84% (Grade G).
- **Visual 2.2: Observed Default Rate across Loan Purposes (%)**
  - **Visual Type**: Horizontal Bar Chart
  - **Y-Axis**: `fact_loans[purpose]`
  - **X-Axis**: `[Observed Default Rate]`
  - **Key Finding**: Small business loans exhibit 29.45% default rate vs 16.77% for credit card refinancing.
- **Visual 2.3: Observed Default Rate across DTI Leverage Bands (%)**
  - **Visual Type**: Clustered Column Chart
  - **X-Axis**: `fact_loans[dti_band]` (`< 10%`, `10-15%`, `15-20%`, `20-25%`, `25-30%`, `30%+`)
  - **Y-Axis**: `[Observed Default Rate]`
  - **Color**: Amber (`#D97706`)
- **Visual 2.4: Strategic Segment Exposure vs. Default Rate Scatter Matrix**
  - **Visual Type**: Scatter Chart
  - **X-Axis**: `[Total Original Loan Amount]` ($ Millions)
  - **Y-Axis**: `[Observed Default Rate]` (%)
  - **Size**: `[Total Loans]` (Facility count)
  - **Details**: `dim_loan_purpose[purpose]`
  - **Quadrant Reference Lines**: X = $250M, Y = 19.61%

---

## PAGE 3: PORTFOLIO VINTAGES & DATA QUALITY
**Purpose:** Chronological cohort maturation tracking and data governance audit scorecard.

### 1. Data Governance Scorecard (Row 1)
- **Card 1**: `Total Rules Evaluated`: `12`
- **Card 2**: `Checks Passed`: `10`
- **Card 3**: `Warning Alerts`: `1` (Extreme DTI Outliers > 100%)
- **Card 4**: `Critical Exceptions`: `1` (Non-Positive Income: 1 record)
- **Card 5**: `Compliance Rate`: `83.3%`

### 2. Analytical Visuals
- **Visual 3.1: Origination Vintage Default Rate Trajectory**
  - **Visual Type**: Line Chart
  - **X-Axis**: `dim_date[year_num]` (2007–2016)
  - **Y-Axis**: `[Observed Default Rate]`
- **Visual 3.2: Interest Rate Pricing Distribution by Grade**
  - **Visual Type**: Box and Whisker / Error Bar Chart
  - **X-Axis**: `dim_risk_grade[grade]`
  - **Y-Axis**: `fact_loans[int_rate]`
- **Visual 3.3: Data Quality Check Results Table**
  - **Visual Type**: Grid Table
  - **Columns**: `check_name`, `severity`, `records_checked`, `failures_found`, `failure_rate`, `result`
  - **Conditional Formatting**: Background color based on `result` (Green = PASS, Yellow = WARNING, Red = FAIL).
- **Visual 3.4: Income vs Loan Principal Sizing**
  - **Visual Type**: Scatter Plot
  - **X-Axis**: `annual_inc` ($0 - $250k)
  - **Y-Axis**: `loan_amnt` ($500 - $40k)
  - **Legend**: `loan_status` (Fully Paid vs Charged Off)
