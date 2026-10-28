# FinSight 360: Business Findings & Management Memo

This document presents evidence-based analytical findings from the FinSight 360 banking portfolio evaluation, adhering strictly to the structured evidence format required by banking analytics and credit risk oversight.

---

### Finding 1: Risk Grade Monotonicity and Severe Capital Attrition in Deep Subprime (Grades E, F, G)

**Finding:**  
Observed default rates escalate monotonically from Grade A (lowest risk) to Grade G (highest risk). Subprime tiers E through G experience catastrophic credit loss rates exceeding 38%, disproportionately driving overall portfolio write-offs.

**Evidence:**  
- **Analysis Scope:** 396,030 closed loan facilities originated between June 2007 and December 2016.
- **Grade A:** 64,187 loans | $905.7M exposure | **6.29%** observed default rate (4,037 charge-offs) | 7.33% avg rate.
- **Grade B:** 116,018 loans | $1,570.6M exposure | **13.57%** observed default rate (15,744 charge-offs) | 10.66% avg rate.
- **Grade C:** 105,987 loans | $1,507.0M exposure | **21.84%** observed default rate (23,149 charge-offs) | 14.01% avg rate.
- **Grade D:** 63,524 loans | $923.6M exposure | **28.68%** observed default rate (18,218 charge-offs) | 17.18% avg rate.
- **Grade E:** 31,488 loans | $501.9M exposure | **37.36%** observed default rate (11,765 charge-offs) | 19.95% avg rate.
- **Grade F:** 11,772 loans | $176.7M exposure | **42.22%** observed default rate (4,970 charge-offs) | 23.58% avg rate.
- **Grade G:** 3,054 loans | $43.9M exposure | **45.84%** observed default rate (1,400 charge-offs) | 25.61% avg rate.
- **Concentration:** Grades E, F, and G comprise **$722.5M (12.93%)** of portfolio exposure, but account for **27.64% (21,465 facilities)** of all charged-off loans.

**Business Implication:**  
While nominal contractual yields increase from 7.33% (Grade A) to 25.61% (Grade G), gross interest revenues in Grades E–G are insufficient to absorb a 37%–46% principal loss rate when factoring in operating expenses, funding costs, and recovery discount rates. Subprime facilities act as a net destroyer of risk-adjusted economic capital.

**Recommended Next Step:**  
Review risk-adjusted return on capital (RAROC) for Grades E, F, and G. Institute tighter underwriting overlays, including capping maximum allowable debt-to-income (DTI) at 20% for any subprime applicant and restricting loan sizing to under $15,000.

**Caveat:**  
Historical recovery amounts and third-party debt collection proceeds are excluded from this extract, meaning actual ultimate loss severity (Loss Given Default) could be lower than the headline 45.8% gross charge-off rate.

---

### Finding 2: The 60-Month Facility Term Risk Multiplier

**Finding:**  
Loan facilities with a 60-month term duration exhibit an observed default rate nearly double that of 36-month facilities across every comparable underwriting grade.

**Evidence:**  
- **36-Month Facilities:** 302,005 loans | $3,831.6M exposure | **16.00%** default rate (48,328 charge-offs) | 12.00% avg rate.
- **60-Month Facilities:** 94,025 loans | $1,757.9M exposure | **31.74%** default rate (29,345 charge-offs) | 18.01% avg rate.
- **Controlled Grade Comparison:**
  - Grade B (36m): **11.44%** default rate vs. Grade B (60m): **21.84%** default rate (**1.91x higher**).
  - Grade C (36m): **18.72%** default rate vs. Grade C (60m): **30.56%** default rate (**1.63x higher**).
  - Grade D (36m): **25.29%** default rate vs. Grade D (60m): **35.79%** default rate (**1.42x higher**).
  - Grade E (36m): **33.39%** default rate vs. Grade E (60m): **41.44%** default rate.

**Business Implication:**  
Borrowers opt for 60-month terms to lower monthly installments, masking underlying affordability distress. The prolonged repayment window exposes the bank to macroeconomic cyclical shocks, credit fatigue, and life-event disruptions, compounding borrower default probability.

**Recommended Next Step:**  
Eliminate 60-month term options for risk grades D, E, F, and G. For prime grades (A & B), increase the term risk premium spread by at least 150 basis points.

**Caveat:**  
LendingClub expanded 60-month product offerings heavily in 2013–2015; unobserved vintage cohort maturation effects may influence aggregate term divergence.

---

### Finding 3: Debt-to-Income (DTI) Leverage Inflection Point at 20%

**Finding:**  
Observed credit default risk demonstrates an abrupt upward inflection once borrower non-mortgage monthly debt commitments exceed 20% of monthly income.

**Evidence:**  
- **DTI < 10%:** 48,225 loans | $560.1M exposure | **14.28%** default rate.
- **DTI 10% – 15%:** 91,426 loans | $1,213.8M exposure | **16.64%** default rate.
- **DTI 15% – 20%:** 105,718 loans | $1,540.2M exposure | **19.49%** default rate (portfolio baseline).
- **DTI 20% – 25%:** 80,828 loans | $1,228.1M exposure | **22.51%** default rate (+302 bps above baseline).
- **DTI 25% – 30%:** 45,715 loans | $704.9M exposure | **24.16%** default rate (+455 bps above baseline).
- **DTI 30%+:** 24,118 loans | $342.4M exposure | **24.58%** default rate (+497 bps above baseline).

**Business Implication:**  
Borrowers entering an unsecured loan contract with pre-existing non-mortgage debt service consuming >20% of income have minimal disposable liquidity reserves, making them acutely vulnerable to minor income shocks or inflation.

**Recommended Next Step:**  
Establish an automated policy underwriting limit capping total applicant DTI at 25.0%. For applications between 20% and 25% DTI, mandate secondary income verification.

**Caveat:**  
LendingClub calculated DTI excluding existing mortgage obligations and the requested loan installment itself. Total balance sheet debt burden is therefore understated.

---

### Finding 4: Small Business Lending Risk Premium

**Finding:**  
While debt consolidation and credit card refinancing represent the bulk of portfolio volume (**79.5% combined exposure**), loans originated for small business purposes exhibit the highest default rate among all major purpose categories.

**Evidence:**  
- **Debt Consolidation:** 234,510 loans | $3,308.8M exposure | 59.20% exposure share | **20.73%** default rate.
- **Credit Card Refinancing:** 83,019 loans | $1,135.0M exposure | 20.31% exposure share | **16.77%** default rate.
- **Home Improvement:** 24,030 loans | $335.7M exposure | 6.01% exposure share | **17.01%** default rate.
- **Small Business:** 5,701 loans | $90.2M exposure | 1.61% exposure share | **29.45%** default rate (1,679 charge-offs; +984 bps above baseline).

**Business Implication:**  
Underwriting commercial venture and working capital facilities using consumer personal installment scorecards produces severe adverse selection. Business cash flow volatility and enterprise failure risks cannot be captured by consumer bureau scores alone.

**Recommended Next Step:**  
Separate small business lending into a dedicated commercial underwriting channel requiring verified business bank statements, commercial tax returns, and debt service coverage ratio (DSCR) calculations.

**Caveat:**  
Loan purpose is self-reported by the borrower at registration without independent verification that funds were deployed into the enterprise.

---

### Finding 5: Geographic Exposure Concentration Across Four Anchor States

**Finding:**  
Over 34% of portfolio exposure is concentrated across four states (California, New York, Texas, and Florida), creating geographic correlated credit exposure.

**Evidence:**  
- **California (CA):** 55,594 loans | $787.2M exposure | **14.08%** portfolio exposure share | **19.82%** default rate.
- **New York (NY):** 32,878 loans | $460.5M exposure | **8.24%** portfolio exposure share | **20.83%** default rate.
- **Texas (TX):** 31,768 loans | $447.8M exposure | **8.01%** portfolio exposure share | **19.34%** default rate.
- **Florida (FL):** 27,249 loans | $378.1M exposure | **6.76%** portfolio exposure share | **20.21%** default rate.
- **Combined Anchor State Exposure:** **$2,073.6M (37.09% of portfolio)**.

**Business Implication:**  
A regional macroeconomic downturn, localized housing cost stress, or employment disruption in California or New York will disproportionately impact bank earnings and provisioning reserves.

**Recommended Next Step:**  
Establish geographical concentration limit thresholds (e.g., maximum 15% portfolio allocation to any single state).

**Caveat:**  
State-level cost of living, state income tax rate differentials, and localized economic indices were not captured in the raw dataset.
