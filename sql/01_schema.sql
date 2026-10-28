-- =============================================================================
-- FinSight 360: PostgreSQL DDL Schema
-- Script: 01_schema.sql
-- Description: Core analytical star schema for banking credit risk intelligence.
-- =============================================================================

-- 1. Pipeline Run History
CREATE TABLE IF NOT EXISTS pipeline_run_history (
    run_id VARCHAR(50) PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    records_ingested INT,
    records_processed INT,
    status VARCHAR(20) NOT NULL,
    notes TEXT
);

-- 2. Data Quality Audit Exceptions Log
CREATE TABLE IF NOT EXISTS dq_audit_log (
    log_id INTEGER PRIMARY KEY,
    check_name VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    records_checked INT NOT NULL,
    failures_found INT NOT NULL,
    failure_rate NUMERIC(8, 4) NOT NULL,
    result VARCHAR(10) NOT NULL,
    details TEXT,
    timestamp TIMESTAMP NOT NULL
);

-- 3. Staging Raw Loans Table
CREATE TABLE IF NOT EXISTS stg_loans (
    loan_amnt NUMERIC(12, 2),
    term VARCHAR(20),
    int_rate NUMERIC(6, 2),
    installment NUMERIC(10, 2),
    grade VARCHAR(5),
    sub_grade VARCHAR(10),
    emp_title VARCHAR(255),
    emp_length VARCHAR(50),
    home_ownership VARCHAR(20),
    annual_inc NUMERIC(14, 2),
    verification_status VARCHAR(50),
    issue_d VARCHAR(20),
    loan_status VARCHAR(50),
    purpose VARCHAR(50),
    title VARCHAR(255),
    dti NUMERIC(8, 2),
    earliest_cr_line VARCHAR(20),
    open_acc NUMERIC(6, 0),
    pub_rec NUMERIC(6, 0),
    revol_bal NUMERIC(14, 2),
    revol_util NUMERIC(6, 2),
    total_acc NUMERIC(6, 0),
    initial_list_status VARCHAR(10),
    application_type VARCHAR(50),
    mort_acc NUMERIC(6, 0),
    pub_rec_bankruptcies NUMERIC(6, 0),
    address TEXT
);

-- 4. Dimension: Risk Grade
CREATE TABLE IF NOT EXISTS dim_risk_grade (
    grade VARCHAR(5) PRIMARY KEY,
    risk_tier VARCHAR(20) NOT NULL,
    prime_status VARCHAR(20) NOT NULL,
    expected_loss_range VARCHAR(50)
);

-- 5. Dimension: Loan Purpose
CREATE TABLE IF NOT EXISTS dim_loan_purpose (
    purpose VARCHAR(50) PRIMARY KEY,
    purpose_group VARCHAR(50) NOT NULL,
    is_refinancing INT NOT NULL
);

-- 6. Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_key VARCHAR(10) PRIMARY KEY,
    full_date DATE NOT NULL,
    year_num INT NOT NULL,
    quarter_num INT NOT NULL,
    month_num INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    year_month VARCHAR(7) NOT NULL
);

-- 7. Fact: Cleaned Loans & Outcomes
CREATE TABLE IF NOT EXISTS fact_loans (
    loan_id VARCHAR(50) PRIMARY KEY,
    loan_amnt NUMERIC(12, 2) NOT NULL,
    term VARCHAR(20) NOT NULL,
    term_months INT NOT NULL,
    int_rate NUMERIC(6, 2) NOT NULL,
    installment NUMERIC(10, 2) NOT NULL,
    grade VARCHAR(5) NOT NULL,
    sub_grade VARCHAR(10) NOT NULL,
    home_ownership VARCHAR(20) NOT NULL,
    annual_inc NUMERIC(14, 2) NOT NULL,
    verification_status VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    issue_year INT NOT NULL,
    issue_month INT NOT NULL,
    issue_quarter VARCHAR(10) NOT NULL,
    issue_year_month VARCHAR(7) NOT NULL,
    loan_status VARCHAR(50) NOT NULL,
    is_default INT NOT NULL,
    purpose VARCHAR(50) NOT NULL,
    dti NUMERIC(8, 2),
    addr_state VARCHAR(10),
    zip_code VARCHAR(10),
    emp_length VARCHAR(50),
    emp_length_years NUMERIC(4, 1),
    credit_history_years NUMERIC(5, 1),
    open_acc NUMERIC(6, 0),
    pub_rec NUMERIC(6, 0),
    revol_bal NUMERIC(14, 2),
    revol_util NUMERIC(6, 2),
    total_acc NUMERIC(6, 0),
    mort_acc NUMERIC(6, 0),
    pub_rec_bankruptcies NUMERIC(6, 0),
    loan_amount_band VARCHAR(20),
    income_band VARCHAR(20),
    dti_band VARCHAR(20),
    int_rate_band VARCHAR(20),
    installment_burden_pct NUMERIC(6, 2),
    is_high_risk_segment INT NOT NULL
);
