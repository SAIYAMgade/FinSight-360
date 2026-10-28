"""Business metrics calculation and reconciliation engine for FinSight 360."""
import logging
from typing import Dict, Any, List
import pandas as pd
import numpy as np

logger = logging.getLogger("finsight360.metrics")


def calculate_portfolio_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate executive KPI portfolio metrics from loan data.
    """
    total_loans = int(len(df))
    if total_loans == 0:
        return {}

    total_exposure = float(df["loan_amnt"].sum())
    avg_loan_size = float(df["loan_amnt"].mean())
    median_loan_size = float(df["loan_amnt"].median())
    avg_int_rate = float(df["int_rate"].mean())
    avg_dti = float(df["dti"].dropna().mean())
    avg_income = float(df["annual_inc"].dropna().mean())

    charged_off_count = int((df["is_default"] == 1).sum())
    fully_paid_count = int((df["is_default"] == 0).sum())
    observed_default_rate = round((charged_off_count / total_loans) * 100.0, 4)

    defaulted_exposure = float(df[df["is_default"] == 1]["loan_amnt"].sum())
    defaulted_exposure_share = round((defaulted_exposure / total_exposure) * 100.0, 4)

    return {
        "total_loans": total_loans,
        "total_exposure": round(total_exposure, 2),
        "avg_loan_size": round(avg_loan_size, 2),
        "median_loan_size": round(median_loan_size, 2),
        "avg_int_rate": round(avg_int_rate, 2),
        "avg_dti": round(avg_dti, 2),
        "avg_annual_income": round(avg_income, 2),
        "charged_off_count": charged_off_count,
        "fully_paid_count": fully_paid_count,
        "observed_default_rate": observed_default_rate,
        "defaulted_exposure": round(defaulted_exposure, 2),
        "defaulted_exposure_share": defaulted_exposure_share
    }


def calculate_segment_performance(
    df: pd.DataFrame,
    segment_col: str,
    min_records: int = 100
) -> pd.DataFrame:
    """
    Calculate segment-level risk performance metrics with sample-size filtering.
    """
    grouped = df.groupby(segment_col).agg(
        loan_count=("loan_amnt", "count"),
        total_loan_amount=("loan_amnt", "sum"),
        avg_loan_amount=("loan_amnt", "mean"),
        avg_interest_rate=("int_rate", "mean"),
        avg_dti=("dti", "mean"),
        default_count=("is_default", "sum")
    ).reset_index()

    total_portfolio_volume = df["loan_amnt"].sum()
    grouped["observed_default_rate"] = (
        (grouped["default_count"] / grouped["loan_count"]) * 100.0
    ).round(2)
    grouped["portfolio_exposure_share"] = (
        (grouped["total_loan_amount"] / total_portfolio_volume) * 100.0
    ).round(2)
    grouped["avg_loan_amount"] = grouped["avg_loan_amount"].round(2)
    grouped["avg_interest_rate"] = grouped["avg_interest_rate"].round(2)
    grouped["avg_dti"] = grouped["avg_dti"].round(2)

    # Flag segments below minimum statistical reliability threshold
    grouped["is_statistically_reliable"] = grouped["loan_count"] >= min_records

    return grouped.sort_values(by="observed_default_rate", ascending=False)


def calculate_vintage_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate loan origination vintage cohort performance over time.
    """
    vintage = df.groupby("issue_year").agg(
        loan_count=("loan_amnt", "count"),
        total_origination_amount=("loan_amnt", "sum"),
        avg_loan_amount=("loan_amnt", "mean"),
        avg_interest_rate=("int_rate", "mean"),
        avg_dti=("dti", "mean"),
        charged_off_count=("is_default", "sum")
    ).reset_index()

    vintage["observed_default_rate"] = (
        (vintage["charged_off_count"] / vintage["loan_count"]) * 100.0
    ).round(2)
    vintage["avg_loan_amount"] = vintage["avg_loan_amount"].round(2)
    vintage["avg_interest_rate"] = vintage["avg_interest_rate"].round(2)
    vintage["avg_dti"] = vintage["avg_dti"].round(2)

    return vintage.sort_values(by="issue_year")


def reconcile_metrics(
    python_kpis: Dict[str, Any],
    sql_kpis: Dict[str, Any],
    tolerance: float = 0.01
) -> List[Dict[str, Any]]:
    """
    Perform reconciliation comparison between Python and SQL analytics outputs.
    """
    reconciliation_results = []
    comparable_keys = [
        "total_loans", "total_exposure", "avg_loan_size",
        "charged_off_count", "fully_paid_count", "observed_default_rate"
    ]

    for key in comparable_keys:
        py_val = python_kpis.get(key)
        sql_val = sql_kpis.get(key)

        if py_val is not None and sql_val is not None:
            diff = abs(float(py_val) - float(sql_val))
            is_match = diff <= tolerance
            reconciliation_results.append({
                "metric_name": key,
                "python_value": py_val,
                "sql_value": sql_val,
                "absolute_difference": round(diff, 4),
                "status": "MATCH" if is_match else "DISCREPANCY"
            })

    return reconciliation_results
