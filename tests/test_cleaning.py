"""Unit tests for data cleaning and transformation module."""
import pytest
import pandas as pd
import numpy as np
from src.clean import clean_lending_data, extract_state_and_zip
from src.transform import add_analytical_features


@pytest.fixture
def sample_raw_df():
    """Construct minimal synthetic raw lending dataframe for unit testing."""
    return pd.DataFrame({
        "loan_amnt": [10000.0, 15000.0, 5000.0],
        "term": [" 36 months", " 60 months", " 36 months"],
        "int_rate": [11.44, 18.25, 7.89],
        "installment": [329.48, 382.95, 156.42],
        "grade": ["B", "D", "A"],
        "sub_grade": ["B4", "D2", "A1"],
        "emp_title": ["Marketing", "Nurse", "Engineer"],
        "emp_length": ["10+ years", "2 years", "< 1 year"],
        "home_ownership": ["RENT", "MORTGAGE", "OWN"],
        "annual_inc": [75000.0, 60000.0, 95000.0],
        "verification_status": ["Not Verified", "Source Verified", "Verified"],
        "issue_d": ["Jan-2015", "Mar-2014", "Jul-2016"],
        "loan_status": ["Fully Paid", "Charged Off", "Fully Paid"],
        "purpose": ["debt_consolidation", "credit_card", "home_improvement"],
        "title": ["Debt consolidation", "Credit card refinancing", "Home improvement"],
        "dti": [18.5, 24.2, 8.1],
        "earliest_cr_line": ["Jun-2000", "May-2005", "Nov-1998"],
        "open_acc": [10.0, 14.0, 8.0],
        "pub_rec": [0.0, 1.0, 0.0],
        "revol_bal": [12000.0, 25000.0, 4500.0],
        "revol_util": [45.2, 78.5, 22.1],
        "total_acc": [20.0, 28.0, 15.0],
        "initial_list_status": ["w", "f", "w"],
        "application_type": ["INDIVIDUAL", "INDIVIDUAL", "INDIVIDUAL"],
        "mort_acc": [2.0, 0.0, 1.0],
        "pub_rec_bankruptcies": [0.0, 0.0, 0.0],
        "address": [
            "0174 Michelle Gateway\r\nMendozaberg, OK 22690",
            "1076 Carney Fort Apt. 347\r\nLoganmouth, SD 05113",
            "87025 Mark Dale Apt. 269\r\nNew Sabrina, WV 05113"
        ]
    })


def test_clean_lending_data_basic(sample_raw_df):
    """Test basic cleaning transformations and target variable creation."""
    cleaned, audit = clean_lending_data(sample_raw_df)

    assert len(cleaned) == 3
    assert audit["fully_paid_count"] == 2
    assert audit["charged_off_count"] == 1
    assert "loan_id" in cleaned.columns
    assert cleaned["loan_id"].iloc[0] == "LN-1000001"
    assert cleaned["is_default"].tolist() == [0, 1, 0]
    assert cleaned["term_months"].tolist() == [36, 60, 36]
    assert cleaned["addr_state"].tolist() == ["OK", "SD", "WV"]
    assert cleaned["zip_code"].tolist() == ["22690", "05113", "05113"]


def test_extract_state_and_zip():
    """Test regex state and postal code extraction."""
    addresses = pd.Series([
        "123 Main St, Austin, TX 78701",
        "456 Elm Ave\r\nSeattle, WA 98101",
        "Invalid Address String Without State"
    ])
    states, zips = extract_state_and_zip(addresses)

    assert states.iloc[0] == "TX"
    assert zips.iloc[0] == "78701"
    assert states.iloc[1] == "WA"
    assert zips.iloc[1] == "98101"
    assert states.iloc[2] == "UNKNOWN"
    assert zips.iloc[2] == "UNKNOWN"


def test_add_analytical_features(sample_raw_df):
    """Test segmentation banding and analytical feature generation."""
    cleaned, _ = clean_lending_data(sample_raw_df)
    transformed = add_analytical_features(cleaned)

    assert "loan_amount_band" in transformed.columns
    assert "income_band" in transformed.columns
    assert "dti_band" in transformed.columns
    assert "int_rate_band" in transformed.columns
    assert "installment_burden_pct" in transformed.columns

    # Test installment burden calculation
    # Row 0: installment 329.48, income 75000 -> (329.48 * 12 / 75000) * 100 = 5.27%
    expected_burden = round((329.48 * 12 / 75000) * 100, 2)
    assert transformed["installment_burden_pct"].iloc[0] == expected_burden
