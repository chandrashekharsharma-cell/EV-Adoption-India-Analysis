# DAX Measures — EV Adoption Analysis Dashboard

Model: `Fact_EV_Registrations` joined to `Dim_State`, `Dim_Date`, `Dim_Manufacturer`, `Dim_VehicleCategory` (star schema).

## Core KPIs

```dax
Total EV Registrations =
SUM ( Fact_EV_Registrations[Monthly_EV_Registrations] )

Total Charging Stations =
CALCULATE (
    MAX ( Fact_EV_Registrations[Charging_Stations] ),
    LASTDATE ( Dim_Date[date_key] )
)

Total States Covered =
DISTINCTCOUNT ( Fact_EV_Registrations[State_UT] )

Avg Monthly Registrations =
AVERAGE ( Fact_EV_Registrations[Monthly_EV_Registrations] )
```

## Growth & Trend Measures

```dax
EV Registrations PY =
CALCULATE (
    [Total EV Registrations],
    SAMEPERIODLASTYEAR ( Dim_Date[date_key] )
)

YoY Growth % =
DIVIDE (
    [Total EV Registrations] - [EV Registrations PY],
    [EV Registrations PY]
)

YoY Growth % (Colored Label) =
VAR growth = [YoY Growth %]
RETURN
    IF ( growth >= 0, "▲ " & FORMAT ( growth, "0.0%" ), "▼ " & FORMAT ( growth, "0.0%" ) )

Rolling 3-Month Avg =
AVERAGEX (
    DATESINPERIOD ( Dim_Date[date_key], MAX ( Dim_Date[date_key] ), -3, MONTH ),
    [Total EV Registrations]
)

CAGR (5Y) =
VAR StartVal = CALCULATE ( [Total EV Registrations], Dim_Date[Year] = 2019 )
VAR EndVal   = CALCULATE ( [Total EV Registrations], Dim_Date[Year] = 2024 )
RETURN
    IF ( StartVal > 0, ( EndVal / StartVal ) ^ ( 1 / 5 ) - 1, BLANK () )
```

## Ranking Measures

```dax
State Rank =
RANKX (
    ALL ( Dim_State[state_ut] ),
    CALCULATE ( [Total EV Registrations] ),
    ,
    DESC
)

Top 10 State Flag =
IF ( [State Rank] <= 10, "Top 10", "Other" )

Bottom 10 State Flag =
VAR TotalStates = CALCULATE ( DISTINCTCOUNT ( Dim_State[state_ut] ), ALL ( Dim_State ) )
RETURN
    IF ( [State Rank] > TotalStates - 10, "Bottom 10", "Other" )
```

## Market Share Measures

```dax
Category Market Share % =
DIVIDE (
    [Total EV Registrations],
    CALCULATE ( [Total EV Registrations], ALL ( Fact_EV_Registrations[Vehicle_Category] ) )
)

Manufacturer Market Share % (within Category) =
DIVIDE (
    [Total EV Registrations],
    CALCULATE (
        [Total EV Registrations],
        ALL ( Fact_EV_Registrations[Manufacturer] )
    )
)
```

## Infrastructure Measures

```dax
EV to Charging Station Ratio =
DIVIDE ( [Total EV Registrations], [Total Charging Stations] )

Charging Stations per Million Population =
DIVIDE (
    [Total Charging Stations] * 1000000,
    SUM ( Dim_State[population] )
)

Infrastructure Gap Status =
VAR ratio = [EV to Charging Station Ratio]
RETURN
    SWITCH (
        TRUE (),
        ratio > 150, "🔴 Critical Gap",
        ratio > 80,  "🟡 Moderate Gap",
        "🟢 Adequate"
    )
```

## Forecast Page Measures
(Sourced from `ev_forecast_2026_2030.csv`, imported as a second table `Fact_Forecast`)

```dax
Forecasted Registrations =
SUM ( Fact_Forecast[forecast_ensemble] )

Forecast Lower Bound =
SUM ( Fact_Forecast[lower_95_ci] )

Forecast Upper Bound =
SUM ( Fact_Forecast[upper_95_ci] )

Historical vs Forecast Switch =
VAR SelectedYear = MAX ( Dim_Date[Year] )
RETURN
    IF ( SelectedYear <= 2025, [Total EV Registrations], [Forecasted Registrations] )
```

## Dynamic Titles (for tooltips / cards)

```dax
Dynamic KPI Title =
"EV Registrations — " &
    IF (
        ISFILTERED ( Dim_State[state_ut] ),
        SELECTEDVALUE ( Dim_State[state_ut] ),
        "All India"
    )
```
