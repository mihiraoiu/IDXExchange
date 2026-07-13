

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("/Users/mihir/Desktop/internshipcrmls/csv")

NUMERIC_COLUMNS = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt"
]

CORE_FIELDS = {
    "PropertyType",
    "CloseDate",
    "ListingContractDate",
    "PurchaseContractDate",
    *NUMERIC_COLUMNS
}



def missing_value_report(df, name):
    report = pd.DataFrame({
        "MissingCount": df.isna().sum(),
        "MissingPercent": df.isna().mean() * 100
    }).sort_values("MissingPercent", ascending=False)

    report.to_csv(DATA_DIR / f"{name}_missing_report.csv")

    high_missing = report[report["MissingPercent"] > 90]

    print(f"\n{name} columns above 90% missing:")
    print(high_missing if not high_missing.empty else "None")

    drop_columns = [
        column for column in high_missing.index
        if column not in CORE_FIELDS
    ]

    df = df.drop(columns=drop_columns)

    print(f"Dropped {len(drop_columns)} non-core columns.")
    return df


def numeric_summary(df, name):
    available = [
        column for column in NUMERIC_COLUMNS
        if column in df.columns
    ]

    summary = df[available].describe(
        percentiles=[0.10, 0.25, 0.50, 0.75, 0.90]
    ).T

    summary["median"] = df[available].median()

    summary = summary[
        ["count", "mean", "std", "min", "10%", "25%",
         "50%", "75%", "90%", "max", "median"]
    ]

    print(f"\n{name} numeric summary:")
    print(summary)

    summary.to_csv(DATA_DIR / f"{name}_numeric_summary.csv")


def create_plots(df, name):
    plot_dir = DATA_DIR / f"{name}_plots"
    plot_dir.mkdir(exist_ok=True)

    for column in NUMERIC_COLUMNS:
        if column not in df.columns:
            continue

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if values.empty:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        plot_values = values[values.between(lower, upper)]

        plt.figure()
        plt.hist(plot_values, bins=20, edgecolor="black")
        plt.title(f"{name.title()}: {column} Distribution")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(plot_dir / f"{column}_histogram.png")
        plt.show()

        plt.figure()
        plt.boxplot(plot_values)
        plt.title(f"{name.title()}: {column} Boxplot")
        plt.ylabel(column)
        plt.tight_layout()
        plt.savefig(plot_dir / f"{column}_boxplot.png")
        plt.show()


def extreme_outlier_report(df, name):
    report = pd.DataFrame(index=df.index)

    for column in NUMERIC_COLUMNS:
        if column not in df.columns:
            continue

        values = pd.to_numeric(df[column], errors="coerce")

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 3 * iqr
        upper = q3 + 3 * iqr

        report[f"{column}_extreme_outlier"] = (
            (values < lower) | (values > upper)
        )

    print(f"\n{name} extreme outlier counts:")
    print(report.sum())

    report.to_csv(
        DATA_DIR / f"{name}_extreme_outlier_flags.csv",
        index=False
    )


def fetch_monthly_mortgage_rates():
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

    mortgage = pd.read_csv(
        url,
        parse_dates=["observation_date"]
    )

    mortgage.columns = ["date", "rate_30yr_fixed"]
    mortgage["year_month"] = mortgage["date"].dt.to_period("M")

    return (
        mortgage.groupby("year_month", as_index=False)["rate_30yr_fixed"]
        .mean()
    )



# LISTING DATA ANALYSIS


LISTING_FILE = DATA_DIR / "CRMLSListing.csv"

listing = pd.read_csv(LISTING_FILE, low_memory=False)

print(
    f"Loaded listing data: "
    f"{listing.shape[0]:,} rows × {listing.shape[1]:,} columns"
)

print("\nListing data types:")
print(listing.dtypes)

print("\nListing property types:")
print(listing["PropertyType"].value_counts(dropna=False))

before = len(listing)
listing = listing[
    listing["PropertyType"] == "Residential"
].copy()
after = len(listing)

print(f"\nResidential filter: {before:,} → {after:,} rows")

listing = missing_value_report(listing, "listing")
numeric_summary(listing, "listing")
create_plots(listing, "listing")
extreme_outlier_report(listing, "listing")

listing.to_csv(
    DATA_DIR / "CRMLSListing_Residential.csv",
    index=False
)

mortgage_monthly = fetch_monthly_mortgage_rates()

listing["ListingContractDate"] = pd.to_datetime(
    listing["ListingContractDate"],
    errors="coerce"
)

listing["year_month"] = (
    listing["ListingContractDate"].dt.to_period("M")
)

listing_enriched = listing.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)

print(
    "\nListing unmatched mortgage-rate rows:",
    listing_enriched["rate_30yr_fixed"].isna().sum()
)

listing_enriched.to_csv(
    DATA_DIR / "CRMLSListing_Residential_WithRates.csv",
    index=False
)

print("\nListing analysis complete.")