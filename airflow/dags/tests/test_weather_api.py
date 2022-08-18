
from weather_api import *
from datetime import date, timedelta

def test_download_batch_weather_data():
    data = download_weather_data_batch('91732', 'zip_code', date(2020,1,1), date(2020,1,30))
    assert data[0] == {'date': '2020-01-01',
                        'maxtemp_c': 19.1,
                        'maxtemp_f': 66.4,
                        'mintemp_c': 8.8,
                        'mintemp_f': 47.8,
                        'avgtemp_c': 14.8,
                        'avgtemp_f': 58.6,
                        'maxwind_mph': 4.0,
                        'maxwind_kph': 6.5,
                        'totalprecip_mm': 0.0,
                        'totalprecip_in': 0.0,
                        'avgvis_km': 10.0,
                        'avgvis_miles': 6.0,
                        'avghumidity': 33.0,
                        'uv': 0.0,
                        'zip_code': '91732'
                        }
    assert len(data) == 30
