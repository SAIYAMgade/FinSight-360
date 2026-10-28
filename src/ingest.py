"""Data ingestion and schema verification module for FinSight 360."""
import logging
from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("finsight360.ingest")

EXPECTED_RAW_COLUMNS = [
    "loan_amnt", "term", "int_rate", "installment", "grade", "sub_grade",
    "emp_title", "emp_length", "home_ownership", "annual_inc",
    "verification_status", "issue_d", "loan_status", "purpose", "title",
    "dti", "earliest_cr_line", "open_acc", "pub_rec", "revol_bal",
    "revol_util", "total_acc", "initial_list_status", "application_type",
    "mort_acc", "pub_rec_bankruptcies", "address"
]


def ingest_raw_data(file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Ingest the raw lending dataset and perform baseline schema verification.

    Args:
        file_path: Path to the raw CSV file.

    Returns:
        Tuple containing loaded DataFrame and ingestion audit metadata.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found at: {file_path}")

    logger.info(f"Ingesting raw data from {file_path}...")
    df = pd.read_csv(file_path, low_memory=False)

    total_rows, total_cols = df.shape
    logger.info(f"Loaded {total_rows:,} records with {total_cols} columns.")

    if total_rows == 0:
        raise ValueError("Ingested dataset contains 0 records.")

    # Schema inspection
    present_cols = set(df.columns)
    missing_cols = [c for c in EXPECTED_RAW_COLUMNS if c not in present_cols]
    extra_cols = [c for c in df.columns if c not in EXPECTED_RAW_COLUMNS]

    if missing_cols:
        logger.warning(f"Missing expected columns ({len(missing_cols)}): {missing_cols}")
    else:
        logger.info("All expected columns verified successfully.")

    metadata = {
        "source_file": str(file_path),
        "total_rows_ingested": total_rows,
        "total_cols_ingested": total_cols,
        "missing_columns": missing_cols,
        "extra_columns": extra_cols,
        "is_schema_valid": len(missing_cols) == 0,
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
    }

    return df, metadata
