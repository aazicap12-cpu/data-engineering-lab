-- dbt Model: marts/mart_city_weather_summary.sql
-- ================================================
-- Analytics mart: daily city weather KPIs
-- Used by BI dashboards (Tableau / Power BI)

{{ config(materialized='table') }}

SELECT
    city,
    country,
    ingested_date,

    -- Temperature KPIs
    ROUND(AVG(temperature_c), 2)        AS avg_temp_c,
    ROUND(MIN(temperature_c), 2)        AS min_temp_c,
    ROUND(MAX(temperature_c), 2)        AS max_temp_c,
    ROUND(AVG(feels_like_c), 2)         AS avg_feels_like_c,

    -- Humidity & Pressure
    ROUND(AVG(humidity_pct), 1)         AS avg_humidity_pct,
    ROUND(AVG(pressure_hpa), 1)         AS avg_pressure_hpa,

    -- Wind
    ROUND(AVG(wind_speed_kmh), 2)       AS avg_wind_kmh,
    ROUND(MAX(wind_speed_kmh), 2)       AS max_wind_kmh,

    -- Visibility
    ROUND(AVG(visibility_km), 2)        AS avg_visibility_km,

    -- Weather classification
    MODE() WITHIN GROUP
        (ORDER BY weather_main)         AS dominant_weather,

    -- Record count for audit
    COUNT(*)                            AS readings_count

FROM {{ ref('stg_weather') }}

GROUP BY city, country, ingested_date
ORDER BY ingested_date DESC, city
