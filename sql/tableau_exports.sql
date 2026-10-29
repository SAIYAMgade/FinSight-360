-- =============================================================================
-- FinSight 360: Tableau Public Export SQL Queries
-- Script: sql/tableau_exports.sql
-- Description: Aggregated, anonymized export queries powering the Tableau Public
--              Executive Credit Risk & Portfolio Intelligence Dashboard.
-- Standards: Snake_case headers, ISO dates, zero PII, fully aggregated.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- EXPORT 1: Delinquency Rate & NPL Ratio Over Time (Monthly Vintage Trend)
-- Target File: tableau_data/delinquency_npl_trend.csv
-- Business Use: Tracks loan counts, original principal exposure, charged-off
--   counts (delinquent/write-off units), and defaulted capital volume across
--   origination vintages with multi-dimensional slicing capability.
-- -----------------------------------------------------------------------------
SELECT
    f.issue_date AS period_date,
    f.issue_year AS origination_year,
    f.issue_quarter AS origination_quarter,
    f.issue_year_month AS year_month,
    r.risk_tier,
    r.prime_status,
    p.purpose AS segment,
    p.purpose_group,
    COUNT(*) AS loan_count,
    ROUND(SUM(f.loan_amnt), 2) AS total_exposure,
    SUM(CASE WHEN f.is_default = 0 THEN 1 ELSE 0 END) AS fully_paid_count,
    ROUND(SUM(CASE WHEN f.is_default = 0 THEN f.loan_amnt ELSE 0 END), 2) AS fully_paid_exposure,
    SUM(CASE WHEN f.is_default = 1 THEN 1 ELSE 0 END) AS charged_off_count,
    ROUND(SUM(CASE WHEN f.is_default = 1 THEN f.loan_amnt ELSE 0 END), 2) AS charged_off_exposure,
    ROUND(SUM(CASE WHEN f.is_default = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 4) AS delinquency_rate,
    ROUND(SUM(CASE WHEN f.is_default = 1 THEN f.loan_amnt ELSE 0 END) * 100.0 / NULLIF(SUM(f.loan_amnt), 0), 4) AS npl_ratio
FROM fact_loans f
LEFT JOIN dim_risk_grade r ON f.grade = r.grade
LEFT JOIN dim_loan_purpose p ON f.purpose = p.purpose
GROUP BY
    f.issue_date,
    f.issue_year,
    f.issue_quarter,
    f.issue_year_month,
    r.risk_tier,
    r.prime_status,
    p.purpose,
    p.purpose_group
ORDER BY
    f.issue_date ASC,
    r.risk_tier ASC,
    p.purpose ASC;


-- -----------------------------------------------------------------------------
-- EXPORT 2: Capital Exposure & Risk Performance by Underwriting Risk Tier
-- Target File: tableau_data/exposure_by_risk_tier.csv
-- Business Use: Evaluates capital distribution across all 7 verified risk tiers
--   (Grades A through G) with origination year and purpose segment dimensions
--   for global cross-worksheet dashboard filtering.
-- -----------------------------------------------------------------------------
SELECT
    r.risk_tier,
    f.grade,
    r.prime_status,
    f.issue_year AS origination_year,
    p.purpose AS segment,
    COUNT(*) AS loan_count,
    ROUND(SUM(f.loan_amnt), 2) AS total_exposure,
    ROUND(AVG(f.loan_amnt), 2) AS avg_loan_size,
    SUM(CASE WHEN f.is_default = 1 THEN 1 ELSE 0 END) AS charged_off_count,
    ROUND(SUM(CASE WHEN f.is_default = 1 THEN f.loan_amnt ELSE 0 END), 2) AS charged_off_exposure,
    ROUND(SUM(CASE WHEN f.is_default = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 4) AS delinquency_rate,
    ROUND(SUM(CASE WHEN f.is_default = 1 THEN f.loan_amnt ELSE 0 END) * 100.0 / NULLIF(SUM(f.loan_amnt), 0), 4) AS npl_ratio,
    ROUND(SUM(f.loan_amnt) * 100.0 / (SELECT SUM(loan_amnt) FROM fact_loans), 4) AS share_of_total_exposure
FROM fact_loans f
LEFT JOIN dim_risk_grade r ON f.grade = r.grade
LEFT JOIN dim_loan_purpose p ON f.purpose = p.purpose
GROUP BY
    r.risk_tier,
    f.grade,
    r.prime_status,
    f.issue_year,
    p.purpose
ORDER BY
    f.grade ASC,
    f.issue_year ASC,
    p.purpose ASC;


-- -----------------------------------------------------------------------------
-- EXPORT 3: Capital Concentration & Risk Matrix by Loan Purpose Segment
-- Target File: tableau_data/concentration_by_segment.csv
-- Business Use: Breaks down portfolio exposure across borrower loan purposes,
--   flagging dominant concentration drivers (debt_consolidation, credit_card)
--   and high-risk segments exceeding 1.25x baseline credit loss.
-- -----------------------------------------------------------------------------
SELECT
    p.purpose AS segment,
    p.purpose_group,
    f.issue_year AS origination_year,
    r.risk_tier,
    COUNT(*) AS loan_count,
    ROUND(SUM(f.loan_amnt), 2) AS total_exposure,
    ROUND(AVG(f.loan_amnt), 2) AS avg_loan_size,
    SUM(CASE WHEN f.is_default = 1 THEN 1 ELSE 0 END) AS charged_off_count,
    ROUND(SUM(CASE WHEN f.is_default = 1 THEN f.loan_amnt ELSE 0 END), 2) AS charged_off_exposure,
    ROUND(SUM(CASE WHEN f.is_default = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 4) AS delinquency_rate,
    ROUND(SUM(CASE WHEN f.is_default = 1 THEN f.loan_amnt ELSE 0 END) * 100.0 / NULLIF(SUM(f.loan_amnt), 0), 4) AS npl_ratio,
    ROUND(SUM(f.loan_amnt) * 100.0 / (SELECT SUM(loan_amnt) FROM fact_loans), 4) AS share_of_total_exposure,
    CASE 
        WHEN p.purpose IN ('debt_consolidation', 'credit_card') THEN 1 
        ELSE 0 
    END AS is_high_exposure_segment,
    CASE 
        WHEN p.purpose IN ('small_business', 'moving', 'medical') THEN 1 
        ELSE 0 
    END AS is_high_risk_segment
FROM fact_loans f
LEFT JOIN dim_loan_purpose p ON f.purpose = p.purpose
LEFT JOIN dim_risk_grade r ON f.grade = r.grade
GROUP BY
    p.purpose,
    p.purpose_group,
    f.issue_year,
    r.risk_tier
ORDER BY
    total_exposure DESC;


-- -----------------------------------------------------------------------------
-- EXPORT 4: Executive Single-Row Portfolio KPI Scorecard
-- Target File: tableau_data/kpi_summary.csv
-- Business Use: Powers the high-level KPI scorecard tiles on the Tableau header.
-- -----------------------------------------------------------------------------
SELECT
    COUNT(*) AS total_loans,
    COUNT(DISTINCT loan_id) AS total_borrowers,
    ROUND(SUM(loan_amnt), 2) AS total_exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_size,
    ROUND(SUM(CASE WHEN is_default = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 4) AS overall_delinquency_rate,
    ROUND(SUM(CASE WHEN is_default = 1 THEN loan_amnt ELSE 0 END) * 100.0 / SUM(loan_amnt), 4) AS overall_npl_ratio,
    (SELECT COUNT(DISTINCT risk_tier) FROM dim_risk_grade) AS number_of_risk_tiers,
    ROUND(
        (SELECT SUM(loan_amnt) FROM fact_loans WHERE purpose = 'debt_consolidation') * 100.0 / SUM(loan_amnt), 4
    ) AS top_segment_concentration_pct,
    ROUND(
        (SELECT SUM(loan_amnt) FROM fact_loans WHERE is_high_risk_segment = 1) * 100.0 / SUM(loan_amnt), 4
    ) AS high_risk_segment_concentration_pct,
    ROUND(
        (SELECT SUM(loan_amnt) FROM fact_loans WHERE purpose = 'credit_card') * 100.0 / SUM(loan_amnt), 4
    ) AS secondary_concentration_pct
FROM fact_loans;
