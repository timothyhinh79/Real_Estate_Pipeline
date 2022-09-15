
{{ config(materialized = 'table')}}

WITH zipcode_cities AS (
    SELECT DISTINCT zipcode, city
    FROM {{ ref('stg_house_listings_data') }}
),

unique_zipcode_cities AS (
    SELECT RANK() OVER (PARTITION BY zipcode ORDER BY city ASC) AS rn, *
    FROM zipcode_cities
)

SELECT 
    {{ dbt_utils.surrogate_key(
      'weather.zip_code'
      , 'zc.city'
      , 'weather.season'
    ) }} as zipcode_city_season_id
    , weather.zip_code
    , zc.city
    , weather.season
    , AVG(weather.avgtemp_f) AS avg_temperature
    , AVG(weather.avghumidity) AS avg_humidity
    , AVG(weather.totalprecip_in) AS avg_precip_inches

FROM {{ ref('stg_weather_data') }} weather
    INNER JOIN unique_zipcode_cities zc ON weather.zip_code = zc.zipcode

WHERE zc.rn = 1

GROUP BY 
    weather.zip_code
    , zc.city
    , weather.season
    