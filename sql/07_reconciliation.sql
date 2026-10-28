-- =============================================================================
-- FinSight 360: Layer Reconciliation Queries
-- Script: 07_reconciliation.sql
-- Description: Reconciles staging, fact, and analytical views to verify mathematical parity.
-- =============================================================================

-- 1. Staging vs. Fact Row Count & Dollar Parity Reconciliation
WITH stg_summary AS (
    SELECT
        COUNT(*) AS stg_count,
        ROUND(SUM(loan_amnt), 2) AS stg_volume
    FROM stg_loans
),
fact_summary AS (
    SELECT
        COUNT(*) AS fact_count,
        ROUND(SUM(loan_amnt), 2) AS fact_volume
    FROM fact_loans
)
SELECT
    s.stg_count,
    f.fact_count,
    (s.stg_count - f.fact_count) AS count_difference,
    s.stg_volume,
    f.fact_volume,
    ROUND(s.stg_volume - f.fact_volume, 2) AS volume_difference,
    CASE 
        WHEN s.stg_count = f.fact_count AND ROUND(s.stg_volume, 2) = ROUND(f.fact_volume, 2) 
        THEN 'RECONCILED_SUCCESS' 
        ELSE 'RECONCILIATION_DISCREPANCY' 
    END AS reconciliation_status
FROM stg_summary s, fact_summary f;

-- 2. Fact vs. View Portfolio Parity Reconciliation
WITH fact_base AS (
    SELECT
        COUNT(*) AS fact_loans,
        ROUND(SUM(loan_amnt), 2) AS fact_volume,
        ROUND(SUM(CASE WHEN is_default = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS fact_default_rate
    FROM fact_loans
),
view_base AS (
    SELECT
        total_loans AS view_loans,
        total_original_exposure AS view_volume,
        observed_default_rate_pct AS view_default_rate
    FROM v_portfolio_summary
)
SELECT
    f.fact_loans,
    v.view_loans,
    (f.fact_loans - v.view_loans) AS loan_count_diff,
    f.fact_volume,
    v.view_volume,
    ROUND(f.fact_volume - v.view_volume, 2) AS volume_diff,
    f.fact_default_rate,
    v.view_default_rate,
    CASE 
        WHEN f.fact_loans = v.view_loans AND f.fact_volume = v.view_volume 
        THEN 'VIEW_MATCH_PASS' 
        ELSE 'VIEW_MISMATCH_FAIL' 
    END AS view_reconciliation_status
FROM fact_base f, view_base v;
