-- =============================================================================
-- FinSight 360: Reusable Analytical Views
-- Script: 04_analytical_views.sql
-- Description: Core business logic views for executive KPIs, segmentation, and vintages.
-- =============================================================================

-- 1. Executive Portfolio KPI Summary
CREATE VIEW IF NOT EXISTS v_portfolio_summary AS
SELECT
    COUNT(*) AS total_loans,
    ROUND(SUM(loan_amnt), 2) AS total_original_exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(AVG(dti), 2) AS avg_dti,
    SUM(CASE WHEN is_default = 0 THEN 1 ELSE 0 END) AS fully_paid_count,
    SUM(CASE WHEN is_default = 1 THEN 1 ELSE 0 END) AS charged_off_count,
    ROUND(SUM(CASE WHEN is_default = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS observed_default_rate_pct,
    ROUND(SUM(CASE WHEN is_default = 1 THEN loan_amnt ELSE 0 END), 2) AS total_defaulted_exposure,
    ROUND(SUM(CASE WHEN is_default = 1 THEN loan_amnt ELSE 0 END) * 100.0 / SUM(loan_amnt), 2) AS defaulted_exposure_share_pct
FROM fact_loans;

-- 2. Risk Grade and Term Performance Matrix
CREATE VIEW IF NOT EXISTS v_risk_grade_performance AS
SELECT
    f.grade,
    f.term,
    COUNT(*) AS loan_count,
    ROUND(SUM(f.loan_amnt), 2) AS total_exposure,
    ROUND(AVG(f.loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(f.int_rate), 2) AS avg_interest_rate,
    ROUND(AVG(f.dti), 2) AS avg_dti,
    SUM(f.is_default) AS charged_off_count,
    ROUND(SUM(f.is_default) * 100.0 / COUNT(*), 2) AS observed_default_rate_pct,
    ROUND(SUM(f.loan_amnt) * 100.0 / (SELECT SUM(loan_amnt) FROM fact_loans), 2) AS portfolio_exposure_share_pct
FROM fact_loans f
GROUP BY f.grade, f.term;

-- 3. Loan Origination Vintage Cohort Performance
CREATE VIEW IF NOT EXISTS v_vintage_cohort_performance AS
SELECT
    issue_year,
    issue_quarter,
    COUNT(*) AS vintage_loan_count,
    ROUND(SUM(loan_amnt), 2) AS vintage_origination_volume,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    SUM(is_default) AS vintage_charged_off_count,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS observed_default_rate_pct
FROM fact_loans
GROUP BY issue_year, issue_quarter;

-- 4. Loan Purpose Risk Performance
CREATE VIEW IF NOT EXISTS v_purpose_risk_performance AS
SELECT
    purpose,
    COUNT(*) AS loan_count,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(AVG(dti), 2) AS avg_dti,
    SUM(is_default) AS charged_off_count,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS observed_default_rate_pct,
    ROUND(SUM(loan_amnt) * 100.0 / (SELECT SUM(loan_amnt) FROM fact_loans), 2) AS exposure_share_pct
FROM fact_loans
GROUP BY purpose;

-- 5. Geographic State Exposure & Default Summary
CREATE VIEW IF NOT EXISTS v_state_risk_exposure AS
SELECT
    addr_state,
    COUNT(*) AS loan_count,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    SUM(is_default) AS charged_off_count,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2) AS observed_default_rate_pct
FROM fact_loans
WHERE addr_state IS NOT NULL AND addr_state != 'UNKNOWN'
GROUP BY addr_state;
