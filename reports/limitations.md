# FinSight 360: Analytical Limitations & Risk Governance Boundaries

This document provides transparent disclosure regarding dataset boundaries, analytical constraints, and governance considerations governing FinSight 360.

---

## 1. Platform Specificity & Population Demographics
- **Marketplace Lending Skew**: The underlying data reflects historical peer-to-peer consumer unsecured installment facilities originated through LendingClub between 2007 and 2016.
- **Demographic Bias**: Marketplace lending borrowers historically skewed toward refinancing existing revolving credit card debt (accounting for ~80% of exposure).
- **Non-Generalizability to Commercial Banks**: Analytical findings cannot be directly extrapolated to prime retail mortgage portfolios, commercial real estate (CRE), asset-backed auto loans, or syndicated corporate lending, which operate under different collateral mechanics and underwriting regulations.

---

## 2. Information Asymmetry & Unverified Borrower Declarations
- **Self-Reported Income**: Borrower annual gross income was self-reported during online application. While LendingClub flagged verification status, **31.0%** of borrowers were `Not Verified`, and another **37.5%** were only `Source Verified`.
- **Understated Balance Sheet Leverage**: Stated Debt-to-Income (DTI) ratios calculated monthly debt service excluding existing residential mortgages and excluding the newly requested loan facility installment itself. Consequently, true total household balance sheet leverage was systematically higher than reported in the data.

---

## 3. Terminal Contract Scope & Absence of Active Performing Loans
- **Resolved Facility Nature**: The dataset consists exclusively of facilities that reached their terminal resolution (`Fully Paid` or `Charged Off`).
- **Absence of Early-Stage Delinquency**: Loans currently 30-day, 60-day, or 90-day delinquent are not represented. Therefore, roll-rate transition modeling (e.g., probability of a 30-day delinquent loan rolling into 60-day delinquency) cannot be conducted on this extract.

---

## 4. Distinction Between Statistical Correlation and Causation
- **Omitted Variable Bias**: While variables such as `grade`, `int_rate`, and `dti` display strong statistical dependencies with default outcomes ($p < 0.001$), they are descriptive risk markers rather than root causes.
- **Root Drivers of Default**: Unobserved life events—such as unexpected job termination, severe medical illness, divorce, or localized economic recessions—are the primary catalysts of consumer insolvency. The dataset does not track borrower post-origination life shocks.
- **Regulatory Fair Lending Governance**: Under the Equal Credit Opportunity Act (ECOA) and Fair Credit Reporting Act (FCRA), analytical markers must be formally audited for disparate impact before being utilized in automated credit approval policies.

---

## 5. Temporal Validity & Macroeconomic Environment
- **Zero-Interest Rate Policy (ZIRP) Era**: The origination window (2007–2016) took place largely during the post-2008 Federal Reserve Zero Interest Rate Policy regime. Borrower repayment performance, refinancing velocity, and risk appetite under a low-rate environment may differ markedly under higher interest rate or stagflationary regimes.
- **Out-of-Time (OOT) Testing Requirement**: Before implementing any scorecard or risk tier policy derived from this platform, management must validate performance on a modern out-of-time sample (e.g., 2023–2026 originations).
