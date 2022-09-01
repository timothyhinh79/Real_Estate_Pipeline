
{{ config(materialized='view') }}

WITH forecasts_w_rn AS (
    SELECT rank() OVER (PARTITION BY zip_code, date ORDER BY id DESC) as rn, *
    FROM {{ source('staging','daily_forecasts') }}
    WHERE zip_code IS NOT NULL AND date IS NOT NULL
)

SELECT
    id
    , zip_code
    , date
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

