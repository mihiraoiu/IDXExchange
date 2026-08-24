import pandas as pd
from pathlib import Path

DATA_DIR = Path("/Users/mihir/Desktop/internshipcrmls/csv")

SOLD_FILE = DATA_DIR / "CRMLSSold_Clean.csv"
LISTING_FILE = DATA_DIR / "CRMLSListing_Clean.csv"

# Fields to run IQR-based outlier detection on
IQR_COLUMNS = ["ClosePrice", "LivingArea", "DaysOnMarket"]


def flag_outliers_iqr(df, name):
    """Add an IQR-based outlier flag column for each field in IQR_COLUMNS,
    without deleting any rows. Returns df with flag columns added."""

    print(f"\n{'=' * 60}")
    print(f"Week 7 outlier flagging: {name}")
    print(f"{'=' * 60}")

    for column in IQR_COLUMNS:
        if column not in df.columns:
            print(f"{name}: skipping {column} (not in columns)")
            continue

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1

        upper = q3 + 1.5 * iqr
        lower = q1 - 1.5 * iqr

        flag_col = f"{column}_Outlier_Flag"

        df[flag_col] = (df[column] > upper) | (df[column] < lower)

        print(f"\n{name}: {column}")
        print(f"  Q1 = {q1:.2f}, Q3 = {q3:.2f}, IQR = {iqr:.2f}")
        print(f"  lower bound = {lower:.2f}, upper bound = {upper:.2f}")
        print(f"  flagged rows = {df[flag_col].sum()}")

    return df


def build_clean_filtered(df, name):
    """Return a copy of df with any flagged row removed (analysis-ready dataset).
    The full flagged df passed in is left untouched/unfiltered."""

    flag_cols = [
        f"{c}_Outlier_Flag"
        for c in IQR_COLUMNS
        if f"{c}_Outlier_Flag" in df.columns
    ]

    clean = df[~df[flag_cols].any(axis=1)].copy()

    print(f"\n{name}: rows before filtering = {len(df)}")
    print(f"{name}: rows after filtering by all {len(flag_cols)} fields = {len(clean)}")

    return clean


def written_comparison(df_full, df_clean, name):
    """Print row-count and median comparisons before/after IQR filtering."""

    print(f"\n{name}: written comparison (before -> after)")
    print(f"  Row count: {len(df_full)} -> {len(df_clean)}")

    for column in IQR_COLUMNS:
        if column in df_full.columns:
            before_median = df_full[column].median()
            after_median = df_clean[column].median()

            print(
                f"  Median {column}: "
                f"{before_median:.2f} -> {after_median:.2f}"
            )


# SOLD

sold = pd.read_csv(SOLD_FILE, low_memory=False)

sold = flag_outliers_iqr(sold, "sold")
sold_clean = build_clean_filtered(sold, "sold")
written_comparison(sold, sold_clean, "sold")

sold_clean.to_csv(DATA_DIR / "CRMLSSold_Final.csv", index=False)


# LISTING

listing = pd.read_csv(LISTING_FILE, low_memory=False)

listing = flag_outliers_iqr(listing, "listing")
listing_clean = build_clean_filtered(listing, "listing")
written_comparison(listing, listing_clean, "listing")

listing_clean.to_csv(DATA_DIR / "CRMLSListing_Final.csv", index=False)


print("\nExported CRMLSSold_Final.csv and CRMLSListing_Final.csv")