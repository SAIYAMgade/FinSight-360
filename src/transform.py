"""Analytical feature engineering and transformation module for FinSight 360."""
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger("finsight360.transform")


def add_analytical_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construct business features and segmentation bands for analytical reporting.

    All bins are constructed using closed lower/open upper intervals where standard,
    handling edge cases and nulls cleanly.
    """
    logger.info("Generating analytical features and segmentation bands...")
    data = df.copy()

    # 1. Loan Amount Bands
    loan_bins = [0, 5000, 10000, 15000, 20000, 25000, 30000, np.inf]
    loan_labels = [
        "< $5k", "$5k - $10k", "$10k - $15k", "$15k - $20k",
        "$20k - $25k", "$25k - $30k", "$30k+"
    ]
    data["loan_amount_band"] = pd.cut(
        data["loan_amnt"], bins=loan_bins, labels=loan_labels, right=False
    ).astype(str)

    # 2. Annual Income Bands
    inc_bins = [0, 30000, 50000, 75000, 100000, 150000, np.inf]
    inc_labels = [
        "< $30k", "$30k - $50k", "$50k - $75k", "$75k - $100k",
        "$100k - $150k", "$150k+"
    ]
    data["income_band"] = pd.cut(
        data["annual_inc"], bins=inc_bins, labels=inc_labels, right=False
    ).astype(str)

    # 3. Debt-to-Income (DTI) Bands
    dti_bins = [0, 10, 15, 20, 25, 30, np.inf]
    dti_labels = ["< 10%", "10% - 15%", "15% - 20%", "20% - 25%", "25% - 30%", "30%+"]
    data["dti_band"] = pd.cut(
        data["dti"], bins=dti_bins, labels=dti_labels, right=False
    ).astype(str)

    # 4. Interest Rate Bands
    int_bins = [0, 8, 12, 16, 20, np.inf]
    int_labels = ["< 8%", "8% - 12%", "12% - 16%", "16% - 20%", "20%+"]
    data["int_rate_band"] = pd.cut(
        data["int_rate"], bins=int_bins, labels=int_labels, right=False
    ).astype(str)

    # 5. Payment-to-Income Burden (% of annual income committed to annual LC loan installment)
    # Annualized installment = installment * 12
    data["installment_burden_pct"] = np.where(
        data["annual_inc"] > 0,
        ((data["installment"] * 12.0) / data["annual_inc"]) * 100.0,
        np.nan
    ).round(2)

    # 6. Credit History Age Bands
    if "credit_history_years" in data.columns:
        cr_bins = [0, 5, 10, 15, 20, np.inf]
        cr_labels = ["< 5 yrs", "5 - 10 yrs", "10 - 15 yrs", "15 - 20 yrs", "20+ yrs"]
        data["credit_history_band"] = pd.cut(
            data["credit_history_years"], bins=cr_bins, labels=cr_labels, right=False
        ).astype(str)

    # 7. High Risk Indicator (Heuristic segment: Grade E/F/G or DTI >= 25)
    data["is_high_risk_segment"] = (
        data["grade"].isin(["E", "F", "G"]) | (data["dti"] >= 25.0)
    ).astype(int)

    logger.info("Feature engineering completed successfully.")
    return data
