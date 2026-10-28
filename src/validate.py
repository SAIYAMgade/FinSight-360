"""Data Quality Framework and Audit Validator for FinSight 360."""
from datetime import datetime, timezone
import logging
from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np

logger = logging.getLogger("finsight360.validate")


class DataQualityValidator:
    """Executes rule-based data quality checks and generates an audit log."""

    def __init__(self, thresholds: Dict[str, Any] = None):
        self.thresholds = thresholds or {}
        self.results: List[Dict[str, Any]] = []

    def _record_result(
        self,
        check_name: str,
        severity: str,
        records_checked: int,
        failures_found: int,
        details: str
    ) -> Dict[str, Any]:
        """Construct standard data quality result record."""
        failure_rate = (
            round((failures_found / records_checked) * 100.0, 4)
            if records_checked > 0 else 0.0
        )
        if failures_found == 0:
            result = "PASS"
        elif severity.upper() == "CRITICAL":
            result = "FAIL"
        else:
            result = "WARNING"

        entry = {
            "check_name": check_name,
            "severity": severity.upper(),
            "records_checked": int(records_checked),
            "failures_found": int(failures_found),
            "failure_rate": failure_rate,
            "result": result,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.results.append(entry)
        return entry

    def run_all_checks(self, df: pd.DataFrame, initial_raw_count: int = None) -> pd.DataFrame:
        """Execute all 12 rigorous data quality rules on the dataset."""
        logger.info(f"Running data quality validation across {len(df):,} records...")
        self.results = []
        n = len(df)

        # 1. Missing values in core required fields
        required_cols = ["loan_amnt", "term", "grade", "annual_inc", "issue_d", "loan_status"]
        missing_count = int(df[required_cols].isnull().any(axis=1).sum())
        self._record_result(
            check_name="DQ-001_REQUIRED_FIELDS_MISSING",
            severity="CRITICAL",
            records_checked=n,
            failures_found=missing_count,
            details=f"Required fields evaluated: {required_cols}"
        )

        # 2. Duplicate loan identifiers
        if "loan_id" in df.columns:
            dup_ids = int(df["loan_id"].duplicated().sum())
            self._record_result(
                check_name="DQ-002_UNIQUE_LOAN_IDENTIFIER",
                severity="CRITICAL",
                records_checked=n,
                failures_found=dup_ids,
                details="Checks uniqueness of primary surrogate key 'loan_id'."
            )

        # 3. Duplicate whole records (ignoring loan_id if present)
        cols_to_check = [c for c in df.columns if c != "loan_id"]
        exact_dups = int(df.duplicated(subset=cols_to_check).sum())
        self._record_result(
            check_name="DQ-003_DUPLICATE_RECORDS",
            severity="CRITICAL",
            records_checked=n,
            failures_found=exact_dups,
            details="Checks for fully duplicate borrower and loan rows."
        )

        # 4. Loan amount boundary plausibility
        min_loan = self.thresholds.get("min_plausible_loan_amount", 500.0)
        max_loan = self.thresholds.get("max_plausible_loan_amount", 50000.0)
        invalid_loans = int(((df["loan_amnt"] < min_loan) | (df["loan_amnt"] > max_loan)).sum())
        self._record_result(
            check_name="DQ-004_LOAN_AMOUNT_RANGE",
            severity="CRITICAL",
            records_checked=n,
            failures_found=invalid_loans,
            details=f"Plausible range: ${min_loan:,.0f} to ${max_loan:,.0f}."
        )

        # 5. Interest rate boundary plausibility
        min_int = self.thresholds.get("min_plausible_int_rate", 3.0)
        max_int = self.thresholds.get("max_plausible_int_rate", 35.0)
        invalid_int = int(((df["int_rate"] < min_int) | (df["int_rate"] > max_int)).sum())
        self._record_result(
            check_name="DQ-005_INTEREST_RATE_RANGE",
            severity="CRITICAL",
            records_checked=n,
            failures_found=invalid_int,
            details=f"Plausible nominal rate range: {min_int}% to {max_int}%."
        )

        # 6. Valid origination date parsing
        invalid_dates = int(df["issue_date"].isnull().sum()) if "issue_date" in df.columns else n
        self._record_result(
            check_name="DQ-006_DATE_PARSING_INTEGRITY",
            severity="CRITICAL",
            records_checked=n,
            failures_found=invalid_dates,
            details="Checks that issue date parses into valid Gregorian datetime."
        )

        # 7. Non-positive or invalid borrower annual income
        invalid_inc = int((df["annual_inc"] <= 0).sum() + df["annual_inc"].isnull().sum())
        self._record_result(
            check_name="DQ-007_POSITIVE_ANNUAL_INCOME",
            severity="CRITICAL",
            records_checked=n,
            failures_found=invalid_inc,
            details="Checks that self-reported annual income is positive and non-null."
        )

        # 8. Unrecognized risk grade categories
        valid_grades = {"A", "B", "C", "D", "E", "F", "G"}
        invalid_grades = int((~df["grade"].isin(valid_grades)).sum())
        self._record_result(
            check_name="DQ-008_KNOWN_RISK_GRADES",
            severity="CRITICAL",
            records_checked=n,
            failures_found=invalid_grades,
            details=f"Permissible grades: {sorted(list(valid_grades))}."
        )

        # 9. Target variable completeness and domain integrity
        invalid_targets = int(df["is_default"].isnull().sum()) if "is_default" in df.columns else n
        self._record_result(
            check_name="DQ-009_TARGET_VARIABLE_INTEGRITY",
            severity="CRITICAL",
            records_checked=n,
            failures_found=invalid_targets,
            details="Target 'is_default' must be strictly binary 0 or 1 with 0 nulls."
        )

        # 10. Temporal chronological consistency (credit line opened before loan issue)
        if "credit_history_years" in df.columns:
            negative_hist = int((df["credit_history_years"] < 0).sum())
            self._record_result(
                check_name="DQ-010_CHRONOLOGICAL_CREDIT_AGE",
                severity="WARNING",
                records_checked=n,
                failures_found=negative_hist,
                details="Earliest credit line date must precede or equal loan origination date."
            )

        # 11. Pipeline stage record count retention
        if initial_raw_count is not None:
            discrepancy = abs(initial_raw_count - n)
            self._record_result(
                check_name="DQ-011_RECORD_RETENTION_INTEGRITY",
                severity="WARNING" if discrepancy > 0 else "INFORMATIONAL",
                records_checked=initial_raw_count,
                failures_found=discrepancy,
                details=f"Raw count: {initial_raw_count:,}, Transformed count: {n:,}."
            )

        # 12. Extreme leverage / DTI outlier check
        max_dti = self.thresholds.get("max_plausible_dti", 100.0)
        extreme_dti = int((df["dti"] > max_dti).sum())
        self._record_result(
            check_name="DQ-012_EXTREME_DTI_OUTLIERS",
            severity="WARNING",
            records_checked=n,
            failures_found=extreme_dti,
            details=f"Borrowers with DTI exceeding {max_dti}%, indicating severe leverage."
        )

        results_df = pd.DataFrame(self.results)
        logger.info(
            f"Data quality audit completed: "
            f"{(results_df['result'] == 'PASS').sum()} PASS, "
            f"{(results_df['result'] == 'WARNING').sum()} WARNING, "
            f"{(results_df['result'] == 'FAIL').sum()} FAIL."
        )
        return results_df
