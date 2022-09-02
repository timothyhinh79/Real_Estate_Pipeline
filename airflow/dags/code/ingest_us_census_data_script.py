from us_census_api_mappings import table_codes, race_codes, agesex_group_codes, income_group_codes, breakout_type_codes
from us_census_api import *
import psycopg2
import json


def ingest_us_census_callable(year, census_dataset, zips, database, schema, user, password, host, port):

    print('year:', year)
    print('census_dataset:', census_dataset)
    print('database:', database)
    print('user:', user)
    print('password:', password)
    print('host:', host)
    print('port:', port)

    population_by_race_and_zip = get_population_breakout_by_zip(year, census_dataset, 'sex_by_age','population','race',zips)
    population_by_agesex_and_zip = get_population_breakout_by_zip(year, census_dataset, 'sex_by_age','population','agesex_group',zips)
    population_by_incomelevel_and_zip = get_population_breakout_by_zip(year, census_dataset, 'household_income_last_12_months','num_households','income_group',zips)
    median_income_by_zip = get_population_by_zip(year, census_dataset, 'median_household_income_last_12_months', 'median_income', zips)
    median_age_by_zip = get_population_by_zip(year, census_dataset, 'median_age_by_sex', 'median_age', zips)
    
    conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
    conn.autocommit = True
    cursor = conn.cursor()

    insert_sql = f"""
        INSERT INTO {schema}.population_by_race_and_zip (
            year,
            dataset,
            zip,
            race,
            population
        )
        SELECT
            year,
            dataset,
            zip,
            race,
            population
        FROM json_populate_recordset(NULL::{schema}.population_by_race_and_zip, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(population_by_race_and_zip), ))

    insert_sql = f"""
        INSERT INTO {schema}.population_by_agesex_and_zip (
            year,
            dataset,
            zip,
            sex,
            min_age,
            max_age,
            population
        )
        SELECT
            year,
            dataset,
            zip,
            sex,
            min_age,
            max_age,
            population
        FROM json_populate_recordset(NULL::{schema}.population_by_agesex_and_zip, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(population_by_agesex_and_zip), ))

    insert_sql = f"""
        INSERT INTO {schema}.population_by_incomelevel_and_zip (
            year,
            dataset,
            zip,
            min_income,
            max_income,
            population
        )
        SELECT
            year,
            dataset,
            zip,
            min_income,
            max_income,
            population
        FROM json_populate_recordset(NULL::{schema}.population_by_incomelevel_and_zip, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(population_by_incomelevel_and_zip), ))

    insert_sql = f"""
        INSERT INTO {schema}.median_income_by_zip (
            year,
            dataset,
            zip,
            median_income
        )
        SELECT
            year,
            dataset,
            zip,
            median_income
        FROM json_populate_recordset(NULL::{schema}.median_income_by_zip, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(median_income_by_zip), ))

    insert_sql = f"""
        INSERT INTO {schema}.median_age_by_zip (
            year,
            dataset,
            zip,
            median_age
        )
        SELECT
            year,
            dataset,
            zip,
            median_age
        FROM json_populate_recordset(NULL::{schema}.median_age_by_zip, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(median_age_by_zip), ))
    

