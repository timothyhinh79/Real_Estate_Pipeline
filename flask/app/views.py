from app import app
from app.lib import db
from app.models import House_listing, Crime_stats, Zipcode
from flask import jsonify, abort, request
from settings import *

app.config['DB_USER'] = POSTGRES_USER
app.config['DB_PASSWORD'] = POSTGRES_PASSWORD
app.config['DATABASE'] = POSTGRES_DATABASE
app.config['PG_HOST'] = POSTGRES_HOST

@app.route('/')
def home():
    return 'Welcome!'

### House listings views

@app.route('/house_listings')
def house_listings_index():
    conn = db.get_db()
    house_listings = db.find_all(House_listing, conn)
    return jsonify([house_listing.to_json() for house_listing in house_listings])

@app.route('/house_listings/<id>')
def show_house_listing(id):
    conn = db.get_db()
    house_listing = db.find_by_id(House_listing, id, conn)
    return jsonify(house_listing.to_json())

@app.route('/house_listings/search')
def house_listings_query():
    conn = db.get_db()
    house_listings = db.query(House_listing, request.args, conn)
    return jsonify([house_listing.to_json() for house_listing in house_listings])

### Crime statistics views

@app.route('/crime_stats')
def crime_stats_index():
    conn = db.get_db()
    crime_stats_by_city = db.find_all(Crime_stats, conn)
    return jsonify([crime_stats_city.to_json() for crime_stats_city in crime_stats_by_city])

@app.route('/crime_stats/<city>')
def show_crime_stats(city):
    conn = db.get_db()
    crime_stats = db.query(Crime_stats, {'city': city}, conn)
    return jsonify([crime_stat.to_json() for crime_stat in crime_stats])

@app.route('/crime_stats/search')
def crime_stats_query():
    conn = db.get_db()
    crime_stats = db.query(Crime_stats, request.args, conn)
    return jsonify([crime_stat.to_json() for crime_stat in crime_stats])

### Zipcode demographics views

@app.route('/zipcodes')
def zipcodes_index():
    conn = db.get_db()
    zipcodes = db.find_all(Zipcode, conn)
    return jsonify([zipcode.to_json(conn) for zipcode in zipcodes])

@app.route('/zipcodes/<zip>')
def show_zipcode(zip):
    conn = db.get_db()
    zipcode = db.find_by_id(Zipcode, zip, conn)
    return jsonify(zipcode.to_json(conn))
    

