# FinSight 360: Executive Portfolio Summary & Management Memo

**To:** Chief Risk Officer (CRO), Credit Committee, Head of Retail Lending  
**From:** Senior Banking Analytics & Credit Risk Specialist  
**Date:** Local Analytics Audit Period (Historical Portfolio: June 2007 – December 2016)  
**Subject:** Comprehensive Portfolio Credit Risk Intelligence & Portfolio Performance Audit  

---

## 1. Executive Briefing & Macro Portfolio Health

Between June 2007 and December 2016, the analyzed consumer lending portfolio funded **396,030 closed installment loan facilities**, representing **$5,589,522,775 ($5.59 Billion)** in aggregate original principal exposure.

All evaluated contracts represent completed facilities, yielding an authoritative, uncensored credit loss benchmark:
- **Fully Paid Facilities:** **318,357 loans (80.39%)**, representing **$4,430,693,425** in capital recovered with interest.
- **Charged Off Facilities:** **77,673 loans (19.61%)**, representing **$1,158,829,350 ($1.16 Billion)** in cumulative write-offs.
- **Portfolio Baseline Default Rate:** **19.61%**.
- **Average Facility Sizing:** **$14,113.89** (Median: $12,000.00).
- **Portfolio Nominal Gross Yield:** **13.64%** average interest rate.
- **Average Borrower Financial Leverage:** **17.38 DTI**.

![Executive Portfolio Overview](file:///c:/Users/saiya/Desktop/360/reports/screenshots/01_executive_portfolio_overview.png)

---

## 2. Key Diagnostic Findings

### 1. Risk Grade Monotonicity & Subprime Exposure Drag
The internal risk scoring framework demonstrates strong monotonic discrimination, escalating from **6.29%** in Grade A to **45.84%** in Grade G:
- **Prime Tier (Grades A & B):** Accounts for **$2.67 Billion (47.78%)** of exposure with an observed default rate of **10.51%**.
- **Deep Subprime Tier (Grades E, F, & G):** Represents **$717.3 Million (12.83%)** of capital exposure, yet generates **27.64% (21,465 loans)** of total portfolio charge-offs.

### 2. The 60-Month Facility Risk Multiplier
Loan term duration acts as a severe risk multiplier:
- **36-Month Loans:** Represent **76.26% (302,005 loans)** of portfolio volume with an observed default rate of **16.00%**.
- **60-Month Loans:** Represent **23.74% (94,025 loans)** of volume with an observed default rate of **31.74%** — nearly **2.0x higher risk**.

### 3. Leverage Inflection at 20% DTI
Borrowers with Debt-to-Income (DTI) ratios exceeding 20% experience an abrupt increase in default probability, reaching **24.58%** for borrowers with DTI exceeding 30%, compared to **14.28%** for borrowers below 10% DTI.

### 4. Commercial / Small Business Vulnerability
While debt consolidation represents the largest share of exposure (**59.20% / $3.31 Billion**; 20.73% default rate), loans originated for **small business purposes** exhibit the highest segment default rate at **29.45%** across 5,701 facilities.

![Credit Risk Segmentation](file:///c:/Users/saiya/Desktop/360/reports/screenshots/02_credit_risk_segmentation.png)

---

## 3. Data Governance & Audit Confidence

The analytical data foundation was audited through an automated 12-rule Data Quality framework:
- **10 Rules Passed (100% compliance)**: Schema integrity, loan ID uniqueness, loan amount boundary ($500–$40,000), interest rate boundary (4%–35%), date validity, risk grade validity, binary target completeness, and stage-to-stage record parity (396,030 records preserved).
- **1 Critical Exception Isolated**: Exactly 1 facility (`LN-1285675`, $3,700 funded, Grade C) reported $0 annual income with a placeholder DTI of 9999.0; the loan defaulted.
- **1 Warning Alert**: Exactly 8 facilities exhibited DTI > 100%, reflecting extreme pre-existing borrower indebtedness.
- **Cross-Layer Mathematical Reconciliation**: Python, PostgreSQL, SQLite, and Excel metrics reconcile with **0.0000 absolute discrepancy**.

![Vintages and Data Quality](file:///c:/Users/saiya/Desktop/360/reports/screenshots/03_portfolio_vintages_and_data_quality.png)

---

## 4. Immediate Strategic Recommendations for Management

1. **Underwriting Moratorium on 60-Month Subprime Terms**: Cease offering 60-month terms for Grades E, F, and G. This single policy change protects an estimated **$180 Million** in capital from high-probability credit loss.
2. **Hard Leverage Cap at 25% DTI**: Institute a mandatory debt service cap restricting unsecured consumer originations where borrower DTI exceeds 25%.
3. **Small Business Underwriting Adjustment**: Require audited financial statements or business cash flow verification for small business loan requests, rather than evaluating them under consumer scorecards.
4. **Mandatory Income Verification on High-Ticket Requests**: Mandate verified W-2/tax documentation for any loan request exceeding $25,000, addressing the 31% unverified application share.

---

## 5. Analytical Governance & Boundaries
*This report is an analytical investigation utilizing public historical consumer lending data. In compliance with model governance standards, statistical associations describe observed historical cohort behaviors and do not establish direct individual causation or represent production automated underwriting approval systems.*
