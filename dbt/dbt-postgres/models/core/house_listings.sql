{{ config(materialized='table')}}

WITH latest_extract_date AS (
    SELECT MAX(extract_date) AS extract_date
    FROM {{ ref('stg_house_listings_data')}}
)
, latest_extract_date_by_listing AS (
    SELECT zpid, MAX(extract_date) AS extract_date
    FROM {{ ref('stg_house_listings_data')}}
    GROUP BY zpid
)

SELECT 
    listings.*
    , CASE WHEN latest_extract_date.extract_date IS NULL THEN 'CLOSED'
           ELSE 'OPEN' END AS open_status
    , CASE WHEN latest_extract_date.extract_date IS NULL THEN latest_extract_date_by_listing.extract_date + 7
           ELSE NULL END AS closed_date
FROM {{ ref('stg_house_listings_data')}} listings
    LEFT JOIN latest_extract_date 
        ON listings.extract_date = latest_extract_date.extract_date
    INNER JOIN latest_extract_date_by_listing
        ON listings.zpid = latest_extract_date_by_listing.zpid