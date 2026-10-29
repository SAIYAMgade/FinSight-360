"""Unit test verifying Tableau export generation and mathematical reconciliation."""
from pathlib import Path
import pandas as pd
import pytest

from scripts.export_tableau_data import export_tableau_data, OUTPUT_DIR


def test_tableau_exports_and_reconciliation():
    """Verify Tableau CSV outputs and cross-layer reconciliation integrity."""
    result = export_tableau_data()

    # 1. Verify files were generated
    for fname in [
        "delinquency_npl_trend.csv",
        "exposure_by_risk_tier.csv",
        "concentration_by_segment.csv",
        "kpi_summary.csv",
        "VERIFICATION.md"
    ]:
        file_path = OUTPUT_DIR / fname
        assert file_path.exists(), f"Missing export file: {fname}"
        assert file_path.stat().st_size > 0, f"Empty export file: {fname}"

    # 2. Verify KPI row matches portfolio totals
    df_kpi = pd.read_csv(OUTPUT_DIR / "kpi_summary.csv")
    assert len(df_kpi) == 1
    assert df_kpi["total_loans"].iloc[0] == 25000
    assert df_kpi["total_borrowers"].iloc[0] == 25000
    assert round(df_kpi["total_exposure"].iloc[0], 2) == 352408550.00
    assert df_kpi["number_of_risk_tiers"].iloc[0] == 7

    # 3. Verify exposure by risk tier matches KPI totals
    df_tier = pd.read_csv(OUTPUT_DIR / "exposure_by_risk_tier.csv")
    assert df_tier["loan_count"].sum() == 25000
    assert round(df_tier["total_exposure"].sum(), 2) == 352408550.00
    assert set(df_tier["grade"].unique()) == {"A", "B", "C", "D", "E", "F", "G"}

    # 4. Verify trend table matches KPI totals
    df_trend = pd.read_csv(OUTPUT_DIR / "delinquency_npl_trend.csv")
    assert df_trend["loan_count"].sum() == 25000
    assert round(df_trend["total_exposure"].sum(), 2) == 352408550.00

    # 5. Verify reconciliation results have 0.00 delta
    for item in result["reconciliation"]:
        assert item["delta"] == 0.0, f"Discrepancy in {item['metric']}: delta={item['delta']}"
