"""Automated reporting and visualization generator for FinSight 360."""
from pathlib import Path
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("finsight360.reporting")

# Set institutional banking visual style
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.dpi"] = 300

NAVY = "#1E3A8A"
SLATE = "#475569"
TEAL = "#0D9488"
CRIMSON = "#BE123C"
AMBER = "#D97706"
GRAY_BG = "#F8FAFC"


def generate_all_dashboard_visuals(
    parquet_path: str = "data/processed/lending_club_cleaned.parquet",
    output_dir: str = "reports/screenshots"
) -> None:
    """Generate high-resolution analytical visual dashboards matching Power BI specifications."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    logger.info(f"Loading cleaned dataset from {parquet_path}...")
    df = pd.read_parquet(parquet_path)

    # =========================================================================
    # VISUAL 1: PAGE 1 - EXECUTIVE PORTFOLIO OVERVIEW
    # =========================================================================
    logger.info("Generating Visual 1: Executive Portfolio Overview...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), facecolor=GRAY_BG)
    fig.suptitle(
        "FinSight 360 | Executive Portfolio Overview\nPortfolio Scale: 396,030 Facilities | Total Exposure: $5.59 Billion",
        fontsize=16, fontweight="bold", color=NAVY, y=0.98
    )

    # 1.1 Annual Origination Volume Trend
    annual_vol = df.groupby("issue_year")["loan_amnt"].sum() / 1e6
    axes[0, 0].bar(annual_vol.index, annual_vol.values, color=NAVY, width=0.6, edgecolor="none", alpha=0.9)
    axes[0, 0].set_title("Origination Volume by Vintage Year ($ Millions)", fontsize=12, fontweight="bold", color=NAVY)
    axes[0, 0].set_ylabel("Funded Capital ($M)", fontsize=10, color=SLATE)
    axes[0, 0].yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}M"))
    axes[0, 0].grid(axis="y", linestyle="--", alpha=0.5)

    # 1.2 Loan Status Breakdown (Closed Outcome Share)
    status_counts = df["loan_status"].value_counts()
    colors = [TEAL, CRIMSON]
    axes[0, 1].pie(
        status_counts.values,
        labels=[f"{k}\n({v:,} | {v/len(df)*100:.1f}%)" for k, v in status_counts.items()],
        colors=colors,
        startangle=140,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2)
    )
    axes[0, 1].set_title("Terminal Repayment Status Composition", fontsize=12, fontweight="bold", color=NAVY)

    # 1.3 Exposure by Purpose (Top 7)
    purpose_exp = (df.groupby("purpose")["loan_amnt"].sum() / 1e6).sort_values(ascending=False).head(7)
    axes[1, 0].barh(purpose_exp.index, purpose_exp.values, color=TEAL, edgecolor="none", alpha=0.85)
    axes[1, 0].invert_yaxis()
    axes[1, 0].set_title("Portfolio Exposure by Top Loan Purposes ($ Millions)", fontsize=12, fontweight="bold", color=NAVY)
    axes[1, 0].set_xlabel("Funded Capital ($M)", fontsize=10, color=SLATE)
    axes[1, 0].xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}M"))
    axes[1, 0].grid(axis="x", linestyle="--", alpha=0.5)

    # 1.4 Portfolio Exposure by LendingClub Risk Grade
    grade_exp = (df.groupby("grade")["loan_amnt"].sum() / 1e6).sort_index()
    palette = [TEAL, "#14B8A6", AMBER, "#F59E0B", CRIMSON, "#991B1B", "#7F1D1D"]
    axes[1, 1].bar(grade_exp.index, grade_exp.values, color=palette, width=0.6, edgecolor="none")
    axes[1, 1].set_title("Capital Exposure by Internal Risk Grade ($ Millions)", fontsize=12, fontweight="bold", color=NAVY)
    axes[1, 1].set_ylabel("Funded Capital ($M)", fontsize=10, color=SLATE)
    axes[1, 1].yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}M"))
    axes[1, 1].grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(out_path / "01_executive_portfolio_overview.png", dpi=300)
    plt.close(fig)

    # =========================================================================
    # VISUAL 2: PAGE 2 - CREDIT RISK SEGMENTATION
    # =========================================================================
    logger.info("Generating Visual 2: Credit Risk Segmentation...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), facecolor=GRAY_BG)
    fig.suptitle(
        "FinSight 360 | Credit Risk Segmentation & Default Intelligence\nBaseline Default Rate: 19.61% | High-Risk Concentration Analysis",
        fontsize=16, fontweight="bold", color=NAVY, y=0.98
    )

    # 2.1 Default Rate by Grade
    grade_def = df.groupby("grade")["is_default"].mean() * 100.0
    axes[0, 0].plot(grade_def.index, grade_def.values, marker="o", linewidth=2.5, markersize=8, color=CRIMSON)
    axes[0, 0].axhline(19.61, color=SLATE, linestyle="--", linewidth=1.2, label="Portfolio Baseline (19.61%)")
    axes[0, 0].set_title("Observed Default Rate by Risk Grade (%)", fontsize=12, fontweight="bold", color=NAVY)
    axes[0, 0].set_ylabel("Default Rate (%)", fontsize=10, color=SLATE)
    axes[0, 0].yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}%"))
    axes[0, 0].legend(loc="upper left")
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)

    # 2.2 Default Rate by Purpose
    purp_def = (df.groupby("purpose")["is_default"].mean() * 100.0).sort_values(ascending=False).head(8)
    axes[0, 1].barh(purp_def.index, purp_def.values, color=CRIMSON, alpha=0.8, edgecolor="none")
    axes[0, 1].axvline(19.61, color=SLATE, linestyle="--", linewidth=1.2)
    axes[0, 1].invert_yaxis()
    axes[0, 1].set_title("Observed Default Rate across Selected Loan Purposes (%)", fontsize=12, fontweight="bold", color=NAVY)
    axes[0, 1].set_xlabel("Default Rate (%)", fontsize=10, color=SLATE)
    axes[0, 1].xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}%"))
    axes[0, 1].grid(axis="x", linestyle="--", alpha=0.5)

    # 2.3 Default Rate across DTI Leverage Bands
    dti_order = ["< 10%", "10% - 15%", "15% - 20%", "20% - 25%", "25% - 30%", "30%+"]
    dti_def = (df.groupby("dti_band")["is_default"].mean() * 100.0).reindex(dti_order).dropna()
    axes[1, 0].bar(dti_def.index, dti_def.values, color=AMBER, width=0.55, edgecolor="none")
    axes[1, 0].axhline(19.61, color=SLATE, linestyle="--", linewidth=1.2)
    axes[1, 0].set_title("Observed Default Rate by Debt-to-Income (DTI) Band (%)", fontsize=12, fontweight="bold", color=NAVY)
    axes[1, 0].set_ylabel("Default Rate (%)", fontsize=10, color=SLATE)
    axes[1, 0].yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}%"))
    axes[1, 0].grid(axis="y", linestyle="--", alpha=0.5)

    # 2.4 Segment Exposure vs Default Rate Scatter Plot (Matrix)
    seg_summary = df.groupby("purpose").agg(
        exposure=("loan_amnt", "sum"),
        default_rate=("is_default", "mean"),
        count=("loan_amnt", "count")
    ).reset_index()
    seg_summary["exposure_m"] = seg_summary["exposure"] / 1e6
    seg_summary["default_pct"] = seg_summary["default_rate"] * 100.0

    scatter = axes[1, 1].scatter(
        seg_summary["exposure_m"],
        seg_summary["default_pct"],
        s=seg_summary["count"] / 300,
        c=seg_summary["default_pct"],
        cmap="YlOrRd",
        alpha=0.75,
        edgecolors="black",
        linewidth=1
    )
    for _, row in seg_summary.iterrows():
        if row["exposure_m"] > 100 or row["default_pct"] > 22:
            axes[1, 1].annotate(
                row["purpose"],
                (row["exposure_m"], row["default_pct"]),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=8,
                color=NAVY
            )
    axes[1, 1].axhline(19.61, color=SLATE, linestyle="--", linewidth=1.2, label="Avg Default Rate (19.6%)")
    axes[1, 1].set_title("Segment Exposure ($M) vs. Observed Default Rate (%)", fontsize=12, fontweight="bold", color=NAVY)
    axes[1, 1].set_xlabel("Total Exposure ($ Millions)", fontsize=10, color=SLATE)
    axes[1, 1].set_ylabel("Default Rate (%)", fontsize=10, color=SLATE)
    axes[1, 1].yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}%"))
    axes[1, 1].xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}M"))
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(out_path / "02_credit_risk_segmentation.png", dpi=300)
    plt.close(fig)

    # =========================================================================
    # VISUAL 3: PAGE 3 - VINTAGES & DATA QUALITY
    # =========================================================================
    logger.info("Generating Visual 3: Vintages & Data Quality Intelligence...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), facecolor=GRAY_BG)
    fig.suptitle(
        "FinSight 360 | Portfolio Vintages & Data Quality Assurance\nChronological Risk Evolution & Automated Audit Health",
        fontsize=16, fontweight="bold", color=NAVY, y=0.98
    )

    # 3.1 Vintage Default Trajectory
    vintage_def = df.groupby("issue_year")["is_default"].mean() * 100.0
    axes[0, 0].plot(vintage_def.index, vintage_def.values, marker="s", color=NAVY, linewidth=2.5, markersize=7)
    axes[0, 0].axhline(19.61, color=SLATE, linestyle="--", linewidth=1.2, label="Portfolio Mean (19.6%)")
    axes[0, 0].set_title("Default Rate Evolution by Origination Vintage Year (%)", fontsize=12, fontweight="bold", color=NAVY)
    axes[0, 0].set_ylabel("Vintage Default Rate (%)", fontsize=10, color=SLATE)
    axes[0, 0].yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}%"))
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)
    axes[0, 0].legend()

    # 3.2 Pricing / Interest Rate Boxplot by Grade
    sns.boxplot(
        data=df.sample(min(20000, len(df)), random_state=42),
        x="grade",
        y="int_rate",
        palette="Blues_r",
        order=sorted(df["grade"].unique()),
        ax=axes[0, 1],
        fliersize=1.5
    )
    axes[0, 1].set_title("Interest Rate Pricing Distribution by Risk Grade", fontsize=12, fontweight="bold", color=NAVY)
    axes[0, 1].set_xlabel("Underwriting Grade", fontsize=10, color=SLATE)
    axes[0, 1].set_ylabel("Nominal Interest Rate (%)", fontsize=10, color=SLATE)
    axes[0, 1].yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}%"))

    # 3.3 Data Quality Audit Rule Pass Rates
    dq_df = pd.read_csv("reports/data_quality_results.csv")
    rule_labels = [c.replace("DQ-", "").split("_")[0] + "_" + "_".join(c.split("_")[1:3]) for c in dq_df["check_name"]]
    pass_colors = [TEAL if r == "PASS" else (AMBER if r == "WARNING" else CRIMSON) for r in dq_df["result"]]
    axes[1, 0].barh(rule_labels, [100 - f for f in dq_df["failure_rate"]], color=pass_colors, height=0.6)
    axes[1, 0].set_xlim(95, 100.5)
    axes[1, 0].invert_yaxis()
    axes[1, 0].set_title("Data Quality Rule Pass Rates (12 Automated Checks)", fontsize=12, fontweight="bold", color=NAVY)
    axes[1, 0].set_xlabel("Compliance Rate (%)", fontsize=10, color=SLATE)
    axes[1, 0].xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}%"))
    axes[1, 0].grid(axis="x", linestyle="--", alpha=0.5)

    # 3.4 Income vs Loan Amount Scatter with Default Hue
    sample_vis = df.sample(min(10000, len(df)), random_state=42)
    sample_vis = sample_vis[sample_vis["annual_inc"] <= 250000]
    sns.scatterplot(
        data=sample_vis,
        x="annual_inc",
        y="loan_amnt",
        hue="loan_status",
        palette={"Fully Paid": TEAL, "Charged Off": CRIMSON},
        alpha=0.4,
        s=15,
        ax=axes[1, 1]
    )
    axes[1, 1].set_title("Borrower Income vs. Loan Principal Sizing", fontsize=12, fontweight="bold", color=NAVY)
    axes[1, 1].set_xlabel("Annual Income ($)", fontsize=10, color=SLATE)
    axes[1, 1].set_ylabel("Loan Amount ($)", fontsize=10, color=SLATE)
    axes[1, 1].xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    axes[1, 1].yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(out_path / "03_portfolio_vintages_and_data_quality.png", dpi=300)
    plt.close(fig)

    logger.info(f"All dashboard screenshots generated successfully in {out_path}.")


if __name__ == "__main__":
    generate_all_dashboard_visuals()
