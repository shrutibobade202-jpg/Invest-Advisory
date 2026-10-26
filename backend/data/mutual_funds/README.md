# GoalInvest Advisor — Mutual Fund Datasets

## 1. Overview
This directory contains real, structured mutual fund data for the **GoalInvest Advisor** platform. It provides scheme details, metrics, categorization, risk ratings, and historical Net Asset Value (NAV) records.

## 2. Dataset Files

### `mutual_fund_dataset.csv`
- **Total Records**: 814 mutual fund schemes.
- **Source**: Industry-standard verified mutual fund portfolio database merged with official AMFI (Association of Mutual Funds in India) daily Net Asset Value reporting.
- **AMFI Direct Match Coverage**: 537 schemes enriched with official AMFI Scheme Code, ISIN, and verified NAV.
- **Key Fields**:
  - `scheme_name`: Full scheme name as registered.
  - `scheme_code`: Official AMFI Scheme Code (where mapped).
  - `category`: Asset class (Equity, Debt, Hybrid, Solution Oriented, Other).
  - `sub_category`: Investment mandate (Large Cap, Mid Cap, Small Cap, Flexi Cap, Corporate Bond, etc.).
  - `amc_name`: Asset Management Company / Fund House (e.g., HDFC, ICICI Prudential, Axis, Mirae Asset).
  - `min_sip`: Minimum monthly SIP installment amount in INR (₹).
  - `min_lumpsum`: Minimum initial lump-sum investment in INR (₹).
  - `expense_ratio`: Total Expense Ratio (TER) in percentage (%).
  - `fund_size_cr`: Assets Under Management (AUM) in ₹ Crores.
  - `fund_age_yr`: Age of the fund in years.
  - `fund_manager`: Primary portfolio manager.
  - `risk_level`: SEBI Riskometer level (1 = Low to 6 = Very High).
  - `rating`: Overall Value Research / Morningstar quantitative rating (1 to 5 stars).
  - `returns_1yr`, `returns_3yr`, `returns_5yr`: Historical annualized returns (CAGR) in percentage.
  - `sortino`, `sharpe`, `alpha`, `beta`, `sd`: Quantitative risk-adjusted performance ratios.
  - `nav`: Net Asset Value in INR (from AMFI).
  - `nav_date`: Official NAV valuation date.
  - `plan_type`: Direct Plan vs. Regular Plan.
  - `option_type`: Growth Option vs. IDCW Option.

### `historical_nav.csv`
- **Records**: 6000 daily historical NAV records across representative benchmark schemes.
- **Source**: Official AMFI scheme NAV time-series via open AMFI NAV data service (`api.mfapi.in`).
- **Date Range**: Multi-year daily trading history up to October 2026.
- **Fields**:
  - `scheme_code`: AMFI scheme identifier.
  - `scheme_name`: Name of the fund scheme.
  - `category`: Equity / Debt / Hybrid.
  - `sub_category`: Fund subcategory.
  - `date`: Trading date (DD-MM-YYYY).
  - `nav`: Net Asset Value per unit.

## 3. Data Integrity & Compliance Notice
- **No Fabricated Records**: All schemes, performance metrics, risk ratings, and NAV points originate from verified public datasets and official AMFI publications.
- **Educational Disclaimer**: Historical returns and past NAV trends are for educational comparison only and do not guarantee future returns. Mutual fund investments are subject to market risks.
- **Update Frequency**: Live NAV updates are published by AMFI on business days by 11:00 PM IST. The datasets can be refreshed using `python backend/scripts/load_mutual_fund_dataset.py`.
