import sys
sys.path.append('/opt/airflow/dags/code/')

import csv
import os
from datetime import datetime, date
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from weather_api import *
from ingest_weather_data_script import ingest_monthly_weather_data_batch

PG_HOST = os.getenv('POSTGRES_HOST')
PG_USER = os.getenv('POSTGRES_USER')
PG_PASSWORD = os.getenv('POSTGRES_PASSWORD')
PG_PORT = os.getenv('POSTGRES_PORT')
PG_DATABASE = os.getenv('POSTGRES_DB')

ingestion_start_date = date(2021,1,1)
ingestion_end_date = date(2021,12,1)

# getting list of all CA zip codes
with open('/opt/airflow/dags/data/Zip_Codes_(LA_County).csv') as csvfile:
    rows = csv.reader(csvfile)
    next(rows)
    res = zip(*rows)
    ca_zips = list(res)[1][:5] # list of California zip codes

retry_sleep_time = 60
api_max_attempts = 2

local_workflow = DAG(
    "WeatherBatchIngestionDAG",
    schedule_interval="@once", # monthly run on first of every month  "0 0 1 * *"
    max_active_runs = 1,
    start_date=datetime(ingestion_start_date.year, ingestion_start_date.month, ingestion_start_date.day),
    end_date=datetime(ingestion_end_date.year, ingestion_end_date.month, ingestion_end_date.day)
)

with local_workflow:

    batch_ingest_task = PythonOperator(
        task_id = 'ingest_data_batch',
        python_callable = ingest_monthly_weather_data_batch,
        provide_context = True,
        # database, user, password, host, port,
        op_kwargs = {
            'database': PG_DATABASE,
            'user': PG_USER,
            'password': PG_PASSWORD,
            'host': PG_HOST,
            'port': PG_PORT,
            'locations': ca_zips,
            'date_to_drop_table': ingestion_start_date,
            'retry_sleep_time': retry_sleep_time,
            'api_max_attempts': api_max_attempts,
        }
    )

    batch_ingest_task

