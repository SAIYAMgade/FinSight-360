"""Unit tests for the Data Quality Framework validator."""
import pytest
import pandas as pd
from src.validate import DataQualityValidator


@pytest.fixture
def clean_valid_df():
    """Construct completely valid test dataset."""
    return pd.DataFrame({
        "loan_id": ["LN-1", "LN-2", "LN-3"],
        "loan_amnt": [10000.0, 15000.0, 5000.0],
        "term": ["36 months", "60 months", "36 months"],
        "int_rate": [10.5, 14.2, 7.8],
        "grade": ["B", "C", "A"],
        "annual_inc": [75000.0, 60000.0, 95000.0],
        "issue_d": ["Jan-2015", "Mar-2014", "Jul-2016"],
        "issue_date": pd.to_datetime(["2015-01-01", "2014-03-01", "2016-07-01"]),
        "loan_status": ["Fully Paid", "Charged Off", "Fully Paid"],
        "is_default": [0, 1, 0],
        "dti": [15.2, 22.1, 9.4],
        "credit_history_years": [12.5, 8.2, 16.0]
    })


def test_data_quality_validator_all_pass(clean_valid_df):
    """Test that clean data produces 100% pass across all rules."""
    validator = DataQualityValidator()
    results = validator.run_all_checks(clean_valid_df, initial_raw_count=3)

    assert len(results) == 12
    # Verify no critical failure
    failures = results[results["result"] == "FAIL"]
    assert len(failures) == 0


def test_data_quality_detects_duplicate_loan_id(clean_valid_df):
    """Test detection of duplicate loan IDs."""
    invalid_df = clean_valid_df.copy()
    invalid_df.loc[1, "loan_id"] = "LN-1"  # Duplicate ID

    validator = DataQualityValidator()
    results = validator.run_all_checks(invalid_df)

    dup_check = results[results["check_name"] == "DQ-002_UNIQUE_LOAN_IDENTIFIER"].iloc[0]
    assert dup_check["failures_found"] == 1
    assert dup_check["result"] == "FAIL"


def test_data_quality_detects_invalid_loan_amount(clean_valid_df):
    """Test detection of negative or out-of-range loan amounts."""
    invalid_df = clean_valid_df.copy()
    invalid_df.loc[0, "loan_amnt"] = -500.0  # Negative loan amount

    validator = DataQualityValidator()
    results = validator.run_all_checks(invalid_df)

    loan_check = results[results["check_name"] == "DQ-004_LOAN_AMOUNT_RANGE"].iloc[0]
    assert loan_check["failures_found"] == 1
    assert loan_check["result"] == "FAIL"


def test_data_quality_detects_non_positive_income(clean_valid_df):
    """Test detection of non-positive borrower annual income."""
    invalid_df = clean_valid_df.copy()
    invalid_df.loc[2, "annual_inc"] = 0.0  # Zero income

    validator = DataQualityValidator()
    results = validator.run_all_checks(invalid_df)

    inc_check = results[results["check_name"] == "DQ-007_POSITIVE_ANNUAL_INCOME"].iloc[0]
    assert inc_check["failures_found"] == 1
    assert inc_check["result"] == "FAIL"
