-- ============================================================
-- 03_analysis_queries.sql
-- Advanced SQL analysis: GROUP BY, JOINS, CTEs, Window Functions,
-- Ranking, YoY Growth, Top/Bottom States, Market Share
-- ============================================================

-- ------------------------------------------------------------
-- Q1. Total EV registrations & YoY growth rate (national level)
-- ------------------------------------------------------------
WITH yearly_totals AS (
    SELECT year, SUM(monthly_ev_registrations) AS total_registrations
    FROM ev_registrations
    GROUP BY year
)
SELECT
    year,
    total_registrations,
    LAG(total_registrations) OVER (ORDER BY year) AS prev_year_registrations,
    ROUND(
        100.0 * (total_registrations - LAG(total_registrations) OVER (ORDER BY year))
        / NULLIF(LAG(total_registrations) OVER (ORDER BY year), 0), 2
    ) AS yoy_growth_pct
FROM yearly_totals
ORDER BY year;

-- ------------------------------------------------------------
-- Q2. State-wise ranking by total registrations (latest year)
-- ------------------------------------------------------------
WITH latest_year AS (SELECT MAX(year) AS yr FROM ev_registrations),
state_totals AS (
    SELECT r.state_ut, SUM(r.monthly_ev_registrations) AS total_registrations
    FROM ev_registrations r, latest_year ly
    WHERE r.year = ly.yr
    GROUP BY r.state_ut
)
SELECT
    state_ut,
    total_registrations,
    RANK() OVER (ORDER BY total_registrations DESC) AS state_rank,
    NTILE(4) OVER (ORDER BY total_registrations DESC) AS quartile
FROM state_totals
ORDER BY state_rank;

-- ------------------------------------------------------------
-- Q3. Top 10 and Bottom 10 states (all-time, using UNION ALL)
-- ------------------------------------------------------------
WITH state_totals AS (
    SELECT state_ut, SUM(monthly_ev_registrations) AS total_registrations
    FROM ev_registrations
    GROUP BY state_ut
),
ranked AS (
    SELECT state_ut, total_registrations,
           RANK() OVER (ORDER BY total_registrations DESC) AS rank_desc,
           RANK() OVER (ORDER BY total_registrations ASC)  AS rank_asc
    FROM state_totals
)
SELECT 'Top 10' AS segment, state_ut, total_registrations, rank_desc AS rank_position
FROM ranked WHERE rank_desc <= 10
UNION ALL
SELECT 'Bottom 10' AS segment, state_ut, total_registrations, rank_asc AS rank_position
FROM ranked WHERE rank_asc <= 10
ORDER BY segment, rank_position;

-- ------------------------------------------------------------
-- Q4. Vehicle category market share (national)
-- ------------------------------------------------------------
SELECT
    vehicle_category,
    SUM(monthly_ev_registrations) AS total_registrations,
    ROUND(100.0 * SUM(monthly_ev_registrations) / SUM(SUM(monthly_ev_registrations)) OVER (), 2) AS market_share_pct
FROM ev_registrations
GROUP BY vehicle_category
ORDER BY total_registrations DESC;

-- ------------------------------------------------------------
-- Q5. Manufacturer market share within each vehicle category
-- ------------------------------------------------------------
WITH manu_totals AS (
    SELECT vehicle_category, manufacturer, SUM(monthly_ev_registrations) AS total_units
    FROM ev_registrations
    GROUP BY vehicle_category, manufacturer
)
SELECT
    vehicle_category,
    manufacturer,
    total_units,
    ROUND(100.0 * total_units / SUM(total_units) OVER (PARTITION BY vehicle_category), 2) AS category_market_share_pct,
    RANK() OVER (PARTITION BY vehicle_category ORDER BY total_units DESC) AS rank_in_category
FROM manu_totals
QUALIFY rank_in_category <= 3   -- Snowflake/Databricks syntax; use a wrapping SELECT + WHERE for ANSI SQL
ORDER BY vehicle_category, rank_in_category;

-- ANSI-SQL-safe equivalent (no QUALIFY) for Postgres/MySQL/SQL Server:
-- SELECT * FROM (
--     SELECT vehicle_category, manufacturer, total_units,
--            RANK() OVER (PARTITION BY vehicle_category ORDER BY total_units DESC) AS rank_in_category
--     FROM manu_totals
-- ) ranked
-- WHERE rank_in_category <= 3;

-- ------------------------------------------------------------
-- Q6. Charging infrastructure gap analysis (state-wise)
-- Join fact table to a derived state summary via CTE
-- ------------------------------------------------------------
WITH state_summary AS (
    SELECT
        state_ut,
        SUM(monthly_ev_registrations) AS total_ev,
        MAX(charging_stations) AS latest_charging_stations,
        MAX(population) AS population
    FROM ev_registrations
    GROUP BY state_ut
)
SELECT
    state_ut,
    total_ev,
    latest_charging_stations,
    ROUND(total_ev::NUMERIC / NULLIF(latest_charging_stations, 0), 1) AS ev_per_charging_station,
    ROUND(latest_charging_stations::NUMERIC / (population / 1000000.0), 2) AS stations_per_million_pop,
    CASE
        WHEN total_ev::NUMERIC / NULLIF(latest_charging_stations, 0) > 150 THEN 'Critical Gap'
        WHEN total_ev::NUMERIC / NULLIF(latest_charging_stations, 0) > 80  THEN 'Moderate Gap'
        ELSE 'Adequate'
    END AS infrastructure_status
FROM state_summary
ORDER BY ev_per_charging_station DESC;

-- ------------------------------------------------------------
-- Q7. Month-over-month rolling 3-month average (trend smoothing)
-- ------------------------------------------------------------
WITH monthly_national AS (
    SELECT year, month, SUM(monthly_ev_registrations) AS total_registrations
    FROM ev_registrations
    GROUP BY year, month
)
SELECT
    year, month, total_registrations,
    ROUND(AVG(total_registrations) OVER (
        ORDER BY year, month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 0) AS rolling_3m_avg
FROM monthly_national
ORDER BY year, month;

-- ------------------------------------------------------------
-- Q8. Fastest-growing vehicle category (CAGR-style, first vs last year)
-- ------------------------------------------------------------
WITH first_last AS (
    SELECT
        vehicle_category,
        MIN(year) AS first_year,
        MAX(year) AS last_year
    FROM ev_registrations
    GROUP BY vehicle_category
),
endpoints AS (
    SELECT f.vehicle_category,
           SUM(CASE WHEN r.year = f.first_year THEN r.monthly_ev_registrations ELSE 0 END) AS start_volume,
           SUM(CASE WHEN r.year = f.last_year THEN r.monthly_ev_registrations ELSE 0 END) AS end_volume,
           (f.last_year - f.first_year) AS num_years
    FROM ev_registrations r
    JOIN first_last f ON r.vehicle_category = f.vehicle_category
    GROUP BY f.vehicle_category, f.first_year, f.last_year
)
SELECT
    vehicle_category,
    start_volume,
    end_volume,
    num_years,
    ROUND((POWER(end_volume::NUMERIC / NULLIF(start_volume, 0), 1.0 / NULLIF(num_years, 0)) - 1) * 100, 2) AS cagr_pct
FROM endpoints
ORDER BY cagr_pct DESC;

-- ------------------------------------------------------------
-- Q9. State x Category pivot-style summary using conditional aggregation (JOIN + GROUP BY)
-- ------------------------------------------------------------
SELECT
    ds.state_ut,
    ds.region,
    SUM(CASE WHEN r.vehicle_category = '2W' THEN r.monthly_ev_registrations ELSE 0 END) AS two_wheelers,
    SUM(CASE WHEN r.vehicle_category = '3W' THEN r.monthly_ev_registrations ELSE 0 END) AS three_wheelers,
    SUM(CASE WHEN r.vehicle_category = 'Car' THEN r.monthly_ev_registrations ELSE 0 END) AS cars,
    SUM(CASE WHEN r.vehicle_category = 'Bus' THEN r.monthly_ev_registrations ELSE 0 END) AS buses,
    SUM(CASE WHEN r.vehicle_category = 'Commercial' THEN r.monthly_ev_registrations ELSE 0 END) AS commercial,
    SUM(r.monthly_ev_registrations) AS total
FROM ev_registrations r
JOIN dim_state ds ON r.state_ut = ds.state_ut
GROUP BY ds.state_ut, ds.region
ORDER BY total DESC;

-- ------------------------------------------------------------
-- Q10. Year-over-year growth by state (window function, LAG)
-- ------------------------------------------------------------
WITH state_year AS (
    SELECT state_ut, year, SUM(monthly_ev_registrations) AS total_registrations
    FROM ev_registrations
    GROUP BY state_ut, year
)
SELECT
    state_ut,
    year,
    total_registrations,
    ROUND(
        100.0 * (total_registrations - LAG(total_registrations) OVER (PARTITION BY state_ut ORDER BY year))
        / NULLIF(LAG(total_registrations) OVER (PARTITION BY state_ut ORDER BY year), 0), 2
    ) AS yoy_growth_pct
FROM state_year
ORDER BY state_ut, year;
