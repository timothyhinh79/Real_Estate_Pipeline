import sys
sys.path.append('/opt/airflow/dags/code/')

import requests

from us_census_api_mappings import table_codes, race_codes, agesex_group_codes, income_group_codes, breakout_type_codes

def retrieve_code(mapping_dict, value):
    code = [k for k, v in mapping_dict.items() if v == value]
    if code:
        return code[0]
    else:
        return ''

def construct_table_id(table = '', race = '', agesex_group = '', income_group = ''):
    if agesex_group and income_group:
        print('Only one of agesex_group or income_group can be defined, not both.')
        return ''

    table_code = retrieve_code(table_codes, table)
    race_code = retrieve_code(race_codes, race)

    if agesex_group:
        line_number_code = retrieve_code(agesex_group_codes, agesex_group)
    elif income_group:
        line_number_code = retrieve_code(income_group_codes, income_group)
    else:
        line_number_code = '001'

    return f'{table_code}{race_code}_{line_number_code}E'

def construct_get_url(table = '', race = '', agesex_group = '', income_group = ''):
    table_id = construct_table_id(table, race, agesex_group, income_group)
    return f'get=NAME,{table_id}'

def construct_breakout_url(breakout = 'zip code tabulation area', filters = {}):
    breakout_url = ''
    if breakout:
        if breakout in filters:
            value = filters[breakout]
        else:
            value = '*'
        breakout_url += f'&for={breakout}:{value}'

    return breakout_url

def construct_filter_url(breakout = 'zip code tabulation area', filters = {}):
    filter_url = ''
    for filter_field, filter_val in filters.items():
        if filter_field != breakout:
            filter_url += f'&in={filter_field}:{filter_val}'
    return filter_url

def census_url(year, dataset = 'acs5', table = '', race = '', agesex_group = '', income_group = '', breakout = 'zip code tabulation area', filters = {}):
    get_url = construct_get_url(table, race, agesex_group, income_group)
    breakout_url = construct_breakout_url(breakout, filters)
    filter_url = construct_filter_url(breakout, filters)

    return f'https://api.census.gov/data/{year}/acs/{dataset}?{get_url}{breakout_url}{filter_url}'

def convert_to_json(census_output):
    keys = census_output[0]
    json_rows = []
    for row in census_output[1:]:
        json_rows.append({key: value for key, value in zip(keys, row)})
    return json_rows

def get_census_data(year, dataset = 'acs5', table = '', race = '', agesex_group = '', income_group = '', breakout = 'zip code tabulation area', filters = {}):
    url = census_url(year, dataset, table, race, agesex_group, income_group, breakout, filters)
    response = requests.get(url)
    return convert_to_json(response.json())

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


