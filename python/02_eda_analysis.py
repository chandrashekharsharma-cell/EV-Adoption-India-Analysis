"""
02_eda_analysis.py
------------------------------------------------------------
Exploratory Data Analysis for the India EV Adoption dataset.
Produces summary tables + charts (saved as PNGs for the README
/ portfolio) covering:
 - National trend
 - State leaderboard
 - Vehicle category market share
 - Charging infrastructure gap
 - Manufacturer share
------------------------------------------------------------
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")
CLEAN_PATH = "/home/claude/EV_Adoption_India_Analysis/data/cleaned/ev_registrations_cleaned.csv"
ASSETS = "/home/claude/EV_Adoption_India_Analysis/assets"

df = pd.read_csv(CLEAN_PATH, parse_dates=["Registration_Date"])

ACCENT = "#00E5A0"
ACCENT2 = "#2F80ED"
BG = "#0E1117"

# ------------------------------------------------------------
# 1. National yearly trend
# ------------------------------------------------------------
yearly = df.groupby("Year")["Monthly_EV_Registrations"].sum().reset_index()
yearly["YoY_Growth_%"] = yearly["Monthly_EV_Registrations"].pct_change() * 100

fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)
ax.set_facecolor(BG)
ax.bar(yearly["Year"], yearly["Monthly_EV_Registrations"], color=ACCENT)
ax.set_title("India EV Registrations by Year (2018–2025 YTD)", color="white", fontsize=13, weight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Total Registrations")
ax.tick_params(colors="white")
for spine in ax.spines.values():
    spine.set_visible(False)
plt.tight_layout()
plt.savefig(f"{ASSETS}/01_national_yearly_trend.png", dpi=150)
plt.close()

# ------------------------------------------------------------
# 2. State leaderboard (Top 10 / Bottom 10)
# ------------------------------------------------------------
state_totals = df.groupby("State_UT")["Monthly_EV_Registrations"].sum().sort_values(ascending=False)
top10 = state_totals.head(10)
bottom10 = state_totals.tail(10)

fig, ax = plt.subplots(figsize=(9, 6), facecolor=BG)
ax.set_facecolor(BG)
ax.barh(top10.index[::-1], top10.values[::-1], color=ACCENT)
ax.set_title("Top 10 States by Total EV Registrations", color="white", fontsize=13, weight="bold")
ax.tick_params(colors="white")
for spine in ax.spines.values():
    spine.set_visible(False)
plt.tight_layout()
plt.savefig(f"{ASSETS}/02_top10_states.png", dpi=150)
plt.close()

# ------------------------------------------------------------
# 3. Vehicle category market share
# ------------------------------------------------------------
cat_share = df.groupby("Vehicle_Category")["Monthly_EV_Registrations"].sum().sort_values(ascending=False)
cat_share_pct = (cat_share / cat_share.sum() * 100).round(1)

fig, ax = plt.subplots(figsize=(7, 7), facecolor=BG)
colors = [ACCENT, ACCENT2, "#F2C94C", "#EB5757", "#9B51E0"]
ax.pie(cat_share.values, labels=cat_share.index, autopct="%1.1f%%",
       colors=colors, textprops={"color": "white"}, wedgeprops={"edgecolor": BG, "linewidth": 2})
ax.set_title("EV Market Share by Vehicle Category", color="white", fontsize=13, weight="bold")
plt.tight_layout()
plt.savefig(f"{ASSETS}/03_category_market_share.png", dpi=150)
plt.close()

# ------------------------------------------------------------
# 4. Charging infrastructure gap (EV-to-station ratio by state)
# ------------------------------------------------------------
infra = df.groupby("State_UT").agg(
    total_ev=("Monthly_EV_Registrations", "sum"),
    charging_stations=("Charging_Stations", "max"),
).reset_index()
infra["ev_per_station"] = (infra["total_ev"] / infra["charging_stations"]).round(1)
infra = infra.sort_values("ev_per_station", ascending=False).head(15)

fig, ax = plt.subplots(figsize=(9, 6), facecolor=BG)
ax.set_facecolor(BG)
ax.barh(infra["State_UT"][::-1], infra["ev_per_station"][::-1], color="#EB5757")
ax.set_title("Charging Infrastructure Gap — EVs per Charging Station (Top 15 Gaps)",
             color="white", fontsize=12, weight="bold")
ax.tick_params(colors="white")
for spine in ax.spines.values():
    spine.set_visible(False)
plt.tight_layout()
plt.savefig(f"{ASSETS}/04_charging_infra_gap.png", dpi=150)
plt.close()

# ------------------------------------------------------------
# 5. Manufacturer market share (overall, top 8)
# ------------------------------------------------------------
manu_share = df.groupby("Manufacturer")["Monthly_EV_Registrations"].sum().sort_values(ascending=False).head(8)

fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)
ax.set_facecolor(BG)
ax.bar(manu_share.index, manu_share.values, color=ACCENT2)
ax.set_title("Top 8 Manufacturers by Total EV Registrations", color="white", fontsize=13, weight="bold")
plt.xticks(rotation=35, ha="right", color="white")
ax.tick_params(colors="white")
for spine in ax.spines.values():
    spine.set_visible(False)
plt.tight_layout()
plt.savefig(f"{ASSETS}/05_manufacturer_share.png", dpi=150)
plt.close()

# ------------------------------------------------------------
# 6. Monthly seasonality (avg registrations by calendar month)
# ------------------------------------------------------------
seasonal = df.groupby("Month")["Monthly_EV_Registrations"].mean()

fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)
ax.set_facecolor(BG)
ax.plot(seasonal.index, seasonal.values, color=ACCENT, marker="o", linewidth=2)
ax.set_title("Average Monthly Seasonality in EV Registrations", color="white", fontsize=13, weight="bold")
ax.set_xlabel("Month")
ax.set_xticks(range(1, 13))
ax.tick_params(colors="white")
for spine in ax.spines.values():
    spine.set_visible(False)
plt.tight_layout()
plt.savefig(f"{ASSETS}/06_seasonality.png", dpi=150)
plt.close()

# ------------------------------------------------------------
# Print key summary stats used in insights / README
# ------------------------------------------------------------
print("=== KEY METRICS ===")
print(f"Total EV Registrations (2018-2025 YTD): {df['Monthly_EV_Registrations'].sum():,}")
print(f"Total unique States/UTs: {df['State_UT'].nunique()}")
print(f"Latest year (2024) total: {df[df.Year==2024]['Monthly_EV_Registrations'].sum():,}")
print(f"\nTop 5 states:\n{top10.head(5)}")
print(f"\nCategory market share (%):\n{cat_share_pct}")
print(f"\nTop 5 manufacturers:\n{manu_share.head(5)}")
print(f"\nTop 5 infrastructure gap states:\n{infra[['State_UT','ev_per_station']].head(5).to_string(index=False)}")
print("\nCharts saved to /assets/")
