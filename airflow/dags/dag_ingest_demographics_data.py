import sys
sys.path.append('/opt/airflow/dags/code/')

import csv
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from us_census_api import *
from ingest_us_census_data_script import ingest_us_census_callable

with open('/opt/airflow/dags/data/Zip_Codes_(LA_County).csv') as csvfile:
    rows = csv.reader(csvfile)
    next(rows)
    res = list(zip(*rows))

# each location consists of city, state, and zip (zip is optional)
zips = res[2]

census_year = os.getenv('CENSUS_YEAR')
census_dataset = os.getenv('CENSUS_DATASET')
PG_HOST = os.getenv('POSTGRES_HOST')
PG_USER = os.getenv('POSTGRES_USER')
PG_PASSWORD = os.getenv('POSTGRES_PASSWORD')
PG_PORT = os.getenv('POSTGRES_PORT')
PG_DATABASE = os.getenv('POSTGRES_DB')

local_workflow = DAG(
    "DemoDataIngestionDAG",
    max_active_runs = 1,
    schedule_interval="@once",
    start_date=datetime(2022, 8, 14)
)

with local_workflow:

    ingest_task = PythonOperator(
        task_id = 'ingest_data',
        python_callable = ingest_us_census_callable,
        op_kwargs = {
            'year': census_year,
            'census_dataset': census_dataset,
            'zips': zips,
            'database': PG_DATABASE,
            'user': PG_USER,
            'password': PG_PASSWORD,
            'host': PG_HOST,
            'port': PG_PORT
        }
    )

    ingest_task