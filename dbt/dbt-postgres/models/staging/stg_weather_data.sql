
{{ config(materialized='view') }}

WITH forecasts_w_rn AS (
    SELECT 
        rank() OVER (PARTITION BY zip_code, date ORDER BY id DESC) as rn
        , EXTRACT(MONTH FROM date) * 100 + EXTRACT(DAY FROM date) AS month_day
        , *
    FROM {{ source('staging','daily_forecasts') }}
    WHERE zip_code IS NOT NULL AND date IS NOT NULL
)

SELECT
    id
    , zip_code
    , date
    , CASE WHEN month_day >= 1220 OR month_day < 320 THEN 'WINTER'
           WHEN month_day >= 320 and month_day < 620 THEN 'SPRING' 
           WHEN month_day >= 620 and month_day < 920 THEN 'SUMMER' 
           WHEN month_day >= 920 and month_day < 1220 THEN 'FALL' 
      END AS season
    , maxtemp_c
    , maxtemp_f
    , mintemp_c
    , mintemp_f
    , avgtemp_c
    , avgtemp_f
    , maxwind_mph
    , maxwind_kph
    , totalprecip_mm
    , totalprecip_in
    , avgvis_km
    , avgvis_miles
    , avghumidity
    , uv
FROM forecasts_w_rn
WHERE rn = 1

