
{{ config(materialized='view')}}

WITH all_zips AS (
    SELECT DISTINCT zip FROM (
        SELECT zip
        FROM {{ source('staging','median_age_by_zip') }} 
        UNION
        SELECT zip
        FROM {{ source('staging','median_income_by_zip') }}
    ) zips
)

SELECT 
    age.id
    , age.year
    , age.dataset
    , zips.zip
    , CASE WHEN age.median_age < 0 THEN NULL ELSE age.median_age END AS median_age
    , CASE WHEN income.median_income < 0 THEN NULL ELSE income.median_income END AS median_income
FROM all_zips zips
    JOIN {{ source('staging','median_age_by_zip') }} age
        ON zips.zip = age.zip
    JOIN {{ source('staging','median_income_by_zip') }} income 
        ON zips.zip = income.zip 
        AND age.year = income.year
        AND age.dataset = income.dataset

