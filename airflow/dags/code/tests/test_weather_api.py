
from weather_api import *
from datetime import date, timedelta

sample_current_response = \
    {
        "location":{
            "name":"Los Angeles","region":"California","country":"USA",
            "lat":33.97,"lon":-118.24,"tz_id":"America/Los_Angeles",
            "localtime_epoch":1661553924,"localtime":"2022-08-26 15:45"
        },
        "current":{
            "last_updated_epoch":1661553000,"last_updated":"2022-08-26 15:30",
            "temp_c":26.0,"temp_f":78.8,"is_day":1,
            "condition":{"text":"Partly cloudy",
                        "icon":"//cdn.weatherapi.com/weather/64x64/day/116.png","code":1003},
            "wind_mph":19.2,"wind_kph":31.0,"wind_degree":280,"wind_dir":"W","pressure_mb":1013.0,
            "pressure_in":29.9,"precip_mm":0.0,"precip_in":0.0,"humidity":61,"cloud":25,"feelslike_c":26.1,
            "feelslike_f":79.1,"vis_km":16.0,"vis_miles":9.0,"uv":8.0,"gust_mph":11.9,"gust_kph":19.1
        }
    }

def test_request_current():
    current_weather = request_current('90001')
    assert 'location' in current_weather.keys()
    assert 'current' in current_weather.keys()
    expected_fields = ['temp_c', 'temp_f', 'is_day','condition','wind_mph','wind_kph','wind_degree', 'wind_dir', 
                        'precip_mm','precip_in','humidity',
                        'feelslike_f','vis_km', 'vis_miles','uv']
    assert all([expected_field in current_weather['current'].keys() for expected_field in expected_fields])

def test_request_historical():
    historical_weather = request_historical('90001', '2022-08-01')
    assert 'location' in historical_weather.keys()
    assert 'forecast' in historical_weather.keys()
    expected_fields = [ 'maxtemp_c',
                        'maxtemp_f',
                        'mintemp_c',
                        'mintemp_f',
                        'avgtemp_c',
                        'avgtemp_f',
                        'maxwind_mph',
                        'maxwind_kph',
                        'totalprecip_mm',
                        'totalprecip_in',
                        'avgvis_km',
                        'avgvis_miles',
                        'avghumidity',
                        'uv'
                        ]
    assert all([expected_field in historical_weather['forecast']['forecastday'][0]['day'].keys() for expected_field in expected_fields])

def test_request_historical_batch():
    historical_weather_batch = request_historical_batch('90001', '2022-07-01','2022-07-31')
    assert 'location' in historical_weather_batch.keys()
    assert 'forecast' in historical_weather_batch.keys()
    assert len(historical_weather_batch['forecast']['forecastday']) == 31
    expected_fields = [ 'maxtemp_c',
                        'maxtemp_f',
                        'mintemp_c',
                        'mintemp_f',
                        'avgtemp_c',
                        'avgtemp_f',
                        'maxwind_mph',
                        'maxwind_kph',
                        'totalprecip_mm',
                        'totalprecip_in',
                        'avgvis_km',
                        'avgvis_miles',
                        'avghumidity',
                        'uv'
                        ]
    assert all([expected_field in historical_weather_batch['forecast']['forecastday'][0]['day'].keys() for expected_field in expected_fields])

def test_extract_day_forecast():
    historical_weather = request_historical('90001', '2022-08-01')
    json = extract_day_forecast(historical_weather, 0)
    expected_fields = [ 'date',
                        'maxtemp_c',
                        'maxtemp_f',
                        'mintemp_c',
                        'mintemp_f',
                        'avgtemp_c',
                        'avgtemp_f',
                        'maxwind_mph',
                        'maxwind_kph',
                        'totalprecip_mm',
                        'totalprecip_in',
                        'avgvis_km',
                        'avgvis_miles',
                        'avghumidity',
                        'uv'
                        ]
    assert sorted(expected_fields) == sorted(list(json.keys()))

def test_download_weather_data():
    data = download_weather_data('90001', 'zip_code', date(2020,1,1), date(2020,1,30))
    assert data[0] == {
        'date': '2020-01-01', 
        'maxtemp_c': 19.5, 
        'maxtemp_f': 67.1, 
        'mintemp_c': 14.5, 
        'mintemp_f': 58.1, 
        'avgtemp_c': 17.0, 
        'avgtemp_f': 62.6, 
        'maxwind_mph': 5.1, 
        'maxwind_kph': 8.3, 
        'totalprecip_mm': 0.0, 
        'totalprecip_in': 0.0, 
        'avgvis_km': 10.0, 
        'avgvis_miles': 6.0, 
        'avghumidity': 30.0, 
        'uv': 0.0,
        'zip_code': '90001'
    }
    assert len(data) == 30
    
def test_download_batch_weather_data():
    data = download_weather_data_batch('90001', 'zip_code', date(2020,1,1), date(2020,1,30))
    assert data[0] == {
        'date': '2020-01-01', 
        'maxtemp_c': 19.5, 
        'maxtemp_f': 67.1, 
        'mintemp_c': 14.5, 
        'mintemp_f': 58.1, 
        'avgtemp_c': 17.0, 
        'avgtemp_f': 62.6, 
        'maxwind_mph': 5.1, 
        'maxwind_kph': 8.3, 
        'totalprecip_mm': 0.0, 
        'totalprecip_in': 0.0, 
        'avgvis_km': 10.0, 
        'avgvis_miles': 6.0, 
        'avghumidity': 30.0, 
        'uv': 0.0,
        'zip_code': '90001'
    }
    assert len(data) == 30
