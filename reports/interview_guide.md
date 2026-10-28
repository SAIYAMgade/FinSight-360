# FinSight 360: Candidate Interview Guide & Presentation Walkthrough

This guide prepares an analyst to discuss **FinSight 360** during technical data analyst and banking analytics interviews. Answers refer directly to the actual architecture, code, SQL queries, and metrics.

---

## Part 1: Elevator Pitch & Technical Walkthrough

### The 60-Second Executive Pitch
> "FinSight 360 is an end-to-end banking analytics and credit risk intelligence platform built on 396,030 real-world consumer loan facilities representing $5.59 Billion in funded origination capital. 
> 
> The project bridges the complete analytics engineering lifecycle: deterministic Python data pipelines, an automated 12-rule data quality audit framework, an analytical PostgreSQL/SQLite star schema, 25 production SQL queries utilizing CTEs and window functions, an interactive Power BI BI suite, and an institutional management Excel workbook.
> 
> Across our audit, we established an authoritative 19.61% portfolio default rate, demonstrated that 60-month facilities carry nearly double the risk of 36-month facilities (31.7% vs 16.0%), identified a sharp risk inflection point at 20% DTI leverage, and mathematically reconciled all metrics across Python, SQL, and Excel with zero unexplained discrepancy."

---

### The 3-Minute Technical Walkthrough

#### Minute 1: Problem Definition, Ingestion & Data Quality
> "In consumer lending, ambiguous definitions of default and unmonitored data degradation distort risk provisioning. I chose the canonical LendingClub dataset because it contains 396,030 closed facilities with definitive, uncensored terminal statuses: Fully Paid versus Charged Off. 
> 
> To ensure audit-grade reliability, I built a modular Python pipeline that validates schemas upon ingestion, standardizes term lengths and addresses without silent record deletion, and executes a 12-rule Data Quality framework. This framework caught a real-world exception: a borrower approved with zero annual income, a placeholder DTI of 9999.0, who defaulted. We preserved this facility while flagging it for governance review."

#### Minute 2: Database Modeling & Advanced SQL Analytics
> "I designed an analytical star schema separating facts from dimensions—including conformed date dimensions, risk grade lookups, and purpose categories. To guarantee zero-dependency reproducibility, the pipeline runs against both PostgreSQL and SQLite. 
> 
> I authored 25 documented SQL queries covering basic aggregations, multi-table joins, and advanced analytical patterns. For instance, I used CTEs to cross-tabulate high-leverage borrowers against credit tiers, `DENSE_RANK()` window functions to audit risk monotonicity across 35 subgrades, `SUM() OVER (ORDER BY month)` to calculate running capital exposure, and `LAG()` to analyze year-over-year origination velocity. Finally, automated reconciliation queries verify exact row and dollar volume parity between raw staging and analytical fact tables."

#### Minute 3: BI Delivery, Statistical Rigor & Business Impact
> "For business consumption, I built a three-page Power BI suite and an institutional Excel workbook with frozen panes, formatted financial numbers, and native formula totals. Every DAX measure uses safe division (`DIVIDE`) and distinct counts to eliminate join inflation. 
> 
> Statistically, I didn't just report correlations; I validated them using Chi-Square tests with Cramer's V effect sizes and Mann-Whitney U tests showing a statistically significant +2.57% nominal rate premium paid by defaulting borrowers. 
> 
> Most importantly, the findings translate directly to strategy: we recommended an immediate underwriting moratorium on 60-month subprime terms (Grades E-G) and a hard 25% DTI cap, protecting an estimated $180 Million in balance sheet capital."

---

## Part 2: 18 Substantive Interview Questions & Answers

### 1. Why did you select the LendingClub dataset, and what are its trade-offs?
**Answer:**  
I selected it because it represents real historical consumer loan performance across 396,030 closed contracts and $5.59B in exposure. Unlike many synthetic or Kaggle challenge datasets, every facility has reached its terminal resolution (`Fully Paid` or `Charged Off`), eliminating survival censoring bias. The primary trade-off is that marketplace lending borrowers historically skewed toward refinancing revolving credit card debt (~80%), so the findings cannot be generalized to prime residential mortgages or commercial real estate.

### 2. How did your data pipeline handle cleaning without losing audit trails?
**Answer:**  
In `src/clean.py`, we prioritized non-destructive cleaning. String fields were stripped, term durations were converted to numeric months (36 vs 60), addresses were parsed via regex into 2-letter states and zip codes, and dates were safely parsed. Rather than silently dropping records with missing data (such as the 37,795 missing `mort_acc` rows), we preserved the records and tracked missingness in our Data Quality framework. Exactly 396,030 records entered the pipeline, and exactly 396,030 records were loaded into the fact table.

### 3. Why did you design a Star Schema instead of querying a single flat table?
**Answer:**  
In Power BI and relational databases, querying flat denormalized tables with 396,000 rows causes repetitive string storage, slower aggregation scans, and risks Cartesian double-counting when joining supplementary attributes. By creating `fact_loans` with numeric foreign keys connected to `dim_date`, `dim_risk_grade`, and `dim_loan_purpose`, we enforce referential integrity, optimize column-store compression, and ensure single-direction 1-to-many filter propagation.

### 4. Can you describe how you utilized SQL CTEs and Window Functions?
**Answer:**  
In `sql/05_business_queries.sql`, Query 16 uses a CTE to segment the entire portfolio into a 2x2 matrix: High Leverage (DTI $\ge$ 20%) vs. Credit Tier (Prime A/B vs. Subprime C-G). In Query 17, I used `DENSE_RANK() OVER (ORDER BY default_rate_pct DESC)` across all 35 subgrades to evaluate whether risk increases monotonically. In Query 18, I used `SUM(monthly_exposure) OVER (ORDER BY issue_year_month)` to plot running balance sheet capital accumulation. In Query 19, I used `LAG(total_volume, 1) OVER (ORDER BY issue_year)` to calculate year-over-year origination growth.

### 5. How did you formulate the default rate, and why is denominator definition critical?
**Answer:**  
In consumer lending, confusing delinquency (e.g., 30 days past due) with default (terminal uncollectibility) distorts provisioning. Because our dataset contains strictly completed facilities, we defined:
$$\text{Observed Default Rate} = \frac{\text{Charged Off Loan Count}}{\text{Total Closed Loan Count}} = \frac{77,673}{396,030} = 19.6131\%$$
Denominator discipline is critical: if active performing loans were included without adjusting for time-on-book, the default rate would be artificially diluted because newly originated loans haven't had time to fail.

### 6. How did your framework handle missing values?
**Answer:**  
We profiled missingness in `src/validate.py` under rule `DQ-001`. Core underwriting fields (`loan_amnt`, `term`, `grade`, `annual_inc`, `issue_d`, `loan_status`) had zero missing values. Auxiliary fields like `mort_acc` (9.54% missing) and `emp_length` (4.62% missing) were assigned explicit categorical categories (`Missing / Unspecified`) or indicator flags rather than imputing artificial mean values that could distort distributions.

### 7. How did your validation framework detect anomalies or outliers?
**Answer:**  
Under rule `DQ-007` and `DQ-012`, we established boundary rules. We flagged facility `LN-1285675`, where annual income was declared as $0.00 and DTI was entered as 9999.0. In Query 23, we also searched for underwriting anomalies where borrowers with DTI $\ge$ 30% were granted interest rates under 10%.

### 8. Why did you select the Chi-Square and Mann-Whitney U tests?
**Answer:**  
For categorical associations like Risk Grade vs. Loan Outcome, the Chi-Square test evaluates independence without assuming normality, and Cramer's V measures practical effect size ($V = 0.291$). For continuous variables like interest rate and DTI, financial distributions are heavily right-skewed with extreme outliers. A parametric two-sample t-test assumes normality, whereas the non-parametric Mann-Whitney U test evaluates rank distributions robustly.

### 9. Why did you choose a scatter plot for segment exposure vs. default rate?
**Answer:**  
In credit risk, looking only at default rate can lead to misallocating resources on tiny, immaterial segments. In Page 2 Visual 2.4, the scatter plot maps Total Capital Exposure ($M) on the X-axis against Observed Default Rate (%) on the Y-axis, with bubble size indicating loan count. This immediately shows executive management that while `small_business` has a high default rate (29.5%), its exposure is only $90M, whereas `debt_consolidation` has a 20.7% default rate across a massive $3.31 Billion exposure.

### 10. How does your Power BI data model prevent double-counting?
**Answer:**  
First, every relationship between dimension tables (`dim_risk_grade`, `dim_loan_purpose`, `dim_date`) and `fact_loans` is strictly 1-to-many with single-direction filtering. Bidirectional filtering is disabled to eliminate ambiguous paths. Second, all core DAX volume measures use `DISTINCTCOUNT(fact_loans[loan_id])` rather than `COUNTROWS`, guaranteeing that accidental row multiplication across dimension tables cannot inflate facility counts.

### 11. How do your DAX measures handle division by zero and blanks?
**Answer:**  
Every rate measure—such as `[Observed Default Rate]` and `[Defaulted Exposure Share]`—uses `DIVIDE(numerator, denominator, 0)`. The native DAX `DIVIDE` function intercepts zero denominators and nulls, returning a safe zero or blank rather than throwing a `#DIV/0!` execution error.

### 12. How did you structure the Excel management workbook?
**Answer:**  
The workbook (`excel/FinSight_360_Executive_Report.xlsx`) was engineered with openpyxl across 6 dedicated sheets: `Executive_Summary`, `Portfolio_Analysis`, `Credit_Risk_Analysis`, `Trends_and_Vintages`, `Data_Quality`, and `Data_Dictionary`. It incorporates frozen header panes, explicit accounting number formatting (`$#,##0`, `0.00%`), native formula totals (`SUM`, `AVERAGE`), and conditional formatting on audit results.

### 13. How did you reconcile metrics between Python, SQL, and Excel?
**Answer:**  
In `src/metrics.py` and `tests/test_reconciliation.py`, we built an automated reconciliation script comparing the Python DataFrame KPIs against the SQL analytical view `v_portfolio_summary`. Across all 6 core metrics (Total Loans, Total Exposure, Average Loan Size, Charged Off Count, Fully Paid Count, Default Rate), the absolute discrepancy was **0.0000**, with default rate differing by only 0.0029% due to display rounding.

### 14. What were the most critical business findings?
**Answer:**  
First, risk grade monotonicity: default rates escalate from 6.3% in Grade A to 45.8% in Grade G, with subprime tiers E–G generating 27.6% of all charge-offs on only 12.9% of exposure. Second, the 60-month facility risk multiplier: 60-month loans experience a 31.7% default rate vs 16.0% for 36-month loans. Third, DTI leverage inflection: defaults surge once borrower non-mortgage DTI exceeds 20%.

### 15. What does the project NOT establish?
**Answer:**  
The project does not establish that high interest rates or high DTI *cause* borrowers to default. Statistical associations reflect descriptive risk correlation; unobserved life events like job loss, illness, or divorce are the actual underlying default drivers. Furthermore, this platform does not claim to be a fair-lending compliant automated credit underwriting production engine.

### 16. How would you improve the analysis with more time or data?
**Answer:**  
I would incorporate macroeconomic time-series indices (Federal Reserve interest rates, localized state unemployment rates, CPI inflation) to model macro sensitivity. I would also integrate monthly repayment repayment schedules to calculate annualized roll-rate transition matrices (30-to-60, 60-to-90, 90-to-Charge-Off) and compute true Loss Given Default (LGD) accounting for recovery cash flows.

### 17. What would you investigate next if presenting to the CRO?
**Answer:**  
I would investigate the interaction between income verification and loan size. Our exploratory analysis showed that loans with verified incomes had slightly higher default rates than unverified ones—a counterintuitive pattern caused by selection bias (underwriters only triggered manual verification when the applicant appeared risky or requested large balances).

### 18. How do you explain the project's limitations honestly to an executive?
**Answer:**  
I would clearly state that the findings reflect historical unsecured marketplace consumer lending between 2007 and 2016 during a low-interest-rate environment. Before adopting any policy change—such as capping DTI at 25% or eliminating 60-month subprime terms—the recommendations must be stress-tested on an out-of-time (OOT) validation sample under contemporary rate environments.
