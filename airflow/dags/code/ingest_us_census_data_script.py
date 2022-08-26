from us_census_api_mappings import table_codes, race_codes, agesex_group_codes, income_group_codes
from us_census_api import *
import psycopg2
import json

breakout_type_codes = {
    'agesex_group': agesex_group_codes,
    'income_group': income_group_codes,
    'race': race_codes
}

def clean_row(row, year, dataset, new_value_col_name, old_value_col_name, new_col_name = '', new_col_val = ''):
    output = row.copy()
    if new_col_val:
        if type(new_col_val) == dict:
            output.update(new_col_val)
        else:
            output.update({new_col_name: new_col_val})
    output[new_value_col_name] = output.pop(old_value_col_name)
    output['zip'] = output.pop('zip code tabulation area')
    output['year'] = year
    output['dataset'] = dataset
    return output

def filter_rows(rows, field, values):
    return [row for row in rows if row[field] in values]

def get_population_breakout_by_zip(year, census_dataset, table, table_measure, breakout_type, zips):
    output = []
    breakout_values = [breakout_value for breakout_value in breakout_type_codes[breakout_type].values() if breakout_value not in ['total','male','female']]
    # getting population by zip code for each ethnicity, limited to the provided zip codes
    for breakout_value in breakout_values:
        breakout_dict = {breakout_type: breakout_value}
        pop_by_zip = get_census_data(year, dataset = census_dataset, table = table, **breakout_dict, breakout = 'zip code tabulation area')
        pop_by_zip_local = filter_rows(pop_by_zip, 'zip code tabulation area', zips)
        pop_by_zip_local_clean = [clean_row(row, year, census_dataset, table_measure, construct_table_id(table, **breakout_dict), breakout_type, breakout_value) for row in pop_by_zip_local]
        output += pop_by_zip_local_clean
    return output

def get_population_by_zip(year, census_dataset, table, table_measure, zips):
    pop_by_zip = get_census_data(year, dataset = census_dataset, table = table, breakout = 'zip code tabulation area')
    pop_by_zip_local = filter_rows(pop_by_zip, 'zip code tabulation area', zips) 
    pop_by_zip_local_clean = [clean_row(row, year, census_dataset, table_measure, construct_table_id(table)) for row in pop_by_zip_local]
    return pop_by_zip_local_clean


def ingest_us_census_callable(year, census_dataset, zips, database, user, password, host, port):

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

    insert_sql = """
        INSERT INTO population_by_race_and_zip (
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
        FROM json_populate_recordset(NULL::population_by_race_and_zip, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(population_by_race_and_zip), ))

    insert_sql = """
        INSERT INTO population_by_agesex_and_zip (
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
        FROM json_populate_recordset(NULL::population_by_agesex_and_zip, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(population_by_agesex_and_zip), ))

    insert_sql = """
        INSERT INTO population_by_incomelevel_and_zip (
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
        FROM json_populate_recordset(NULL::population_by_incomelevel_and_zip, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(population_by_incomelevel_and_zip), ))

    insert_sql = """
        INSERT INTO median_income_by_zip (
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
        FROM json_populate_recordset(NULL::median_income_by_zip, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(median_income_by_zip), ))

    insert_sql = """
        INSERT INTO median_age_by_zip (
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
        FROM json_populate_recordset(NULL::median_age_by_zip, %s)
    """
    cursor.execute(insert_sql, vars = (json.dumps(median_age_by_zip), ))
    

