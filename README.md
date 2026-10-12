
# Discount & Profitability Diagnostic

A business analytics project using Python, pandas, Excel, and Tableau to investigate sales, profit margins, and observed discount patterns in the Superstore dataset.

## Business Problem

Where are discounts associated with weaker profitability, and which product categories or business areas should management investigate?

The goal is to turn transaction-level data into clear business metrics and actionable investigation priorities.

## Project Objectives

- Measure overall sales, profit, and profit margin.
- Compare profitability across product categories and sub-categories.
- Investigate relationships between discount bands and profit.
- Compare profitability across regions.
- Track sales and profit over time.
- Present results through an interactive Tableau dashboard.

## Tools

- **Python:** analysis and data-quality checks
- **pandas:** data cleaning, grouping, and aggregation
- **Excel:** original workbook
- **Tableau Public:** planned interactive visualization
- **Git and GitHub:** version control and project documentation

## Dataset

The project uses a Superstore-style sample workbook containing order, product, customer, geographic, sales, discount, and profit fields.

Official Tableau sample data:
https://public.tableau.com/app/learn/sample-data

The dataset is fictional training data. Its recorded dates range from January 2023 to December 2026; the date range should be verified against the source before being interpreted as historical business data.

The original Excel file is excluded from Git using `.gitignore`.

## Project Structure

```text
discount-profitability-diagnostic/
├── data/
│   ├── processed/
│   └── sample_-_superstore.xls   # local only; excluded from Git
├── docs/
├── notebooks/
├── outputs/
├── screenshots/
├── src/
│   ├── 01_data_audit.py
│   └── 02_analyze_superstore.py
├── insights.md
├── requirements.txt
└── README.md
```

## Key Results from Python Analysis

| Metric | Result |
|---|---:|
| Transaction rows analysed | 10,194 |
| Distinct orders | 5,111 |
| Units sold | 38,654 |
| Total sales | 2,326,534.35 |
| Total profit | 292,296.81 |
| Overall profit margin | 12.56% |
| Average row-level discount | 15.54% |

### Initial Findings

1. The group with discounts above 30% has recorded profit of approximately -125,507.24 and a profit margin of -48.22%.
2. The no-discount group has recorded profit of approximately 326,718.59 and a profit margin of 29.56%.
3. Tables, Bookcases, and Supplies are among the sub-categories with negative total profit in the supplied workbook.

These comparisons identify areas for further investigation. They do not establish that discounts caused losses.

Detailed findings and limitations are documented in [`insights.md`](insights.md).

## Metrics

- **Total Sales:** Sum of recorded sales.
- **Total Profit:** Sum of recorded profit.
- **Profit Margin:** Total Profit / Total Sales.
- **Distinct Orders:** Count of unique Order ID values.
- **Average Discount:** Simple average of transaction-row discount values.
- **Discount Band:** Exploratory grouping of discount levels.

## Run the Python Analysis

### 1. Create and activate a virtual environment

On macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the data audit

```bash
python src/01_data_audit.py
```

### 4. Run the analysis

```bash
python src/02_analyze_superstore.py
```

The analysis writes summary CSV files to the `outputs/` directory.

The local Excel workbook is required to run the scripts and must be obtained separately from the official sample-data source.

## Tableau Dashboard

- **Dashboard URL:** To be added after publication.
- **Screenshot:** To be added in `screenshots/`.

The planned dashboard will include KPI cards, profit by sub-category, profit margin by discount band, and monthly sales/profit trends.

## Limitations

- The dataset is fictional sample data.
- The analysis is observational and does not prove causality.
- Discount bands are project-defined.
- The supplied workbook's date range requires verification.
- Currency should be labelled only after verifying the workbook's source and units.

## Author

Sana Khan
