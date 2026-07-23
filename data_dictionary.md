# Data Dictionary — EV Adoption India Dataset

**File:** `data/cleaned/ev_registrations_cleaned.csv`
**Grain:** One row = one Vehicle Category × Manufacturer × District × Month combination
**Rows:** 7,163 (post-cleaning) | **Coverage:** 24 States/UTs, Jan 2018 – Jun 2025

| Column | Type | Description | Example |
|---|---|---|---|
| `State_UT` | string | Indian State or Union Territory (standardized naming) | `Maharashtra` |
| `District` | string | District within the state; `"Not Specified"` where unavailable | `Pune` |
| `Registration_Date` | date | First day of the registration month | `2023-04-01` |
| `Year` | integer | Calendar year of registration | `2023` |
| `Month` | integer | Calendar month (1–12) | `4` |
| `Quarter` | integer | Calendar quarter (1–4), derived from `Month` | `2` |
| `Vehicle_Category` | string | One of: `2W`, `3W`, `Car`, `Bus`, `Commercial` | `2W` |
| `Fuel_Type` | string | `Battery Electric (BEV)` or `Plug-in Hybrid (PHEV)` | `Battery Electric (BEV)` |
| `Manufacturer` | string | OEM brand | `Ola Electric` |
| `Monthly_EV_Registrations` | integer | New EV registrations for that category/manufacturer/district/month (outlier-capped via IQR) | `142` |
| `Charging_Stations` | integer | Cumulative public charging stations in that state as of that year (outlier-capped) | `310` |
| `Population` | integer | State/UT population (approx., static reference figure) | `123000000` |
| `EV_per_100k_Population` | float | `Monthly_EV_Registrations / (Population / 100,000)` — adoption intensity metric | `0.0012` |
| `EV_to_Charging_Station_Ratio` | float | `Monthly_EV_Registrations / Charging_Stations` — infrastructure pressure metric (null when stations = 0) | `4.6` |

## Related Files

| File | Description |
|---|---|
| `data/raw/ev_registrations_raw.csv` | Uncleaned source data, includes intentional duplicates, missing values, inconsistent state naming and outliers (for demonstrating the cleaning pipeline) |
| `data/cleaned/ev_forecast_2026_2030.csv` | Output of the forecasting model — yearly projections 2026–2030 with 95% confidence bounds |

## Forecast File Schema (`ev_forecast_2026_2030.csv`)

| Column | Description |
|---|---|
| `year` | Forecast year (2026–2030) |
| `forecast_log_linear` | Prediction from the log-linear (compound growth) regression model |
| `forecast_damped_holt` | Prediction from the damped Holt's linear trend model |
| `forecast_ensemble` | Average of the two models — the headline forecast figure |
| `lower_95_ci` / `upper_95_ci` | 95% confidence interval bounds (residual-based, widening with horizon) |

## Data Quality Notes

- This is a **synthetic dataset** generated to model realistic India EV adoption patterns (state tiering, festive-season seasonality, FAME-II-era acceleration, COVID-era dip in 2020). It is designed for portfolio/demonstration purposes and is not official Vahan/MoRTH data.
- Growth patterns, state rankings, and manufacturer shares are directionally aligned with publicly reported industry trends as of early 2026 but exact figures are simulated.
- 2025 contains only partial-year data (through June); the forecasting model annualizes this figure before fitting trend models.
