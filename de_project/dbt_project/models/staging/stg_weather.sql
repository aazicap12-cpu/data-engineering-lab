-- dbt Model: staging/stg_weather.sql
-- =====================================
-- Staging layer: clean raw weather data
-- Interview talking point:
--   "Used dbt to build modular SQL transformations
--    with staging → marts layered architecture."

{{ config(materialized='view') }}

SELECT
    id,
    UPPER(city)                             AS city,
    country,
    temperature_c,
    feels_like_c,
    ROUND(temperature_c - feels_like_c, 2)  AS temp_feels_diff,
    humidity_pct,
    pressure_hpa,
    wind_speed_ms,
    ROUND(wind_speed_ms * 3.6, 2)           AS wind_speed_kmh,
    weather_main,
    weather_desc,
    visibility_m,
    ROUND(visibility_m / 1000.0, 2)         AS visibility_km,
    cloudiness_pct,
    ingested_at,
    DATE(ingested_at)                        AS ingested_date,
    EXTRACT(HOUR FROM ingested_at)           AS ingested_hour,
    source

FROM {{ source('de_lab', 'weather_raw') }}

WHERE temperature_c BETWEEN -50 AND 60
  AND humidity_pct  BETWEEN 0   AND 100
  AND city IS NOT NULL
