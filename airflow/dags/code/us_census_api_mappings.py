table_codes = {
    'B01001': 'sex_by_age',
    'B19001I': 'household_income_last_12_months',
    'B19013': 'median_household_income_last_12_months',
    'B01002': 'median_age_by_sex'
}

race_codes = {
    'A': 'White',
    'B': 'Black or African American',
    'C': 'American Indian and Alaska Native',
    'D': 'Asian',
    'E': 'Native Hawaiian and Other Pacific Islander',
    'F': 'Some Other Race',
    'G': 'Two or More Races',
    'H': 'White, Not Hispanic or Latino',
    'I': 'Hispanic or Latino'
}

agesex_group_codes = {
    '001': 'total',
    '002': 'male',
    '003': {'sex': 'male', 'min_age': 0, 'max_age': 4},
    '004': {'sex': 'male', 'min_age': 5, 'max_age': 9},
    '005': {'sex': 'male', 'min_age': 10, 'max_age': 14},
    '006': {'sex': 'male', 'min_age': 15, 'max_age': 17},
    '007': {'sex': 'male', 'min_age': 18, 'max_age': 19},
    '008': {'sex': 'male', 'min_age': 20, 'max_age': 20},
    '009': {'sex': 'male', 'min_age': 21, 'max_age': 21},
    '010': {'sex': 'male', 'min_age': 22, 'max_age': 24},
    '011': {'sex': 'male', 'min_age': 25, 'max_age': 29},
    '012': {'sex': 'male', 'min_age': 30, 'max_age': 34},
    '013': {'sex': 'male', 'min_age': 35, 'max_age': 39},
    '014': {'sex': 'male', 'min_age': 40, 'max_age': 44},
    '015': {'sex': 'male', 'min_age': 45, 'max_age': 49},
    '016': {'sex': 'male', 'min_age': 50, 'max_age': 54},
    '017': {'sex': 'male', 'min_age': 55, 'max_age': 59},
    '018': {'sex': 'male', 'min_age': 60, 'max_age': 61},
    '019': {'sex': 'male', 'min_age': 62, 'max_age': 64},
    '020': {'sex': 'male', 'min_age': 65, 'max_age': 66},
    '021': {'sex': 'male', 'min_age': 67, 'max_age': 69},
    '022': {'sex': 'male', 'min_age': 70, 'max_age': 74},
    '023': {'sex': 'male', 'min_age': 75, 'max_age': 79},
    '024': {'sex': 'male', 'min_age': 80, 'max_age': 84},
    '025': {'sex': 'male', 'min_age': 85, 'max_age': 1000},
    '026': 'female',
    '027': {'sex': 'female', 'min_age': 0, 'max_age': 4},
    '028': {'sex': 'female', 'min_age': 5, 'max_age': 9},
    '029': {'sex': 'female', 'min_age': 10, 'max_age': 14},
    '030': {'sex': 'female', 'min_age': 15, 'max_age': 17},
    '031': {'sex': 'female', 'min_age': 18, 'max_age': 19},
    '032': {'sex': 'female', 'min_age': 20, 'max_age': 20},
    '033': {'sex': 'female', 'min_age': 21, 'max_age': 21},
    '034': {'sex': 'female', 'min_age': 22, 'max_age': 24},
    '035': {'sex': 'female', 'min_age': 25, 'max_age': 29},
    '036': {'sex': 'female', 'min_age': 30, 'max_age': 34},
    '037': {'sex': 'female', 'min_age': 35, 'max_age': 39},
    '038': {'sex': 'female', 'min_age': 40, 'max_age': 44},
    '039': {'sex': 'female', 'min_age': 45, 'max_age': 49},
    '040': {'sex': 'female', 'min_age': 50, 'max_age': 54},
    '041': {'sex': 'female', 'min_age': 55, 'max_age': 59},
    '042': {'sex': 'female', 'min_age': 60, 'max_age': 61},
    '043': {'sex': 'female', 'min_age': 62, 'max_age': 64},
    '044': {'sex': 'female', 'min_age': 65, 'max_age': 66},
    '045': {'sex': 'female', 'min_age': 67, 'max_age': 69},
    '046': {'sex': 'female', 'min_age': 70, 'max_age': 74},
    '047': {'sex': 'female', 'min_age': 75, 'max_age': 79},
    '048': {'sex': 'female', 'min_age': 80, 'max_age': 84},
    '049': {'sex': 'female', 'min_age': 85, 'max_age': 1000}
}

income_group_codes = {
    '001': 'total',
    '002': {'min_income': 0, 'max_income': 9_999},
    '003': {'min_income': 10_000, 'max_income': 14_999},
    '004': {'min_income': 15_000, 'max_income': 19_999},
    '005': {'min_income': 20_000, 'max_income': 24_999},
    '006': {'min_income': 25_000, 'max_income': 29_999},
    '007': {'min_income': 30_000, 'max_income': 34_999},
    '008': {'min_income': 35_000, 'max_income': 39_999},
    '009': {'min_income': 40_000, 'max_income': 44_999},
    '010': {'min_income': 45_000, 'max_income': 49_999},
    '011': {'min_income': 50_000, 'max_income': 59_999},
    '012': {'min_income': 60_000, 'max_income': 74_999},
    '013': {'min_income': 75_000, 'max_income': 99_999},
    '014': {'min_income': 100_000, 'max_income': 124_999},
    '015': {'min_income': 125_000, 'max_income': 149_999},
    '016': {'min_income': 150_000, 'max_income': 199_999},
    '017': {'min_income': 200_000, 'max_income': 1_000_000_000}
}

breakout_type_codes = {
    'agesex_group': agesex_group_codes,
    'income_group': income_group_codes,
    'race': race_codes
}
