"""
03_forecasting_model.py
------------------------------------------------------------
Forecasts national EV registrations for the next 5 years
(2026-2030). India's EV market is in an S-curve adoption phase
(similar to smartphone/UPI adoption curves), so a naive linear
or unconstrained polynomial extrapolation is unreliable — it
either understates the boom or (worse) curves downward outside
the training range.

Approach:
 1. Work at ANNUAL granularity (2025 is annualized from its
    available months to avoid a partial-year dip biasing the fit).
 2. Model A - Log-Linear (exponential) Regression via scikit-learn:
    fits registrations on a log scale, i.e. compound growth.
 3. Model B - Damped Holt's Linear Trend (NumPy implementation):
    captures deceleration as the market matures, preventing
    unrealistic indefinite exponential growth.
 4. Ensemble = average of A and B, with a widening confidence
    interval each year out (reflecting rising forecast uncertainty).
------------------------------------------------------------
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

plt.style.use("dark_background")
CLEAN_PATH = "/home/claude/EV_Adoption_India_Analysis/data/cleaned/ev_registrations_cleaned.csv"
ASSETS = "/home/claude/EV_Adoption_India_Analysis/assets"
OUT_CSV = "/home/claude/EV_Adoption_India_Analysis/data/cleaned/ev_forecast_2026_2030.csv"

df = pd.read_csv(CLEAN_PATH, parse_dates=["Registration_Date"])

# ------------------------------------------------------------
# 1. Build annual series; annualize the partial 2025 (H1 only)
# ------------------------------------------------------------
yearly = df.groupby("Year")["Monthly_EV_Registrations"].sum().reset_index()
yearly.columns = ["year", "registrations"]

months_available_2025 = df[df.Year == 2025]["Month"].nunique()
if months_available_2025 and months_available_2025 < 12:
    idx = yearly.index[yearly.year == 2025][0]
    yearly.loc[idx, "registrations"] = round(
        yearly.loc[idx, "registrations"] / months_available_2025 * 12
    )
    print(f"2025 annualized from {months_available_2025} months of data: "
          f"{yearly.loc[idx, 'registrations']:,.0f}")

train = yearly.copy()  # full historical series used for fitting

# ------------------------------------------------------------
# 2. Model A: Log-Linear (compound growth) Regression
# ------------------------------------------------------------
X = train[["year"]].values
y_log = np.log(train["registrations"].values)

model_log = LinearRegression()
model_log.fit(X, y_log)

pred_log_train = model_log.predict(X)
mae_log = mean_absolute_error(train["registrations"], np.exp(pred_log_train))
r2_log = r2_score(y_log, pred_log_train)
implied_cagr = np.exp(model_log.coef_[0]) - 1
print(f"Log-Linear Regression - Train MAE: {mae_log:,.0f} | R^2 (log-space): {r2_log:.3f} "
      f"| Implied CAGR: {implied_cagr*100:.1f}%")

future_years = np.arange(2026, 2031)
forecast_log = np.exp(model_log.predict(future_years.reshape(-1, 1)))

# ------------------------------------------------------------
# 3. Model B: Damped Holt's Linear Trend (NumPy)
# ------------------------------------------------------------
def damped_holt_forecast(series, alpha=0.5, beta=0.3, phi=0.85, n_forecast=5):
    """Holt's trend method with a damping factor phi (0<phi<1) so the
    trend decays toward a steady state rather than compounding forever
    - appropriate for a maturing adoption curve."""
    level = series[0]
    trend = series[1] - series[0]
    for y in series[1:]:
        last_level = level
        level = alpha * y + (1 - alpha) * (level + phi * trend)
        trend = beta * (level - last_level) + (1 - beta) * phi * trend

    forecast = []
    damp_sum = 0
    for h in range(1, n_forecast + 1):
        damp_sum += phi ** h
        forecast.append(level + damp_sum * trend)
    return np.array(forecast)

forecast_holt = damped_holt_forecast(train["registrations"].values, n_forecast=5)
forecast_holt = np.clip(forecast_holt, 0, None)

# ------------------------------------------------------------
# 4. Ensemble + widening confidence interval
# ------------------------------------------------------------
forecast_ensemble = (forecast_log + forecast_holt) / 2

residual_std = np.std(train["registrations"].values - np.exp(pred_log_train))
horizon = np.arange(1, 6)
ci_margin = 1.96 * residual_std * np.sqrt(horizon)  # widens with forecast horizon

lower_ci = np.clip(forecast_ensemble - ci_margin, 0, None)
upper_ci = forecast_ensemble + ci_margin

forecast_df = pd.DataFrame({
    "year": future_years,
    "forecast_log_linear": forecast_log.round(0),
    "forecast_damped_holt": forecast_holt.round(0),
    "forecast_ensemble": forecast_ensemble.round(0),
    "lower_95_ci": lower_ci.round(0),
    "upper_95_ci": upper_ci.round(0),
})
forecast_df.to_csv(OUT_CSV, index=False)
print(f"\nForecast saved -> {OUT_CSV}")
print("\n=== YEARLY FORECAST (2026-2030) ===")
print(forecast_df.set_index("year")[["forecast_ensemble", "lower_95_ci", "upper_95_ci"]])

print("\n=== HISTORICAL (2018-2025, 2025 annualized) ===")
print(train.set_index("year")["registrations"])

hist_cagr = (train.loc[train.year == 2024, "registrations"].values[0]
             / train.loc[train.year == 2019, "registrations"].values[0]) ** (1/5) - 1
fcst_cagr = (forecast_df.loc[forecast_df.year == 2030, "forecast_ensemble"].values[0]
             / train.loc[train.year == 2024, "registrations"].values[0]) ** (1/6) - 1
print(f"\nHistorical CAGR (2019->2024): {hist_cagr*100:.1f}%")
print(f"Projected CAGR (2024->2030): {fcst_cagr*100:.1f}%")
print(f"Projected 2030 total EV registrations (index year): {forecast_df.loc[forecast_df.year==2030,'forecast_ensemble'].values[0]:,.0f}")

# ------------------------------------------------------------
# 5. Plot: historical + forecast with confidence band
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6), facecolor="#0E1117")
ax.set_facecolor("#0E1117")
ax.plot(train["year"], train["registrations"],
        marker="o", color="#00E5A0", linewidth=2.5, label="Historical (2025 annualized)")
ax.plot(forecast_df["year"], forecast_df["forecast_ensemble"],
        marker="o", linestyle="--", color="#2F80ED", linewidth=2.5, label="Forecast (Ensemble)")
ax.fill_between(forecast_df["year"], forecast_df["lower_95_ci"], forecast_df["upper_95_ci"],
                 color="#2F80ED", alpha=0.2, label="95% Confidence Interval")
ax.set_title("India EV Registrations - Historical & 5-Year Forecast (2026-2030)",
             color="white", fontsize=13, weight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Total EV Registrations (index)")
ax.legend(facecolor="#0E1117", labelcolor="white", edgecolor="none")
ax.tick_params(colors="white")
for spine in ax.spines.values():
    spine.set_visible(False)
plt.tight_layout()
plt.savefig(f"{ASSETS}/07_forecast_2026_2030.png", dpi=150)
plt.close()
print("\nForecast chart saved -> assets/07_forecast_2026_2030.png")
