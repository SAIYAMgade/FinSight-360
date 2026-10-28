"""Unit tests for business metrics calculation and reconciliation engine."""
import pytest
import pandas as pd
from src.metrics import calculate_portfolio_kpis, calculate_segment_performance, reconcile_metrics


@pytest.fixture
def sample_metrics_df():
    """Construct minimal dataframe for KPI calculations."""
    return pd.DataFrame({
        "loan_id": ["LN-1", "LN-2", "LN-3", "LN-4"],
        "loan_amnt": [10000.0, 20000.0, 15000.0, 5000.0],
        "int_rate": [10.0, 15.0, 12.0, 8.0],
        "dti": [15.0, 25.0, 18.0, 10.0],
        "annual_inc": [80000.0, 60000.0, 75000.0, 50000.0],
        "is_default": [0, 1, 0, 0],
        "grade": ["A", "C", "B", "A"],
        "purpose": ["debt_consolidation", "credit_card", "debt_consolidation", "car"]
    })


def test_calculate_portfolio_kpis(sample_metrics_df):
    """Test core portfolio KPI mathematical accuracy."""
    kpis = calculate_portfolio_kpis(sample_metrics_df)

    assert kpis["total_loans"] == 4
    assert kpis["total_exposure"] == 50000.0
    assert kpis["avg_loan_size"] == 12500.0
    assert kpis["charged_off_count"] == 1
    assert kpis["fully_paid_count"] == 3
    assert kpis["observed_default_rate"] == 25.0  # 1 / 4 * 100
    assert kpis["defaulted_exposure"] == 20000.0
    assert kpis["defaulted_exposure_share"] == 40.0  # 20000 / 50000 * 100


def test_calculate_portfolio_kpis_empty():
    """Test KPI calculation behavior on empty dataframe."""
    empty_df = pd.DataFrame(columns=["loan_amnt", "is_default", "int_rate", "dti", "annual_inc"])
    kpis = calculate_portfolio_kpis(empty_df)
    assert kpis == {}


def test_calculate_segment_performance(sample_metrics_df):
    """Test segment-level breakdown and default rate ranking."""
    seg_df = calculate_segment_performance(sample_metrics_df, segment_col="grade", min_records=1)

    assert len(seg_df) == 3
    # Grade C has 1 loan which defaulted -> 100% default rate
    grade_c = seg_df[seg_df["grade"] == "C"].iloc[0]
    assert grade_c["observed_default_rate"] == 100.0
    # Grade A has 2 loans, 0 defaults -> 0% default rate
    grade_a = seg_df[seg_df["grade"] == "A"].iloc[0]
    assert grade_a["observed_default_rate"] == 0.0


def test_reconcile_metrics_matching():
    """Test reconciliation with identical metrics."""
    py_kpis = {
        "total_loans": 1000,
        "total_exposure": 15000000.0,
        "avg_loan_size": 15000.0,
        "charged_off_count": 200,
        "fully_paid_count": 800,
        "observed_default_rate": 20.0
    }
    sql_kpis = py_kpis.copy()
    results = reconcile_metrics(py_kpis, sql_kpis)

    assert len(results) == 6
    for r in results:
        assert r["status"] == "MATCH"
        assert r["absolute_difference"] == 0.0


def test_reconcile_metrics_discrepancy():
    """Test reconciliation alerting when values diverge."""
    py_kpis = {"total_loans": 1000, "total_exposure": 15000000.0}
    sql_kpis = {"total_loans": 995, "total_exposure": 15000000.0}
    results = reconcile_metrics(py_kpis, sql_kpis)

    loan_result = [r for r in results if r["metric_name"] == "total_loans"][0]
    assert loan_result["status"] == "DISCREPANCY"
    assert loan_result["absolute_difference"] == 5.0
