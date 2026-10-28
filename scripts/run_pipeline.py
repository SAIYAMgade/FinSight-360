"""End-to-end data pipeline execution script for FinSight 360."""
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime, timezone
import logging
import time
import uuid
import pandas as pd
from sqlalchemy import text

from src.config import load_config
from src.ingest import ingest_raw_data
from src.clean import clean_lending_data
from src.transform import add_analytical_features
from src.validate import DataQualityValidator
from src.database import get_db_engine, load_dataframe_to_table, execute_sql_file, run_query
from src.metrics import calculate_portfolio_kpis, reconcile_metrics
from scripts.setup_database import setup_database

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("finsight360.pipeline")


def run_pipeline(config_path: str = "config/config.yaml") -> dict:
    """Execute complete FinSight 360 analytical data pipeline."""
    start_time = datetime.now(timezone.utc)
    run_id = f"RUN-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{str(uuid.uuid4())[:6]}"
    logger.info(f"=== Starting FinSight 360 Pipeline [{run_id}] ===")

    config = load_config(config_path)
    raw_path = config["paths"]["raw_data"]
    processed_parquet = config["paths"]["processed_data"]
    processed_csv = config["paths"]["processed_csv"]
    dq_csv = config["paths"]["dq_report_csv"]

    # 1. Database schema initialization
    setup_database(config_path)
    engine = get_db_engine(config)

    # 2. Ingestion
    t0 = time.time()
    raw_df, ingest_meta = ingest_raw_data(raw_path)
    logger.info(f"Ingestion completed in {time.time() - t0:.2f}s.")

    # 3. Load Staging table in database
    t0 = time.time()
    load_dataframe_to_table(engine, raw_df, "stg_loans", if_exists="replace")
    logger.info(f"Staging table loaded in {time.time() - t0:.2f}s.")

    # 4. Cleaning
    t0 = time.time()
    cleaned_df, clean_audit = clean_lending_data(raw_df)
    logger.info(f"Data cleaning completed in {time.time() - t0:.2f}s.")

    # 5. Transformation / Feature Engineering
    t0 = time.time()
    transformed_df = add_analytical_features(cleaned_df)
    logger.info(f"Transformation completed in {time.time() - t0:.2f}s.")

    # 6. Data Quality Framework Audit
    t0 = time.time()
    validator = DataQualityValidator(thresholds=config.get("thresholds"))
    dq_results = validator.run_all_checks(
        transformed_df, initial_raw_count=ingest_meta["total_rows_ingested"]
    )
    Path(dq_csv).parent.mkdir(parents=True, exist_ok=True)
    dq_results.to_csv(dq_csv, index=False)
    load_dataframe_to_table(engine, dq_results, "dq_audit_log", if_exists="replace")
    logger.info(f"Data quality audit completed in {time.time() - t0:.2f}s. Report saved to {dq_csv}.")

    # 7. Export Processed Data (Parquet & CSV)
    t0 = time.time()
    Path(processed_parquet).parent.mkdir(parents=True, exist_ok=True)
    transformed_df.to_parquet(processed_parquet, index=False)
    logger.info(f"Processed dataset saved to {processed_parquet} ({time.time() - t0:.2f}s).")

    # 8. Load Analytical Fact Table
    t0 = time.time()
    # Select columns matching fact_loans schema
    fact_cols = [
        "loan_id", "loan_amnt", "term", "term_months", "int_rate", "installment",
        "grade", "sub_grade", "home_ownership", "annual_inc", "verification_status",
        "issue_date", "issue_year", "issue_month", "issue_quarter", "issue_year_month",
        "loan_status", "is_default", "purpose", "dti", "addr_state", "zip_code",
        "emp_length", "emp_length_years", "credit_history_years", "open_acc", "pub_rec",
        "revol_bal", "revol_util", "total_acc", "mort_acc", "pub_rec_bankruptcies",
        "loan_amount_band", "income_band", "dti_band", "int_rate_band",
        "installment_burden_pct", "is_high_risk_segment"
    ]
    fact_df = transformed_df[[c for c in fact_cols if c in transformed_df.columns]].copy()
    # Convert dates to string for SQL insertion
    fact_df["issue_date"] = fact_df["issue_date"].dt.strftime("%Y-%m-%d")
    load_dataframe_to_table(engine, fact_df, "fact_loans", if_exists="replace")
    logger.info(f"Fact table 'fact_loans' loaded in {time.time() - t0:.2f}s.")

    # 9. Re-run Analytical Views
    execute_sql_file(engine, "sql/03_staging_views.sql")
    execute_sql_file(engine, "sql/04_analytical_views.sql")

    # 10. Metrics Calculation & Reconciliation
    py_kpis = calculate_portfolio_kpis(transformed_df)
    sql_summary_df = run_query(engine, "SELECT * FROM v_portfolio_summary")
    sql_kpis = {
        "total_loans": int(sql_summary_df["total_loans"].iloc[0]),
        "total_exposure": float(sql_summary_df["total_original_exposure"].iloc[0]),
        "avg_loan_size": float(sql_summary_df["avg_loan_size"].iloc[0]),
        "charged_off_count": int(sql_summary_df["charged_off_count"].iloc[0]),
        "fully_paid_count": int(sql_summary_df["fully_paid_count"].iloc[0]),
        "observed_default_rate": float(sql_summary_df["observed_default_rate_pct"].iloc[0])
    }
    reconciled = reconcile_metrics(py_kpis, sql_kpis)
    logger.info(f"Reconciliation Summary:\n{pd.DataFrame(reconciled)}")

    # 11. Pipeline Run History Record
    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds()
    run_record = pd.DataFrame([{
        "run_id": run_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "records_ingested": ingest_meta["total_rows_ingested"],
        "records_processed": len(transformed_df),
        "status": "SUCCESS",
        "notes": f"Completed in {duration:.2f}s. Default rate: {py_kpis['observed_default_rate']}%."
    }])
    load_dataframe_to_table(engine, run_record, "pipeline_run_history", if_exists="append")

    summary = {
        "run_id": run_id,
        "duration_seconds": round(duration, 2),
        "records_ingested": ingest_meta["total_rows_ingested"],
        "records_processed": len(transformed_df),
        "portfolio_kpis": py_kpis,
        "reconciliation": reconciled,
        "dq_pass_count": int((dq_results["result"] == "PASS").sum()),
        "dq_warning_count": int((dq_results["result"] == "WARNING").sum()),
        "dq_fail_count": int((dq_results["result"] == "FAIL").sum())
    }

    logger.info(f"=== FinSight 360 Pipeline Completed Successfully in {duration:.2f}s ===")
    return summary


if __name__ == "__main__":
    run_pipeline()
