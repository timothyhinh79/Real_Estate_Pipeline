import json
import psycopg2
from weather_api import *

def ingest_weekly_weather_data(execution_date, database, schema, table, user, password, host, port, locations, retry_sleep_time, api_max_attempts, **kwargs):

    print('execution_date:', execution_date)
    print('database:', database)
    print('user:', user)
    print('password:', password)
    print('Host:', host)
    print('port:', port)

    execution_date_param  = date(execution_date.year, execution_date.month, execution_date.day)
    json_data = []
    for location in locations:
        json_data = json_data + download_weather_data(location, 'zip_code', execution_date_param, execution_date_param + timedelta(6), retry_sleep_time, api_max_attempts)

    conn = psycopg2.connect(database=database,user = user, password = password, host = host, port = port)
    conn.autocommit = True
    cursor = conn.cursor()

    insert_sql = f"""
        INSERT INTO {schema}.{table} (
            zip_code,
            date,
            maxtemp_c,
            maxtemp_f,
            mintemp_c,
            mintemp_f,
            avgtemp_c,
            avgtemp_f,
            maxwind_mph,
            maxwind_kph,
            totalprecip_mm,
            totalprecip_in,
            avgvis_km,
            avgvis_miles,
            avghumidity,
            uv
        )
        SELECT
            zip_code,
            date,
            maxtemp_c,
            maxtemp_f,
            mintemp_c,
            mintemp_f,
            avgtemp_c,
            avgtemp_f,
            maxwind_mph,
            maxwind_kph,
            totalprecip_mm,
            totalprecip_in,
            avgvis_km,
            avgvis_miles,
            avghumidity,
            uv
        FROM json_populate_recordset(NULL::{schema}.{table}, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(json_data), ))


def ingest_monthly_weather_data_batch(execution_date, database, schema, table, user, password, host, port, locations, retry_sleep_time, api_max_attempts, **kwargs):

    print('execution_date:', execution_date)
    print('database:', database)
    print('user:', user)
    print('password:', password)
    print('Host:', host)
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

    json_data = []
    for location in locations:
        # download_weather_data_batch(location, location_field_name, start_date, end_date):
        json_data = json_data + download_weather_data_batch(location, 'zip_code', begin_date, end_date, retry_sleep_time, api_max_attempts)

    conn = psycopg2.connect(database=database,user = user, password = password, host = host, port = port)
    conn.autocommit = True
    cursor = conn.cursor()

    insert_sql = f"""
        INSERT INTO {schema}.{table} (
            zip_code,
            date,
            maxtemp_c,
            maxtemp_f,
            mintemp_c,
            mintemp_f,
            avgtemp_c,
            avgtemp_f,
            maxwind_mph,
            maxwind_kph,
            totalprecip_mm,
            totalprecip_in,
            avgvis_km,
            avgvis_miles,
            avghumidity,
            uv
        )
        SELECT
            zip_code,
            date,
            maxtemp_c,
            maxtemp_f,
            mintemp_c,
            mintemp_f,
            avgtemp_c,
            avgtemp_f,
            maxwind_mph,
            maxwind_kph,
            totalprecip_mm,
            totalprecip_in,
            avgvis_km,
            avgvis_miles,
            avghumidity,
            uv
        FROM json_populate_recordset(NULL::{schema}.{table}, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(json_data), ))