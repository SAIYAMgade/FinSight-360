# FinSight 360
### Banking Analytics & Credit Risk Intelligence Platform

<p align="center">
  <img src="reports/screenshots/01_executive_portfolio_overview.png" alt="FinSight 360 Banner" width="100%">
</p>

<p align="center">
  <a href="https://github.com/SAIYAMgade/FinSight-360"><img src="https://img.shields.io/badge/GitHub-SAIYAMgade%2FFinSight--360-1E3A8A?style=for-the-badge&logo=github" alt="GitHub Repository"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11%20%7C%203.14-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/Database-PostgreSQL%20%7C%20SQLite-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="Database"></a>
  <a href="https://powerbi.microsoft.com/"><img src="https://img.shields.io/badge/Power_BI-Desktop_Suite-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI"></a>
  <a href="https://www.microsoft.com/excel"><img src="https://img.shields.io/badge/Excel-openpyxl_Model-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white" alt="Excel"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-0D9488?style=for-the-badge" alt="License"></a>
  <a href="tests/"><img src="https://img.shields.io/badge/Tests-13%20Passed%20(100%25)-brightgreen?style=for-the-badge" alt="Tests"></a>
</p>

---

## Table of Contents
1. [Executive Summary & Core Portfolio KPIs](#1-executive-summary--core-portfolio-kpis)
2. [Interactive Visual Intelligence Dashboards](#2-interactive-visual-intelligence-dashboards)
3. [Key Evidence-Based Analytical Findings](#3-key-evidence-based-analytical-findings)
4. [Technology Stack & Repository Architecture](#4-technology-stack--repository-architecture)
5. [Data Quality & Governance Audit Scorecard](#5-data-quality--governance-audit-scorecard)
6. [Database Modeling & Analytical Star Schema](#6-database-modeling--analytical-star-schema)
7. [Analytical SQL Query Library (25 Business Queries)](#7-analytical-sql-query-library-25-business-queries)
8. [Python Statistical Testing & Scorecard Modeling](#8-python-statistical-testing--scorecard-modeling)
9. [Power BI Suite & DAX Measures](#9-power-bi-suite--dax-measures)
10. [Executive Excel Management Model](#10-executive-excel-management-model)
11. [Quickstart & Complete Reproducibility](#11-quickstart--complete-reproducibility)
12. [Interview Guide & Presentation Pitch](#12-interview-guide--presentation-pitch)
13. [Governance Boundaries & Limitations](#13-governance-boundaries--limitations)

---

## 1. Executive Summary & Core Portfolio KPIs

**FinSight 360** is an institutional banking analytics and credit risk intelligence platform engineered to evaluate consumer lending health, uncover risk concentrations, and deliver board-level Business Intelligence deliverables.

The platform is evaluated across **396,030 closed loan facilities** spanning **$5,589,522,775 ($5.59 Billion)** in original funded principal (June 2007 – December 2016). Every contract in the evaluation scope reached a verified terminal outcome (`Fully Paid` or `Charged Off`), eliminating survival censoring bias and yielding an authoritative **19.61% baseline default rate**.

```
+-------------------------------------------------------------------------------------------------------+
|                                  FINSIGHT 360 EXECUTIVE SCORECARD                                     |
+------------------------------+------------------------------+-----------------------------------------+
| TOTAL CLOSED FACILITIES      | TOTAL FUNDED CAPITAL         | BASELINE OBSERVED DEFAULT RATE          |
| 396,030 Loans                | $5,589,522,775 ($5.59B)      | 19.61% (77,673 Write-Offs)              |
+------------------------------+------------------------------+-----------------------------------------+
| FULLY PAID CAPITAL           | CHARGED OFF LOSS EXPOSURE    | AVERAGE FACILITY SIZING                 |
| $4,430,693,425 (80.39%)      | $1,158,829,350 (20.73%)      | $14,113.89 (Median: $12,000.00)         |
+------------------------------+------------------------------+-----------------------------------------+
| NOMINAL GROSS YIELD          | MEAN DEBT-TO-INCOME (DTI)    | AUDIT GOVERNANCE STATUS                 |
| 13.64% Contract Rate         | 17.38 Leverage Ratio         | 100% Math Reconciliation (0.00 Delta)   |
+------------------------------+------------------------------+-----------------------------------------+
```

---

## 2. Interactive Visual Intelligence Dashboards

FinSight 360 includes three high-resolution visual dashboards matching executive Power BI specifications:

### Visual 1: Executive Portfolio Overview
*Strategic macro briefing tracking origination expansion, terminal repayment status composition, primary loan purpose allocations, and capital deployment across internal underwriting risk grades.*
<p align="center">
  <img src="reports/screenshots/01_executive_portfolio_overview.png" alt="Executive Portfolio Overview" width="95%">
</p>

- **Origination Expansion**: Exponential post-2008 recovery expansion, scaling from under $50M in 2007 to over $1.7B in 2015.
- **Terminal Status Split**: 80.39% Performing Full Repayment vs. 19.61% Terminal Default Write-Off.
- **Core Product Mix**: Heavy concentration in debt refinancing (`debt_consolidation` at $3.31B and `credit_card` at $1.14B).
- **Capital Allocation by Grade**: 47.8% of portfolio capital allocated to prime tiers (Grades A & B).

---

### Visual 2: Credit Risk Segmentation & Diagnostic Intelligence
*Deep-dive risk segmentation examining observed default rates across underwriting grades, loan purposes, borrower debt-to-income leverage bands, and segment exposure.*
<p align="center">
  <img src="reports/screenshots/02_credit_risk_segmentation.png" alt="Credit Risk Segmentation" width="95%">
</p>

- **Grade Escalation**: Strict monotonic risk progression from **6.29%** in Grade A to **45.84%** in Grade G.
- **Purpose Risk Premium**: Small business loans display the highest default rate (**29.45%**) among all major sectors.
- **Leverage Inflection Point**: Observed default rate accelerates once monthly debt obligations exceed **20% DTI**.
- **Exposure Matrix (Quadrant Scatter)**: Visualizes dollar exposure vs. default rate, confirming that debt consolidation poses the largest absolute loss exposure ($686M).

---

### Visual 3: Portfolio Vintages & Automated Data Quality Scorecard
*Origination vintage cohort tracking over time, interest rate pricing dispersion across grades, and automated 12-rule data quality audit scorecard.*
<p align="center">
  <img src="reports/screenshots/03_portfolio_vintages_and_data_quality.png" alt="Vintages and Data Quality" width="95%">
</p>

- **Vintage Trajectory**: Vintages 2011–2014 matured into stable ~18%–20% default rates following early post-crisis calibration.
- **Pricing Dispersion**: Nominal interest rates scale cleanly with credit grade, spanning from 5.3% (Grade A) to 31.0% (Grade G).
- **Data Quality Compliance**: 10 of 12 rules passed with 100% compliance; exactly 1 zero-income anomaly isolated; 8 extreme DTI outliers flagged.

---

## 3. Key Evidence-Based Analytical Findings

Detailed reports are documented in [reports/business_findings.md](reports/business_findings.md) and [reports/executive_summary.md](reports/executive_summary.md):

1. **Risk Grade Monotonicity & Subprime Drag**:
   - Default rates escalate from **6.29%** (Grade A) to **45.84%** (Grade G).
   - Grades E, F, and G comprise **$722.5M (12.93%)** of portfolio exposure, yet drive **27.64% (21,465 facilities)** of all default events. High subprime contractual rates (25.6%) are mathematically insufficient to absorb a 45.8% principal loss.
2. **The 60-Month Facility Term Risk Multiplier**:
   - 60-month facilities exhibit a **31.74%** default rate vs **16.00%** on 36-month facilities (**1.98x higher risk**).
   - Grade B 60-month loans experience a higher default rate (**21.84%**) than Grade C 36-month loans (**18.72%**). Eliminating 60-month terms for Grades D–G protects an estimated **$180M** in balance sheet capital.
3. **Debt-to-Income (DTI) Leverage Inflection at 20%**:
   - Default rates remain stable below 15% DTI (14.3%–16.6%), but spike to **22.51%** for DTI 20%–25% and **24.58%** for DTI > 30%.
4. **Commercial / Small Business Volatility**:
   - Small business facilities exhibit the highest default rate (**29.45%**) of any major purpose category (+984 bps above portfolio baseline). Underwriting commercial ventures using consumer personal scorecards produces severe adverse selection.
5. **Geographic Concentration Risk**:
   - Over **37%** of portfolio exposure is concentrated across 4 anchor states: California ($787M | 14.1%), New York ($460M | 8.2%), Texas ($448M | 8.0%), and Florida ($378M | 6.8%).

---

## 4. Technology Stack & Repository Architecture

```
finsight-360/
|-- README.md                               # Primary project documentation
|-- requirements.txt                        # Pinned dependencies
|-- docker-compose.yml                      # PostgreSQL 16 container definition
|-- .env.example                            # Database credentials template
|-- LICENSE                                 # MIT License
|
|-- config/
|   |-- config.yaml                         # Production pipeline configuration
|   |-- config.example.yaml                 # Template configuration
|
|-- data/
|   |-- README.md                           # Dataset selection note & data dictionary
|   |-- raw/                                # Raw LendingClub source CSVs
|   |-- processed/                          # Parquet extracts & SQLite database
|   |-- sample/loans_sample.csv             # 25,000-row stratified sample (seed 42) for fast CI
|
|-- notebooks/
|   |-- 01_data_understanding.ipynb         # Schema profiling & missingness analysis
|   |-- 02_exploratory_analysis.ipynb       # Bivariate analysis & feature distributions
|   |-- 03_credit_risk_analysis.ipynb       # Statistical testing & baseline model
|   |-- 04_business_findings.ipynb          # Strategic synthesis & executive memo
|
|-- src/
|   |-- ingest.py                           # Schema validation and metadata tracking
|   |-- clean.py                            # Non-destructive data cleaning & regex parsing
|   |-- transform.py                        # Risk banding (loan amount, income, DTI, rate bands)
|   |-- validate.py                         # Automated 12-rule Data Quality framework
|   |-- database.py                         # Dual-engine DB loader (PostgreSQL & SQLite)
|   |-- metrics.py                          # Portfolio KPI & cross-layer reconciliation engine
|   |-- reporting.py                        # Automated dashboard screenshot generator
|
|-- sql/
|   |-- 01_schema.sql                       # Star schema DDL tables
|   |-- 02_constraints_indexes.sql          # Constraints, foreign keys & analytical indexes
|   |-- 03_staging_views.sql                # Staging profiling views
|   |-- 04_analytical_views.sql             # Business KPI views (v_portfolio_summary, v_risk_grade)
|   |-- 05_business_queries.sql             # 25 production analytical business queries
|   |-- 06_data_quality.sql                 # SQL test queries for data health
|   |-- 07_reconciliation.sql               # Staging vs Fact layer reconciliation
|
|-- powerbi/
|   |-- README.md                           # Power BI overview & build instructions
|   |-- data_model.md                       # Star schema model & relationship specification
|   |-- dax_measures.md                     # 18 documented DAX measures with DIVIDE safety
|   |-- dashboard_specification.md          # 3-page visual wireframes & layout rules
|   |-- data_exports/                       # CSV tables ready for Power BI Desktop import
|
|-- excel/
|   |-- README.md                           # Workbook user guide
|   |-- report_specification.md             # Cell mappings & formula documentation
|   |-- FinSight_360_Executive_Report.xlsx  # 6-sheet formatted executive workbook
|
|-- reports/
|   |-- executive_summary.md                # Management memo to CRO & Credit Committee
|   |-- business_findings.md                # Structured evidence-based findings
|   |-- data_quality_report.md              # 12-rule audit log & forensics
|   |-- methodology.md                      # Analytical & statistical methodology
|   |-- limitations.md                      # Governance boundaries & constraints
|   |-- interview_guide.md                  # 18 interview questions + 60s pitch + 3min walkthrough
|   |-- screenshots/                        # High-resolution dashboard figures
|
|-- tests/
|   |-- test_cleaning.py                    # Unit tests for cleaning & parsing
|   |-- test_metrics.py                     # Unit tests for KPI calculations
|   |-- test_data_quality.py                # Unit tests for validation rules
|   |-- test_reconciliation.py              # Cross-layer mathematical parity tests
|
|-- .github/workflows/tests.yml             # GitHub Actions CI workflow
`-- scripts/
    |-- setup_database.py                   # DB initialization & static dimensions
    |-- run_pipeline.py                     # End-to-end execution pipeline
    |-- generate_sample.py                  # Stratified sampling utility
    |-- build_notebooks.py                  # Notebook generator
    `-- build_excel_report.py               # Excel workbook generator
```

---

## 5. Data Quality & Governance Audit Scorecard

In `src/validate.py`, the platform executes an automated 12-rule validation audit across all 396,030 ingested records, logging results to `reports/data_quality_results.csv` and database table `dq_audit_log`:

| Check Name | Severity | Records Evaluated | Failures Found | Failure Rate | Result | Audit Findings & Forensics |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `DQ-001_REQUIRED_FIELDS` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Evaluated `loan_amnt`, `term`, `grade`, `annual_inc`, `issue_d`, `loan_status`. 0 missing. |
| `DQ-002_UNIQUE_LOAN_ID` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Verified surrogate key `loan_id` uniqueness. 396,030 distinct values; 0 duplicates. |
| `DQ-003_DUPLICATE_RECORDS` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Verified full row deduplication. 0 duplicate records. |
| `DQ-004_LOAN_AMOUNT_RANGE` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Range check ($500 to $50,000). Actual range: $500 to $40,000. |
| `DQ-005_INTEREST_RATE_RANGE`| CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Range check (4.0% to 35.0%). Actual range: 5.32% to 30.99%. |
| `DQ-006_DATE_PARSING` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Converted `issue_d` strings (`%b-%Y`) to ISO Gregorian dates. 0 parsing failures. |
| `DQ-007_POSITIVE_INCOME` | CRITICAL | 396,030 | 1 | 0.0003% | **FAIL** | **Forensic finding:** Isolated facility `LN-1285675` ($3,700 funded, Grade C) with $0.00 income and placeholder DTI 9999.0; facility defaulted. |
| `DQ-008_KNOWN_RISK_GRADES` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Verified risk grade domain in `['A', 'B', 'C', 'D', 'E', 'F', 'G']`. 0 invalid values. |
| `DQ-009_TARGET_INTEGRITY` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Verified binary target `is_default` domain strictly in `[0, 1]`. 0 nulls. |
| `DQ-010_CREDIT_AGE` | WARNING | 396,030 | 0 | 0.0000% | **PASS** | Verified that earliest credit line opening precedes loan origination. 0 negative values. |
| `DQ-011_RECORD_RETENTION` | INFORMATIONAL | 396,030 | 0 | 0.0000% | **PASS** | Ingested = 396,030, Cleaned = 396,030, Fact = 396,030. Discrepancy = 0. |
| `DQ-012_DTI_OUTLIERS` | WARNING | 396,030 | 8 | 0.0020% | **WARNING** | Flagged 8 facilities with DTI > 100% (62.5% default rate). Binned into `30%+` category. |

---

## 6. Database Modeling & Analytical Star Schema

The database architecture is documented in [powerbi/data_model.md](powerbi/data_model.md) and implemented in [sql/01_schema.sql](sql/01_schema.sql):

```
       +--------------------+
       |      dim_date      |
       +--------------------+
       | PK: date_key       |
       |     full_date      |
       |     year_num       |
       |     year_month     |
       +---------+----------+
                 | 1
                 |
                 | * (issue_year_month -> year_month)
+----------------+---+      * +---------------------+
|     dim_risk_grade |<-------+      fact_loans     |
+--------------------+ 1      +---------------------+
| PK: grade          |        | PK: loan_id         |
|     risk_tier      |        | FK: grade           |
|     prime_status   |        | FK: purpose         |
+--------------------+        | FK: issue_date      |
                              |     loan_amnt       |
+--------------------+ 1      |     int_rate        |
|  dim_loan_purpose  |<-------+     installment     |
+--------------------+ *      |     annual_inc      |
| PK: purpose        |        |     dti             |
|     purpose_group  |        |     is_default      |
+--------------------+        +----------+----------+
                                         |
                                         | (Independent audit table)
                              +----------+----------+
                              |     dq_audit_log    |
                              +---------------------+
                              | PK: check_name      |
                              |     severity        |
                              |     failure_rate    |
                              |     result          |
                              +---------------------+
```

- **Dual-Engine Architecture**: Operates against PostgreSQL 16 (via `docker-compose.yml`) or zero-dependency embedded SQLite (`data/processed/finsight360.db`).
- **Single-Direction Filter Propagation**: No bidirectional relationships exist, completely eliminating ambiguous filter paths and Cartesian inflation.

---

## 7. Analytical SQL Query Library (25 Business Queries)

All 25 SQL queries in [sql/05_business_queries.sql](sql/05_business_queries.sql) have been tested and verified against the live database:

| # | Business Question | SQL Method / Technique | Result / Output Focus |
| :-: | :--- | :--- | :--- |
| **01** | Executive Portfolio Size & Exposure | Multi-metric aggregate (`COUNT`, `SUM`, `AVG`) | 396,030 loans, $5.59B exposure, 19.61% default rate |
| **02** | Loan Amount Central Tendency | Min, max, avg, installment calculations | $500 min, $40,000 max, $14,114 average |
| **03** | Term Structure Allocation | `GROUP BY term`, volume & loss share | 36m (76.3% volume, 16.0% default) vs 60m (23.7%, 31.7%) |
| **04** | Terminal Repayment Breakdown | Terminal status volume and share | Fully Paid (80.39% / $4.43B) vs Charged Off (19.61% / $1.16B) |
| **05** | Missing Value Profiling | Conditional null sums (`CASE WHEN`) | Confirms zero missingness in core underwriting columns |
| **06** | Income Verification vs. Performance | `GROUP BY verification_status` | Highlights selection bias in verified borrower tiers |
| **07** | Risk Grade Performance Escalation | `GROUP BY grade ORDER BY grade` | Monotonic escalation from 6.29% (A) to 45.84% (G) |
| **08** | Purpose Concentration & Risk | `GROUP BY purpose ORDER BY total DESC` | Debt consolidation ($3.31B); Small Business (29.45% default) |
| **09** | Borrower Income Band Slicing | `GROUP BY income_band` | Higher income mitigates default rate (12.8% for $150k+) |
| **10** | DTI Leverage Inflection | `GROUP BY dti_band` | Sharp loss acceleration above 20% DTI (reaching 24.58%) |
| **11** | Pricing Yield Tier Analysis | `GROUP BY int_rate_band` | Escalating default rates across higher contract pricing |
| **12** | Top 10 States Exposure | `GROUP BY addr_state LIMIT 10` | Top 4 states (CA, NY, TX, FL) represent 37.1% exposure |
| **13** | Annual Origination Growth | `GROUP BY issue_year` | Post-crisis origination recovery and scaling |
| **14** | Employment Stability Assessment | `GROUP BY emp_tenure` | Stability profiling across employment tenures |
| **15** | Home Ownership Risk | `GROUP BY home_ownership` | Renters (21.3% default) vs Mortgage holders (17.0% default) |
| **16** | High Leverage vs Credit Tier | **CTE-based 2x2 Risk Matrix** | High DTI Non-Prime defaults at 29.8% vs 8.2% Low DTI Prime |
| **17** | Granular Subgrade Risk Ordering | **`DENSE_RANK() OVER (ORDER BY default)`** | Ranks all 35 subgrades from A1 (2.6%) to G5 (50.6%) |
| **18** | Running Origination Volume | **`SUM() OVER (ORDER BY month)`** | Running balance sheet capital accumulation |
| **19** | Year-over-Year Volume Growth | **`LAG(total_volume, 1) OVER (ORDER BY year)`**| Year-over-Year origination expansion velocity |
| **20** | Vintage Cohort Matrix | Cross-tabulate `issue_year` by `term` | Vintage cohort maturation tracking |
| **21** | Statistical Reliability Filter | **`HAVING COUNT(*) >= 500`** | Isolates statistically robust high-risk segments |
| **22** | Risk Concentration Outliers | Subquery filtering **`default_rate > 1.25x baseline`**| Surfaces purpose segments exceeding 24.51% default rate |
| **23** | Underwriting Anomaly Check | Conditional filter (`int_rate < 10 AND dti >= 30`) | Mispriced credit risk detection |
| **24** | Pipeline Layer Reconciliation | **`UNION ALL`** Staging vs Fact comparison | Proves zero row loss between staging and analytical fact table |
| **25** | Cross-Layer Baseline Benchmark | Authoritative benchmark summary | Benchmark numbers for automated Python/Power BI reconciliation |

---

## 8. Python Statistical Testing & Scorecard Modeling

Notebooks are located in `notebooks/`:
- `notebooks/01_data_understanding.ipynb`: Ingestion, schema profiling, and missingness analysis.
- `notebooks/02_exploratory_analysis.ipynb`: Bivariate feature distributions across repayment statuses.
- `notebooks/03_credit_risk_analysis.ipynb`: Inferential statistical tests and scorecard modeling.
- `notebooks/04_business_findings.ipynb`: Synthesis, scatter exposure matrix, and executive memo.

### Inferential Statistical Test Results

| Test Description | Null Hypothesis ($H_0$) | Test Statistic | p-value | Effect Size | Analytical Conclusion |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Chi-Square Independence** (Risk Grade vs Default) | Grade and Loan Outcome are statistically independent. | $\chi^2 = 33,548.81$ | $< 10^{-300}$ | Cramer's $V = 0.291$ | **Reject $H_0$**: Highly significant practical association. |
| **Chi-Square Independence** (Term Length vs Default) | Term Length and Outcome are statistically independent. | $\chi^2 = 11,465.12$ | $< 10^{-300}$ | Cramer's $V = 0.170$ | **Reject $H_0$**: Significant term-duration risk penalty. |
| **Mann-Whitney U Test** (Interest Rate Spread) | Paid and Default cohorts have identical rate distributions. | $U = 1.63 \times 10^{10}$ | $< 10^{-300}$ | Cohen's $d = 0.584$ | **Reject $H_0$**: Defaulting cohort paid +2.57% higher rate. |
| **Mann-Whitney U Test** (DTI Leverage Spread) | Paid and Default cohorts have identical DTI distributions. | $U = 1.41 \times 10^{10}$ | $< 10^{-300}$ | Cohen's $d = 0.264$ | **Reject $H_0$**: Defaulting cohort had higher leverage. |

### Leakage-Free Predictive Scorecard Baseline
In `notebooks/03_credit_risk_analysis.ipynb`, an honest logistic regression baseline was trained using strictly origination-time predictors (`loan_amnt`, `int_rate`, `dti`, `annual_inc`, `installment_burden_pct`, `credit_history_years`), strictly avoiding post-origination leakage fields:
- **Held-Out Test Sample**: 20% stratified test split (79,206 facilities).
- **ROC-AUC Score**: **0.692**, aligning with standard unsecured retail banking underwriting scorecards prior to integrating comprehensive credit bureau tradeline files.

---

## 9. Power BI Suite & DAX Measures

The Power BI analytical model is documented in [powerbi/dax_measures.md](powerbi/dax_measures.md) and [powerbi/dashboard_specification.md](powerbi/dashboard_specification.md).

Ready-to-import CSV files are located in `powerbi/data_exports/`:
- `powerbi/data_exports/fact_loans_sample_25k.csv`
- `powerbi/data_exports/dim_date.csv`
- `powerbi/data_exports/dim_risk_grade.csv`
- `powerbi/data_exports/dim_loan_purpose.csv`
- `powerbi/data_exports/dq_audit_log.csv`

### Core DAX Measures (Formulated for Zero-Error Safety)

```dax
// 1. Total Distinct Loan Facilities
Total Loans = DISTINCTCOUNT(fact_loans[loan_id])

// 2. Total Funded Capital Exposure
Total Original Loan Amount = SUM(fact_loans[loan_amnt])

// 3. Observed Default Rate (Denominator Safe)
Observed Default Rate = 
DIVIDE(
    CALCULATE([Total Loans], fact_loans[is_default] = 1),
    [Total Loans],
    0
)

// 4. Defaulted Capital Exposure
Defaulted Principal Exposure = 
CALCULATE([Total Original Loan Amount], fact_loans[is_default] = 1)

// 5. Defaulted Capital Share
Defaulted Exposure Share = 
DIVIDE([Defaulted Principal Exposure], [Total Original Loan Amount], 0)

// 6. Segment Risk Index vs. Portfolio Baseline
Segment Risk Index = 
VAR BaselineRate = CALCULATE([Observed Default Rate], ALL(fact_loans))
RETURN DIVIDE([Observed Default Rate], BaselineRate, 1.0)
```

---

## 10. Executive Excel Management Model

The institutional workbook [`excel/FinSight_360_Executive_Report.xlsx`](excel/FinSight_360_Executive_Report.xlsx) was generated with openpyxl across 6 dedicated sheets:

1. **`Executive_Summary`**: High-level portfolio KPIs, executive briefing commentary, and workbook navigation links.
2. **`Portfolio_Analysis`**: Terminal loan status profile (`Fully Paid` vs `Charged Off`), loan term breakdown, and 14-purpose breakdown.
3. **`Credit_Risk_Analysis`**: Underwriting risk grade matrix (A to G), DTI leverage performance, and income tiers.
4. **`Trends_and_Vintages`**: Annual origination trends (2007–2016), YoY volume growth (%), and vintage default rate maturation.
5. **`Data_Quality`**: 12-rule validation scorecard with conditional formatting (Green = PASS, Yellow = WARNING, Red = FAIL).
6. **`Data_Dictionary`**: 25 core analytical attributes documented with source origins, data types, and business definitions.

*Features: Frozen top panes, accounting number formats (`$#,##0`, `0.00%`, `#,##0`), and native Excel formulas (`SUM`, `AVERAGE`) on total rows.*

---

## 11. Quickstart & Complete Reproducibility

### Step 1: Clone the Repository
```bash
git clone https://github.com/SAIYAMgade/FinSight-360.git
cd FinSight-360
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run End-to-End Pipeline
Executes ingestion, non-destructive cleaning, transformation, 12-rule data quality audit, and database loading in ~45 seconds:
```bash
python scripts/run_pipeline.py
```

### Step 4: Run Automated Tests & Mathematical Reconciliation
```bash
python -m pytest -v
```

### Step 5: Regenerate Excel Report & Dashboard Visuals
```bash
python scripts/build_excel_report.py
python src/reporting.py
```

### Step 6: (Optional) Spin Up PostgreSQL in Docker
```bash
docker compose up -d
python scripts/setup_database.py
```

---

## 12. Interview Guide & Presentation Pitch

Candidates presenting FinSight 360 can reference [reports/interview_guide.md](reports/interview_guide.md):
- **60-Second Elevator Pitch**: High-level problem definition, portfolio scale, key discoveries, and strategic takeaways.
- **3-Minute Technical Walkthrough**: Deep dive covering data ingestion, SQL star schema, CTEs/window functions, DAX safety, and mathematical reconciliation.
- **18 Substantive Interview Questions & Answers**: Thorough interview prep addressing dataset selection trade-offs, handling missing values, statistical test choices, Power BI modeling, and governance limits.

---

## 13. Governance Boundaries & Limitations

In compliance with banking model governance standards, detailed disclosures are documented in [reports/limitations.md](reports/limitations.md):
- **Platform Demographics**: Findings reflect historical consumer unsecured marketplace facilities (2007–2016) skewed toward revolving credit refinancing (~80% exposure) and cannot be directly generalized to residential mortgages or commercial real estate.
- **Unverified Declarations**: 31% of borrower incomes were unverified at application; DTI excluded existing mortgage debt.
- **Correlation vs. Causation**: Statistical dependencies describe historical cohort behaviors; unobserved life events (job loss, illness, divorce) are the true underlying catalysts of personal insolvency.
- **Out-of-Time Validation**: Underwriting policy recommendations must be validated on modern out-of-time (OOT) cohorts before deployment in active credit environments.

---

## License

This project is licensed under the terms of the [MIT License](LICENSE).  
Copyright (c) 2026 SAIYAM Gade & FinSight 360 Contributors.
