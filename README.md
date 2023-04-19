# Real Estate Pipeline

The “Real Estate Pipeline” is a data engineering project that sets up a pipeline to scrape/ingest real estate data from Zillow into a Postgres database, hooked up to a Streamlit dashboard. This data is supplemented by other data sources such as demographics, LA crime rates, and weather data. The goal of this project is to provide a comprehensive and up-to-date view of the real estate market in LA by combining data from multiple sources.

## Tools

* Python
* Docker
* Airflow
* DBT
* Postgres
* Streamlit
* Flask

## Requirements 

* Must have a local Postgres server, with a database named "real_estate_properties"

## Instructions to Launch

* Clone the repo into a directory, and set the repo as the current directory
* Update `POSTGRES_USER` and `POSTGRES_PASSWORD`
    * Note: for better security, these credentials should be saved in a local .env file. These are current being left in docker-compose.yaml as a matter of convenience.
* Run `docker-compose build`
* Run `docker-compose up`
* You should be able to visit localhost:8080 on your web browser and see your Airflow instance running.
