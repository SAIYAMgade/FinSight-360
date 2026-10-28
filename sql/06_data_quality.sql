-- =============================================================================
-- FinSight 360: SQL Data Quality Profiling & Exception Queries
-- Script: 06_data_quality.sql
-- Description: Automated SQL test scripts for data health and integrity audit.
-- =============================================================================

-- 1. Uniqueness check on primary surrogate key
SELECT 
    'DQ_LOAN_ID_DUPLICATES' AS check_name,
    COUNT(*) - COUNT(DISTINCT loan_id) AS failed_records,
    CASE WHEN COUNT(*) = COUNT(DISTINCT loan_id) THEN 'PASS' ELSE 'FAIL' END AS status
FROM fact_loans;

-- 2. Null check on required fields
SELECT 
    'DQ_NULL_CORE_FIELDS' AS check_name,
    COUNT(*) AS failed_records,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM fact_loans
WHERE loan_amnt IS NULL 
   OR term IS NULL 
   OR grade IS NULL 
   OR annual_inc IS NULL 
   OR issue_date IS NULL 
   OR is_default IS NULL;

-- 3. Loan amount plausibility range check ($500 to $50,000)
SELECT 
    'DQ_LOAN_AMOUNT_RANGE' AS check_name,
    COUNT(*) AS failed_records,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM fact_loans
WHERE loan_amnt < 500.0 OR loan_amnt > 50000.0;

-- 4. Interest rate plausibility range check (3.0% to 35.0%)
SELECT 
    'DQ_INTEREST_RATE_RANGE' AS check_name,
    COUNT(*) AS failed_records,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM fact_loans
WHERE int_rate < 3.0 OR int_rate > 35.0;

-- 5. Target variable integrity check (must be strictly 0 or 1)
SELECT 
    'DQ_TARGET_VARIABLE_DOMAIN' AS check_name,
    COUNT(*) AS failed_records,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status
FROM fact_loans
WHERE is_default NOT IN (0, 1) OR is_default IS NULL;

-- 6. Chronological integrity check (credit history age >= 0)
SELECT 
    'DQ_CHRONOLOGICAL_CREDIT_AGE' AS check_name,
    COUNT(*) AS failed_records,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status
FROM fact_loans
WHERE credit_history_years < 0;

-- 7. High DTI outlier profiling
SELECT 
    'DQ_EXTREME_DTI_OUTLIERS' AS check_name,
    COUNT(*) AS records_exceeding_100_dti,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_loans), 4) AS outlier_rate_pct,
    'WARNING' AS status
FROM fact_loans
WHERE dti > 100.0;
