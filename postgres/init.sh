#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';
  CREATE DATABASE $APP_DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $APP_DB_NAME TO $APP_DB_USER;
  \connect $APP_DB_NAME $APP_DB_USER
  BEGIN;
    CREATE SCHEMA IF NOT EXISTS development;
    CREATE SCHEMA IF NOT EXISTS production;

    CREATE TABLE IF NOT EXISTS development.house_listings (
        id SERIAL PRIMARY KEY,
        extract_date DATE NOT NULL,
        zpid INTEGER,
        street_address VARCHAR(255),
        zipcode VARCHAR(20),
        city VARCHAR(255),
        state VARCHAR(20),
        latitude FLOAT,
        longitude FLOAT,
        price FLOAT,
        bathrooms FLOAT,
        bedrooms FLOAT,
        living_area FLOAT,
        home_type VARCHAR(255),
        home_status VARCHAR(255),
        days_on_zillow INTEGER,
        is_featured BOOLEAN,
        should_highlight BOOLEAN,
        zestimate FLOAT,
        rent_zestimate FLOAT,
        is_open_house BOOLEAN,
        is_fsba BOOLEAN,
        open_house VARCHAR(255),
        is_unmappable BOOLEAN,
        is_preforeclosure_auction BOOLEAN,
        home_status_for_hdp VARCHAR(255),
        price_for_hdp FLOAT,
        is_non_owner_occupied BOOLEAN,
        is_premier_builder BOOLEAN,
        is_zillow_owned BOOLEAN,
        currency VARCHAR(20),
        country VARCHAR(255),
        tax_assessed_value FLOAT,
        lot_area_value FLOAT,
        lot_area_unit VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS development.crimes (
        id SERIAL PRIMARY KEY,
        extract_date DATE,
        source_file VARCHAR(255),
        lurn_sak INTEGER,
        incident_date TIMESTAMP,
        incident_reported_date DATE,
        category VARCHAR(255),
        stat INTEGER,
        stat_desc VARCHAR(255),
        address VARCHAR(255),
        street VARCHAR (255),
        city VARCHAR(255),
        zip VARCHAR(10),
        incident_id VARCHAR(255),
        gang_related VARCHAR(255),
        unit_name VARCHAR(255),
        longitude FLOAT,
        latitude FLOAT,
        part_category INTEGER
    );

    CREATE TABLE IF NOT EXISTS development.population_by_race_and_zip (
        id SERIAL PRIMARY KEY,
        year INTEGER,
        dataset VARCHAR(50),
        zip VARCHAR(20),
        race varchar(255),
        population INTEGER
    );

    CREATE TABLE IF NOT EXISTS development.population_by_agesex_and_zip (
        id SERIAL PRIMARY KEY,
        year INTEGER,
        dataset VARCHAR(50),
        zip VARCHAR(20),
        sex varchar(20),
        min_age INTEGER,
        max_age INTEGER,
        population INTEGER
    );

    CREATE TABLE IF NOT EXISTS development.population_by_incomelevel_and_zip (
        id SERIAL PRIMARY KEY,
        year INTEGER,
        dataset VARCHAR(50),
        zip VARCHAR(20),
        min_income INTEGER,
        max_income INTEGER,
        population INTEGER
    );

    CREATE TABLE IF NOT EXISTS development.median_income_by_zip (
        id SERIAL PRIMARY KEY,
        year INTEGER,
        dataset VARCHAR(50),
        zip VARCHAR(20),
        median_income INTEGER
    );

    CREATE TABLE IF NOT EXISTS development.median_age_by_zip (
        id SERIAL PRIMARY KEY,
        year INTEGER,
        dataset VARCHAR(50),
        zip VARCHAR(20),
        median_age FLOAT
    );

    CREATE TABLE IF NOT EXISTS development.daily_forecasts (
        id SERIAL PRIMARY KEY,
        zip_code VARCHAR(255),
        date DATE,
        maxtemp_c FLOAT,
        maxtemp_f FLOAT,
        mintemp_c FLOAT,
        mintemp_f FLOAT,
        avgtemp_c FLOAT,
        avgtemp_f FLOAT,
        maxwind_mph FLOAT,
        maxwind_kph FLOAT,
        totalprecip_mm FLOAT,
        totalprecip_in FLOAT,
        avgvis_km FLOAT,
        avgvis_miles FLOAT,
        avghumidity FLOAT,
        uv FLOAT
    );
  COMMIT;
EOSQL