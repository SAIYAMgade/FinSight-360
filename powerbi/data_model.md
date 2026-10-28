# FinSight 360: Power BI Star Schema Data Model Specification

## 1. Dimensional Architecture
The data model is engineered strictly as an **analytical star schema** to optimize DAX query performance, prevent circular filter paths, and eliminate many-to-many relationship ambiguity.

```
       +--------------------+
       |      dim_date      |
       +--------------------+
       | PK: date_key       |
       |     full_date      |
       |     year_num       |
       |     year_month     |
       +---------+----------+
                 | 1
                 |
                 | * (issue_year_month -> year_month)
+----------------+---+      * +---------------------+
|     dim_risk_grade |<-------+      fact_loans     |
+--------------------+ 1      +---------------------+
| PK: grade          |        | PK: loan_id         |
|     risk_tier      |        | FK: grade           |
|     prime_status   |        | FK: purpose         |
+--------------------+        | FK: issue_date      |
                              |     loan_amnt       |
+--------------------+ 1      |     int_rate        |
|  dim_loan_purpose  |<-------+     installment     |
+--------------------+ *      |     annual_inc      |
| PK: purpose        |        |     dti             |
|     purpose_group  |        |     is_default      |
+--------------------+        +----------+----------+
                                         |
                                         | (Independent audit table)
                              +----------+----------+
                              |     dq_audit_log    |
                              +---------------------+
                              | PK: check_name      |
                              |     severity        |
                              |     failure_rate    |
                              |     result          |
                              +---------------------+
```

---

## 2. Table Schemas & Cardinality Specifications

### Table 1: `fact_loans` (Central Fact Table)
- **Role**: Grain is one individual consumer loan facility.
- **Record Count**: 396,030 rows.
- **Key Fields**:
  - `loan_id` (Text, Primary Key): Format `LN-1000001`
  - `loan_amnt` (Currency): Funded loan principal
  - `int_rate` (Percentage): Nominal annual interest rate
  - `installment` (Currency): Monthly payment obligation
  - `annual_inc` (Currency): Self-reported annual borrower income
  - `dti` (Decimal): Debt-to-Income leverage ratio
  - `is_default` (Integer): Terminal outcome flag (`1` = Charged Off, `0` = Fully Paid)
  - `term` (Text): `36 months` or `60 months`
  - `grade` (Text, Foreign Key -> `dim_risk_grade.grade`)
  - `purpose` (Text, Foreign Key -> `dim_loan_purpose.purpose`)
  - `issue_year_month` (Text, Foreign Key -> `dim_date.year_month`)
  - `addr_state` (Text): 2-letter state code

### Table 2: `dim_risk_grade` (Underwriting Dimension)
- **Role**: Underwriting risk category lookup.
- **Record Count**: 7 rows (`A` to `G`).
- **Key Fields**:
  - `grade` (Text, Primary Key)
  - `risk_tier` (Text): Institutional tier name (`Prime Low Risk`, `Near Prime`, `Subprime`, etc.)
  - `prime_status` (Text): High-level split (`Prime` vs `Non-Prime` vs `Subprime`)
  - `expected_loss_range` (Text): Historical benchmark loss range

### Table 3: `dim_loan_purpose` (Purpose Dimension)
- **Role**: Business purpose grouping lookup.
- **Record Count**: 14 rows.
- **Key Fields**:
  - `purpose` (Text, Primary Key)
  - `purpose_group` (Text): Higher-level categorization (`Debt Refinancing`, `Home & Property`, `Commercial`, etc.)
  - `is_refinancing` (Integer): Binary indicator for refinancing facilities

### Table 4: `dim_date` (Calendar Dimension)
- **Role**: Conformed date dimension for time-series and vintage intelligence.
- **Record Count**: 132 rows (covering all months from Jan 2007 to Dec 2017).
- **Key Fields**:
  - `date_key` (Text, Primary Key): Format `YYYYMM`
  - `year_month` (Text, Unique): Format `YYYY-MM`
  - `year_num` (Integer): `2007` to `2017`
  - `quarter_num` (Integer): `1` to `4`
  - `month_num` (Integer): `1` to `12`
  - `month_name` (Text): `January`, `February`, etc.

### Table 5: `dq_audit_log` (Quality Dimension)
- **Role**: Standalone logging table capturing automated test results from `src/validate.py`.
- **Record Count**: 12 rows (one for each rule).

---

## 3. Relationships & Filter Flow Rules
1. `dim_risk_grade[grade]` (1) $\longrightarrow$ (Many) `fact_loans[grade]`
   - **Cross Filter Direction**: Single (Dimension filters Fact)
   - **Enforce Referential Integrity**: Yes
2. `dim_loan_purpose[purpose]` (1) $\longrightarrow$ (Many) `fact_loans[purpose]`
   - **Cross Filter Direction**: Single (Dimension filters Fact)
3. `dim_date[year_month]` (1) $\longrightarrow$ (Many) `fact_loans[issue_year_month]`
   - **Cross Filter Direction**: Single (Dimension filters Fact)

**Integrity Verification**: No bidirectional relationships exist in this data model. This completely eliminates ambiguous filter paths and prevents Cartesian product inflation.
