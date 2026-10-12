from pathlib import Path

import pandas as pd


# 1. Find the main project folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# 2. Look for the dataset in data/ or data/raw/.
DATA_FOLDERS = [
    PROJECT_ROOT / "data",
    PROJECT_ROOT / "data" / "raw",
]

SUPPORTED_EXTENSIONS = {".xls", ".xlsx", ".csv"}


def find_dataset():
    """Find the first supported dataset file."""

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
        "Dataset not found. Place the Superstore file "
        "inside the project's data/ folder."
    )


def load_dataset(file_path):
    """Load the dataset from Excel or CSV."""

    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)

    excel_file = pd.ExcelFile(file_path)

    print("\nAvailable Excel sheets:")
    print(excel_file.sheet_names)

    # Prefer the Orders sheet when it exists.
    sheet_name = next(
        (
            sheet
            for sheet in excel_file.sheet_names
            if sheet.lower() == "orders"
        ),
        excel_file.sheet_names[0],
    )

    print(f"\nReading sheet: {sheet_name}")

    return pd.read_excel(
        file_path,
        sheet_name=sheet_name,
    )


def main():
    # Find and load the dataset.
    file_path = find_dataset()

    print("=" * 55)
    print("SUPERSTORE DATA AUDIT")
    print("=" * 55)

    print(f"\nFile: {file_path.name}")

    df = load_dataset(file_path)

    # Check the size of the data.
    print("\n1. DATASET SIZE")
    print(f"Number of rows: {df.shape[0]:,}")
    print(f"Number of columns: {df.shape[1]:,}")

    # Inspect the column names.
    print("\n2. COLUMN NAMES")
    for column in df.columns:
        print(f"- {column}")

    # Check data types.
    print("\n3. DATA TYPES")
    print(df.dtypes.to_string())

    # Find missing values.
    print("\n4. MISSING VALUES")
    missing = df.isna().sum().sort_values(ascending=False)
    print(missing.to_string())

    # Find completely duplicated rows.
    print("\n5. DUPLICATE ROWS")
    print(f"Exact duplicate rows: {df.duplicated().sum():,}")

    # Check the order date range if that column exists.
    if "Order Date" in df.columns:
        dates = pd.to_datetime(
            df["Order Date"],
            errors="coerce",
        )

        print("\n6. ORDER DATE RANGE")

        if dates.notna().any():
            print(f"First date: {dates.min().date()}")
            print(f"Last date:  {dates.max().date()}")
        else:
            print("No valid order dates were found.")

        print(f"Invalid dates: {dates.isna().sum():,}")

    # Show a small preview.
    print("\n7. FIRST FIVE ROWS")
    print(df.head().to_string(index=False))

    print("\nData audit complete.")


if __name__ == "__main__":
    main()