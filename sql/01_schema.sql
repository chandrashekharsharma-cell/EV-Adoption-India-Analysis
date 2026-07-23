-- ============================================================
-- 01_schema.sql
-- Driving the Future: EV Adoption Analysis in India
-- Database schema (compatible with PostgreSQL / SQL Server /
-- SQLite with minor type adjustments)
-- ============================================================

DROP TABLE IF EXISTS ev_registrations;

CREATE TABLE ev_registrations (
    registration_id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    state_ut                  VARCHAR(50)   NOT NULL,
    district                  VARCHAR(100),
    registration_date         DATE          NOT NULL,
    year                      SMALLINT      NOT NULL,
    month                     SMALLINT      NOT NULL,
    quarter                   SMALLINT      NOT NULL,
    vehicle_category          VARCHAR(20)   NOT NULL,   -- 2W, 3W, Car, Bus, Commercial
    fuel_type                 VARCHAR(30)   NOT NULL,   -- BEV, PHEV
    manufacturer               VARCHAR(50)   NOT NULL,
    monthly_ev_registrations  INT           NOT NULL,
    charging_stations         INT           NOT NULL,
    population                BIGINT        NOT NULL,
    ev_per_100k_population     NUMERIC(10,4),
    ev_to_charging_station_ratio NUMERIC(10,2)
);

-- Reference / dimension tables (star-schema friendly for Power BI)

CREATE TABLE dim_state (
    state_ut      VARCHAR(50) PRIMARY KEY,
    region        VARCHAR(20),         -- North / South / East / West / Central / Northeast
    tier          SMALLINT,            -- 1 = leading adoption, 2 = emerging, 3 = nascent
    population    BIGINT
);

CREATE TABLE dim_date (
    date_key      DATE PRIMARY KEY,
    year          SMALLINT,
    month         SMALLINT,
    month_name    VARCHAR(15),
    quarter       SMALLINT,
    fiscal_year   VARCHAR(10)          -- Indian FY: Apr-Mar
);

CREATE TABLE dim_manufacturer (
    manufacturer     VARCHAR(50) PRIMARY KEY,
    primary_category VARCHAR(20),
    origin_type      VARCHAR(20)       -- Domestic / Foreign JV
);

-- Indexes to support common analytical queries
CREATE INDEX idx_ev_state_year ON ev_registrations (state_ut, year);
CREATE INDEX idx_ev_category ON ev_registrations (vehicle_category);
CREATE INDEX idx_ev_date ON ev_registrations (registration_date);
CREATE INDEX idx_ev_manufacturer ON ev_registrations (manufacturer);
