
{{ config(materialized = 'table')}}

SELECT 
    {{ dbt_utils.surrogate_key(
      'city'
      , 'category'
      , 'gang_related'
    ) }} as crime_stats_id
    , city
    , category
    , gang_related
    , SUM(CASE WHEN time_of_incident > CURRENT_DATE - 30 THEN 1 ELSE 0 END) AS num_crimes_last30days
    , SUM(CASE WHEN time_of_incident > CURRENT_DATE - 180 THEN 1 ELSE 0 END) AS num_crimes_last180days
    , SUM(CASE WHEN time_of_incident > CURRENT_DATE - 365 THEN 1 ELSE 0 END) AS num_crimes_lastyear

FROM {{ ref('stg_crimes_data') }}

GROUP BY 
    crime_stats_id
    , city
    , category
    , gang_related