"""
01_data_cleaning.py
------------------------------------------------------------
Cleans the raw EV registrations dataset:
 1. Remove exact duplicates
 2. Standardize State/UT names
 3. Fix data types (numeric columns stored as messy strings)
 4. Handle missing values (impute / drop by column-specific rule)
 5. Detect & treat outliers using IQR method
 6. Feature engineering: EV_per_100k_Population, Quarter, etc.
------------------------------------------------------------
"""

import pandas as pd
import numpy as np

RAW_PATH = "/home/claude/EV_Adoption_India_Analysis/data/raw/ev_registrations_raw.csv"
CLEAN_PATH = "/home/claude/EV_Adoption_India_Analysis/data/cleaned/ev_registrations_cleaned.csv"

df = pd.read_csv(RAW_PATH)
print(f"Raw rows: {len(df):,}")

# ------------------------------------------------------------
# 1. Remove exact duplicates
# ------------------------------------------------------------
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df):,} exact duplicate rows")

# ------------------------------------------------------------
# 2. Standardize State/UT names
# ------------------------------------------------------------
state_map = {
    "MAHARASHTRA": "Maharashtra", "maharashtra ": "Maharashtra", "Mahrashtra": "Maharashtra",
    "UP": "Uttar Pradesh", "uttar pradesh": "Uttar Pradesh", "Uttar  Pradesh": "Uttar Pradesh",
    "New Delhi": "Delhi", "DELHI": "Delhi", "NCT of Delhi": "Delhi",
    "Orissa": "Odisha", "ODISHA": "Odisha",
    "TamilNadu": "Tamil Nadu", "tamil nadu": "Tamil Nadu",
    "WB": "West Bengal", "west bengal": "West Bengal",
}
df["State_UT"] = df["State_UT"].astype(str).str.strip()
df["State_UT"] = df["State_UT"].replace(state_map)
df["State_UT"] = df["State_UT"].str.title().replace({"Nct Of Delhi": "Delhi"})

# ------------------------------------------------------------
# 3. Fix data types
# ------------------------------------------------------------
df["Monthly_EV_Registrations"] = (
    df["Monthly_EV_Registrations"].astype(str).str.strip().replace("nan", np.nan).astype(float)
)
df["Registration_Date"] = pd.to_datetime(df["Registration_Date"], errors="coerce")
df["Year"] = df["Year"].astype(int)
df["Month"] = df["Month"].astype(int)
df["Charging_Stations"] = pd.to_numeric(df["Charging_Stations"], errors="coerce")
df["Population"] = pd.to_numeric(df["Population"], errors="coerce")

# ------------------------------------------------------------
# 4. Handle missing values
# ------------------------------------------------------------
missing_before = df.isna().sum()

# District: unknown -> "Not Specified" (categorical, safe to flag rather than drop)
df["District"] = df["District"].fillna("Not Specified")

# Manufacturer: impute using the most common manufacturer for that vehicle category
cat_mode_manufacturer = df.groupby("Vehicle_Category")["Manufacturer"].agg(
    lambda s: s.mode().iloc[0] if not s.mode().empty else "Unknown"
)
df["Manufacturer"] = df.apply(
    lambda r: cat_mode_manufacturer[r["Vehicle_Category"]] if pd.isna(r["Manufacturer"]) else r["Manufacturer"],
    axis=1,
)

# Fuel_Type: impute with dataset-wide mode (BEV dominates >90%)
df["Fuel_Type"] = df["Fuel_Type"].fillna(df["Fuel_Type"].mode().iloc[0])

# Charging_Stations: impute with state+year median (structural, not random)
df["Charging_Stations"] = df.groupby(["State_UT", "Year"])["Charging_Stations"].transform(
    lambda s: s.fillna(s.median())
)
df["Charging_Stations"] = df["Charging_Stations"].fillna(df["Charging_Stations"].median())

# Any remaining rows with missing core numeric fields (registrations) are dropped —
# a missing registration count cannot be safely imputed without distorting totals
df = df.dropna(subset=["Monthly_EV_Registrations", "Registration_Date"])

print("\nMissing values handled:")
print(missing_before[missing_before > 0])

# ------------------------------------------------------------
# 5. Outlier detection & treatment (IQR method, per Vehicle_Category)
# ------------------------------------------------------------
def iqr_bounds(s):
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    return max(0, q1 - 1.5 * iqr), q3 + 1.5 * iqr

def cap_series_by_group(df, group_col, val_col):
    lower = df.groupby(group_col)[val_col].transform(lambda s: iqr_bounds(s)[0])
    upper = df.groupby(group_col)[val_col].transform(lambda s: iqr_bounds(s)[1])
    return df[val_col].clip(lower=lower, upper=upper)

outlier_flag_before = df["Monthly_EV_Registrations"].copy()
df["Monthly_EV_Registrations"] = cap_series_by_group(df, "Vehicle_Category", "Monthly_EV_Registrations")
n_capped = (outlier_flag_before.values != df["Monthly_EV_Registrations"].values).sum()
print(f"\nOutliers capped in Monthly_EV_Registrations (IQR method): {n_capped:,} rows")

# Same treatment for charging stations
cs_before = df["Charging_Stations"].copy()
df["Charging_Stations"] = cap_series_by_group(df, "State_UT", "Charging_Stations")
n_capped_cs = (cs_before.values != df["Charging_Stations"].values).sum()
print(f"Outliers capped in Charging_Stations (IQR method): {n_capped_cs:,} rows")

df["Monthly_EV_Registrations"] = df["Monthly_EV_Registrations"].round().astype(int)
df["Charging_Stations"] = df["Charging_Stations"].round().astype(int)

# ------------------------------------------------------------
# 6. Feature engineering
# ------------------------------------------------------------
df["Quarter"] = df["Registration_Date"].dt.quarter
df["EV_per_100k_Population"] = (df["Monthly_EV_Registrations"] / (df["Population"] / 100_000)).round(4)
df["EV_to_Charging_Station_Ratio"] = np.where(
    df["Charging_Stations"] > 0,
    (df["Monthly_EV_Registrations"] / df["Charging_Stations"]).round(2),
    np.nan,
)

# ------------------------------------------------------------
# 7. Final checks & export
# ------------------------------------------------------------
df = df.sort_values(["State_UT", "Registration_Date"]).reset_index(drop=True)

print(f"\nFinal cleaned rows: {len(df):,}")
print(f"Unique States/UTs: {df['State_UT'].nunique()}")
print(f"Date range: {df['Registration_Date'].min().date()} to {df['Registration_Date'].max().date()}")
print(f"\nColumn dtypes:\n{df.dtypes}")

df.to_csv(CLEAN_PATH, index=False)
print(f"\nSaved cleaned dataset -> {CLEAN_PATH}")
