import pandas as pd


def clean_data(df):

    # Convert date columns
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  dayfirst=True)

    # Drop Postal Code — 80% of rows are null for this column
    # (only USA has postal codes in this dataset). Dropping the column
    # instead of the rows preserves all 51,290 records and all 147 countries.
    # Postal Code is not used anywhere in the dashboard.
    if "Postal Code" in df.columns:
        df = df.drop(columns=["Postal Code"])

    # Remove true duplicate records
    df = df.drop_duplicates()

    # Drop rows only where genuinely critical columns are missing
    # Never use dropna() with no arguments — it deletes any row with
    # ANY null in ANY column, which is almost always too aggressive.
    critical_columns = ["Order ID", "Country", "Region", "Category",
                        "Sales", "Profit", "Order Date"]
    df = df.dropna(subset=critical_columns)

    return df


def feature_engineering(df):

    df["Year"]       = df["Order Date"].dt.year
    df["Month"]      = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.month_name()

    # Guard against division by zero on zero-sales rows
    df["Profit Margin"] = df.apply(
        lambda row: row["Profit"] / row["Sales"] if row["Sales"] != 0 else 0,
        axis=1
    )

    return df