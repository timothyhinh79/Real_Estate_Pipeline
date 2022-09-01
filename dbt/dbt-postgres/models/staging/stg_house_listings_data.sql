
{{ config(materialized='view') }}

WITH house_listings_w_rn AS (
    SELECT rank() OVER (PARTITION BY zpid ORDER BY extract_date DESC) as rn, *
    FROM {{ source('staging','house_listings') }}
    WHERE zpid IS NOT NULL
)

SELECT
    id
    , extract_date
    , zpid
    , street_address
    , zipcode
    , city
    , state
    , latitude
    , longitude
    , price
    , bathrooms
    , bedrooms
    , living_area
    , home_type
    , home_status
    , days_on_zillow
    , is_featured
    , should_highlight
    , zestimate
    , rent_zestimate
    , is_open_house
    , is_fsba
    , open_house
    , is_unmappable
    , is_preforeclosure_auction
    , home_status_for_hdp
    , price_for_hdp
    , is_non_owner_occupied
    , is_premier_builder
    , is_zillow_owned
    , currency
    , country
    , tax_assessed_value
    , lot_area_value
    , lot_area_unit
FROM house_listings_w_rn
WHERE rn = 1

