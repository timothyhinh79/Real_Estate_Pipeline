{{ config(materialized='view')}}

SELECT
    id
    , year
    , dataset
    , zip
    , sex
    , CASE WHEN max_age < 1000 THEN min_age || ' - ' ||  max_age 
           ELSE min_age || '+' END AS age_range
    , population

FROM {{ source('staging', 'population_by_agesex_and_zip')}}
