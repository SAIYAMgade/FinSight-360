# FinSight 360: Tableau Public Desktop Dashboard Build Specification

**Project:** FinSight 360 – Banking Analytics & Credit Risk Intelligence Platform  
**Target Platform:** Tableau Public Desktop (Windows / macOS)  
**Deliverable:** 1-Page Interactive Executive Credit Risk Dashboard  
**Data Sources:** `tableau_data/*.csv` (UTF-8, aggregated, zero PII)

---

## 1. Architecture & Data Source Setup

Tableau Public connects to flat files (`.csv`) rather than direct PostgreSQL database sockets. All datasets in `tableau_data/` are pre-aggregated, anonymized, and reconciled to 0.00 delta against the analytical warehouse.

### 1.1 Data Connection Procedure
1. Open **Tableau Public Desktop**.
2. In the left navigation pane under **Connect > To a File**, click **Text file**.
3. Navigate to `<project_root>/tableau_data/` and select **`delinquency_npl_trend.csv`**.
4. In the Data Source canvas, add the remaining three files:
   - Click **Add** next to Connections and select **`exposure_by_risk_tier.csv`**.
   - Click **Add** again and select **`concentration_by_segment.csv`**.
   - Click **Add** again and select **`kpi_summary.csv`**.

### 1.2 Relationship Modeling (Logical Layer)
Tableau Public Desktop 2020.2+ uses logical relationships (noodles). Establish relationships between the primary table and supplementary tables:

```
[delinquency_npl_trend] (Root)
       |
       +--- [exposure_by_risk_tier]   ON origination_year = origination_year 
       |                                 AND risk_tier = risk_tier 
       |                                 AND segment = segment
       |
       +--- [concentration_by_segment] ON origination_year = origination_year 
       |                                 AND segment = segment 
       |                                 AND risk_tier = risk_tier
       |
       +--- [kpi_summary]              (Standalone single-row scorecard)
```

> **Alternative (Multi-Source Cross-Filtering):** If using each CSV as an independent data source, keep them separate and use Tableau's native **Apply to Worksheets > All Using Related Data Sources** on the shared filter fields (`origination_year`, `risk_tier`, `segment`). Both methods work identically.

---

## 2. Calculated Fields Library (Exact Tableau Syntax)

Create the following calculated fields in the Data pane before building worksheets.

### 2.1 Dynamic Delinquency Rate
```tableau
// Authoritative Observed Default Rate (% of loan facilities charged off)
SUM([charged_off_count]) / SUM([loan_count])
```
- **Name:** `Delinquency Rate`
- **Default Number Format:** Percentage (`0.00%`)

### 2.2 Dynamic NPL Ratio (Defaulted Exposure Share)
```tableau
// Capital loss ratio (% of original principal charged off)
SUM([charged_off_exposure]) / SUM([total_exposure])
```
- **Name:** `NPL Ratio`
- **Default Number Format:** Percentage (`0.00%`)

### 2.3 Dynamic Average Facility Sizing
```tableau
// Facility ticket size
SUM([total_exposure]) / SUM([loan_count])
```
- **Name:** `Average Loan Sizing`
- **Default Number Format:** Currency (Standard, `$#,##0`)

### 2.4 Portfolio Capital Exposure Share
```tableau
// Table-scoped capital allocation share
SUM([total_exposure]) / TOTAL(SUM([total_exposure]))
```
- **Name:** `Portfolio Exposure Share`
- **Default Number Format:** Percentage (`0.0%`)

### 2.5 High Exposure Flag Label
```tableau
IF [is_high_exposure_segment] = 1 THEN 
    "High Exposure Anchor (>=20%)" 
ELSE 
    "Standard Portfolio Segment" 
END
```
- **Name:** `Segment Exposure Category`

### 2.6 Risk Tier Monotonicity Sort Order
```tableau
CASE [risk_tier]
    WHEN "Prime Low Risk" THEN 1
    WHEN "Near Prime" THEN 2
    WHEN "Standard Consumer" THEN 3
    WHEN "Elevated Risk" THEN 4
    WHEN "Subprime" THEN 5
    WHEN "Deep Subprime" THEN 6
    WHEN "High Default Risk" THEN 7
    ELSE 8
END
```
- **Name:** `Risk Tier Sort Key`

---

## 3. Worksheet Specifications (Click-by-Click)

### Worksheet A: `Delinquency & NPL Trend` (Dual-Axis Line Chart)
- **Objective:** Track vintage maturation, comparing unit default rate against dollar-weighted capital loss rate over time.
- **Data Source:** `delinquency_npl_trend.csv`
- **Click-by-Click Instructions:**
  1. Drag `period_date` to **Columns**. Right-click the pill and choose **Continuous Month** (`Month YYYY` green pill).
  2. Drag calculated field `[Delinquency Rate]` to **Rows**.
  3. Drag calculated field `[NPL Ratio]` to the right vertical axis of the chart to trigger **Dual Axis**.
  4. Right-click the secondary axis on the right and select **Synchronize Axis**.
  5. In the **Marks** card:
     - Set Mark type to **Line** for both measures.
     - Under `[Delinquency Rate]` Marks: Set Color to **Deep Navy** (`#1E3A8A`), Line size to medium, Marker to small circles.
     - Under `[NPL Ratio]` Marks: Set Color to **Crimson** (`#BE123C`), Line size to medium with dashed styling if desired.
  6. Right-click the X-axis > **Edit Axis...** > Title: `"Loan Origination Vintage (Monthly Cohorts)"`.
  7. Right-click the Y-axis > **Edit Axis...** > Title: `"Loss & Delinquency Rate (%)"`.
  8. Click **Tooltip** on the Marks card and format as:
     ```text
     Origination Cohort: <MONTH(period_date)> <YEAR(period_date)>
     --------------------------------------------------
     Total Originated Loans: <AGG(SUM(loan_count))>
     Total Origination Capital: <AGG(SUM(total_exposure))>
     Delinquency Rate (ODR): <AGG([Delinquency Rate])>
     NPL Capital Loss Ratio: <AGG([NPL Ratio])>
     Default Write-Off Exposure: <AGG(SUM(charged_off_exposure))>
     ```

---

### Worksheet B: `Exposure by Risk Tier` (Sorted Horizontal Bar Chart)
- **Objective:** Show original capital exposure allocated to each of the 7 risk tiers, highlighting credit quality concentration.
- **Data Source:** `exposure_by_risk_tier.csv`
- **Click-by-Click Instructions:**
  1. Drag `risk_tier` to **Rows**.
  2. Drag `total_exposure` to **Columns** (aggregates as `SUM(total_exposure)`).
  3. Sort `risk_tier`: Click the sort icon on the axis or right-click `risk_tier` > **Sort...** > Sort by Field: `Risk Tier Sort Key` (Ascending) or by `total_exposure` (Descending).
  4. Drag `prime_status` to **Color** on the Marks card:
     - `Prime`: Teal (`#0D9488`)
     - `Non-Prime`: Slate Navy (`#3B82F6`)
     - `Subprime`: Amber/Crimson (`#D97706` / `#BE123C`)
  5. Drag `total_exposure` to **Label** on the Marks card. Format Label as Currency in Millions (`$#,##0.0M`).
  6. Add calculated field `[Delinquency Rate]` to **Tooltip**.
  7. Edit Tooltip:
     ```text
     Risk Tier: <risk_tier> (Grade <grade>)
     Classification: <prime_status>
     --------------------------------------------------
     Funded Exposure: <SUM(total_exposure)> (<AGG([Portfolio Exposure Share])> of portfolio)
     Total Loan Facilities: <SUM(loan_count)>
     Average Facility Size: <AGG([Average Loan Sizing])>
     Observed Delinquency Rate: <AGG([Delinquency Rate])>
     ```

---

### Worksheet C: `Concentration by Segment` (Highlighted Exposure Matrix)
- **Objective:** Surface loan purpose capital allocation, highlighting dominant anchor segments (`debt_consolidation` and `credit_card`) and detailing default risk premiums.
- **Data Source:** `concentration_by_segment.csv`
- **Click-by-Click Instructions:**
  1. Drag `segment` to **Rows**.
  2. Drag `total_exposure` to **Columns** (aggregates as `SUM(total_exposure)`).
  3. Click Sort descending on the toolbar.
  4. Drag `[Segment Exposure Category]` to **Color**:
     - `High Exposure Anchor (>=20%)`: Deep Navy (`#1E3A8A`)
     - `Standard Portfolio Segment`: Soft Slate (`#94A3B8`)
  5. Drag `[Portfolio Exposure Share]` to **Label** on the Marks card. Set label alignment to right inside/outside bar.
  6. Add `is_high_risk_segment` to Detail.
  7. Edit Tooltip:
     ```text
     Loan Purpose: <segment> (<purpose_group>)
     Exposure Classification: <[Segment Exposure Category]>
     --------------------------------------------------
     Total Exposure: <SUM(total_exposure)> (<AGG([Portfolio Exposure Share])>)
     Facility Volume: <SUM(loan_count)> loans
     Average Loan Size: <AGG([Average Loan Sizing])>
     Observed Default Rate: <AGG([Delinquency Rate])>
     High Risk Outlier: <ATTR(is_high_risk_segment)>
     ```

---

### Worksheet D: `Executive KPI Scorecard Tiles` (Card Grid)
- **Objective:** Present the 6 primary executive metrics at the top of the dashboard.
- **Data Source:** `kpi_summary.csv` (or aggregated from `delinquency_npl_trend.csv`)
- **Click-by-Click Instructions:**
  1. Create 4 separate mini KPI worksheets (or 1 combined text matrix):
     - **Card 1: Total Funded Facilities** -> Text: `total_loans` (`25,000` / `396,030`)
     - **Card 2: Total Balance Sheet Exposure** -> Text: `total_exposure` (`$352.4M` / `$5.59B`)
     - **Card 3: Baseline Delinquency Rate (ODR)** -> Text: `overall_delinquency_rate` (`19.54%` / `19.61%`)
     - **Card 4: Capital Loss Ratio (NPL / DES)** -> Text: `overall_npl_ratio` (`21.03%` / `20.73%`)
     - **Card 5: Monitored Risk Tiers** -> Text: `number_of_risk_tiers` (`7 Tiers`)
     - **Card 6: Top Anchor Concentration** -> Text: `concentration_percentage` (`62.20%` Debt Consolidation)
  2. In Marks card: Set Mark type to **Text**.
  3. Format Font: Segoe UI / Tableau Bold, size 20pt for metric value, 9pt Slate (`#64748B`) for metric label above/below.

---

## 4. Global Interactive Dashboard Filters

Configure global interactive filters so selecting a year, risk tier, or purpose updates every sheet on the canvas.

1. On Worksheet A (`Delinquency & NPL Trend`), drag the following fields to the **Filters** shelf:
   - `origination_year`: Select **All**.
   - `risk_tier`: Select **All**.
   - `segment`: Select **All**.
2. Right-click each filter pill on the Filters shelf:
   - Click **Apply to Worksheets > All Using Related Data Sources** (or **All Using This Data Source**).
3. On the Dashboard canvas, ensure filter controls appear as:
   - `Origination Year`: **Single Value (Slider)** or **Multiple Values (Dropdown)**.
   - `Risk Tier`: **Multiple Values (Dropdown)** with "Select All" enabled.
   - `Segment`: **Multiple Values (Dropdown)** with search box enabled.

---

## 5. Dashboard Canvas Layout & Assembly

### 5.1 Geometry & Fixed Sizing
- **Canvas Size:** Fixed Size **1400 x 920 pixels** (Standard 16:10 executive desktop display, no scrollbars).
- **Background Color:** `#F8FAFC` (Clean executive soft slate).

### 5.2 Visual Structure
```
+-------------------------------------------------------------------------------------------------------+
| FINSIGHT 360 | Executive Credit Risk & Portfolio Intelligence Dashboard                               |
| Management Briefing | Completed Facilities Scope | Fully Reconciled Analytical Model                  |
+-------------------------------------------------------------------------------------------------------+
| [ KPI 1: $352.4M ]  [ KPI 2: 25.0K ]  [ KPI 3: 19.54% ]  [ KPI 4: 21.03% ]  [ KPI 5: 7 Tiers ]  |
|   Total Capital       Total Loans        Delinquency        NPL Loss Ratio     Credit Hierarchy       |
+-------------------------------------------------------------------------------------------------------+
| FILTERS: [ Year: All v ]  |  [ Risk Tier: All v ]  |  [ Loan Segment: All v ]                         |
+---------------------------------------------------+---------------------------------------------------+
| WORKSHEET A: Delinquency & NPL Ratio Trend        | WORKSHEET B: Capital Exposure by Risk Tier        |
| - Dual-axis monthly vintage line chart            | - Horizontal sorted bars colored by Prime Status  |
| - Compares unit default rate vs dollar loss share | - Callout labels: exposure ($M) & delinquency rate|
+---------------------------------------------------+---------------------------------------------------+
| WORKSHEET C: Portfolio Concentration by Segment   | MANAGEMENT EXECUTIVE TAKEAWAYS                    |
| - High-exposure anchors highlighted (Navy)        | - Debt Consolidation consumes 62.2% of balance sh.|
| - Displays exposure share & default risk index    | - Subprime tiers (E-G) drive 27.6% of defaults    |
+---------------------------------------------------+---------------------------------------------------+
```

### 5.3 Color Palette Tokens
| Token | Hex Code | Visual Role |
| :--- | :--- | :--- |
| **Deep Institutional Navy** | `#1E3A8A` | Primary headers, Delinquency Rate line, High-Exposure Anchor bars |
| **Teal / Performing Green** | `#0D9488` | Prime risk tier bars, Fully Paid indicators |
| **Warning Amber** | `#D97706` | Elevated / Near-Prime risk tiers |
| **Severe Crimson** | `#BE123C` | NPL ratio line, Subprime risk tiers, Charge-Off indicators |
| **Slate Gray** | `#64748B` | Subheaders, gridlines, axis labels |
| **Soft Slate Background** | `#F8FAFC` | Main dashboard canvas background |

---

## 6. Publishing to Tableau Public & Screenshot Guide

1. In Tableau Public Desktop, navigate to top menu: **Server > Tableau Public > Save to Tableau Public As...**
2. Sign in with your Tableau Public credentials.
3. Title the workbook: **`FinSight 360 - Banking Analytics & Credit Risk Dashboard`**.
4. In workbook publishing settings:
   - Ensure sheets are hidden; publish only the finalized **Dashboard** tab.
   - Enable **Show workbook sheets as tabs** (Uncheck).
   - Allow others to download the workbook: **Checked**.
5. Once published, Tableau Public will open your dashboard in the browser:
   - Copy the live URL (e.g., `https://public.tableau.com/views/FinSight360/...`).
   - Click the **Download** button > **Image** (PNG format) or take a full-screen screenshot (1920x1080).
   - Save the screenshot to `<project_root>/docs/images/tableau_dashboard.png`.
6. Update the placeholder `<TABLEAU_PUBLIC_URL>` in `README.md` with your published link.
