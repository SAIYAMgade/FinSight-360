# FinSight 360: Data Quality & Governance Audit Report

**Report Execution Date:** 2026-10-28  
**Audit Scope:** 396,030 Records Ingested from LendingClub Public Source (`lending_club_loan_two.csv`)  
**Auditing Framework:** `src/validate.py` (DataQualityValidator)  
**Overall Audit Compliance Score:** **83.3% Rule Compliance (10 PASS, 1 WARNING, 1 FAIL)**  

---

## 1. Machine-Readable Validation Audit Log

| check_name | severity | records_checked | failures_found | failure_rate (%) | result | details | timestamp |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| `DQ-001_REQUIRED_FIELDS_MISSING` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Required fields evaluated: `['loan_amnt', 'term', 'grade', 'annual_inc', 'issue_d', 'loan_status']`. All records populated. | 2026-10-28T10:44:09Z |
| `DQ-002_UNIQUE_LOAN_IDENTIFIER` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Evaluated primary surrogate key `loan_id`. 396,030 distinct values; 0 duplicates detected. | 2026-10-28T10:44:09Z |
| `DQ-003_DUPLICATE_RECORDS` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Checked for fully duplicate borrower and facility records across all attributes. 0 duplicate rows. | 2026-10-28T10:44:10Z |
| `DQ-004_LOAN_AMOUNT_RANGE` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Verified loan amounts against underwriting policy limits ($500 to $50,000). Range: $500 to $40,000. | 2026-10-28T10:44:10Z |
| `DQ-005_INTEREST_RATE_RANGE` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Verified nominal interest rate boundary (4.0% to 35.0%). Range: 5.32% to 30.99%. | 2026-10-28T10:44:10Z |
| `DQ-006_DATE_PARSING_INTEGRITY` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Converted `issue_d` strings (`%b-%Y`) into valid Gregorian ISO dates. 0 parsing failures. | 2026-10-28T10:44:10Z |
| `DQ-007_POSITIVE_ANNUAL_INCOME` | CRITICAL | 396,030 | 1 | 0.0003% | **FAIL** | Evaluated self-reported annual income > $0. Found exactly 1 record with $0.00 income. | 2026-10-28T10:44:10Z |
| `DQ-008_KNOWN_RISK_GRADES` | CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Verified grade domain strictly in `['A', 'B', 'C', 'D', 'E', 'F', 'G']`. 0 invalid categories. | 2026-10-28T10:44:10Z |
| `DQ-009_TARGET_VARIABLE_INTEGRITY`| CRITICAL | 396,030 | 0 | 0.0000% | **PASS** | Verified `is_default` binary domain (0 or 1). 0 nulls, 0 ambiguous categories. | 2026-10-28T10:44:10Z |
| `DQ-010_CHRONOLOGICAL_CREDIT_AGE` | WARNING | 396,030 | 0 | 0.0000% | **PASS** | Verified that earliest credit line opening precedes or equals loan origination date. 0 negative values. | 2026-10-28T10:44:10Z |
| `DQ-011_RECORD_RETENTION_INTEGRITY`| INFORMATIONAL| 396,030 | 0 | 0.0000% | **PASS** | Stage-to-stage parity check: Ingested = 396,030, Cleaned = 396,030, Fact = 396,030. Discrepancy = 0. | 2026-10-28T10:44:10Z |
| `DQ-012_EXTREME_DTI_OUTLIERS` | WARNING | 396,030 | 8 | 0.0020% | **WARNING** | Scanned for debt-to-income leverage exceeding 100%. Found 8 records with extreme leverage. | 2026-10-28T10:44:10Z |

---

## 2. In-Depth Exception Diagnostics & Forensics

### Critical Failure Investigation: `DQ-007_POSITIVE_ANNUAL_INCOME`
- **Affected Facility ID:** `LN-1285675`
- **Underwriting Profile:**
  - Original Funded Amount: **$3,700.00**
  - Contract Term: **36 months**
  - Interest Rate: **13.67%** (Grade C, Subgrade C3)
  - Stated Purpose: `credit_card`
  - Self-Reported Income: **$0.00**
  - Stated DTI: **9999.00** (Platform placeholder value indicating mathematically undefined division by zero)
  - Terminal Outcome: **Charged Off**
- **Forensic Assessment:**
  This facility was approved despite applicant declaring zero annual income, using a placeholder DTI of 9999.0. The borrower predictably failed to service the loan and defaulted.
- **Remediation Action:**
  Retained in the cleaned fact table with an explicit data quality exception flag to maintain audit integrity; excluded from income-band logarithm regressions. Underwriting policy recommendation: mandate automated hard rejection rule if income $\le \$0$.

### Warning Alert Investigation: `DQ-012_EXTREME_DTI_OUTLIERS`
- **Affected Population:** Exactly 8 records (0.002% of portfolio).
- **Profile:** Borrowers with reported DTI ratios between **109.0%** and **9999.0%**.
- **Performance:** 5 of the 8 facilities resulted in terminal Charge-Off (62.5% default rate).
- **Remediation Action:**
  Binned into the highest leverage bucket (`30%+`) to prevent skewing linear statistical models.

---

## 3. Missing Value Analysis on Non-Core Fields

While core underwriting fields displayed 0% missingness, several auxiliary credit bureau fields exhibited natural missing patterns:
- `mort_acc`: **37,795 missing records (9.54%)**.
  - *Root Cause:* Borrowers who have never maintained a mortgage facility. Handled as categorical missingness without arbitrary imputation.
- `emp_title`: **22,927 missing records (5.79%)**.
  - *Root Cause:* Self-employed, retired, or unstated employment.
- `emp_length`: **18,301 missing records (4.62%)**.
  - *Root Cause:* Standardized to `Missing / Unspecified` in categorical reporting and `-1.0` indicator in model feature matrices.
- `pub_rec_bankruptcies`: **535 missing records (0.14%)**.
  - *Root Cause:* Early vintage records (2007–2008) where bankruptcy reporting fields were not yet standardized on the platform.

---

## 4. Cross-Layer Mathematical Reconciliation Audit

To ensure mathematical parity across the technology stack, portfolio metrics were reconciled between Python, PostgreSQL/SQLite, and Excel:

```
+-----------------------+---------------------+---------------------+--------------+--------+
| Metric Name           | Python Metric Layer | SQL Analytical View | Discrepancy  | Status |
+-----------------------+---------------------+---------------------+--------------+--------+
| Total Closed Loans    | 396,030             | 396,030             | 0.0000       | MATCH  |
| Total Exposure        | $5,589,522,775.00   | $5,589,522,775.00   | 0.0000       | MATCH  |
| Average Loan Size     | $14,113.89          | $14,113.89          | 0.0000       | MATCH  |
| Charged Off Count     | 77,673              | 77,673              | 0.0000       | MATCH  |
| Fully Paid Count      | 318,357             | 318,357             | 0.0000       | MATCH  |
| Observed Default Rate | 19.6129%            | 19.6100%            | 0.0029% (rnd)| MATCH  |
+-----------------------+---------------------+---------------------+--------------+--------+
```

**Audit Verdict:** Zero unrecorded data loss across ingestion, transformation, relational database views, and management reporting deliverables.
