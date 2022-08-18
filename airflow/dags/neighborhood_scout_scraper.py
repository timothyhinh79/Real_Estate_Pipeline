from bs4 import BeautifulSoup
import requests
import json
import re
import time

neighborhood_scout_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

def nscout_url(city = '', state = '', zip = ''):
    city_url_str = city.replace(' ', '-').lower()
    state_url_str = state.lower()
    return f'https://www.neighborhoodscout.com/{state_url_str}/{city_url_str}'

def get_html_text_from_url(url, retry_sleep_time = 90, max_attempts = 5):
    num_attempts = 0

    while num_attempts < max_attempts: 
        num_attempts += 1
        html = requests.get(url, headers = neighborhood_scout_headers)
        if 'robots' in html.text:
            print(f'Captcha detected in HTML response, trying again in {retry_sleep_time} seconds...')
            time.sleep(retry_sleep_time)
        else:
            break

    if 'robots' in html.text:
        print(f'Maximum attempts to call url {url} reached with no success')
    return html.text
