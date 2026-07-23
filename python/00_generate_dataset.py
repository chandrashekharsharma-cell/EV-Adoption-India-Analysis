"""
00_generate_dataset.py
------------------------------------------------------------
Generates a realistic SYNTHETIC dataset simulating India's EV
registration landscape (2018-2025), modeled loosely on public
patterns reported by the Vahan Dashboard (Ministry of Road
Transport & Highways) and industry reports (SMEV, NITI Aayog).

NOTE: This is simulated data for portfolio/demo purposes — not
official government data. Growth curves, state rankings and
manufacturer shares are directionally realistic (Maharashtra,
UP, Delhi, Karnataka, Tamil Nadu lead; 2W dominates volume;
Ola Electric/TVS/Bajaj/Tata lead category shares) but exact
figures are randomized.

The raw file is generated WITH intentional data-quality issues
(duplicates, missing values, inconsistent state naming, a few
outliers) so the cleaning scripts have real work to do.
------------------------------------------------------------
"""

import numpy as np
import pandas as pd
from datetime import datetime

np.random.seed(42)

# ------------------------------------------------------------
# 1. Reference data
# ------------------------------------------------------------

states = {
    "Maharashtra": {"pop": 123_000_000, "tier": 1, "districts": ["Pune", "Mumbai City", "Nagpur", "Nashik", "Thane"]},
    "Uttar Pradesh": {"pop": 231_000_000, "tier": 1, "districts": ["Lucknow", "Noida", "Kanpur", "Ghaziabad", "Varanasi"]},
    "Delhi": {"pop": 32_000_000, "tier": 1, "districts": ["New Delhi", "South Delhi", "North Delhi", "East Delhi"]},
    "Karnataka": {"pop": 67_000_000, "tier": 1, "districts": ["Bengaluru Urban", "Mysuru", "Mangaluru", "Hubli"]},
    "Tamil Nadu": {"pop": 77_000_000, "tier": 1, "districts": ["Chennai", "Coimbatore", "Madurai", "Salem"]},
    "Gujarat": {"pop": 71_000_000, "tier": 1, "districts": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"]},
    "Rajasthan": {"pop": 81_000_000, "tier": 2, "districts": ["Jaipur", "Jodhpur", "Udaipur", "Kota"]},
    "West Bengal": {"pop": 99_000_000, "tier": 2, "districts": ["Kolkata", "Howrah", "Siliguri", "Durgapur"]},
    "Telangana": {"pop": 39_000_000, "tier": 1, "districts": ["Hyderabad", "Warangal", "Nizamabad"]},
    "Kerala": {"pop": 35_000_000, "tier": 2, "districts": ["Ernakulam", "Thiruvananthapuram", "Kozhikode"]},
    "Madhya Pradesh": {"pop": 85_000_000, "tier": 2, "districts": ["Bhopal", "Indore", "Gwalior", "Jabalpur"]},
    "Haryana": {"pop": 30_000_000, "tier": 2, "districts": ["Gurugram", "Faridabad", "Panipat"]},
    "Bihar": {"pop": 128_000_000, "tier": 3, "districts": ["Patna", "Gaya", "Bhagalpur"]},
    "Punjab": {"pop": 30_000_000, "tier": 2, "districts": ["Ludhiana", "Amritsar", "Jalandhar"]},
    "Odisha": {"pop": 46_000_000, "tier": 3, "districts": ["Bhubaneswar", "Cuttack", "Rourkela"]},
    "Assam": {"pop": 35_000_000, "tier": 3, "districts": ["Guwahati", "Dibrugarh", "Silchar"]},
    "Andhra Pradesh": {"pop": 53_000_000, "tier": 2, "districts": ["Visakhapatnam", "Vijayawada", "Guntur"]},
    "Chhattisgarh": {"pop": 30_000_000, "tier": 3, "districts": ["Raipur", "Bhilai", "Bilaspur"]},
    "Jharkhand": {"pop": 39_000_000, "tier": 3, "districts": ["Ranchi", "Jamshedpur", "Dhanbad"]},
    "Uttarakhand": {"pop": 11_000_000, "tier": 3, "districts": ["Dehradun", "Haridwar"]},
    "Himachal Pradesh": {"pop": 7_500_000, "tier": 3, "districts": ["Shimla", "Kangra"]},
    "Goa": {"pop": 1_600_000, "tier": 3, "districts": ["North Goa", "South Goa"]},
    "Chandigarh": {"pop": 1_200_000, "tier": 3, "districts": ["Chandigarh"]},
    "Jammu and Kashmir": {"pop": 13_000_000, "tier": 3, "districts": ["Srinagar", "Jammu"]},
}

# Deliberately "messy" alternate spellings to be cleaned later
state_name_variants = {
    "Maharashtra": ["Maharashtra", "MAHARASHTRA", "maharashtra ", "Mahrashtra"],
    "Uttar Pradesh": ["Uttar Pradesh", "UP", "uttar pradesh", "Uttar  Pradesh"],
    "Delhi": ["Delhi", "New Delhi", "DELHI", "NCT of Delhi"],
    "Odisha": ["Odisha", "Orissa", "ODISHA"],
    "Tamil Nadu": ["Tamil Nadu", "TamilNadu", "tamil nadu"],
    "West Bengal": ["West Bengal", "WB", "west bengal"],
}

vehicle_categories = {
    "2W": {"base_share": 0.62, "avg_price_uplift": 1.0},
    "3W": {"base_share": 0.15, "avg_price_uplift": 1.0},
    "Car": {"base_share": 0.14, "avg_price_uplift": 1.0},
    "Commercial": {"base_share": 0.06, "avg_price_uplift": 1.0},
    "Bus": {"base_share": 0.03, "avg_price_uplift": 1.0},
}

fuel_types = ["Battery Electric (BEV)", "Plug-in Hybrid (PHEV)"]
fuel_weights = [0.90, 0.10]

manufacturers_by_cat = {
    "2W": ["Ola Electric", "TVS Motor", "Ather Energy", "Bajaj Auto", "Hero Electric", "Okinawa Autotech"],
    "3W": ["Mahindra Electric", "Piaggio", "YC Electric", "Kinetic Green", "Bajaj Auto"],
    "Car": ["Tata Motors", "MG Motor", "Mahindra Electric", "Hyundai", "BYD", "Kia"],
    "Commercial": ["Tata Motors", "Ashok Leyland", "Mahindra Electric", "Eicher Motors"],
    "Bus": ["Tata Motors", "Ashok Leyland", "Olectra Greentech", "PMI Electro"],
}

years = list(range(2018, 2026))
months = list(range(1, 13))

rows = []

for state, meta in states.items():
    tier = meta["tier"]
    pop = meta["pop"]
    districts = meta["districts"]

    # base adoption index driven by tier (metro/industrial states adopt faster)
    tier_multiplier = {1: 1.0, 2: 0.55, 3: 0.28}[tier]

    for year in years:
        # National EV push accelerated post-2021 (FAME-II, state subsidies)
        year_growth_factor = {
            2018: 0.15, 2019: 0.22, 2020: 0.18,  # COVID dip
            2021: 0.35, 2022: 0.75, 2023: 1.15,
            2024: 1.55, 2025: 1.85,
        }[year]

        for month in months:
            if year == 2025 and month > 6:
                continue  # data available through mid-2025

            seasonal = 1 + 0.12 * np.sin((month / 12) * 2 * np.pi)  # festive-season bump ~Oct-Nov

            for cat, cat_meta in vehicle_categories.items():
                base_monthly = (pop / 1_000_000) * tier_multiplier * cat_meta["base_share"] * year_growth_factor * seasonal
                noise = np.random.normal(1.0, 0.18)
                registrations = max(0, int(base_monthly * noise * np.random.uniform(0.8, 1.3)))

                if registrations == 0 and np.random.rand() > 0.3:
                    continue

                manufacturer = np.random.choice(manufacturers_by_cat[cat])
                fuel = np.random.choice(fuel_types, p=fuel_weights)
                district = np.random.choice(districts)

                # charging stations - cumulative-ish, correlated with tier & year
                charging_stations = int(
                    (year - 2017) * tier_multiplier * np.random.uniform(8, 25)
                    + np.random.normal(0, 5)
                )
                charging_stations = max(0, charging_stations)

                reg_date = datetime(year, month, np.random.randint(1, 28))

                # inject messy state naming occasionally
                variants = state_name_variants.get(state, [state])
                state_display = np.random.choice(variants) if np.random.rand() < 0.12 else state

                rows.append({
                    "State_UT": state_display,
                    "District": district,
                    "Registration_Date": reg_date.strftime("%Y-%m-%d"),
                    "Year": year,
                    "Month": month,
                    "Vehicle_Category": cat,
                    "Fuel_Type": fuel,
                    "Manufacturer": manufacturer,
                    "Monthly_EV_Registrations": registrations,
                    "Charging_Stations": charging_stations,
                    "Population": pop,
                })

df = pd.DataFrame(rows)

# ------------------------------------------------------------
# 2. Inject data-quality issues intentionally
# ------------------------------------------------------------

# a) Duplicates (~1.5%)
dupe_sample = df.sample(frac=0.015, random_state=1)
df = pd.concat([df, dupe_sample], ignore_index=True)

# b) Missing values in several columns
for col, frac in [("District", 0.03), ("Charging_Stations", 0.02),
                   ("Fuel_Type", 0.015), ("Manufacturer", 0.01)]:
    idx = df.sample(frac=frac, random_state=2).index
    df.loc[idx, col] = np.nan

# c) A handful of extreme outliers in registrations & charging stations
outlier_idx = df.sample(n=25, random_state=3).index
df.loc[outlier_idx, "Monthly_EV_Registrations"] = df.loc[outlier_idx, "Monthly_EV_Registrations"] * np.random.randint(15, 40)

outlier_idx2 = df.sample(n=15, random_state=4).index
df.loc[outlier_idx2, "Charging_Stations"] = df.loc[outlier_idx2, "Charging_Stations"] * np.random.randint(20, 50)

# d) Inconsistent data types (numbers stored as strings with stray spaces)
df["Monthly_EV_Registrations"] = df["Monthly_EV_Registrations"].astype(object)
str_noise_idx = df.sample(frac=0.02, random_state=5).index
df.loc[str_noise_idx, "Monthly_EV_Registrations"] = df.loc[str_noise_idx, "Monthly_EV_Registrations"].astype(str) + " "

# e) shuffle rows
df = df.sample(frac=1, random_state=6).reset_index(drop=True)

out_path = "/home/claude/EV_Adoption_India_Analysis/data/raw/ev_registrations_raw.csv"
df.to_csv(out_path, index=False)
print(f"Raw rows: {len(df):,}")
print(f"Saved to {out_path}")
