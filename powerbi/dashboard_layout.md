# Power BI Dashboard — Design & Layout Specification
### "Driving the Future: EV Adoption Analysis in India"

This spec is written so the dashboard can be rebuilt directly in Power BI Desktop
using the cleaned dataset (`data/cleaned/ev_registrations_cleaned.csv`) and the
forecast output (`data/cleaned/ev_forecast_2026_2030.csv`), plus the DAX in
`dax_measures.md`.

---

## 1. Visual Theme (Dark, Premium)

| Token | Value |
|---|---|
| Canvas background | `#0E1117` |
| Panel / card background | `#161B22` |
| Primary accent (EV green) | `#00E5A0` |
| Secondary accent (electric blue) | `#2F80ED` |
| Warning / gap accent | `#EB5757` |
| Highlight / gold | `#F2C94C` |
| Text primary | `#FFFFFF` |
| Text secondary | `#9CA3AF` |
| Font | Segoe UI (headers semi-bold), Consolas for KPI numerals |
| Grid | 12-column responsive grid, 1920×1080 base canvas, safe margins 24px |

Import as a Power BI JSON theme (`theme/ev_dark_theme.json`) with the palette above,
`visualStyles` set for card border-radius 8px, and data colors ordered
`["#00E5A0","#2F80ED","#F2C94C","#EB5757","#9B51E0","#56CCF2"]`.

---

## 2. Page 1 — Executive Overview

**Layout (top→bottom):**
- **Header band**: Title left, global filter icons (State / Year / Category) right, last-refresh timestamp.
- **KPI card row (4 cards)**: Total EV Registrations · Total Charging Stations · Annual Growth Rate (YoY %) · Avg Monthly Registrations — each with a small sparkline and a ▲/▼ trend chip.
- **EV Growth Trend** — large area/line chart, 2018–2025, dual-line (Registrations + Rolling 3-Month Avg), gradient fill under primary line.
- **Category mini-donut** (bottom-left) — quick market share glance, links to Page 3 via drill-through.
- **India mini-map** (bottom-right) — filled map colored by registration density, links to Page 2.

**Visuals used:** Card, Area chart, Donut chart, Filled map, Slicer (Year range).

---

## 3. Page 2 — State-wise Analysis

- **Interactive Filled Map of India** (left, 60% width) — bubble/choropleth sized & colored by `Total EV Registrations`; click to cross-filter every visual on the page.
- **State Ranking table** (right, 40%) — `State Rank`, `State_UT`, `Total EV Registrations`, `YoY Growth %`, conditional-formatted data bars.
- **Top 10 States** — horizontal bar chart, green gradient.
- **Bottom 10 States** — horizontal bar chart, red/gray gradient.
- **Tooltip page**: hovering a state shows a mini tooltip report with category breakdown + charging stations for that state.

**Visuals used:** Filled/Shape map, Table w/ data bars, Bar chart ×2, Tooltip page, Slicer (Region).

---

## 4. Page 3 — Vehicle Category Analysis

- **KPI strip**: 2W / 3W / Car / Bus / Commercial — five compact cards with category icon + total + share %.
- **Market Share Donut** — center, large.
- **Category Trend Over Time** — stacked area chart, 2018–2025, one series per category.
- **Category × State Heatmap (Matrix)** — rows = State, columns = Category, values = registrations, color scale.
- **Fastest-Growing Category** callout card — driven by the CAGR SQL query (Q8), auto-updating text box via DAX measure.

**Visuals used:** Cards ×5, Donut chart, Stacked area chart, Matrix (heatmap conditional formatting), Callout card.

---

## 5. Page 4 — Charging Infrastructure

- **Charging Stations by State** — bar chart, sorted descending.
- **EV-to-Charging-Station Ratio** — bar chart with reference line at national average; red bars = above threshold (gap).
- **Infrastructure Gap Matrix** — table: State | EV Count | Charging Stations | Ratio | Status badge (🔴🟡🟢) using `Infrastructure Gap Status` measure.
- **Stations per Million Population** — scatter plot (X = population, Y = charging stations, size = EV registrations, color = gap status) to spot underserved high-population states.

**Visuals used:** Bar chart ×2, Table w/ conditional icons, Scatter chart.

---

## 6. Page 5 — Time Series Analysis

- **Monthly Trend** — line chart with a range slicer (2018–2025).
- **Yearly Trend** — column chart with YoY % data labels.
- **Seasonal Pattern** — small-multiple line charts, one per year, X-axis = month, overlaid to show festive-season (Oct–Nov) spikes.
- **Decomposition callouts**: trend / seasonality text insights auto-generated via DAX + Analyze feature.

**Visuals used:** Line chart, Column chart, Small multiples, Insight text boxes.

---

## 7. Page 6 — Forecast Dashboard

- **Forecast KPI row**: Projected 2030 Registrations · Projected CAGR (2024–2030) · Projected Charging Station Need (derived: forecast EV × current national avg ratio).
- **Historical + Forecast Combo Chart** — solid line 2018–2025 (actual), dashed line 2026–2030 (forecast), shaded band = 95% confidence interval (`lower_95_ci` / `upper_95_ci`).
- **Model comparison table**: Log-Linear vs Damped Holt vs Ensemble, by year.
- **Scenario slicer**: toggle between "Conservative (Lower CI)", "Base (Ensemble)", "Optimistic (Upper CI)" using a disconnected parameter table + `SWITCH` measure.

**Visuals used:** Cards, Combo chart (line + area for CI band), Table, What-if parameter slicer.

---

## 8. Interactivity Checklist

| Feature | Implementation |
|---|---|
| State filter | Slicer synced across all pages (Sync Slicers pane) |
| Year filter | Slicer + relative-date on `Dim_Date` |
| Vehicle Category filter | Slicer + used in Page 3 matrix |
| Manufacturer filter | Slicer, active on Pages 1, 3 |
| Drill-through | Page 2 state bar → "State Deep Dive" drill-through page (category mix, top manufacturers, monthly trend for that state) |
| Tooltips | Custom tooltip page for map hover (Page 2), std tooltips elsewhere with `Manufacturer`, `Fuel_Type` context |
| Bookmarks | "Executive View" vs "Analyst View" bookmark toggle (hides/shows the ranking table); "Forecast Scenario" bookmarks for CI toggle |
| Navigation buttons | Left-rail icon nav (6 pages) built with bookmark-linked image buttons, active-page highlighted in accent green |

---

## 9. Chart-to-KPI Mapping Summary

| KPI / Question | Chart Type | Page |
|---|---|---|
| Total EV Registrations | Card | 1 |
| Growth trend | Area/Line | 1, 5 |
| Leading states | Map + Bar | 2 |
| Category share | Donut + Stacked Area | 3 |
| Infra gaps | Bar + Scatter + Matrix | 4 |
| Seasonality | Small multiples | 5 |
| Future growth | Combo chart w/ CI band | 6 |

---

## 10. Screenshot / Portfolio Presentation Suggestions

- Export each page as PNG at 1920×1080, add a subtle drop-shadow + rounded 12px frame when embedding in the README / LinkedIn carousel.
- Record a 30–45s screen capture (GIF or MP4) showing: State filter click → cross-filter cascade → drill-through to state deep dive → forecast scenario toggle. This single clip is the strongest portfolio asset — recruiters engage more with a moving dashboard than static screenshots.
- Lead the README/LinkedIn post with the Executive Overview page (highest information density, most "dashboard-y" first impression), then Forecast page second (most memorable "so what").
