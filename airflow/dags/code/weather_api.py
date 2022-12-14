import sys
sys.path.append('/opt/airflow/dags/code/')

from constants import weather_api_token
import requests
from datetime import timedelta, date
import time

def request_current(place):
    place_clean = place.replace(' ', '%20')
    search_url = f'https://api.weatherapi.com/v1/current.json?key={weather_api_token}%20&q={place_clean}'
    response = requests.get(search_url)
    return response.json()

def request_historical(place, date, retry_sleep_time = 60, max_attempts = 3):
    place_clean = place.replace(' ', '%20')
    search_url = f'https://api.weatherapi.com/v1/history.json?key={weather_api_token}%20&q={place_clean}&dt={date}'
    for i in range(max_attempts):
        response = requests.get(search_url)
        if response.status_code == 200:
            return response.json()
        else:
            if i < max_attempts - 1:
                print(f'API call failed, retrying in {retry_sleep_time} seconds...')
                time.sleep(retry_sleep_time)
    print('Maximum number of attempts reached without success')
    return {} # return nothing if API call fails

# request daily forecast data over date range (smaller than 30 days) - only available while PRO plan trial is active
def request_historical_batch(place, start_date, end_date, retry_sleep_time = 60, max_attempts = 3):
    place_clean = place.replace(' ', '%20')
    search_url = f'https://api.weatherapi.com/v1/history.json?key={weather_api_token}%20&q={place_clean}&dt={start_date}&end_dt={end_date}'
    for i in range(max_attempts):
        response = requests.get(search_url)
        if response.status_code == 200:
            return response.json()
        else:
            if i < max_attempts - 1:
                print(f'API call failed, retrying in {retry_sleep_time} seconds...')
                time.sleep(retry_sleep_time)
    print('Maximum number of attempts reached without success')
    return {} # return nothing if API call fails

def extract_day_forecast(json, day_num):
    output = {'date': json['forecast']['forecastday'][day_num]['date']}
    output.update(json['forecast']['forecastday'][day_num]['day'])
    output.pop('condition')
    return output

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def download_weather_data(location, location_field_name, start_date, end_date, retry_sleep_time = 60, api_max_attempts = 3):
    data = []
    for day in daterange(start_date, end_date + timedelta(1)):
        json = request_historical(location, day.strftime('%Y-%m-%d'), retry_sleep_time, api_max_attempts)
        if json:
            daily_forecast = extract_day_forecast(json, 0)
            daily_forecast.update({location_field_name: location})
            data.append(daily_forecast)
    return data

# downloading weather data in batches (only available while PRO plan trial is active) to minimize number of calls for ingesting old weather data
def download_weather_data_batch(location, location_field_name, start_date, end_date, retry_sleep_time = 60, api_max_attempts = 3):
    data = []
    # for day in daterange(start_date, end_date + timedelta(1)):
    json = request_historical_batch(location, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), retry_sleep_time, api_max_attempts)
    if json:
        num_days = len(json['forecast']['forecastday'])
        for idx in range(num_days):
            daily_forecast = extract_day_forecast(json, idx)
            daily_forecast.update({location_field_name: location})
            data.append(daily_forecast)
    return data

# IDEA: loop through all zip codes in CA or US and use that as query parameter for retrieving weather data
# consider getting air pollution data from weather API - could be interesting to track over time
# loop to extract data for extended historical period?
# could use airflow to do batch download of historical data, and to set up future daily/weekly pulls
    # would set up pythonOperator function that loops over each day and calls on API

# set up DAG to request current/forecast data on daily basis
# probably have to think about how to combine current with historical data, since data is different between the two requests
    # historical data gives values in ranges (e.g. min and max temp), current data only shows one exact value (probably at the time of call)