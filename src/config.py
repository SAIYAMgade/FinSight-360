"""Configuration loader for FinSight 360."""
from pathlib import Path
import os
import yaml

DEFAULT_CONFIG = {
    "project": {
        "name": "FinSight 360",
        "description": "Banking Analytics & Credit Risk Intelligence Platform",
        "version": "1.0.0"
    },
    "paths": {
        "raw_data": "data/raw/lending_club_loan_two.csv",
        "data_dictionary": "data/raw/lending_club_info.csv",
        "processed_data": "data/processed/lending_club_cleaned.parquet",
        "processed_csv": "data/processed/lending_club_cleaned.csv",
        "sample_data": "data/sample/loans_sample.csv",
        "db_path": "data/processed/finsight360.db",
        "dq_report_csv": "reports/data_quality_results.csv",
        "excel_report": "excel/FinSight_360_Executive_Report.xlsx"
    },
    "database": {
        "engine": os.getenv("DB_ENGINE", "sqlite"),
        "pg_host": os.getenv("PG_HOST", "localhost"),
        "pg_port": int(os.getenv("PG_PORT", 5432)),
        "pg_database": os.getenv("PG_DATABASE", "finsight360"),
        "pg_user": os.getenv("PG_USER", "postgres"),
        "pg_password": os.getenv("PG_PASSWORD", "password123")
    },
    "thresholds": {
        "min_segment_sample_size": 100,
        "max_plausible_int_rate": 35.0,
        "min_plausible_int_rate": 4.0,
        "max_plausible_loan_amount": 50000.0,
        "min_plausible_loan_amount": 500.0,
        "max_plausible_annual_inc": 5000000.0,
        "min_plausible_annual_inc": 1000.0,
        "max_plausible_dti": 100.0,
        "min_plausible_dti": 0.0
    },
    "sampling": {
        "sample_size": 25000,
        "random_seed": 42,
        "stratify_col": "loan_status"
    }
}


def load_config(config_path: str = "config/config.yaml") -> dict:
    """Load configuration from YAML file with fallback to defaults."""
    path = Path(config_path)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
            # Deep merge with defaults
            config = DEFAULT_CONFIG.copy()
            for key, val in user_config.items():
                if isinstance(val, dict) and key in config:
                    config[key].update(val)
                else:
                    config[key] = val
            return config
    return DEFAULT_CONFIG.copy()
