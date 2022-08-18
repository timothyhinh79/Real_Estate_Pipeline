from zillow_scraper import *

example_home_dict = {
    'zpid': 20698287, 'streetAddress': '420 E Pine St', 'zipcode': '91801', 'city': 'Alhambra', 'state': 'CA', 'latitude': 34.106586, 'longitude': -118.12959, 
    'price': 1650000.0, 'bathrooms': 4.0, 'bedrooms': 4.0, 'livingArea': 3018.0, 'homeType': 'SINGLE_FAMILY', 'homeStatus': 'FOR_SALE', 'daysOnZillow': -1, 'isFeatured': False, 
    'shouldHighlight': False, 'zestimate': 1737200, 'rentZestimate': 5899, 'listing_sub_type': {'is_openHouse': True, 'is_FSBA': True}, 'openHouse': 'Sat. 2-4pm', 'isUnmappable': False, 
    'isPreforeclosureAuction': False, 'homeStatusForHDP': 'FOR_SALE', 'priceForHDP': 1650000.0, 'open_house_info': {'open_house_showing': [{'open_house_start': 1661029200000, 'open_house_end': 1661036400000}, {'open_house_start': 1661115600000, 'open_house_end': 1661122800000}]}, 
    'isNonOwnerOccupied': True, 'isPremierBuilder': False, 'isZillowOwned': False, 'currency': 'USD', 'country': 'USA', 'taxAssessedValue': 192413.0, 'lotAreaValue': 0.394811753902663, 
    'lotAreaUnit': 'acres'
}

example_clean_home_dict = {
    'zpid': 20698287, 'street_address': '420 E Pine St', 'zipcode': '91801', 'city': 'Alhambra', 'state': 'CA', 'latitude': 34.106586, 'longitude': -118.12959, 
    'price': 1650000.0, 'bathrooms': 4.0, 'bedrooms': 4.0, 'living_area': 3018.0, 'home_type': 'SINGLE_FAMILY', 'home_status': 'FOR_SALE', 'days_on_zillow': -1, 'is_featured': False, 
    'should_highlight': False, 'zestimate': 1737200, 'rent_zestimate': 5899, 'is_open_house': True, 'is_fsba': True, 'open_house': 'Sat. 2-4pm', 'is_unmappable': False, 
    'is_preforeclosure_auction': False, 'home_status_for_hdp': 'FOR_SALE', 'price_for_hdp': 1650000.0, 
    'is_non_owner_occupied': True, 'is_premier_builder': False, 'is_zillow_owned': False, 'currency': 'USD', 'country': 'USA', 'tax_assessed_value': 192413.0, 'lot_area_value': 0.394811753902663, 
    'lot_area_unit': 'acres'
}

def test_zillow_url():
    assert zillow_url(zip = '91732') == 'https://www.zillow.com/homes/--91732_rb/'  
    assert zillow_url(city = 'Los Angeles', state = 'CA') == 'https://www.zillow.com/homes/Los-Angeles-CA-_rb/'  

def test_get_html_text_from_url():
    url = zillow_url(city = 'Los Angeles', state = 'CA')
    extract_json = get_html_text_from_url(url)
    assert 'data-zrr-shared-data-key' in extract_json

def test_get_listing_extract_from_url():
    
    url = zillow_url(city = 'Los Angeles', state = 'CA')
    extract_json = get_listing_extract_from_url(url)

    # make sure certain keys are in the json extract that we use to find the listings and next page
    assert 'cat1' in extract_json.keys()
    assert 'searchList' in extract_json['cat1'].keys()
    assert 'searchResults' in extract_json['cat1'].keys()
    assert 'listResults' in extract_json['cat1']['searchResults'].keys()

def test_next_page():
    # zip code 90011 is most populous area in LA, so likely to have over 40 listings
    url = zillow_url(zip = '90011')
    extract_json = get_listing_extract_from_url(url)
    assert next_page(extract_json) == True

    # zip code 90071 has very small population, so unlikely to have listings
    url = zillow_url(zip = '90071')
    extract_json = get_listing_extract_from_url(url)
    assert next_page(extract_json) == False

def test_clean_listing():
    clean_dict = clean_listing(example_home_dict)
    assert clean_dict == example_clean_home_dict

def test_get_listings():

    listings = get_listings(city = 'Alhambra', state = 'CA', sleep_time_between_pages=0)
    first_listing = listings[0]

    # make sure some standard listing fields are in at least the first listing
    assert 'zpid' in first_listing.keys()
    assert 'street_address' in first_listing.keys()
    assert 'price' in first_listing.keys()
