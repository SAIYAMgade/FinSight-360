"""Generate institutional-grade Excel workbook for FinSight 360."""
from pathlib import Path
import logging
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("finsight360.excel")

# Institutional Banking Styling Tokens
COLOR_PRIMARY = "1E3A8A"      # Deep Navy
COLOR_SECONDARY = "0D9488"    # Teal
COLOR_ACCENT = "BE123C"       # Crimson
COLOR_LIGHT_GRAY = "F1F5F9"   # Slate 100
COLOR_HEADER_FILL = "1E3A8A"  # Table headers Navy
COLOR_SUBHEADER = "334155"    # Slate 700

FONT_NAME = "Segoe UI"
FONT_TITLE = Font(name=FONT_NAME, size=16, bold=True, color="1E3A8A")
FONT_SECTION = Font(name=FONT_NAME, size=12, bold=True, color="1E3A8A")
FONT_HEADER = Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")
FONT_DATA = Font(name=FONT_NAME, size=10, bold=False, color="000000")
FONT_TOTAL = Font(name=FONT_NAME, size=10, bold=True, color="000000")

FILL_HEADER = PatternFill(start_color=COLOR_PRIMARY, end_color=COLOR_PRIMARY, fill_type="solid")
FILL_SUBHEADER = PatternFill(start_color=COLOR_LIGHT_GRAY, end_color=COLOR_LIGHT_GRAY, fill_type="solid")
FILL_PASS = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")     # Light green
FILL_WARN = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")     # Light yellow
FILL_FAIL = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")     # Light red

THIN_BORDER = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="thin", color="CBD5E1")
)
TOTAL_BORDER = Border(
    top=Side(style="thin", color="000000"),
    bottom=Side(style="double", color="000000")
)

# Number Formats
FMT_CURRENCY = "$#,##0"
FMT_PERCENT = "0.00%"
FMT_INTEGER = "#,##0"
FMT_DECIMAL = "0.00"


def autofit_columns(ws, max_len_cap=45):
    """Auto-adjust worksheet column widths based on cell contents."""
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), max_len_cap)


def build_excel_workbook(
    parquet_path: str = "data/processed/lending_club_cleaned.parquet",
    output_path: str = "excel/FinSight_360_Executive_Report.xlsx"
) -> None:
    """Generate multi-tab executive management reporting workbook."""
    logger.info(f"Loading cleaned dataset from {parquet_path} for Excel generation...")
    df = pd.read_parquet(parquet_path)
    dq_df = pd.read_csv("reports/data_quality_results.csv")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Remove default blank sheet

    # =========================================================================
    # SHEET 1: EXECUTIVE SUMMARY
    # =========================================================================
    logger.info("Building Sheet 1: Executive_Summary...")
    ws1 = wb.create_sheet(title="Executive_Summary")
    ws1.views.sheetView[0].showGridLines = True

    # Title Block
    ws1["A1"] = "FINSIGHT 360 | EXECUTIVE LENDING PORTFOLIO REPORT"
    ws1["A1"].font = FONT_TITLE
    ws1["A2"] = "Management Intelligence Briefing | Analysis Period: June 2007 – December 2016"
    ws1["A2"].font = Font(name=FONT_NAME, size=10, italic=True, color="64748B")

    # Key Performance Indicators Table
    ws1["A4"] = "CORE PORTFOLIO METRICS"
    ws1["A4"].font = FONT_SECTION

    headers1 = ["Metric Name", "Portfolio Value", "Unit / Format", "Analytical Interpretation"]
    for c_idx, h in enumerate(headers1, 1):
        cell = ws1.cell(row=5, column=c_idx, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = Alignment(horizontal="center" if c_idx > 1 else "left")

    kpi_rows = [
        ("Total Closed Facilities", len(df), FMT_INTEGER, "Total completed loan contracts in evaluation scope"),
        ("Total Funded Capital Exposure", df["loan_amnt"].sum(), FMT_CURRENCY, "Aggregate original principal funded across portfolio"),
        ("Average Facility Size", df["loan_amnt"].mean(), FMT_CURRENCY, "Arithmetic mean of facility loan principal"),
        ("Median Facility Size", df["loan_amnt"].median(), FMT_CURRENCY, "Median facility size (reduces high-ticket skew)"),
        ("Average Nominal Contract Rate", df["int_rate"].mean() / 100.0, FMT_PERCENT, "Nominal portfolio gross yield benchmark"),
        ("Average Debt-to-Income (DTI)", df["dti"].mean(), FMT_DECIMAL, "Average borrower monthly debt leverage ratio"),
        ("Average Borrower Annual Income", df["annual_inc"].mean(), FMT_CURRENCY, "Mean self-reported gross annual borrower capacity"),
        ("Fully Paid Facilities Count", (df["is_default"] == 0).sum(), FMT_INTEGER, "Borrowers who repaid principal and interest in full"),
        ("Charged Off Facilities Count", (df["is_default"] == 1).sum(), FMT_INTEGER, "Facilities written off as uncollectible credit losses"),
        ("Observed Default Rate", (df["is_default"] == 1).mean(), FMT_PERCENT, "Primary benchmark portfolio credit loss rate"),
        ("Defaulted Capital Exposure", df[df["is_default"] == 1]["loan_amnt"].sum(), FMT_CURRENCY, "Original principal funded on defaulted facilities"),
        ("Defaulted Capital Exposure Share", df[df["is_default"] == 1]["loan_amnt"].sum() / df["loan_amnt"].sum(), FMT_PERCENT, "Dollar-weighted portfolio credit loss share")
    ]

    for r_idx, (m_name, m_val, m_fmt, m_desc) in enumerate(kpi_rows, 6):
        ws1.cell(row=r_idx, column=1, value=m_name).font = FONT_DATA
        c2 = ws1.cell(row=r_idx, column=2, value=m_val)
        c2.font = FONT_DATA
        c2.number_format = m_fmt
        c2.alignment = Alignment(horizontal="right")
        ws1.cell(row=r_idx, column=3, value=m_fmt).font = Font(name=FONT_NAME, size=9, color="64748B")
        ws1.cell(row=r_idx, column=4, value=m_desc).font = FONT_DATA
        for c in range(1, 5):
            ws1.cell(row=r_idx, column=c).border = THIN_BORDER

    # Executive Commentary Block
    ws1["A19"] = "EXECUTIVE FINDINGS & MANAGEMENT BRIEFING"
    ws1["A19"].font = FONT_SECTION

    commentary = [
        "1. Risk Grade Monotonicity: Observed default rates escalate monotonically from 6.29% in Grade A to 45.84% in Grade G.",
        "2. Term Structure Risk: 60-month facilities exhibit a 31.74% default rate, nearly 2.0x higher than 36-month facilities (16.00%).",
        "3. High-Leverage Spikes: Borrowers with DTI exceeding 25% experience a 23.4% default rate, warranting strict underwriting caps.",
        "4. Purpose Concentration: Debt consolidation represents 59.2% ($3.31B) of exposure. Small business loans exhibit 29.45% default rates.",
        "5. Data Quality Assurance: 10 of 12 rules passed cleanly; 1 zero-income exception identified and isolated; 8 extreme DTI outliers flagged."
    ]
    for idx, c_text in enumerate(commentary, 20):
        cell = ws1.cell(row=idx, column=1, value=c_text)
        cell.font = Font(name=FONT_NAME, size=10, italic=False, color="1E293B")

    # Workbook Navigation Block
    ws1["A26"] = "WORKBOOK SHEET INDEX"
    ws1["A26"].font = FONT_SECTION
    nav_items = [
        ("Sheet 2: Portfolio_Analysis", "Breakdown by loan status, term duration, and comprehensive loan purpose performance"),
        ("Sheet 3: Credit_Risk_Analysis", "Segment diagnostics across underwriting risk grades, DTI leverage, and income bands"),
        ("Sheet 4: Trends_and_Vintages", "Chronological origination trends and vintage default cohort maturation tracking"),
        ("Sheet 5: Data_Quality", "Automated 12-rule validation audit log, severity rankings, and compliance metrics"),
        ("Sheet 6: Data_Dictionary", "Comprehensive definitions, data types, and analytical usage for all data attributes")
    ]
    for idx, (tab, desc) in enumerate(nav_items, 27):
        ws1.cell(row=idx, column=1, value=tab).font = Font(name=FONT_NAME, size=10, bold=True, color=COLOR_PRIMARY)
        ws1.cell(row=idx, column=2, value=desc).font = FONT_DATA

    autofit_columns(ws1)

    # =========================================================================
    # SHEET 2: PORTFOLIO ANALYSIS
    # =========================================================================
    logger.info("Building Sheet 2: Portfolio_Analysis...")
    ws2 = wb.create_sheet(title="Portfolio_Analysis")
    ws2.views.sheetView[0].showGridLines = True
    ws2.freeze_panes = "A5"

    ws2["A1"] = "PORTFOLIO VOLUME & REPAYMENT STATUS ANALYSIS"
    ws2["A1"].font = FONT_TITLE

    # Table 2A: Terminal Loan Status
    ws2["A3"] = "1. Terminal Repayment Status Profile"
    ws2["A3"].font = FONT_SECTION
    status_headers = ["Loan Status", "Facility Count", "Volume Share (%)", "Total Principal ($)", "Exposure Share (%)", "Average Ticket ($)"]
    for c, h in enumerate(status_headers, 1):
        cell = ws2.cell(row=4, column=c, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = Alignment(horizontal="center" if c > 1 else "left")

    status_grp = df.groupby("loan_status").agg(
        count=("loan_amnt", "count"),
        total=("loan_amnt", "sum"),
        avg=("loan_amnt", "mean")
    ).reset_index()

    total_vol = df["loan_amnt"].sum()
    total_cnt = len(df)

    for r, row in enumerate(status_grp.itertuples(), 5):
        ws2.cell(row=r, column=1, value=row.loan_status).font = FONT_DATA
        c2 = ws2.cell(row=r, column=2, value=row.count)
        c2.number_format = FMT_INTEGER
        c3 = ws2.cell(row=r, column=3, value=row.count / total_cnt)
        c3.number_format = FMT_PERCENT
        c4 = ws2.cell(row=r, column=4, value=row.total)
        c4.number_format = FMT_CURRENCY
        c5 = ws2.cell(row=r, column=5, value=row.total / total_vol)
        c5.number_format = FMT_PERCENT
        c6 = ws2.cell(row=r, column=6, value=row.avg)
        c6.number_format = FMT_CURRENCY
        for c in range(1, 7):
            ws2.cell(row=r, column=c).border = THIN_BORDER

    # Total Row for Status
    tot_row = len(status_grp) + 5
    ws2.cell(row=tot_row, column=1, value="Portfolio Total").font = FONT_TOTAL
    c_cnt = ws2.cell(row=tot_row, column=2, value=f"=SUM(B5:B{tot_row-1})")
    c_cnt.number_format = FMT_INTEGER
    c_cnt.font = FONT_TOTAL
    c_pct1 = ws2.cell(row=tot_row, column=3, value=f"=SUM(C5:C{tot_row-1})")
    c_pct1.number_format = FMT_PERCENT
    c_pct1.font = FONT_TOTAL
    c_exp = ws2.cell(row=tot_row, column=4, value=f"=SUM(D5:D{tot_row-1})")
    c_exp.number_format = FMT_CURRENCY
    c_exp.font = FONT_TOTAL
    c_pct2 = ws2.cell(row=tot_row, column=5, value=f"=SUM(E5:E{tot_row-1})")
    c_pct2.number_format = FMT_PERCENT
    c_pct2.font = FONT_TOTAL
    c_avg = ws2.cell(row=tot_row, column=6, value=f"=AVERAGE(F5:F{tot_row-1})")
    c_avg.number_format = FMT_CURRENCY
    c_avg.font = FONT_TOTAL
    for c in range(1, 7):
        ws2.cell(row=tot_row, column=c).border = TOTAL_BORDER

    # Table 2B: Loan Purpose Breakdown
    p_start = tot_row + 3
    ws2.cell(row=p_start, column=1, value="2. Loan Purpose Exposure & Performance Breakdown").font = FONT_SECTION
    purp_headers = ["Loan Purpose", "Facility Count", "Exposure Share (%)", "Total Funded ($)", "Average Ticket ($)", "Average Rate (%)", "Charged Off Count", "Default Rate (%)"]
    for c, h in enumerate(purp_headers, 1):
        cell = ws2.cell(row=p_start+1, column=c, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = Alignment(horizontal="center" if c > 1 else "left")

    purp_grp = df.groupby("purpose").agg(
        count=("loan_amnt", "count"),
        total=("loan_amnt", "sum"),
        avg_amt=("loan_amnt", "mean"),
        avg_rate=("int_rate", "mean"),
        defaults=("is_default", "sum")
    ).reset_index().sort_values(by="total", ascending=False)

    for r, row in enumerate(purp_grp.itertuples(), p_start+2):
        ws2.cell(row=r, column=1, value=row.purpose).font = FONT_DATA
        ws2.cell(row=r, column=2, value=row.count).number_format = FMT_INTEGER
        ws2.cell(row=r, column=3, value=row.total / total_vol).number_format = FMT_PERCENT
        ws2.cell(row=r, column=4, value=row.total).number_format = FMT_CURRENCY
        ws2.cell(row=r, column=5, value=row.avg_amt).number_format = FMT_CURRENCY
        ws2.cell(row=r, column=6, value=row.avg_rate / 100.0).number_format = FMT_PERCENT
        ws2.cell(row=r, column=7, value=row.defaults).number_format = FMT_INTEGER
        ws2.cell(row=r, column=8, value=row.defaults / row.count).number_format = FMT_PERCENT
        for c in range(1, 9):
            ws2.cell(row=r, column=c).border = THIN_BORDER

    autofit_columns(ws2)

    # =========================================================================
    # SHEET 3: CREDIT RISK ANALYSIS
    # =========================================================================
    logger.info("Building Sheet 3: Credit_Risk_Analysis...")
    ws3 = wb.create_sheet(title="Credit_Risk_Analysis")
    ws3.views.sheetView[0].showGridLines = True
    ws3.freeze_panes = "A5"

    ws3["A1"] = "CREDIT RISK SEGMENTATION & DEFAULT INTELLIGENCE"
    ws3["A1"].font = FONT_TITLE

    # Table 3A: Risk Grade Matrix
    ws3["A3"] = "1. Underwriting Risk Grade Performance Matrix"
    ws3["A3"].font = FONT_SECTION
    grade_headers = ["Risk Grade", "Facility Count", "Exposure Share (%)", "Total Capital ($)", "Average Ticket ($)", "Average Interest Rate (%)", "Average DTI", "Observed Default Rate (%)"]
    for c, h in enumerate(grade_headers, 1):
        cell = ws3.cell(row=4, column=c, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = Alignment(horizontal="center" if c > 1 else "left")

    grade_grp = df.groupby("grade").agg(
        count=("loan_amnt", "count"),
        total=("loan_amnt", "sum"),
        avg_amt=("loan_amnt", "mean"),
        avg_rate=("int_rate", "mean"),
        avg_dti=("dti", "mean"),
        defaults=("is_default", "sum")
    ).reset_index().sort_values(by="grade")

    for r, row in enumerate(grade_grp.itertuples(), 5):
        ws3.cell(row=r, column=1, value=row.grade).font = Font(name=FONT_NAME, bold=True)
        ws3.cell(row=r, column=2, value=row.count).number_format = FMT_INTEGER
        ws3.cell(row=r, column=3, value=row.total / total_vol).number_format = FMT_PERCENT
        ws3.cell(row=r, column=4, value=row.total).number_format = FMT_CURRENCY
        ws3.cell(row=r, column=5, value=row.avg_amt).number_format = FMT_CURRENCY
        ws3.cell(row=r, column=6, value=row.avg_rate / 100.0).number_format = FMT_PERCENT
        ws3.cell(row=r, column=7, value=row.avg_dti).number_format = FMT_DECIMAL
        c8 = ws3.cell(row=r, column=8, value=row.defaults / row.count)
        c8.number_format = FMT_PERCENT
        c8.font = Font(name=FONT_NAME, bold=True, color=COLOR_ACCENT if (row.defaults / row.count) > 0.20 else "000000")
        for c in range(1, 9):
            ws3.cell(row=r, column=c).border = THIN_BORDER

    # Table 3B: DTI Leverage Performance
    d_start = len(grade_grp) + 7
    ws3.cell(row=d_start, column=1, value="2. Debt-to-Income (DTI) Leverage Performance").font = FONT_SECTION
    dti_headers = ["DTI Leverage Band", "Facility Count", "Total Funded ($)", "Average Ticket ($)", "Average Rate (%)", "Observed Default Rate (%)"]
    for c, h in enumerate(dti_headers, 1):
        cell = ws3.cell(row=d_start+1, column=c, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = Alignment(horizontal="center" if c > 1 else "left")

    dti_order = ["< 10%", "10% - 15%", "15% - 20%", "20% - 25%", "25% - 30%", "30%+"]
    dti_grp = df.groupby("dti_band").agg(
        count=("loan_amnt", "count"),
        total=("loan_amnt", "sum"),
        avg_amt=("loan_amnt", "mean"),
        avg_rate=("int_rate", "mean"),
        defaults=("is_default", "sum")
    ).reindex(dti_order).dropna().reset_index()

    for r, row in enumerate(dti_grp.itertuples(), d_start+2):
        ws3.cell(row=r, column=1, value=row.dti_band).font = FONT_DATA
        ws3.cell(row=r, column=2, value=row.count).number_format = FMT_INTEGER
        ws3.cell(row=r, column=3, value=row.total).number_format = FMT_CURRENCY
        ws3.cell(row=r, column=4, value=row.avg_amt).number_format = FMT_CURRENCY
        ws3.cell(row=r, column=5, value=row.avg_rate / 100.0).number_format = FMT_PERCENT
        c_dr = ws3.cell(row=r, column=6, value=row.defaults / row.count)
        c_dr.number_format = FMT_PERCENT
        c_dr.font = Font(name=FONT_NAME, bold=True, color=COLOR_ACCENT if (row.defaults / row.count) > 0.20 else "000000")
        for c in range(1, 7):
            ws3.cell(row=r, column=c).border = THIN_BORDER

    autofit_columns(ws3)

    # =========================================================================
    # SHEET 4: TRENDS AND VINTAGES
    # =========================================================================
    logger.info("Building Sheet 4: Trends_and_Vintages...")
    ws4 = wb.create_sheet(title="Trends_and_Vintages")
    ws4.views.sheetView[0].showGridLines = True
    ws4.freeze_panes = "A5"

    ws4["A1"] = "ORIGINATION VINTAGE COHORT & TIME-SERIES INTELLIGENCE"
    ws4["A1"].font = FONT_TITLE
    ws4["A3"] = "Annual Origination Trends & Vintage Default Maturation (2007–2016)"
    ws4["A3"].font = FONT_SECTION

    vintage_headers = ["Vintage Year", "Originated Loans", "Origination Capital ($)", "YoY Volume Growth (%)", "Average Loan Sizing ($)", "Average Contract Rate (%)", "Charged Off Loans", "Vintage Default Rate (%)"]
    for c, h in enumerate(vintage_headers, 1):
        cell = ws4.cell(row=4, column=c, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = Alignment(horizontal="center" if c > 1 else "left")

    v_grp = df.groupby("issue_year").agg(
        count=("loan_amnt", "count"),
        total=("loan_amnt", "sum"),
        avg_amt=("loan_amnt", "mean"),
        avg_rate=("int_rate", "mean"),
        defaults=("is_default", "sum")
    ).reset_index().sort_values(by="issue_year")

    v_grp["yoy_growth"] = v_grp["total"].pct_change()

    for r, row in enumerate(v_grp.itertuples(), 5):
        ws4.cell(row=r, column=1, value=int(row.issue_year)).font = Font(name=FONT_NAME, bold=True)
        ws4.cell(row=r, column=2, value=row.count).number_format = FMT_INTEGER
        ws4.cell(row=r, column=3, value=row.total).number_format = FMT_CURRENCY
        c_yoy = ws4.cell(row=r, column=4, value=row.yoy_growth if pd.notnull(row.yoy_growth) else "-")
        if pd.notnull(row.yoy_growth):
            c_yoy.number_format = FMT_PERCENT
        ws4.cell(row=r, column=5, value=row.avg_amt).number_format = FMT_CURRENCY
        ws4.cell(row=r, column=6, value=row.avg_rate / 100.0).number_format = FMT_PERCENT
        ws4.cell(row=r, column=7, value=row.defaults).number_format = FMT_INTEGER
        c_vdr = ws4.cell(row=r, column=8, value=row.defaults / row.count)
        c_vdr.number_format = FMT_PERCENT
        c_vdr.font = Font(name=FONT_NAME, bold=True)
        for c in range(1, 9):
            ws4.cell(row=r, column=c).border = THIN_BORDER

    autofit_columns(ws4)

    # =========================================================================
    # SHEET 5: DATA QUALITY
    # =========================================================================
    logger.info("Building Sheet 5: Data_Quality...")
    ws5 = wb.create_sheet(title="Data_Quality")
    ws5.views.sheetView[0].showGridLines = True
    ws5.freeze_panes = "A5"

    ws5["A1"] = "DATA GOVERNANCE & AUTOMATED AUDIT RESULTS"
    ws5["A1"].font = FONT_TITLE
    ws5["A3"] = "Rule-by-Rule Compliance & Exception Audit Log"
    ws5["A3"].font = FONT_SECTION

    dq_headers = ["Rule Identifier", "Severity", "Records Checked", "Failures Found", "Failure Rate (%)", "Audit Result", "Rule Description & Business Rationale", "Audit Timestamp"]
    for c, h in enumerate(dq_headers, 1):
        cell = ws5.cell(row=4, column=c, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = Alignment(horizontal="center" if c in [2, 6] else "left")

    for r, row in enumerate(dq_df.itertuples(), 5):
        ws5.cell(row=r, column=1, value=row.check_name).font = Font(name=FONT_NAME, bold=True)
        ws5.cell(row=r, column=2, value=row.severity).font = FONT_DATA
        ws5.cell(row=r, column=3, value=row.records_checked).number_format = FMT_INTEGER
        ws5.cell(row=r, column=4, value=row.failures_found).number_format = FMT_INTEGER
        ws5.cell(row=r, column=5, value=row.failure_rate / 100.0).number_format = "0.0000%"

        c_res = ws5.cell(row=r, column=6, value=row.result)
        c_res.font = Font(name=FONT_NAME, bold=True)
        c_res.alignment = Alignment(horizontal="center")
        if row.result == "PASS":
            c_res.fill = FILL_PASS
        elif row.result == "WARNING":
            c_res.fill = FILL_WARN
        else:
            c_res.fill = FILL_FAIL

        ws5.cell(row=r, column=7, value=row.details).font = FONT_DATA
        ws5.cell(row=r, column=8, value=str(row.timestamp)[:19]).font = Font(name=FONT_NAME, size=9, color="64748B")
        for c in range(1, 9):
            ws5.cell(row=r, column=c).border = THIN_BORDER

    autofit_columns(ws5)

    # =========================================================================
    # SHEET 6: DATA DICTIONARY
    # =========================================================================
    logger.info("Building Sheet 6: Data_Dictionary...")
    ws6 = wb.create_sheet(title="Data_Dictionary")
    ws6.views.sheetView[0].showGridLines = True
    ws6.freeze_panes = "A5"

    ws6["A1"] = "FINSIGHT 360 | ANALYTICAL DATA DICTIONARY"
    ws6["A1"].font = FONT_TITLE
    ws6["A3"] = "Schema Definitions, Data Types, and Business Logic Mappings"
    ws6["A3"].font = FONT_SECTION

    dict_headers = ["Field Name", "Layer / Origin", "Data Type", "Business Definition & Transformation Notes"]
    for c, h in enumerate(dict_headers, 1):
        cell = ws6.cell(row=4, column=c, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER

    dict_items = [
        ("loan_id", "Derived (Pipeline)", "VARCHAR(50)", "Deterministic unique loan identifier (LN-1000001 ...)"),
        ("loan_amnt", "Raw LendingClub", "NUMERIC(12,2)", "Original principal amount applied for and funded ($)"),
        ("term", "Cleaned", "VARCHAR(20)", "Duration of the loan contract ('36 months' or '60 months')"),
        ("term_months", "Derived (Pipeline)", "INTEGER", "Numeric loan term duration (36 or 60)"),
        ("int_rate", "Raw LendingClub", "NUMERIC(6,2)", "Annualized nominal interest rate on the loan facility (%)"),
        ("installment", "Raw LendingClub", "NUMERIC(10,2)", "Monthly payment owed by borrower including principal and interest"),
        ("grade", "Raw LendingClub", "VARCHAR(5)", "LendingClub assigned underwriting risk grade (A through G)"),
        ("sub_grade", "Raw LendingClub", "VARCHAR(10)", "Granular subgrade credit classification (A1 to G5)"),
        ("home_ownership", "Cleaned", "VARCHAR(20)", "Standardized home ownership status (MORTGAGE, RENT, OWN, OTHER)"),
        ("annual_inc", "Raw LendingClub", "NUMERIC(14,2)", "Self-reported borrower gross annual income ($)"),
        ("verification_status", "Raw LendingClub", "VARCHAR(50)", "Income verification status (Verified, Source Verified, Not Verified)"),
        ("issue_date", "Derived (Pipeline)", "DATE", "Origination funding date parsed as standard ISO Gregorian date"),
        ("loan_status", "Raw LendingClub", "VARCHAR(50)", "Terminal repayment contract status ('Fully Paid' vs 'Charged Off')"),
        ("is_default", "Target Variable", "INTEGER", "Binary credit default indicator: 1 = Charged Off, 0 = Fully Paid"),
        ("purpose", "Raw LendingClub", "VARCHAR(50)", "Borrower-stated use of loan proceeds (e.g. debt_consolidation)"),
        ("dti", "Raw LendingClub", "NUMERIC(8,2)", "Debt-to-income ratio: non-mortgage monthly debt obligations / monthly income"),
        ("addr_state", "Derived (Cleaned)", "VARCHAR(10)", "Two-letter US state postal code extracted from borrower address"),
        ("zip_code", "Derived (Cleaned)", "VARCHAR(10)", "Five-digit borrower postal code extracted from address"),
        ("emp_length_years", "Derived (Pipeline)", "NUMERIC(4,1)", "Borrower employment tenure standardized in numeric years (0.5 to 10.0)"),
        ("credit_history_years", "Derived (Pipeline)", "NUMERIC(5,1)", "Borrower credit history length at origination in years"),
        ("loan_amount_band", "Segmentation Band", "VARCHAR(20)", "Binned loan principal sizing (< $5k, $5k-$10k, ..., $30k+)"),
        ("dti_band", "Segmentation Band", "VARCHAR(20)", "Binned borrower DTI leverage (< 10%, 10-15%, ..., 30%+)"),
        ("income_band", "Segmentation Band", "VARCHAR(20)", "Binned annual income (< $30k, $30k-$50k, ..., $150k+)"),
        ("installment_burden_pct", "Derived (Pipeline)", "NUMERIC(6,2)", "Annual installment burden as percentage of annual income (%)"),
        ("is_high_risk_segment", "Segmentation Flag", "INTEGER", "Binary flag: 1 if Grade in E/F/G or DTI >= 25.0, else 0")
    ]

    for r, (fname, forigin, ftype, fdesc) in enumerate(dict_items, 5):
        ws6.cell(row=r, column=1, value=fname).font = Font(name=FONT_NAME, bold=True)
        ws6.cell(row=r, column=2, value=forigin).font = FONT_DATA
        ws6.cell(row=r, column=3, value=ftype).font = Font(name=FONT_NAME, italic=True, color="475569")
        ws6.cell(row=r, column=4, value=fdesc).font = FONT_DATA
        for c in range(1, 5):
            ws6.cell(row=r, column=c).border = THIN_BORDER

    autofit_columns(ws6)

    # Save finalized workbook
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    logger.info(f"Excel executive workbook generated successfully at: {output_path}")


if __name__ == "__main__":
    build_excel_workbook()
