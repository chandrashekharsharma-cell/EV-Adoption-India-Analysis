# Project Architecture

## Pipeline Overview

```
                 ┌────────────────────┐
                 │  Raw Data Source    │
                 │ (synthetic, models  │
                 │  Vahan-style feed)  │
                 └──────────┬──────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │   Python: Data Cleaning Layer      │
        │  01_data_cleaning.py               │
        │  - Deduplication                   │
        │  - State-name standardization      │
        │  - Type correction                 │
        │  - Missing-value imputation         │
        │  - IQR outlier capping             │
        │  - Feature engineering             │
        └──────────────┬─────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │     Cleaned Dataset (CSV)          │
        │  data/cleaned/*.csv                │
        └──────────┬───────────┬─────────────┘
                    │           │
                    ▼           ▼
      ┌─────────────────┐   ┌──────────────────────────┐
      │  SQL Layer       │   │  Python Analysis Layer    │
      │  (schema, CTEs,  │   │  02_eda_analysis.py       │
      │  window fns,     │   │  03_forecasting_model.py  │
      │  ranking, YoY)   │   │  (scikit-learn + NumPy    │
      └────────┬─────────┘   │   trend models, charts)   │
               │              └───────────┬────────────┘
               │                          │
               └───────────┬──────────────┘
                            ▼
              ┌───────────────────────────┐
              │  Power BI Semantic Model   │
              │  Star schema:              │
              │  Fact_EV_Registrations +   │
              │  Dim_State / Dim_Date /    │
              │  Dim_Manufacturer          │
              │  + DAX measure layer       │
              └─────────────┬─────────────┘
                            ▼
              ┌───────────────────────────┐
              │   6-Page Power BI          │
              │   Dashboard (dark theme)   │
              │   + drill-through,         │
              │   bookmarks, tooltips      │
              └───────────────────────────┘
```

## Layered Design Rationale

1. **Raw → Cleaned separation**: keeps a reproducible audit trail. Anyone can re-run `01_data_cleaning.py` against the raw file and get the same cleaned output — a standard data-engineering practice recruiters look for.
2. **SQL layer mirrors the Python cleaning logic**: demonstrates the same transformations can be done in a database engine (for teams working off a warehouse rather than flat files), plus adds advanced analytical SQL (CTEs, window functions, ranking) independent of the BI tool.
3. **Star schema for Power BI**: fact table (`ev_registrations`) at the finest grain, with `dim_state`, `dim_date`, `dim_manufacturer` for clean slicing and fast DAX evaluation — avoids a flat single-table model which would bloat and slow filter context.
4. **Forecast as a separate fact table**: `Fact_Forecast` is intentionally decoupled from the historical fact table so Power BI can toggle between "Actual" and "Forecast" contexts cleanly via a measure switch, rather than mixing projected and actual rows in one column.

## Tech Stack

| Layer | Tools |
|---|---|
| Data generation & cleaning | Python (Pandas, NumPy) |
| Advanced analytics | SQL (PostgreSQL-flavored, ANSI-compatible notes included) |
| Forecasting | scikit-learn (LinearRegression on log-space), custom NumPy damped Holt's trend model |
| Visualization (EDA) | Matplotlib |
| BI Dashboard | Power BI (star schema, DAX, bookmarks, drill-through) |
| Version control / portfolio | Git + GitHub |

## Folder Structure

```
EV_Adoption_India_Analysis/
├── README.md
├── data_dictionary.md
├── data/
│   ├── raw/
│   │   └── ev_registrations_raw.csv
│   └── cleaned/
│       ├── ev_registrations_cleaned.csv
│       └── ev_forecast_2026_2030.csv
├── sql/
│   ├── 01_schema.sql
│   ├── 02_data_cleaning.sql
│   └── 03_analysis_queries.sql
├── python/
│   ├── 00_generate_dataset.py
│   ├── 01_data_cleaning.py
│   ├── 02_eda_analysis.py
│   └── 03_forecasting_model.py
├── powerbi/
│   ├── dashboard_layout.md
│   └── dax_measures.md
├── assets/
│   ├── 01_national_yearly_trend.png
│   ├── 02_top10_states.png
│   ├── 03_category_market_share.png
│   ├── 04_charging_infra_gap.png
│   ├── 05_manufacturer_share.png
│   ├── 06_seasonality.png
│   └── 07_forecast_2026_2030.png
└── docs/
    ├── project_architecture.md
    ├── business_insights.md
    ├── linkedin_post.md
    ├── github_description.md
    └── resume_bullets.md
```
