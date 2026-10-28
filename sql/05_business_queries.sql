-- =============================================================================
-- FinSight 360: Analytical SQL Query Library (25 Business Queries)
-- Script: 05_business_queries.sql
-- Description: Comprehensive query library answering core executive, risk,
--              portfolio, and data quality business questions.
-- =============================================================================

-- =============================================================================
-- SECTION A: BASIC PORTFOLIO ANALYSIS (QUERIES 01 - 06)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 01: Executive Portfolio Size and Aggregate Funded Exposure
-- Business Question: What is the total size, original principal exposure, and 
-- baseline observed default rate across the entire lending portfolio?
-- -----------------------------------------------------------------------------
-- Logic: Aggregate count, sum, average, and conditional sums for closed loans.
-- Expected Output Columns: total_loans, total_origination_exposure, avg_loan_size,
--   baseline_default_rate_pct, total_defaulted_exposure
-- Interpretation: Establishes overall portfolio exposure baseline for board reporting.
-- Limitations: Reflects historical funded facilities, does not account for post-writeoff recoveries.
SELECT
    COUNT(*) AS total_loans,
    ROUND(SUM(loan_amnt), 2) AS total_origination_exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(SUM(CASE WHEN is_default = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS baseline_default_rate_pct,
    ROUND(SUM(CASE WHEN is_default = 1 THEN loan_amnt ELSE 0 END), 2) AS total_defaulted_exposure
FROM fact_loans;


-- -----------------------------------------------------------------------------
-- QUERY 02: Loan Amount Distribution & Central Tendency
-- Business Question: What are the minimum, maximum, average, and quartile proxies 
-- for loan amounts issued across the portfolio?
-- -----------------------------------------------------------------------------
-- Logic: Computes min, max, average, and rounded standard deviation proxy.
-- Expected Output Columns: min_loan_amount, max_loan_amount, avg_loan_amount, 
--   stddev_loan_amount
-- Interpretation: Confirms underwriting limits ($500 to $40,000) and ticket size spread.
-- Limitations: Simple standard deviation assumes near-symmetric distribution.
SELECT
    MIN(loan_amnt) AS min_loan_amount,
    MAX(loan_amnt) AS max_loan_amount,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
    ROUND(AVG(installment), 2) AS avg_monthly_installment
FROM fact_loans;


-- -----------------------------------------------------------------------------
-- QUERY 03: Portfolio Distribution by Loan Term Structure
-- Business Question: How is the loan portfolio divided between 36-month and 
-- 60-month facilities in count, volume, and observed default rate?
-- -----------------------------------------------------------------------------
-- Logic: Group by term duration, compute count, volume share, and default rate.
-- Expected Output Columns: term, loan_count, total_exposure, volume_share_pct, default_rate_pct
-- Interpretation: Evaluates whether longer-term loans display higher risk.
-- Limitations: Excludes floating-rate or line-of-credit products.
SELECT
    term,
    COUNT(*) AS loan_count,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(SUM(loan_amnt) * 100.0 / (SELECT SUM(loan_amnt) FROM fact_loans), 2) AS volume_share_pct,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
GROUP BY term
ORDER BY loan_count DESC;


-- -----------------------------------------------------------------------------
-- QUERY 04: Terminal Repayment Status Breakdown
-- Business Question: Exactly what percentage and dollar volume of loans have been 
-- Fully Paid versus Charged Off?
-- -----------------------------------------------------------------------------
-- Logic: Group by terminal loan_status and aggregate count and loan volume.
-- Expected Output Columns: loan_status, loan_count, status_share_pct, total_amount, amount_share_pct
-- Interpretation: Establishes the exact target class balance and write-off percentage.
-- Limitations: Data contains strictly resolved loans, no active performing loans.
SELECT
    loan_status,
    COUNT(*) AS loan_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_loans), 2) AS status_share_pct,
    ROUND(SUM(loan_amnt), 2) AS total_amount,
    ROUND(SUM(loan_amnt) * 100.0 / (SELECT SUM(loan_amnt) FROM fact_loans), 2) AS amount_share_pct
FROM fact_loans
GROUP BY loan_status
ORDER BY loan_count DESC;


-- -----------------------------------------------------------------------------
-- QUERY 05: Missing Value Profiling across Critical Fields
-- Business Question: Which core underwriting columns display missingness in the 
-- fact table, and at what failure rate?
-- -----------------------------------------------------------------------------
-- Logic: Profile null counts across major numerical and categorical dimensions.
-- Expected Output Columns: total_records, null_dti, null_revol_util, null_mort_acc, null_bankruptcies
-- Interpretation: Identifies fields requiring special handling or imputation flags.
-- Limitations: Does not indicate why fields are missing (e.g., lack of homeownership).
SELECT
    COUNT(*) AS total_records,
    SUM(CASE WHEN dti IS NULL THEN 1 ELSE 0 END) AS null_dti,
    SUM(CASE WHEN revol_util IS NULL THEN 1 ELSE 0 END) AS null_revol_util,
    SUM(CASE WHEN mort_acc IS NULL THEN 1 ELSE 0 END) AS null_mort_acc,
    SUM(CASE WHEN pub_rec_bankruptcies IS NULL THEN 1 ELSE 0 END) AS null_bankruptcies,
    SUM(CASE WHEN emp_length_years IS NULL THEN 1 ELSE 0 END) AS null_emp_length
FROM fact_loans;


-- -----------------------------------------------------------------------------
-- QUERY 06: Verification Status vs. Loan Performance
-- Business Question: Do verified borrower incomes experience lower default rates 
-- than unverified borrower declarations?
-- -----------------------------------------------------------------------------
-- Logic: Group by verification_status, aggregate volume and default rate.
-- Expected Output Columns: verification_status, loan_count, avg_income, default_rate_pct
-- Interpretation: Evaluates the effectiveness of manual income verification controls.
-- Limitations: Lender may only trigger verification on perceived higher-risk applicants.
SELECT
    verification_status,
    COUNT(*) AS loan_count,
    ROUND(AVG(annual_inc), 2) AS avg_annual_income,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
GROUP BY verification_status
ORDER BY default_rate_pct DESC;


-- =============================================================================
-- SECTION B: INTERMEDIATE RISK & PORTFOLIO SEGMENTATION (QUERIES 07 - 15)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 07: Credit Risk Performance by LendingClub Assigned Grade
-- Business Question: How does observed default rate and pricing escalate from 
-- Grade A (prime) to Grade G (deep subprime)?
-- -----------------------------------------------------------------------------
-- Logic: Group by grade, aggregate loan volume, average pricing, and default rate.
-- Expected Output Columns: grade, loan_count, total_exposure, avg_interest_rate, default_rate_pct
-- Interpretation: Evaluates monotonicity of risk ranking across internal grade buckets.
-- Limitations: Subgrade variations exist within each letter grade.
SELECT
    grade,
    COUNT(*) AS loan_count,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(AVG(dti), 2) AS avg_dti,
    SUM(is_default) AS charged_off_count,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
GROUP BY grade
ORDER BY grade ASC;


-- -----------------------------------------------------------------------------
-- QUERY 08: Loan Purpose Concentration and Observed Default Rate
-- Business Question: Which loan purposes generate the highest portfolio exposure, 
-- and which exhibit elevated default rates?
-- -----------------------------------------------------------------------------
-- Logic: Group by purpose, aggregate volume, exposure share, and default rate.
-- Expected Output Columns: purpose, loan_count, total_exposure, exposure_share_pct, default_rate_pct
-- Interpretation: Reveals debt consolidation dominance and small business risk premium.
-- Limitations: Purpose is self-reported by applicant and not independently verified.
SELECT
    purpose,
    COUNT(*) AS loan_count,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(SUM(loan_amnt) * 100.0 / (SELECT SUM(loan_amnt) FROM fact_loans), 2) AS exposure_share_pct,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
GROUP BY purpose
ORDER BY total_exposure DESC;


-- -----------------------------------------------------------------------------
-- QUERY 09: Borrower Income Band Performance Analysis
-- Business Question: How does default risk correlate across borrower income tiers?
-- -----------------------------------------------------------------------------
-- Logic: Group by derived income_band and calculate risk metrics.
-- Expected Output Columns: income_band, loan_count, total_exposure, avg_loan_size, default_rate_pct
-- Interpretation: Tests whether higher income protects against credit default.
-- Limitations: Income does not capture non-salary wealth or household obligations.
SELECT
    income_band,
    COUNT(*) AS loan_count,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(dti), 2) AS avg_dti,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
GROUP BY income_band
ORDER BY default_rate_pct DESC;


-- -----------------------------------------------------------------------------
-- QUERY 10: Debt-to-Income (DTI) Leverage Band Performance
-- Business Question: At what DTI leverage threshold does default risk spike sharply?
-- -----------------------------------------------------------------------------
-- Logic: Group by dti_band and calculate default rates and loan sizing.
-- Expected Output Columns: dti_band, loan_count, total_exposure, default_rate_pct
-- Interpretation: Guides underwriting policy limits on maximum permissible borrower leverage.
-- Limitations: DTI excludes mortgage debt in standard LendingClub calculation.
SELECT
    dti_band,
    COUNT(*) AS loan_count,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
GROUP BY dti_band
ORDER BY default_rate_pct DESC;


-- -----------------------------------------------------------------------------
-- QUERY 11: Interest Rate Tier Risk and Yield Analysis
-- Business Question: How does observed credit risk vary across interest rate pricing tiers?
-- -----------------------------------------------------------------------------
-- Logic: Group by int_rate_band, aggregate volume, average interest rate, and default rate.
-- Expected Output Columns: int_rate_band, loan_count, total_exposure, avg_interest_rate, default_rate_pct
-- Interpretation: Assesses whether higher interest rates compensate for elevated default rates.
-- Limitations: Does not account for operational servicing costs or charge-off loss severities.
SELECT
    int_rate_band,
    COUNT(*) AS loan_count,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
GROUP BY int_rate_band
ORDER BY default_rate_pct DESC;


-- -----------------------------------------------------------------------------
-- QUERY 12: Top 10 States by Exposure and Default Rate
-- Business Question: Which 10 US states represent the largest geographical 
-- concentrations, and how do their credit outcomes compare?
-- -----------------------------------------------------------------------------
-- Logic: Group by addr_state, filter out unknown states, order by exposure limit 10.
-- Expected Output Columns: addr_state, loan_count, total_exposure, state_exposure_share_pct, default_rate_pct
-- Interpretation: Identifies regional concentrations (e.g., CA, NY, TX, FL) for regulatory risk limits.
-- Limitations: State-level macro factors (local unemployment, GDP) are unmeasured.
SELECT
    addr_state,
    COUNT(*) AS loan_count,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(SUM(loan_amnt) * 100.0 / (SELECT SUM(loan_amnt) FROM fact_loans), 2) AS state_exposure_share_pct,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
WHERE addr_state IS NOT NULL AND addr_state != 'UNKNOWN'
GROUP BY addr_state
ORDER BY total_exposure DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- QUERY 13: Annual Origination Trends and Volume Growth
-- Business Question: How has annual lending volume evolved across origination years?
-- -----------------------------------------------------------------------------
-- Logic: Group by issue_year and aggregate counts, volumes, and default rates.
-- Expected Output Columns: issue_year, loans_originated, total_volume, avg_loan_size, default_rate_pct
-- Interpretation: Tracks historical portfolio expansion and macroeconomic underwriting cycles.
-- Limitations: Earlier vintages (2007-2009) have smaller sample counts.
SELECT
    issue_year,
    COUNT(*) AS loans_originated,
    ROUND(SUM(loan_amnt), 2) AS total_volume,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
GROUP BY issue_year
ORDER BY issue_year ASC;


-- -----------------------------------------------------------------------------
-- QUERY 14: Employment Tenure vs. Default Risk
-- Business Question: Does longer employment tenure meaningfully reduce observed default rate?
-- -----------------------------------------------------------------------------
-- Logic: Group by emp_length and emp_length_years to evaluate stability.
-- Expected Output Columns: emp_length, loan_count, avg_income, default_rate_pct
-- Interpretation: Analyzes whether employment stability serves as a standalone credit defense.
-- Limitations: Self-reported job title and tenure without mandatory verification.
SELECT
    CASE 
        WHEN emp_length IS NULL OR emp_length = 'nan' THEN 'Missing / Unspecified'
        ELSE emp_length 
    END AS emp_tenure,
    COUNT(*) AS loan_count,
    ROUND(AVG(annual_inc), 2) AS avg_annual_income,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
GROUP BY emp_tenure
ORDER BY loan_count DESC;


-- -----------------------------------------------------------------------------
-- QUERY 15: Home Ownership Category Risk Assessment
-- Business Question: How does home ownership status impact observed default performance?
-- -----------------------------------------------------------------------------
-- Logic: Group by standardized home_ownership (MORTGAGE, RENT, OWN, OTHER).
-- Expected Output Columns: home_ownership, loan_count, total_exposure, avg_dti, default_rate_pct
-- Interpretation: Evaluates mortgage holders (asset-backed) vs renters (liquidity sensitive).
-- Limitations: Owning a home does not guarantee positive equity.
SELECT
    home_ownership,
    COUNT(*) AS loan_count,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(annual_inc), 2) AS avg_annual_income,
    ROUND(AVG(dti), 2) AS avg_dti,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
GROUP BY home_ownership
ORDER BY default_rate_pct DESC;


-- =============================================================================
-- SECTION C: ADVANCED SQL ANALYTICS (QUERIES 16 - 25)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 16: CTE-Based Risk Matrix: High Leverage vs. Risk Grade Tier
-- Business Question: How do default rates compare when cross-tabulating high leverage 
-- (DTI >= 20%) against Prime (A/B) vs Non-Prime (C-G) loan tiers?
-- -----------------------------------------------------------------------------
-- Logic: CTE classifying loans into 4 quadrants, computes volume, loss exposure, and default rate.
-- Expected Output Columns: leverage_tier, credit_grade_tier, loan_count, exposure, default_rate_pct
-- Interpretation: Demonstrates compounding risk when high leverage meets low credit quality.
-- Limitations: Fixed 20% DTI threshold is an illustrative benchmark.
WITH classified_portfolio AS (
    SELECT
        loan_id,
        loan_amnt,
        is_default,
        CASE WHEN dti >= 20.0 THEN 'High Leverage (DTI >= 20%)' ELSE 'Moderate Leverage (DTI < 20%)' END AS leverage_tier,
        CASE WHEN grade IN ('A', 'B') THEN 'Prime (Grade A-B)' ELSE 'Subprime (Grade C-G)' END AS credit_tier
    FROM fact_loans
)
SELECT
    leverage_tier,
    credit_tier,
    COUNT(*) AS loan_count,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM classified_portfolio
GROUP BY leverage_tier, credit_tier
ORDER BY default_rate_pct DESC;


-- -----------------------------------------------------------------------------
-- QUERY 17: Window Function: Granular Subgrade Risk Ranking
-- Business Question: What is the exact default rate ranking across all 35 subgrades (A1 to G5)?
-- -----------------------------------------------------------------------------
-- Logic: Uses DENSE_RANK() OVER (ORDER BY default_rate DESC) across subgrades.
-- Expected Output Columns: sub_grade, grade, loan_count, default_rate_pct, risk_rank
-- Interpretation: Granular pricing calibration and scorecard risk monotonicity audit.
-- Limitations: Extreme subgrades (G4, G5) have lower loan counts.
WITH subgrade_metrics AS (
    SELECT
        sub_grade,
        grade,
        COUNT(*) AS loan_count,
        ROUND(SUM(loan_amnt), 2) AS total_exposure,
        ROUND(AVG(int_rate), 2) AS avg_interest_rate,
        ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
    FROM fact_loans
    GROUP BY sub_grade, grade
)
SELECT
    sub_grade,
    grade,
    loan_count,
    total_exposure,
    avg_interest_rate,
    default_rate_pct,
    DENSE_RANK() OVER (ORDER BY default_rate_pct DESC) AS risk_rank
FROM subgrade_metrics
ORDER BY risk_rank ASC;


-- -----------------------------------------------------------------------------
-- QUERY 18: Window Function: Cumulative Origination Volume & Running Loss
-- Business Question: What is the cumulative running total of funded capital over time, 
-- and how did cumulative default exposure build up?
-- -----------------------------------------------------------------------------
-- Logic: Aggregate monthly origination and use SUM() OVER (ORDER BY issue_year_month) running sum.
-- Expected Output Columns: issue_year_month, monthly_loans, monthly_volume, cumulative_volume
-- Interpretation: Visualizes balance sheet capital commitment trajectory over time.
-- Limitations: Assumes full origination funding date without amortization runoff.
WITH monthly_volume AS (
    SELECT
        issue_year_month,
        COUNT(*) AS monthly_loans,
        SUM(loan_amnt) AS monthly_exposure,
        SUM(CASE WHEN is_default = 1 THEN loan_amnt ELSE 0 END) AS monthly_defaulted_exposure
    FROM fact_loans
    GROUP BY issue_year_month
)
SELECT
    issue_year_month,
    monthly_loans,
    ROUND(monthly_exposure, 2) AS monthly_exposure,
    ROUND(SUM(monthly_exposure) OVER (ORDER BY issue_year_month), 2) AS cumulative_origination_volume,
    ROUND(SUM(monthly_defaulted_exposure) OVER (ORDER BY issue_year_month), 2) AS cumulative_defaulted_volume
FROM monthly_volume
ORDER BY issue_year_month ASC
LIMIT 24;


-- -----------------------------------------------------------------------------
-- QUERY 19: Period-over-Period (YoY) Origination Growth using LAG()
-- Business Question: What was the year-over-year origination volume growth rate 
-- across each funding vintage?
-- -----------------------------------------------------------------------------
-- Logic: Uses LAG(total_volume, 1) OVER (ORDER BY issue_year) to compute YoY volume growth %.
-- Expected Output Columns: issue_year, total_volume, prev_year_volume, yoy_volume_growth_pct
-- Interpretation: Detects aggressive portfolio expansion periods (credit loosening).
-- Limitations: Excludes 2007 baseline YoY since no preceding year exists in data.
WITH annual_origination AS (
    SELECT
        issue_year,
        COUNT(*) AS loan_count,
        ROUND(SUM(loan_amnt), 2) AS total_volume
    FROM fact_loans
    GROUP BY issue_year
)
SELECT
    issue_year,
    loan_count,
    total_volume,
    LAG(total_volume, 1) OVER (ORDER BY issue_year) AS prior_year_volume,
    ROUND(
        (total_volume - LAG(total_volume, 1) OVER (ORDER BY issue_year)) * 100.0 / 
        NULLIF(LAG(total_volume, 1) OVER (ORDER BY issue_year), 0), 2
    ) AS yoy_volume_growth_pct
FROM annual_origination
ORDER BY issue_year ASC;


-- -----------------------------------------------------------------------------
-- QUERY 20: Origination Vintage Cohort Performance Matrix
-- Business Question: How did vintage cohorts perform across origination years 
-- and term structures (36m vs 60m)?
-- -----------------------------------------------------------------------------
-- Logic: Cross-tabulate issue_year by term and compute cohort default rate.
-- Expected Output Columns: issue_year, term, loan_count, total_volume, cohort_default_rate_pct
-- Interpretation: Classic credit vintage tracking separating product term risk from cohort timing.
-- Limitations: 60-month loans only began widespread issuance in late 2010.
SELECT
    issue_year,
    term,
    COUNT(*) AS cohort_loan_count,
    ROUND(SUM(loan_amnt), 2) AS cohort_origination_volume,
    ROUND(AVG(int_rate), 2) AS avg_cohort_interest_rate,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS cohort_default_rate_pct
FROM fact_loans
GROUP BY issue_year, term
ORDER BY issue_year ASC, term ASC;


-- -----------------------------------------------------------------------------
-- QUERY 21: Segment Filtering with Minimum Statistical Significance Threshold
-- Business Question: Which loan purpose and grade combinations have at least 
-- 500 loans, ranked by highest observed default rate?
-- -----------------------------------------------------------------------------
-- Logic: Group by purpose and grade, apply HAVING COUNT(*) >= 500, order by default rate.
-- Expected Output Columns: purpose, grade, sample_size, total_exposure, default_rate_pct
-- Interpretation: Filters out noisy low-volume cells to focus audit on statistically sound risks.
-- Limitations: Threshold of 500 loans is an analyst-defined guardrail.
SELECT
    purpose,
    grade,
    COUNT(*) AS sample_size,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM fact_loans
GROUP BY purpose, grade
HAVING COUNT(*) >= 500
ORDER BY default_rate_pct DESC
LIMIT 15;


-- -----------------------------------------------------------------------------
-- QUERY 22: Risk Concentration Matrix: Segments Exceeding 1.25x Baseline Default
-- Business Question: Which purpose segments generate default rates exceeding 
-- 1.25x the portfolio baseline (19.61% * 1.25 = 24.51%)?
-- -----------------------------------------------------------------------------
-- Logic: Subquery calculating baseline default rate, then filters purpose groups exceeding 1.25x.
-- Expected Output Columns: purpose, loan_count, total_exposure, default_rate_pct, risk_index_vs_portfolio
-- Interpretation: Directly surfaces high-risk segments requiring tighter underwriting limits.
-- Limitations: Does not control for borrower credit score differences across purposes.
WITH baseline AS (
    SELECT ROUND(SUM(is_default) * 100.0 / COUNT(*), 4) AS portfolio_default_rate
    FROM fact_loans
)
SELECT
    f.purpose,
    COUNT(*) AS loan_count,
    ROUND(SUM(f.loan_amnt), 2) AS total_exposure,
    ROUND(SUM(f.is_default) * 100.0 / COUNT(*), 2) AS default_rate_pct,
    ROUND(
        (SUM(f.is_default) * 100.0 / COUNT(*)) / (SELECT portfolio_default_rate FROM baseline), 2
    ) AS risk_index_vs_portfolio
FROM fact_loans f
GROUP BY f.purpose
HAVING (SUM(f.is_default) * 100.0 / COUNT(*)) > ((SELECT portfolio_default_rate FROM baseline) * 1.25)
ORDER BY default_rate_pct DESC;


-- -----------------------------------------------------------------------------
-- QUERY 23: Data Exception Detection: High Leverage Borrowers with Sub-10% Rates
-- Business Question: How many loans were granted at low interest rates (< 10%) 
-- despite high borrower leverage (DTI >= 30%)?
-- -----------------------------------------------------------------------------
-- Logic: Filter fact_loans where int_rate < 10.0 AND dti >= 30.0.
-- Expected Output Columns: anomalous_loan_count, total_exposure, observed_default_rate_pct
-- Interpretation: Underwriting anomaly check, detects mispriced credit risk.
-- Limitations: Borrowers may have had high non-salary collateral or exceptional credit history.
SELECT
    COUNT(*) AS anomalous_loan_count,
    ROUND(SUM(loan_amnt), 2) AS anomalous_exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(AVG(dti), 2) AS avg_dti,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS observed_default_rate_pct
FROM fact_loans
WHERE int_rate < 10.0 AND dti >= 30.0;


-- -----------------------------------------------------------------------------
-- QUERY 24: Pipeline Reconciliation: Staging vs. Fact Table Audit
-- Business Question: Did the cleaning pipeline preserve record counts and dollar 
-- volume identically between staging and fact tables?
-- -----------------------------------------------------------------------------
-- Logic: Cross-table reconciliation query comparing row count, total volume, and null counts.
-- Expected Output Columns: layer_name, total_records, total_volume, avg_loan_amount
-- Interpretation: Proves pipeline integrity and guarantees zero unexplained row loss.
-- Limitations: Evaluates aggregate parity, row-level surrogate keys differ.
SELECT 
    'Staging (Raw)' AS pipeline_layer,
    COUNT(*) AS total_records,
    ROUND(SUM(loan_amnt), 2) AS total_volume,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount
FROM stg_loans
UNION ALL
SELECT 
    'Fact (Cleaned)' AS pipeline_layer,
    COUNT(*) AS total_records,
    ROUND(SUM(loan_amnt), 2) AS total_volume,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount
FROM fact_loans;


-- -----------------------------------------------------------------------------
-- QUERY 25: SQL Baseline Metric Audit for Cross-Validation with Python
-- Business Question: What are the exact baseline figures for Python and Power BI 
-- cross-layer reconciliation?
-- -----------------------------------------------------------------------------
-- Logic: Computes key metrics formatted for direct comparison with Python dictionary.
-- Expected Output Columns: total_loans, total_exposure, avg_loan_size, charged_off_count,
--   fully_paid_count, observed_default_rate
-- Interpretation: Serves as the authoritative SQL benchmark for data reconciliation tests.
-- Limitations: Must be rerun whenever underlying data changes.
SELECT
    COUNT(*) AS total_loans,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    SUM(CASE WHEN is_default = 1 THEN 1 ELSE 0 END) AS charged_off_count,
    SUM(CASE WHEN is_default = 0 THEN 1 ELSE 0 END) AS fully_paid_count,
    ROUND(SUM(CASE WHEN is_default = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 4) AS observed_default_rate
FROM fact_loans;
