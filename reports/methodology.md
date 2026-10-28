# FinSight 360: Analytical Methodology & Technical Architecture

## 1. Analytics Framework: Descriptive, Diagnostic, and Predictive Analytics

FinSight 360 distinguishes between three levels of analytical maturity, avoiding common pitfalls such as confusing statistical correlation with causation or claiming predictive certainty:

```
+---------------------------------------------------------------------------------------+
| 1. DESCRIPTIVE ANALYTICS: "What happened across the portfolio?"                      |
|    - Aggregations, distributions, volume tracking, and baseline default rates.        |
|    - Output: Executive KPI cards, origination trends, loan status donut charts.       |
+---------------------------------------------------------------------------------------+
| 2. DIAGNOSTIC ANALYTICS: "Why did specific segments experience elevated losses?"      |
|    - Bivariate comparisons, cross-tabulations, Chi-Square tests, Mann-Whitney U tests.|
|    - Output: Risk grade matrix, DTI leverage inflection, 60m term risk multiplier.    |
+---------------------------------------------------------------------------------------+
| 3. PREDICTIVE BASELINE: "How well can origination attributes discriminate risk?"      |
|    - Leakage-free baseline logistic regression scorecard evaluated on held-out test.  |
|    - Output: ROC-AUC (0.69), standardized feature coefficients, probability ranking.  |
+---------------------------------------------------------------------------------------+
```

---

## 2. Business Question Framework
The platform is organized around 25 core analytical business questions categorized across four domains:

### Category A: Executive Portfolio Performance
- What is the total portfolio volume, funded principal exposure, and average facility ticket size?
- What proportion of originated loans completed successfully vs. resulted in write-off?
- What is the baseline observed default rate across the total portfolio?
- How has origination volume evolved across funding vintages?

### Category B: Credit Risk Segmentation
- How do default rates escalate across internal underwriting risk grades (A to G)?
- How does term duration (36 vs 60 months) impact default probability across identical credit tiers?
- At what debt-to-income (DTI) leverage threshold does borrower risk experience a steep inflection?
- Which borrower-stated loan purposes represent the highest capital risk?

### Category C: Portfolio Concentration & Vintage Performance
- What proportion of exposure is concentrated in the top geographic states?
- How did origination vintages mature and track macroeconomic credit cycles (2007–2016)?
- Which purpose and grade combinations maintain sufficient statistical sample size ($N \ge 500$) to justify underwriting restrictions?

### Category D: Data Quality & Governance Integrity
- Does the source data contain missing required fields, duplicates, or negative balances?
- Are borrower incomes, interest rates, and loan amounts within plausible banking boundaries?
- Do analytical results reconcile across Python, SQL, Power BI, and Excel layers?

---

## 3. Statistical Testing Methodology & Effect Sizes

To determine whether observed differences in credit performance across borrower segments are statistically reliable or merely random sampling noise, rigorous inferential statistical tests were executed:

### Test 1: Chi-Square Test of Independence ($\chi^2$)
- **Purpose**: Test whether categorical segmentation (e.g., Risk Grade, Term Structure, Verification Status) is statistically dependent with loan outcome (`Fully Paid` vs `Charged Off`).
- **Formulation**:
  $$\chi^2 = \sum \frac{(O - E)^2}{E}$$
- **Effect Size Metric**: **Cramer's V**:
  $$V = \sqrt{\frac{\chi^2}{N \cdot (\min(r, c) - 1)}}$$
- **Result for Grade vs Outcome**: $\chi^2 = 33,548.81$, $p < 10^{-300}$, Cramer's $V = 0.291$ (moderate-to-strong practical association).

### Test 2: Two-Sample Non-Parametric Mann-Whitney U Test
- **Purpose**: Compare continuous financial distributions (interest rate, DTI leverage, annual income) between Fully Paid and Charged Off loans without assuming Gaussian normality.
- **Formulation**: Tests the null hypothesis that a randomly selected borrower from the defaulted cohort has an equal probability of having a higher value than a borrower from the fully paid cohort.
- **Effect Size Metric**: **Cohen's d**:
  $$d = \frac{\bar{X}_1 - \bar{X}_2}{s_{\text{pooled}}}$$
- **Result for Interest Rate**: Defaulted cohort mean = **15.71%** vs Fully Paid = **13.14%** (+2.57% spread; $p < 10^{-300}$; Cohen's $d = 0.584$, representing a substantial medium effect size).

### Test 3: Binomial Proportion Confidence Intervals (Wilson Score Interval)
- **Purpose**: Compute exact 95% confidence intervals for default rates across risk grades and segments, ensuring small-sample subgrades (e.g., G5) are not misinterpreted.
- **Formulation**:
  $$CI = \frac{p + \frac{z^2}{2n} \pm z\sqrt{\frac{p(1-p)}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

---

## 4. Target Leakage Prevention in Predictive Modeling
In banking analytics, a common error is including post-origination fields as predictors (e.g., `total_rec_prncp`, `last_pymnt_d`, `collection_recovery_fee`, `recoveries`). Doing so creates artificial 99% accuracy because these fields are only populated *after* default has occurred.

FinSight 360 strictly enforces **temporal point-in-time underwriting integrity**:
- **Permissible Predictors**: Strictly fields observable at loan application: `loan_amnt`, `int_rate`, `installment`, `annual_inc`, `dti`, `emp_length_years`, `credit_history_years`.
- **Excluded Variables**: All post-origination transaction flows, late fee receipts, and recovery records.
- **Model Baseline Performance**: An honest, leakage-free logistic regression baseline yields **ROC-AUC = 0.692**, consistent with real-world unsecured consumer lending scorecards prior to incorporating comprehensive bureau tradeline attributes.
