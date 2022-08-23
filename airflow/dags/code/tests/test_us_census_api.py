from us_census_api import *


def test_retrieve_code():
    assert retrieve_code(table_codes, 'sex_by_age') == 'B01001'

def test_retrieve_code_if_value_is_empty_string():
    assert retrieve_code(race_codes, '') == ''

def test_construct_get_url_with_agesex_group():
    get_url = construct_get_url(table = 'sex_by_age', race = 'Asian', agesex_group={'sex': 'male', 'min_age': 0, 'max_age': 4}) 
    assert get_url == 'get=NAME,B01001D_003E'

def test_construct_get_url_with_income_group():
    get_url = construct_get_url(table = 'household_income_last_12_months', income_group={'min_income': 100_000, 'max_income': 124_999}) 
    assert get_url == 'get=NAME,B19001I_014E'

def test_construct_get_url_with_no_agesex_or_income_group():
    get_url = construct_get_url(table = 'sex_by_age') 
    assert get_url == 'get=NAME,B01001_001E'

def test_construct_breakout_url():
    breakout_url = construct_breakout_url(breakout = 'county', filters = {'state': '06'})
    assert breakout_url == '&for=county:*'

def test_construct_breakout_url_if_breakout_is_in_filters():
    breakout_url = construct_breakout_url(breakout = 'state', filters = {'state': '06'})
    assert breakout_url == '&for=state:06'

def test_construct_filter_url():
    filter_url = construct_filter_url(breakout = 'county', filters = {'state': '06'})
    assert filter_url == '&in=state:06'

def test_construct_filter_url_if_breakout_is_in_filters():
    filter_url = construct_filter_url(breakout = 'state', filters = {'state': '06'})
    assert filter_url == ''

def test_construct_filter_url_if_multiple_filters():
    filter_url = construct_filter_url(breakout = 'tract', filters = {'state': '06', 'county': '073'})
    assert filter_url == '&in=state:06&in=county:073'

def test_census_url():
    url = census_url(2020, dataset = 'acs5', table = 'sex_by_age', race = 'Asian', breakout = 'tract', filters = {'state': '06', 'county':'073'}) 
    assert url == 'https://api.census.gov/data/2020/acs/acs5?get=NAME,B01001D_001E&for=tract:*&in=state:06&in=county:073'

def test_convert_to_json():
    sample_census_output = [['NAME', 'B01001_001E', 'state'], ['Pennsylvania', '12794885', '42'], ['California', '39346023', '06'], ['West Virginia', '1807426', '54']]
    json = convert_to_json(sample_census_output)
    assert json == [
        {'NAME': 'Pennsylvania', 'B01001_001E': '12794885', 'state': '42'},
        {'NAME': 'California', 'B01001_001E': '39346023', 'state': '06'},
        {'NAME': 'West Virginia', 'B01001_001E': '1807426', 'state': '54'},
    ]

def test_get_census_data():
    sample_output = [{'NAME': 'California', 'B01001_007E': '525740', 'state': '06'}]
    json_data = get_census_data(2020, dataset = 'acs5', table = 'sex_by_age', agesex_group={'sex': 'male', 'min_age' : 18, 'max_age' : 19}, breakout = 'state', filters = {'state':'06'})
    assert json_data == sample_output
