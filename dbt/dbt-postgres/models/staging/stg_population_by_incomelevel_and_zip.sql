{{ config(materialized='view')}}


SELECT
    id
    , year
    , dataset
    , zip
    , CASE WHEN max_income < 1000000000 THEN min_income || ' - ' ||  max_income
           ELSE min_income || '+' END AS income_range
    , population

FROM {{ source('staging', 'population_by_incomelevel_and_zip')}}