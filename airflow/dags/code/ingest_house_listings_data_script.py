import json
import psycopg2
import time
from datetime import date, timedelta
from zillow_scraper import *

def ingest_listings_data(execution_date, database, user, password, host, port, locations, date_to_drop_table, sleep_time_between_pages, **kwargs):

    print('execution_date:', execution_date)
    print('database:', database)
    print('user:', user)
    print('password:', password)
    print('host:', host)
    print('port:', port)

    # begin to end date should cover 1 calendar month
    begin_date = date(execution_date.year, execution_date.month, 1)
    if execution_date.month == 12:
        end_year = execution_date.year + 1
        end_month = 1
    else:
        end_year = execution_date.year
        end_month = execution_date.month + 1
    end_date = date(end_year, end_month, 1) - timedelta(1)

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

    # dropping table if ingesting data for earliest month
    # if begin_date == date_to_drop_table:
    cursor.execute("""
        DROP TABLE IF EXISTS house_listings
    """)

    create_table_sql = """
        CREATE TABLE IF NOT EXISTS house_listings (
            id SERIAL PRIMARY KEY,
            extract_date DATE NOT NULL,
            zpid INTEGER,
            street_address VARCHAR(255),
            zipcode VARCHAR(20),
            city VARCHAR(255),
            state VARCHAR(20),
            latitude FLOAT,
            longitude FLOAT,
            price FLOAT,
            bathrooms FLOAT,
            bedrooms FLOAT,
            living_area FLOAT,
            home_type VARCHAR(255),
            home_status VARCHAR(255),
            days_on_zillow INTEGER,
            is_featured BOOLEAN,
            should_highlight BOOLEAN,
            zestimate FLOAT,
            rent_zestimate FLOAT,
            is_open_house BOOLEAN,
            is_fsba BOOLEAN,
            open_house VARCHAR(255),
            is_unmappable BOOLEAN,
            is_preforeclosure_auction BOOLEAN,
            home_status_for_hdp VARCHAR(255),
            price_for_hdp FLOAT,
            is_non_owner_occupied BOOLEAN,
            is_premier_builder BOOLEAN,
            is_zillow_owned BOOLEAN,
            currency VARCHAR(20),
            country VARCHAR(255),
            tax_assessed_value FLOAT,
            lot_area_value FLOAT,
            lot_area_unit VARCHAR(255)
        )
    """
    cursor.execute(create_table_sql)

    insert_sql = """
        INSERT INTO house_listings (
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
        FROM json_populate_recordset(NULL::house_listings, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(listings), ))

