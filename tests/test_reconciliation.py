"""Reconciliation test verifying mathematical parity across Python and SQL."""
from pathlib import Path
import sqlite3
import pandas as pd
import pytest
from src.metrics import calculate_portfolio_kpis, reconcile_metrics


def test_cross_layer_reconciliation():
    """Verify that Python and SQL produce 100% identical portfolio metrics."""
    db_path = Path("data/processed/finsight360.db")
    parquet_path = Path("data/processed/lending_club_cleaned.parquet")

    if not db_path.exists() or not parquet_path.exists():
        pytest.skip("Pipeline outputs not found; run pipeline first.")

    # 1. Compute Python KPIs directly from processed Parquet
    df = pd.read_parquet(parquet_path)
    py_kpis = calculate_portfolio_kpis(df)

    # 2. Query SQL Analytical View from SQLite
    conn = sqlite3.connect(str(db_path))
    sql_summary_df = pd.read_sql_query("SELECT * FROM v_portfolio_summary", conn)
    conn.close()

    sql_kpis = {
        "total_loans": int(sql_summary_df["total_loans"].iloc[0]),
        "total_exposure": float(sql_summary_df["total_original_exposure"].iloc[0]),
        "avg_loan_size": float(sql_summary_df["avg_loan_size"].iloc[0]),
        "charged_off_count": int(sql_summary_df["charged_off_count"].iloc[0]),
        "fully_paid_count": int(sql_summary_df["fully_paid_count"].iloc[0]),
        "observed_default_rate": float(sql_summary_df["observed_default_rate_pct"].iloc[0])
    }

    # 3. Perform reconciliation audit
    reconciliation = reconcile_metrics(py_kpis, sql_kpis, tolerance=0.01)

    assert len(reconciliation) == 6
    for item in reconciliation:
        assert item["status"] == "MATCH", f"Discrepancy detected in {item['metric_name']}: {item}"
        assert item["absolute_difference"] <= 0.01

    # Verify baseline ground truth numbers
    assert py_kpis["total_loans"] == 396030
    assert py_kpis["charged_off_count"] == 77673
    assert py_kpis["fully_paid_count"] == 318357
