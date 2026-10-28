"""Database initialization and schema migration script for FinSight 360."""
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import logging
import pandas as pd
from sqlalchemy import text
from src.config import load_config
from src.database import get_db_engine, execute_sql_file, load_dataframe_to_table

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("finsight360.setup_db")


def populate_static_dimensions(engine) -> None:
    """Populate reference lookup dimensions (risk grades, loan purposes, dates)."""
    logger.info("Populating static lookup dimensions...")

    # 1. dim_risk_grade
    grades_data = [
        {"grade": "A", "risk_tier": "Prime Low Risk", "prime_status": "Prime", "expected_loss_range": "0% - 7%"},
        {"grade": "B", "risk_tier": "Near Prime", "prime_status": "Prime", "expected_loss_range": "7% - 13%"},
        {"grade": "C", "risk_tier": "Standard Consumer", "prime_status": "Non-Prime", "expected_loss_range": "13% - 22%"},
        {"grade": "D", "risk_tier": "Elevated Risk", "prime_status": "Non-Prime", "expected_loss_range": "22% - 30%"},
        {"grade": "E", "risk_tier": "Subprime", "prime_status": "Subprime", "expected_loss_range": "30% - 38%"},
        {"grade": "F", "risk_tier": "Deep Subprime", "prime_status": "Subprime", "expected_loss_range": "38% - 45%"},
        {"grade": "G", "risk_tier": "High Default Risk", "prime_status": "Subprime", "expected_loss_range": "45%+"}
    ]
    dim_grade_df = pd.DataFrame(grades_data)
    load_dataframe_to_table(engine, dim_grade_df, "dim_risk_grade", if_exists="replace")

    # 2. dim_loan_purpose
    purposes_data = [
        {"purpose": "debt_consolidation", "purpose_group": "Debt Refinancing", "is_refinancing": 1},
        {"purpose": "credit_card", "purpose_group": "Debt Refinancing", "is_refinancing": 1},
        {"purpose": "home_improvement", "purpose_group": "Home & Property", "is_refinancing": 0},
        {"purpose": "house", "purpose_group": "Home & Property", "is_refinancing": 0},
        {"purpose": "small_business", "purpose_group": "Commercial / Venture", "is_refinancing": 0},
        {"purpose": "major_purchase", "purpose_group": "Consumer Durable", "is_refinancing": 0},
        {"purpose": "car", "purpose_group": "Auto / Vehicle", "is_refinancing": 0},
        {"purpose": "medical", "purpose_group": "Emergency / Healthcare", "is_refinancing": 0},
        {"purpose": "moving", "purpose_group": "Lifestyle / Relocation", "is_refinancing": 0},
        {"purpose": "vacation", "purpose_group": "Discretionary / Leisure", "is_refinancing": 0},
        {"purpose": "wedding", "purpose_group": "Lifestyle / Event", "is_refinancing": 0},
        {"purpose": "educational", "purpose_group": "Education", "is_refinancing": 0},
        {"purpose": "renewable_energy", "purpose_group": "Green Energy", "is_refinancing": 0},
        {"purpose": "other", "purpose_group": "Miscellaneous", "is_refinancing": 0}
    ]
    dim_purpose_df = pd.DataFrame(purposes_data)
    load_dataframe_to_table(engine, dim_purpose_df, "dim_loan_purpose", if_exists="replace")

    # 3. dim_date (generated across 2007 to 2017 monthly)
    dates = pd.date_range(start="2007-01-01", end="2017-12-31", freq="MS")
    dim_date_df = pd.DataFrame({
        "date_key": dates.strftime("%Y%m"),
        "full_date": dates.date,
        "year_num": dates.year,
        "quarter_num": dates.quarter,
        "month_num": dates.month,
        "month_name": dates.strftime("%B"),
        "year_month": dates.strftime("%Y-%m")
    })
    load_dataframe_to_table(engine, dim_date_df, "dim_date", if_exists="replace")
    logger.info("Static lookup dimensions populated successfully.")


def setup_database(config_path: str = "config/config.yaml") -> None:
    """Initialize database tables, indexes, static dimensions, and analytical views."""
    config = load_config(config_path)
    engine = get_db_engine(config)

    logger.info("Initializing FinSight 360 database schema...")
    execute_sql_file(engine, "sql/01_schema.sql")
    populate_static_dimensions(engine)
    execute_sql_file(engine, "sql/02_constraints_indexes.sql")
    execute_sql_file(engine, "sql/03_staging_views.sql")
    execute_sql_file(engine, "sql/04_analytical_views.sql")
    logger.info("Database setup complete.")


if __name__ == "__main__":
    setup_database()
