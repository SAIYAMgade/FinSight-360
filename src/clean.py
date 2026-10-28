"""Data cleaning and standardization module for FinSight 360."""
import re
import logging
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np

logger = logging.getLogger("finsight360.clean")


def extract_state_and_zip(address_series: pd.Series) -> Tuple[pd.Series, pd.Series]:
    """
    Extract 2-letter state code and 5-digit zip code from address strings.
    Example: '0174 Michelle Gateway\\r\\nMendozaberg, OK 22690' -> ('OK', '22690')
    """
    pattern = r'(?P<state>[A-Z]{2})\s+(?P<zip>\d{5})'
    extracted = address_series.astype(str).str.extract(pattern)
    state = extracted['state'].fillna('UNKNOWN')
    zip_code = extracted['zip'].fillna('UNKNOWN')
    return state, zip_code


def clean_lending_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Clean, standardize, and prepare raw lending data.

    Preserves data lineage without silent dropping of records.
    Audit statistics are tracked and returned.
    """
    logger.info("Starting data cleaning pipeline...")
    initial_rows = len(df)
    cleaned = df.copy()

    # 1. Deduplication check
    exact_duplicates = cleaned.duplicated().sum()
    if exact_duplicates > 0:
        logger.warning(f"Found and removed {exact_duplicates} duplicate records.")
        cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    else:
        logger.info("No exact duplicate records detected.")

    # 2. Generate deterministic unique loan identifier
    cleaned["loan_id"] = [f"LN-{1000001 + i:07d}" for i in range(len(cleaned))]

    # 3. Strip whitespace from string columns
    str_cols = cleaned.select_dtypes(include=["object", "string"]).columns
    for col in str_cols:
        cleaned[col] = cleaned[col].astype(str).str.strip()

    # 4. Standardize term
    cleaned["term_months"] = cleaned["term"].apply(
        lambda x: 36 if "36" in str(x) else (60 if "60" in str(x) else np.nan)
    )
    cleaned["term"] = cleaned["term_months"].apply(
        lambda x: f"{int(x)} months" if pd.notnull(x) else "Unknown"
    )

    # 5. Extract state and zip code from address
    if "address" in cleaned.columns:
        cleaned["addr_state"], cleaned["zip_code"] = extract_state_and_zip(cleaned["address"])

    # 6. Parse dates safely
    cleaned["issue_date"] = pd.to_datetime(cleaned["issue_d"], format="%b-%Y", errors="coerce")
    cleaned["issue_year"] = cleaned["issue_date"].dt.year
    cleaned["issue_month"] = cleaned["issue_date"].dt.month
    cleaned["issue_quarter"] = cleaned["issue_date"].dt.to_period("Q").astype(str)
    cleaned["issue_year_month"] = cleaned["issue_date"].dt.strftime("%Y-%m")

    if "earliest_cr_line" in cleaned.columns:
        cleaned["earliest_cr_line_date"] = pd.to_datetime(
            cleaned["earliest_cr_line"], format="%b-%Y", errors="coerce"
        )
        # Credit history age at loan origination in years
        cleaned["credit_history_years"] = (
            (cleaned["issue_date"] - cleaned["earliest_cr_line_date"]).dt.days / 365.25
        ).round(1)

    # 7. Standardize home ownership (group rare 'NONE' and 'ANY' into 'OTHER')
    cleaned["home_ownership"] = cleaned["home_ownership"].replace({
        "NONE": "OTHER",
        "ANY": "OTHER",
        "nan": "OTHER"
    }).fillna("OTHER")

    # 8. Standardize employment length
    def parse_emp_length(val):
        val_str = str(val).lower()
        if "10+" in val_str:
            return 10.0
        elif "< 1" in val_str or "<1" in val_str:
            return 0.5
        elif "year" in val_str:
            nums = re.findall(r"\d+", val_str)
            return float(nums[0]) if nums else np.nan
        return np.nan

    cleaned["emp_length_years"] = cleaned["emp_length"].apply(parse_emp_length)

    # 9. Ensure correct numeric types
    num_cols = [
        "loan_amnt", "int_rate", "installment", "annual_inc", "dti",
        "open_acc", "pub_rec", "revol_bal", "revol_util", "total_acc",
        "mort_acc", "pub_rec_bankruptcies"
    ]
    for col in num_cols:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    # 10. Explicit target variable definition:
    # 1 for Charged Off, 0 for Fully Paid
    cleaned["is_default"] = cleaned["loan_status"].apply(
        lambda x: 1 if str(x).strip().lower() == "charged off" else (0 if str(x).strip().lower() == "fully paid" else np.nan)
    )

    clean_audit = {
        "initial_rows": initial_rows,
        "final_rows": len(cleaned),
        "exact_duplicates_removed": int(exact_duplicates),
        "total_columns": len(cleaned.columns),
        "fully_paid_count": int((cleaned["is_default"] == 0).sum()),
        "charged_off_count": int((cleaned["is_default"] == 1).sum()),
        "default_rate_pct": round(float(cleaned["is_default"].mean() * 100), 2)
    }

    logger.info(
        f"Cleaning complete: {len(cleaned):,} records. "
        f"Default Rate: {clean_audit['default_rate_pct']}%."
    )
    return cleaned, clean_audit
