import pandas as pd
from pathlib import Path

DATA_DIR = Path("/Users/mihir/Desktop/internshipcrmls/csv")


SOLD_FILE = DATA_DIR / "CRMLSSold_Clean.csv"
LISTING_FILE = DATA_DIR / "CRMLSListing_Clean.csv"

IQR_COLUMNS = ["ClosePrice", "LivingArea", "DaysOnMarket"]


def iqr_bounds(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return lower, upper


def flag_outliers(df, name):
    print(f"\n{name}: IQR bounds and flag counts")

    for column in IQR_COLUMNS:
        if column not in df.columns:
            continue

        lower, upper = iqr_bounds(df[column])
        flag_column = f"{column}_outlier_flag"

        df[flag_column] = (df[column] < lower) | (df[column] > upper)

        print(
            f"  {column}: lower={lower:,.2f}, upper={upper:,.2f}, "
            f"flagged={df[flag_column].sum()} ({df[flag_column].mean() * 100:.2f}%)"
        )

    return df


def build_filtered_dataset(df, name):

    flag_columns = [f"{c}_outlier_flag" for c in IQR_COLUMNS if f"{c}_outlier_flag" in df.columns]

    any_outlier = df[flag_columns].any(axis=1)
    filtered = df[~any_outlier].copy()

    print(f"\n{name}: row count before IQR filtering = {len(df)}")
    print(f"{name}: row count after IQR filtering = {len(filtered)}")
    print(f"{name}: rows removed = {len(df) - len(filtered)}")

    return filtered


def compare_medians(full_df, filtered_df, name):
    print(f"\n{name}: median comparison, before vs. after IQR filtering")
    for column in IQR_COLUMNS:
        if column not in full_df.columns:
            continue

        before_median = full_df[column].median()
        after_median = filtered_df[column].median()

        print(
            f"  {column}: before={before_median:,.2f}, "
            f"after={after_median:,.2f}, "
            f"change={after_median - before_median:,.2f}"
        )


def process_dataset(df, name):
    print(f"\n{'=' * 60}")
    print(f"Week 7 outlier detection: {name}")
    print(f"{'=' * 60}")

    print(f"{name}: starting row count = {len(df)}")

    flagged = flag_outliers(df, name)
    filtered = build_filtered_dataset(flagged, name)
    compare_medians(flagged, filtered, name)

    return flagged, filtered


# =========================
# SOLD
# =========================

sold = pd.read_csv(SOLD_FILE, low_memory=False)
sold_flagged, sold_filtered = process_dataset(sold, "sold")

sold_flagged.to_csv(DATA_DIR / "CRMLSSold_Flagged.csv", index=False)
sold_filtered.to_csv(DATA_DIR / "CRMLSSold_Filtered.csv", index=False)

# =========================
# LISTING
# =========================

listing = pd.read_csv(LISTING_FILE, low_memory=False)
listing_flagged, listing_filtered = process_dataset(listing, "listing")

listing_flagged.to_csv(DATA_DIR / "CRMLSListing_Flagged.csv", index=False)
listing_filtered.to_csv(DATA_DIR / "CRMLSListing_Filtered.csv", index=False)

print(
    "\nExported CRMLSSold_Flagged.csv, CRMLSSold_Filtered.csv, "
    "CRMLSListing_Flagged.csv, CRMLSListing_Filtered.csv"
)