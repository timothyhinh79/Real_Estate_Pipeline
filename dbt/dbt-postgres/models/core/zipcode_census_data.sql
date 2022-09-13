
{{ config(materialized='table')}}

-- getting latest census data
WITH latest_year AS (
    SELECT MAX(year) as year
    FROM {{ ref('stg_median_age_income_by_zip') }}
)

SELECT 
    age_income.id
    , age_income.year
    , age_income.dataset
    , age_income.zip
    , age_income.median_age
    , age_income.median_income

    -- population breakout by agesex
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '0 - 4' THEN pop_by_agesex.population ELSE 0 END) AS female_0_4_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '5 - 9' THEN pop_by_agesex.population ELSE 0 END) AS female_5_9_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '10 - 14' THEN pop_by_agesex.population ELSE 0 END) AS female_10_14_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '15 - 17' THEN pop_by_agesex.population ELSE 0 END) AS female_15_17_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '18 - 19' THEN pop_by_agesex.population ELSE 0 END) AS female_18_19_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '20 - 20' THEN pop_by_agesex.population ELSE 0 END) AS female_20_20_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '21 - 21' THEN pop_by_agesex.population ELSE 0 END) AS female_21_21_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '22 - 24' THEN pop_by_agesex.population ELSE 0 END) AS female_22_24_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '25 - 29' THEN pop_by_agesex.population ELSE 0 END) AS female_25_29_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '30 - 34' THEN pop_by_agesex.population ELSE 0 END) AS female_30_34_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '35 - 39' THEN pop_by_agesex.population ELSE 0 END) AS female_35_39_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '40 - 44' THEN pop_by_agesex.population ELSE 0 END) AS female_40_44_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '45 - 49' THEN pop_by_agesex.population ELSE 0 END) AS female_45_49_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '50 - 54' THEN pop_by_agesex.population ELSE 0 END) AS female_50_54_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '55 - 59' THEN pop_by_agesex.population ELSE 0 END) AS female_55_59_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '60 - 61' THEN pop_by_agesex.population ELSE 0 END) AS female_60_61_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '62 - 64' THEN pop_by_agesex.population ELSE 0 END) AS female_62_64_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '65 - 66' THEN pop_by_agesex.population ELSE 0 END) AS female_65_66_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '67 - 69' THEN pop_by_agesex.population ELSE 0 END) AS female_67_69_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '70 - 74' THEN pop_by_agesex.population ELSE 0 END) AS female_70_74_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '75 - 79' THEN pop_by_agesex.population ELSE 0 END) AS female_75_79_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '80 - 84' THEN pop_by_agesex.population ELSE 0 END) AS female_80_84_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'female' AND pop_by_agesex.age_range = '85+' THEN pop_by_agesex.population ELSE 0 END) AS female_85plus_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '0 - 4' THEN pop_by_agesex.population ELSE 0 END) AS male_0_4_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '5 - 9' THEN pop_by_agesex.population ELSE 0 END) AS male_5_9_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '10 - 14' THEN pop_by_agesex.population ELSE 0 END) AS male_10_14_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '15 - 17' THEN pop_by_agesex.population ELSE 0 END) AS male_15_17_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '18 - 19' THEN pop_by_agesex.population ELSE 0 END) AS male_18_19_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '20 - 20' THEN pop_by_agesex.population ELSE 0 END) AS male_20_20_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '21 - 21' THEN pop_by_agesex.population ELSE 0 END) AS male_21_21_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '22 - 24' THEN pop_by_agesex.population ELSE 0 END) AS male_22_24_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '25 - 29' THEN pop_by_agesex.population ELSE 0 END) AS male_25_29_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '30 - 34' THEN pop_by_agesex.population ELSE 0 END) AS male_30_34_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '35 - 39' THEN pop_by_agesex.population ELSE 0 END) AS male_35_39_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '40 - 44' THEN pop_by_agesex.population ELSE 0 END) AS male_40_44_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '45 - 49' THEN pop_by_agesex.population ELSE 0 END) AS male_45_49_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '50 - 54' THEN pop_by_agesex.population ELSE 0 END) AS male_50_54_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '55 - 59' THEN pop_by_agesex.population ELSE 0 END) AS male_55_59_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '60 - 61' THEN pop_by_agesex.population ELSE 0 END) AS male_60_61_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '62 - 64' THEN pop_by_agesex.population ELSE 0 END) AS male_62_64_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '65 - 66' THEN pop_by_agesex.population ELSE 0 END) AS male_65_66_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '67 - 69' THEN pop_by_agesex.population ELSE 0 END) AS male_67_69_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '70 - 74' THEN pop_by_agesex.population ELSE 0 END) AS male_70_74_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '75 - 79' THEN pop_by_agesex.population ELSE 0 END) AS male_75_79_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '80 - 84' THEN pop_by_agesex.population ELSE 0 END) AS male_80_84_pop
    , SUM(CASE WHEN pop_by_agesex.sex = 'male' AND pop_by_agesex.age_range = '85+' THEN pop_by_agesex.population ELSE 0 END) AS male_85plus_pop

    -- population breakout by income level
    , SUM(CASE WHEN pop_by_income.income_range = '0 - 9999' THEN pop_by_income.population ELSE 0 END) AS income_0_9999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '10000 - 14999' THEN pop_by_income.population ELSE 0 END) AS income_10000_14999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '15000 - 19999' THEN pop_by_income.population ELSE 0 END) AS income_15000_19999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '20000 - 24999' THEN pop_by_income.population ELSE 0 END) AS income_20000_24999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '25000 - 29999' THEN pop_by_income.population ELSE 0 END) AS income_25000_29999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '30000 - 34999' THEN pop_by_income.population ELSE 0 END) AS income_30000_34999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '35000 - 39999' THEN pop_by_income.population ELSE 0 END) AS income_35000_39999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '40000 - 44999' THEN pop_by_income.population ELSE 0 END) AS income_40000_44999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '45000 - 49999' THEN pop_by_income.population ELSE 0 END) AS income_45000_49999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '50000 - 59999' THEN pop_by_income.population ELSE 0 END) AS income_50000_59999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '60000 - 74999' THEN pop_by_income.population ELSE 0 END) AS income_60000_74999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '75000 - 99999' THEN pop_by_income.population ELSE 0 END) AS income_75000_99999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '100000 - 124999' THEN pop_by_income.population ELSE 0 END) AS income_100000_124999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '125000 - 149999' THEN pop_by_income.population ELSE 0 END) AS income_125000_149999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '150000 - 199999' THEN pop_by_income.population ELSE 0 END) AS income_150000_199999_pop
    , SUM(CASE WHEN pop_by_income.income_range = '200000+' THEN pop_by_income.population ELSE 0 END) AS income_200000plus_pop

    -- population breakout by race
    , SUM(CASE WHEN pop_by_race.race = 'American Indian and Alaska Native' THEN pop_by_race.population ELSE 0 END) AS race_american_native_pop
    , SUM(CASE WHEN pop_by_race.race = 'Asian' THEN pop_by_race.population ELSE 0 END) AS race_asian_pop
    , SUM(CASE WHEN pop_by_race.race = 'Black or African American' THEN pop_by_race.population ELSE 0 END) AS race_black_pop
    , SUM(CASE WHEN pop_by_race.race = 'Hispanic or Latino' THEN pop_by_race.population ELSE 0 END) AS race_hispanic_latino_pop
    , SUM(CASE WHEN pop_by_race.race = 'Native Hawaiian and Other Pacific Islander' THEN pop_by_race.population ELSE 0 END) AS race_native_hawaiian_pop
    , SUM(CASE WHEN pop_by_race.race = 'Some Other Race' THEN pop_by_race.population ELSE 0 END) AS race_other_pop
    , SUM(CASE WHEN pop_by_race.race = 'Two or More Races' THEN pop_by_race.population ELSE 0 END) AS race_two_or_more_pop
    , SUM(CASE WHEN pop_by_race.race = 'White' THEN pop_by_race.population ELSE 0 END) AS race_white_pop
    , SUM(CASE WHEN pop_by_race.race = 'White, Not Hispanic or Latino' THEN pop_by_race.population ELSE 0 END) AS race_white_not_hispanic_pop
     

FROM {{ ref('stg_median_age_income_by_zip') }} age_income
    INNER JOIN latest_year
        ON age_income.year = latest_year.year
    INNER JOIN {{ ref('stg_population_by_agesex_and_zip') }} pop_by_agesex
        ON age_income.zip = pop_by_agesex.zip
    INNER JOIN {{ ref('stg_population_by_incomelevel_and_zip') }} pop_by_income
        ON age_income.zip = pop_by_income.zip
    INNER JOIN {{ ref('stg_population_by_race_and_zip') }} pop_by_race
        ON age_income.zip = pop_by_race.zip
        
GROUP BY 
    age_income.id
    , age_income.year
    , age_income.dataset
    , age_income.zip
    , age_income.median_age
    , age_income.median_income