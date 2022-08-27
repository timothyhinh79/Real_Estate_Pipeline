from bs4 import BeautifulSoup
import requests
import json
import re
from datetime import date
import time

zillow_scraper_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

column_name_mapping = {
    'zpid': 'zpid',
    'extract_date': 'extract_date',
    'streetAddress': 'street_address',
    'zipcode': 'zipcode',
    'city': 'city',
    'state': 'state',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'price': 'price',
    'bathrooms': 'bathrooms',
    'bedrooms': 'bedrooms',
    'livingArea': 'living_area',
    'homeType': 'home_type',
    'homeStatus': 'home_status',
    'daysOnZillow': 'days_on_zillow',
    'isFeatured': 'is_featured',
    'shouldHighlight': 'should_highlight',
    'zestimate': 'zestimate',
    'rentZestimate': 'rent_zestimate',
    'is_openHouse': 'is_open_house',
    'is_FSBA': 'is_fsba',
    'openHouse': 'open_house',
    'isUnmappable': 'is_unmappable',
    'isPreforeclosureAuction': 'is_preforeclosure_auction',
    'homeStatusForHDP': 'home_status_for_hdp',
    'priceForHDP': 'price_for_hdp',
    'isNonOwnerOccupied': 'is_non_owner_occupied',
    'isPremierBuilder': 'is_premier_builder',
    'isZillowOwned': 'is_zillow_owned',
    'currency': 'currency',
    'country': 'country',
    'taxAssessedValue': 'tax_assessed_value',
    'lotAreaValue': 'lot_area_value',
    'lotAreaUnit': 'lot_area_unit'
}

# sleep_time_between_pages = 60 # to avoid getting blocked by zillow
# retry_sleep_time = 90
# max_attempts = 5

# columns_to_keep = ['zpid','streetAddress', 'zipcode','city','state','latitude','longitude','price','bathrooms','bedrooms','livingArea'
#                     ,'homeType','homeStatus','daysOnZillow','isFeatured','shouldHighlight','zestimate','rentZestimate', 'is_openHouse'
#                     ,'is_FSBA','openHouse','is']

def zillow_url(city = '', state = '', zip = ''):
    city_url_str = city.replace(' ', '-')
    return f'https://www.zillow.com/homes/{city_url_str}-{state}-{zip}_rb/'

def get_html_text_from_url(url, retry_sleep_time = 90, max_attempts = 5):
    num_attempts = 0

    while num_attempts < max_attempts: 
        num_attempts += 1
        html = requests.get(url, headers = zillow_scraper_headers)
        if 'robots' in html.text:
            print(f'Captcha detected in HTML response, trying again in {retry_sleep_time} seconds...')
            time.sleep(retry_sleep_time)
        else:
            break

    if 'robots' in html.text:
        print(f'Maximum attempts to call url {url} reached with no success')
    return html.text

def get_listing_extract_from_url(url, retry_sleep_time = 90, max_attempts = 5):
    html_text = get_html_text_from_url(url, retry_sleep_time, max_attempts)
    soup = BeautifulSoup(html_text, 'html.parser')
    extract_str = soup.find_all('script', attrs={"data-zrr-shared-data-key": "mobileSearchPageStore", 'type': 'application/json'})
    extract_json = json.loads(extract_str[0].text[4:-3]) # index from 4 to -3 excludes beginning and ending arrows
    return extract_json 

def next_page(extract_json):
    return 'pagination' in extract_json['cat1']['searchList'] and 'nextUrl' in extract_json['cat1']['searchList']['pagination']

def clean_listing(homeInfo_dict, column_mapping):
    # adding extract date
    homeInfo_dict['extract_date'] = date.today().strftime('%m-%d-%Y')

    # flattening listing_sub_type nested dict
    if 'listing_sub_type' in homeInfo_dict:
        if 'is_openHouse' in homeInfo_dict['listing_sub_type']:
            homeInfo_dict['is_openHouse'] = homeInfo_dict['listing_sub_type']['is_openHouse']
        if 'is_FSBA' in homeInfo_dict['listing_sub_type']:
            homeInfo_dict['is_FSBA'] = homeInfo_dict['listing_sub_type']['is_FSBA']
        homeInfo_dict.pop('listing_sub_type')

    # removing open_house_info
    if 'open_house_info' in homeInfo_dict:
        homeInfo_dict.pop('open_house_info')

    return {column_mapping[key]: value for key, value in homeInfo_dict.items() if key in column_mapping}

def get_listings(city = '', state = '', zip = '', sleep_time_between_pages = 60, retry_sleep_time = 90, max_attempts = 5):

    url = zillow_url(city, state, zip)
    page = 1
    listings = []

    while True:
        print(f'Ingesting {city} {state} {zip} page {page}')
        current_json = get_listing_extract_from_url(f'{url}{page}_p', retry_sleep_time, max_attempts)
        listings += [clean_listing(listing['hdpData']['homeInfo'], column_name_mapping) for listing in current_json['cat1']['searchResults']['listResults']]
        time.sleep(sleep_time_between_pages)

        if next_page(current_json):
            page += 1
        else:
            break

    return listings

