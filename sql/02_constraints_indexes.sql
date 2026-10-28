-- =============================================================================
-- FinSight 360: Constraints and Indexes
-- Script: 02_constraints_indexes.sql
-- Description: Enforces referential integrity, domain validation, and query performance.
-- =============================================================================

-- Performance Indexes for Analytical Slicing & Star Joins
CREATE INDEX IF NOT EXISTS idx_fact_loans_grade ON fact_loans (grade);
CREATE INDEX IF NOT EXISTS idx_fact_loans_issue_date ON fact_loans (issue_date);
CREATE INDEX IF NOT EXISTS idx_fact_loans_purpose ON fact_loans (purpose);
CREATE INDEX IF NOT EXISTS idx_fact_loans_default ON fact_loans (is_default);
CREATE INDEX IF NOT EXISTS idx_fact_loans_state ON fact_loans (addr_state);
CREATE INDEX IF NOT EXISTS idx_fact_loans_vintage ON fact_loans (issue_year, issue_month);
CREATE INDEX IF NOT EXISTS idx_fact_loans_composite_risk ON fact_loans (grade, term_months, is_default);
CREATE INDEX IF NOT EXISTS idx_fact_loans_amount_band ON fact_loans (loan_amount_band);
CREATE INDEX IF NOT EXISTS idx_fact_loans_dti_band ON fact_loans (dti_band);
CREATE INDEX IF NOT EXISTS idx_fact_loans_income_band ON fact_loans (income_band);

-- Dimension Indexes
CREATE INDEX IF NOT EXISTS idx_dim_date_year_month ON dim_date (year_month);
CREATE INDEX IF NOT EXISTS idx_dim_purpose_group ON dim_loan_purpose (purpose_group);
