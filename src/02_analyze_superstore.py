
"""Analyze Superstore sales, profit, discounts, and monthly trends."""

from pathlib import Path
import pandas as pd


# Find the project root automatically.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# The dataset is currently in data/.
DATA_FOLDERS = [
    PROJECT_ROOT / "data",
    PROJECT_ROOT / "data" / "raw",
]

SUPPORTED_EXTENSIONS = {".xls", ".xlsx", ".csv"}

REQUIRED_COLUMNS = [
    "Order ID",
    "Order Date",
    "Region",
    "Category",
    "Sub-Category",
    "Sales",
    "Quantity",
    "Discount",
    "Profit",
]


def find_dataset():
    """Find the Excel or CSV dataset."""

    for folder in DATA_FOLDERS:
        if not folder.exists():
            continue

        files = sorted(
            file
            for file in folder.iterdir()
            if file.is_file()
            and file.suffix.lower() in SUPPORTED_EXTENSIONS
            and not file.name.startswith("~$")
        )

        if files:
            return files[0]

    raise FileNotFoundError(
        "Dataset not found. Place the Superstore Excel file "
        "inside the project's data/ folder."
    )


def load_dataset(file_path):
    """Read the Orders sheet from Excel or read a CSV."""

    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)

    workbook = pd.ExcelFile(file_path)

    sheet_name = next(
        (
            sheet
            for sheet in workbook.sheet_names
            if sheet.lower() == "orders"
        ),
        workbook.sheet_names[0],
    )

    print(f"Excel sheet selected: {sheet_name}")

    return pd.read_excel(file_path, sheet_name=sheet_name)


def add_discount_band(df):
    """
    Create exploratory discount groups.

    These thresholds are defined for this project;
    they are not official discount categories.
    """

    discount = df["Discount"]

    conditions = [
        discount.eq(0),
        discount.gt(0) & discount.le(0.10),
        discount.gt(0.10) & discount.le(0.30),
        discount.gt(0.30),
        discount.lt(0),
    ]

    labels = [
        "No Discount",
        "Low (0-10%)",
        "Medium (>10-30%)",
        "High (>30%)",
        "Negative (check)",
    ]

    df["Discount Band"] = pd.NA

    for condition, label in zip(conditions, labels):
        df.loc[condition, "Discount Band"] = label

    return df


def summarize_by_group(df, group_columns):
    """Calculate business metrics for each group."""

    summary = (
        df.groupby(group_columns, dropna=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Units_Sold=("Quantity", "sum"),
            Distinct_Orders=("Order ID", "nunique"),
            Average_Discount=("Discount", "mean"),
            Transaction_Lines=("Order ID", "size"),
        )
        .reset_index()
    )

    # Profit margin is total profit divided by total sales.
    summary["Profit_Margin"] = (
        summary["Profit"]
        / summary["Sales"].where(summary["Sales"] != 0)
    )

    # Weakest total-profit groups appear first.
    return summary.sort_values("Profit", ascending=True)


def main():
    # 1. Locate and load the dataset.
    file_path = find_dataset()
    df = load_dataset(file_path)

    print("=" * 60)
    print("SUPERSTORE SALES & PROFITABILITY ANALYSIS")
    print("=" * 60)
    print(f"Source file: {file_path.name}")
    print(f"Original rows: {len(df):,}")

    # 2. Make sure the expected fields exist.
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}\n"
            f"Available columns: {df.columns.tolist()}"
        )

    # 3. Convert values to the correct data types.
    numeric_columns = ["Sales", "Profit", "Discount", "Quantity"]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce",
    )

    # 4. Count records that cannot be used in this analysis.
    usable_columns = REQUIRED_COLUMNS

    invalid_rows = df[usable_columns].isna().any(axis=1).sum()

    # Keep the original dataframe unchanged for row-count reporting.
    analysis = df.dropna(subset=usable_columns).copy()

    print(f"Rows excluded due to missing/invalid required values: {invalid_rows:,}")
    print(f"Rows included in analysis: {len(analysis):,}")

    if analysis.empty:
        raise ValueError("No usable rows remain after data validation.")

    # 5. Assign each transaction line to a discount band.
    analysis = add_discount_band(analysis)

    # 6. Create the output folder.
    output_folder = PROJECT_ROOT / "outputs"
    output_folder.mkdir(parents=True, exist_ok=True)

    # 7. Calculate the overall KPIs.
    total_sales = analysis["Sales"].sum()
    total_profit = analysis["Profit"].sum()

    kpis = pd.DataFrame(
        [
            {
                "Original_Rows": len(df),
                "Rows_Analysed": len(analysis),
                "Rows_Excluded": len(df) - len(analysis),
                "Distinct_Orders": analysis["Order ID"].nunique(),
                "Units_Sold": analysis["Quantity"].sum(),
                "Total_Sales": total_sales,
                "Total_Profit": total_profit,
                "Profit_Margin": (
                    total_profit / total_sales
                    if total_sales != 0
                    else None
                ),
                "Average_Discount": analysis["Discount"].mean(),
                "First_Order_Date": analysis["Order Date"].min(),
                "Last_Order_Date": analysis["Order Date"].max(),
            }
        ]
    )

    kpis.to_csv(output_folder / "kpis.csv", index=False)

    # 8. Compare categories and sub-categories.
    summary_jobs = {
        "profit_by_subcategory.csv": ["Category", "Sub-Category"],
        "profit_by_category.csv": ["Category"],
        "profit_by_region.csv": ["Region"],
        "profit_by_discount_band.csv": ["Discount Band"],
    }

    summaries = {}


    for filename, group_columns in summary_jobs.items():
        result = summarize_by_group(analysis, group_columns)

        if filename == "profit_by_discount_band.csv":
            discount_order = {
                "No Discount": 0,
                "Low (0-10%)": 1,
                "Medium (>10-30%)": 2,
                "High (>30%)": 3,
                "Negative (check)": 4,
            }

            result = result.assign(
                _order=result["Discount Band"].map(discount_order)
            )

            result = (
                result.sort_values("_order")
                .drop(columns="_order")
            )

        summaries[filename] = result
        result.to_csv(output_folder / filename, index=False)

    # 9. Calculate monthly sales and profit.
    analysis["Order Month"] = (
        analysis["Order Date"].dt.to_period("M").astype(str)
    )

    monthly = (
        analysis.groupby("Order Month")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Distinct_Orders=("Order ID", "nunique"),
            Units_Sold=("Quantity", "sum"),
        )
        .reset_index()
        .sort_values("Order Month")
    )

    monthly["Profit_Margin"] = (
        monthly["Profit"]
        / monthly["Sales"].where(monthly["Sales"] != 0)
    )

    monthly.to_csv(output_folder / "monthly_trend.csv", index=False)

    # 10. Print results for a quick review.
    print("\nOVERALL KPIs")
    print(kpis.to_string(index=False))

    print("\n10 LOWEST-PROFIT SUB-CATEGORIES")
    print(
        summaries["profit_by_subcategory.csv"]
        .head(10)
        .to_string(index=False)
    )

    print("\nPROFITABILITY BY DISCOUNT BAND")
    print(
        summaries["profit_by_discount_band.csv"]
        .to_string(index=False)
    )

    print(f"\nAnalysis complete. Results saved in: {output_folder}")


if __name__ == "__main__":
    main()
