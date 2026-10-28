# FinSight 360: Dataset Documentation & Selection Note

## 1. Dataset Selection Rationale
To build an authentic, credible, and audit-grade banking analytics platform, **FinSight 360** utilizes the canonical **LendingClub Historical Loan Dataset** (2007–2016). 

This dataset was selected because it fulfills all essential criteria for consumer credit risk and portfolio performance analytics:
- **Comprehensive Volume**: 396,030 completed consumer loan records.
- **Unambiguous Closed Loan Outcomes**: Contains exclusively closed loans (`Fully Paid` vs. `Charged Off`), eliminating survival censoring bias and ambiguous in-flight statuses.
- **Rich Financial & Underwriting Attributes**: Features loan amount, funded amount, nominal interest rate, monthly installment, debt-to-income (DTI) ratio, borrower annual income, credit revolving utilization, and credit bureau derogatory items.
- **Credit Risk Segmentation**: Includes standardized risk grades (`A` through `G`) and granular subgrades (`A1` to `G5`), employment tenure, home ownership type, and loan purpose.
- **Temporal Depth**: Covers 115 distinct origination months from June 2007 to December 2016, enabling authentic vintage cohort analysis, macroeconomic cycle tracking (including the 2008 financial crisis recovery), and origination trend reporting.
- **Geographic Representation**: Incorporates borrower geographic data (state abbreviations and zip prefixes), enabling regional exposure analysis.

## 2. Dataset Origin & Authenticity
- **Origin**: Public historical loan performance data released by LendingClub Corporation under Open Data terms, maintained and mirrored on Hugging Face (`ghty123/lending_club_loan_dataset`, file `lending_club_loan_two.csv`) and GitHub (`sftyo/LendingClub-Dataset`).
- **Nature of Data**: Real-world historical consumer peer-to-peer lending originations. No synthetic rows were manufactured for the primary analysis.
- **Observation Unit**: Each row represents a single funded consumer installment loan application with its associated borrower credit profile at origination and terminal repayment outcome.

## 3. Data Dictionary: Core Schema

| Column Name | Data Type | Description | Analytical Role |
| :--- | :--- | :--- | :--- |
| `loan_amnt` | Float | The listed original principal amount of the loan applied for and funded ($). | Portfolio Exposure / Sizing |
| `term` | String | Duration of the loan (36 months or 60 months). | Term Structure Segment |
| `int_rate` | Float | Annualized nominal interest rate on the loan (%). | Pricing / Yield Analysis |
| `installment` | Float | Monthly payment obligation owed by the borrower ($). | Payment Burden |
| `grade` | String | LendingClub assigned risk grade (`A` = lowest risk to `G` = highest risk). | Underwriting Segment |
| `sub_grade` | String | Granular subgrade (`A1` to `G5`). | Deep Risk Stratification |
| `emp_title` | String | Self-reported job title of the borrower at application. | Occupational Profiling |
| `emp_length` | String | Employment tenure in years (`< 1 year` to `10+ years`). | Employment Stability |
| `home_ownership` | String | Residential status (`RENT`, `MORTGAGE`, `OWN`, `OTHER`, `NONE`, `ANY`). | Collateral / Stability Proxy |
| `annual_inc` | Float | Self-reported annual income of the borrower ($). | Capacity to Pay |
| `verification_status`| String | Income verification status (`Verified`, `Source Verified`, `Not Verified`). | Information Asymmetry |
| `issue_d` | String | Month and year in which the loan was originated and funded (e.g., `Jan-2015`). | Time / Vintage Cohort |
| `loan_status` | String | Terminal repayment outcome (`Fully Paid` or `Charged Off`). | **Target Variable** |
| `purpose` | String | Borrower-provided intended use of funds (e.g., `debt_consolidation`, `credit_card`).| Loan Intent Segmentation |
| `title` | String | Specific loan listing title provided by borrower. | Unstructured Text Reference |
| `dti` | Float | Debt-to-Income ratio: total monthly debt payments / monthly income. | Financial Leverage |
| `earliest_cr_line` | String | Date earliest reported credit line was established in borrower's credit report. | Credit History Length |
| `open_acc` | Float | Number of open credit lines in borrower's credit bureau file. | Credit Depth |
| `pub_rec` | Float | Number of derogatory public records (civil judgments, tax liens). | Negative Credit Events |
| `revol_bal` | Float | Total credit revolving balance ($). | Revolving Debt Burden |
| `revol_util` | Float | Revolving line credit utilization rate (%). | Liquidity Stress Indicator |
| `total_acc` | Float | Total count of credit lines in borrower history. | Credit Experience |
| `initial_list_status`| String | Initial listing status on loan platform (`w` = whole, `f` = fractional). | Syndication Structure |
| `application_type` | String | Application type (`INDIVIDUAL` or `JOINT`). | Borrower Structure |
| `mort_acc` | Float | Number of mortgage accounts. | Property Asset Indicator |
| `pub_rec_bankruptcies`| Float | Number of public record bankruptcies. | Severe Distress History |
| `address` | String | Borrower address text containing city, state abbreviation, and 5-digit zip. | Geographic Dimension |

## 4. Target Variable Definition: Credit Default
In consumer lending analytics, ambiguous definitions of default distort portfolio health. For **FinSight 360**, the target variable is explicitly formulated:

$$\text{Observed Default Rate} = \frac{\text{Charged Off Loans}}{\text{Total Closed Loans}}$$

- **Target Binary Flag (`is_default`)**:
  - `0`: **Fully Paid** (borrower repaid full principal and accrued interest). Total = 318,357 loans (80.39%).
  - `1`: **Charged Off** (loan became severely delinquent, deemed uncollectible, and written off as a credit loss). Total = 77,673 loans (19.61%).
- **Benchmark Default Rate**: The aggregate portfolio observed default rate is **19.61%**.
- **Delinquency vs. Default Distinction**: Because this dataset contains strictly completed historical facilities, loans currently 30–120 days delinquent are not present; the portfolio reflects final credit outcomes.

## 5. Excluded, Unsuitable, and Leaky Columns
- `title`: Contains duplicate, unstructured text duplicating `purpose`. Retained in raw staging; excluded from analytical aggregations.
- `address`: Full street addresses contain noise and potential PII. Stripped down during transformation to standard 2-letter state codes (`state`) and 5-digit postal codes (`zip_code`).
- Target Leakage Prevention: Post-origination fields (such as recoveries, collection fees, total principal received, or last payment date) were explicitly omitted from predictive modeling inputs to prevent look-ahead bias.

## 6. Known Dataset Limitations
1. **Survivorship & Platform Specificity**: LendingClub operated as an online marketplace lender; its borrower demographic skewed toward credit card refinancing and debt consolidation (representing ~59% of exposure). Findings cannot be generalized to prime commercial bank mortgages or corporate credit.
2. **Self-Reported Income**: Borrower income is self-reported at application, with varying verification statuses (`Not Verified` accounts for ~31% of loans).
3. **Missing Value Profiles**: `mort_acc` has ~9.5% missingness, `emp_title` has ~5.8% missingness, and `emp_length` has ~4.6% missingness. These missing patterns are formally tracked in the Data Quality framework rather than imputed arbitrarily.

## 7. Sampling Strategy for Fast CI & Local Replication
- **Primary Analysis**: Runs across the entire population of **396,030** loans.
- **Representative Sample (`data/sample/loans_sample.csv`)**:
  - Sample Size: **25,000** records.
  - Methodology: Stratified random sampling on `loan_status` using fixed seed `42`.
  - Quality Guarantee: The sample preserves the exact 80.39% / 19.61% outcome ratio, identical average loan amounts ($14,113 vs $14,113.82), and identical interest rate distributions within 0.05% error bounds.
  - Purpose: Enables automated GitHub Actions CI and low-spec laptop replication in under 10 seconds.
