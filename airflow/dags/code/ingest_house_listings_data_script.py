import json
import psycopg2
import time
from datetime import date, timedelta
from zillow_scraper import *

def ingest_listings_data(execution_date, database, schema, table, user, password, host, port, locations, sleep_time_between_pages, **kwargs):

    print('execution_date:', execution_date)
    print('database:', database)
    print('user:', user)
    print('password:', password)
    print('host:', host)
    print('port:', port)

    listings = []
    for location in locations:
        city = location['city']
        state = location['state']
        zip = location['zip']
        print(f'{city} {state} {zip}')
        listings += get_listings(city = city, state = state, zip = zip, sleep_time_between_pages=sleep_time_between_pages)
    
    conn = psycopg2.connect(database=database,user = user, password = password, host = host, port = port)
    conn.autocommit = True
    cursor = conn.cursor()

    insert_sql = f"""
        INSERT INTO {schema}.{table} (
            zpid,
            extract_date,
            street_address,
            zipcode,
            city,
            state,
            latitude,
            longitude,
            price,
            bathrooms,
            bedrooms,
            living_area,
            home_type,
            home_status,
            days_on_zillow,
            is_featured,
            should_highlight,
            zestimate,
            rent_zestimate,
            is_open_house,
            is_fsba,
            open_house,
            is_unmappable,
            is_preforeclosure_auction,
            home_status_for_hdp,
            price_for_hdp,
            is_non_owner_occupied,
            is_premier_builder,
            is_zillow_owned,
            currency,
            country,
            tax_assessed_value,
            lot_area_value,
            lot_area_unit
        )
        SELECT
            zpid,
            extract_date,
            street_address,
            zipcode,
            city,
            state,
            latitude,
            longitude,
            price,
            bathrooms,
            bedrooms,
            living_area,
            home_type,
            home_status,
            days_on_zillow,
            is_featured,
            should_highlight,
            zestimate,
            rent_zestimate,
            is_open_house,
            is_fsba,
            open_house,
            is_unmappable,
            is_preforeclosure_auction,
            home_status_for_hdp,
            price_for_hdp,
            is_non_owner_occupied,
            is_premier_builder,
            is_zillow_owned,
            currency,
            country,
            tax_assessed_value,
            lot_area_value,
            lot_area_unit
        FROM json_populate_recordset(NULL::{schema}.{table}, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(listings), ))

