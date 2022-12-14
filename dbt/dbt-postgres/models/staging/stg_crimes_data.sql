
{{ config(materialized='view') }}

WITH crimes_w_rn AS (
    SELECT rank() OVER (PARTITION BY incident_id ORDER BY extract_date DESC) as rn, *
    FROM {{ source('staging','crimes') }}
    WHERE incident_id IS NOT NULL
)

SELECT
    id
    , extract_date
    , source_file
    , lurn_sak
    , incident_date AS time_of_incident
    , incident_reported_date
    , category
    , stat
    , stat_desc
    , address
    , street
    , city
    , zip
    , incident_id
    , gang_related
    , unit_name
    , longitude
    , latitude
    , part_category
FROM crimes_w_rn
WHERE rn = 1

