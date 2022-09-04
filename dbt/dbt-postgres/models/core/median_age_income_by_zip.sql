
{{ config(materialized='table')}}

-- getting latest census data
WITH latest_year AS (
    SELECT MAX(year) as year
    FROM {{ ref('stg_median_age_income_by_zip') }}
)

SELECT demo.*
FROM {{ ref('stg_median_age_income_by_zip') }} demo
    INNER JOIN latest_year
        ON demo.year = latest_year.year

