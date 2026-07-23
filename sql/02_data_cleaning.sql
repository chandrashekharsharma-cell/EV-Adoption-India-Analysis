-- ============================================================
-- 02_data_cleaning.sql
-- SQL-side cleaning (used when raw data is loaded directly into
-- a staging table rather than pre-cleaned in Python). Mirrors
-- the logic in python/01_data_cleaning.py.
-- ============================================================

-- 1. Remove exact duplicates, keeping the lowest surrogate id
DELETE FROM ev_registrations_staging a
USING ev_registrations_staging b
WHERE a.registration_id > b.registration_id
  AND a.state_ut = b.state_ut
  AND a.district IS NOT DISTINCT FROM b.district
  AND a.registration_date = b.registration_date
  AND a.vehicle_category = b.vehicle_category
  AND a.manufacturer IS NOT DISTINCT FROM b.manufacturer
  AND a.monthly_ev_registrations = b.monthly_ev_registrations;

-- 2. Standardize state names
UPDATE ev_registrations_staging
SET state_ut = CASE
    WHEN UPPER(TRIM(state_ut)) IN ('MAHARASHTRA', 'MAHRASHTRA') THEN 'Maharashtra'
    WHEN UPPER(TRIM(state_ut)) IN ('UP', 'UTTAR PRADESH', 'UTTAR  PRADESH') THEN 'Uttar Pradesh'
    WHEN UPPER(TRIM(state_ut)) IN ('NEW DELHI', 'DELHI', 'NCT OF DELHI') THEN 'Delhi'
    WHEN UPPER(TRIM(state_ut)) IN ('ORISSA', 'ODISHA') THEN 'Odisha'
    WHEN UPPER(TRIM(state_ut)) IN ('TAMILNADU', 'TAMIL NADU') THEN 'Tamil Nadu'
    WHEN UPPER(TRIM(state_ut)) IN ('WB', 'WEST BENGAL') THEN 'West Bengal'
    ELSE INITCAP(TRIM(state_ut))
END;

-- 3. Fix data types / strip whitespace on numeric-as-text fields
UPDATE ev_registrations_staging
SET monthly_ev_registrations = CAST(TRIM(monthly_ev_registrations::TEXT) AS INT)
WHERE monthly_ev_registrations::TEXT ~ '^\s*\d+\s*$';

-- 4. Handle missing values
-- District -> 'Not Specified'
UPDATE ev_registrations_staging SET district = 'Not Specified' WHERE district IS NULL;

-- Fuel type -> dataset mode (BEV)
UPDATE ev_registrations_staging SET fuel_type = 'Battery Electric (BEV)' WHERE fuel_type IS NULL;

-- Manufacturer -> most common manufacturer for that vehicle category
WITH cat_mode AS (
    SELECT vehicle_category, manufacturer,
           ROW_NUMBER() OVER (PARTITION BY vehicle_category ORDER BY COUNT(*) DESC) AS rn
    FROM ev_registrations_staging
    WHERE manufacturer IS NOT NULL
    GROUP BY vehicle_category, manufacturer
)
UPDATE ev_registrations_staging s
SET manufacturer = cm.manufacturer
FROM cat_mode cm
WHERE s.manufacturer IS NULL
  AND s.vehicle_category = cm.vehicle_category
  AND cm.rn = 1;

-- Charging stations -> median by state & year
WITH med AS (
    SELECT state_ut, year,
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY charging_stations) AS med_val
    FROM ev_registrations_staging
    WHERE charging_stations IS NOT NULL
    GROUP BY state_ut, year
)
UPDATE ev_registrations_staging s
SET charging_stations = ROUND(m.med_val)
FROM med m
WHERE s.charging_stations IS NULL
  AND s.state_ut = m.state_ut
  AND s.year = m.year;

-- Drop rows still missing the core registration count (cannot be safely imputed)
DELETE FROM ev_registrations_staging WHERE monthly_ev_registrations IS NULL;

-- 5. Outlier treatment (IQR capping) by vehicle category
WITH bounds AS (
    SELECT vehicle_category,
           PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY monthly_ev_registrations) AS q1,
           PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY monthly_ev_registrations) AS q3
    FROM ev_registrations_staging
    GROUP BY vehicle_category
),
limits AS (
    SELECT vehicle_category,
           GREATEST(0, q1 - 1.5 * (q3 - q1)) AS lower_bound,
           q3 + 1.5 * (q3 - q1) AS upper_bound
    FROM bounds
)
UPDATE ev_registrations_staging s
SET monthly_ev_registrations = LEAST(GREATEST(s.monthly_ev_registrations, l.lower_bound), l.upper_bound)
FROM limits l
WHERE s.vehicle_category = l.vehicle_category;

-- 6. Load cleaned staging data into the production fact table
INSERT INTO ev_registrations (
    state_ut, district, registration_date, year, month, quarter,
    vehicle_category, fuel_type, manufacturer, monthly_ev_registrations,
    charging_stations, population, ev_per_100k_population, ev_to_charging_station_ratio
)
SELECT
    state_ut, district, registration_date, year, month,
    CEIL(month / 3.0)::SMALLINT AS quarter,
    vehicle_category, fuel_type, manufacturer, monthly_ev_registrations,
    charging_stations, population,
    ROUND((monthly_ev_registrations::NUMERIC / (population / 100000.0)), 4),
    CASE WHEN charging_stations > 0
         THEN ROUND(monthly_ev_registrations::NUMERIC / charging_stations, 2)
         ELSE NULL END
FROM ev_registrations_staging;
