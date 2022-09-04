{{ config(materialized='view')}}


SELECT
    id
    , year
    , dataset
    , zip
    , race
    , population

FROM {{ source('staging', 'population_by_race_and_zip')}}