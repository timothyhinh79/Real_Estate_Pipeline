import json
import psycopg2
import time
import csv
from datetime import date, timedelta
from zillow_scraper import *

with open('./data/LA_cities.csv') as csvfile:
    rows = csv.reader(csvfile)
    next(rows)
    res = list(zip(*rows))

locations = [(city, state, include) for city, state, include in zip(res[1], res[2], res[5]) if include == 'Y'][:1]

breakpoint()

listings = []
for location in locations:
    print(f'{location[0]} {location[1]}')
    listings += get_listings(location[0], location[1], sleep_time_between_pages=0)



    