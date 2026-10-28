-- =============================================================================
-- FinSight 360: Staging Views
-- Script: 03_staging_views.sql
-- Description: Transformations and profile views directly over staging data.
-- =============================================================================

CREATE VIEW IF NOT EXISTS v_stg_loans_profiling AS
SELECT
    COUNT(*) AS total_raw_records,
    COUNT(DISTINCT address) AS unique_addresses,
    SUM(CASE WHEN loan_amnt IS NULL THEN 1 ELSE 0 END) AS null_loan_amnt,
    SUM(CASE WHEN int_rate IS NULL THEN 1 ELSE 0 END) AS null_int_rate,
    SUM(CASE WHEN annual_inc IS NULL THEN 1 ELSE 0 END) AS null_annual_inc,
    SUM(CASE WHEN dti IS NULL THEN 1 ELSE 0 END) AS null_dti,
    SUM(CASE WHEN mort_acc IS NULL THEN 1 ELSE 0 END) AS null_mort_acc,
    SUM(CASE WHEN pub_rec_bankruptcies IS NULL THEN 1 ELSE 0 END) AS null_bankruptcies,
    ROUND(AVG(loan_amnt), 2) AS raw_avg_loan_amount,
    ROUND(AVG(int_rate), 2) AS raw_avg_int_rate
FROM stg_loans;

CREATE VIEW IF NOT EXISTS v_stg_loan_status_distribution AS
SELECT
    TRIM(loan_status) AS raw_loan_status,
    COUNT(*) AS record_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM stg_loans), 2) AS percentage_of_total
FROM stg_loans
GROUP BY TRIM(loan_status);
