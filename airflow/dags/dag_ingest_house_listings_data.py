import csv
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from code.weather_api import *
from code.ingest_house_listings_data_script import *

# PG_HOST = os.getenv('POSTGRES_USER')
# PG_USER = os.getenv('POSTGRES_USER')
# PG_PASSWORD = os.getenv('POSTGRES_PASSWORD')
# PG_PORT = os.getenv('PG_PORT')
# PG_DATABASE = os.getenv('PG_DATABASE')

PG_HOST = 'pgdatabase'
PG_USER = 'root'
PG_PASSWORD = 'root'
PG_PORT = '5432'
PG_DATABASE = 'weather'

ingestion_start_date = date(2022,8,14)
sleep_time_between_pages = 60

with open('/opt/airflow/dags/data/LA_cities.csv') as csvfile:
    rows = csv.reader(csvfile)
    next(rows)
    res = list(zip(*rows))

# each location consists of city, state, and zip (zip is optional)
locations = [{'city': city, 'state': state, 'zip': ''} for city, state, include in zip(res[1], res[2], res[5]) if include == 'Y']

local_workflow = DAG(
    "HouseListingsIngestionDAG",
    max_active_runs = 1,
    schedule_interval="@once",
    start_date=datetime(2022, 8, 14)
)


with local_workflow:

    ingest_task = PythonOperator(
        task_id = 'ingest_listings_data',
        python_callable = ingest_listings_data,
        provide_context = True,
        op_kwargs = {
            'database': PG_DATABASE,
            'user': PG_USER,
            'password': PG_PASSWORD,
            'host': PG_HOST,
            'port': PG_PORT,
            'locations': locations,
            'date_to_drop_table': ingestion_start_date,
            'sleep_time_between_pages': sleep_time_between_pages
        }
    )

    ingest_task

