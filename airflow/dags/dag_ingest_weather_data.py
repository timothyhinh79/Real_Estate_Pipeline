import csv
from weather_api import *
import os

from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingest_weather_data_script import ingest_weekly_weather_data

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


with open('/opt/airflow/dags/data/ca-zip-code-list.csv') as csvfile:
    rows = csv.reader(csvfile)
    next(rows)
    res = zip(*rows)

ca_zips = list(res)[0][:100] # list of California zip codes

local_workflow = DAG(
    "WeatherIngestionDAG",
    schedule_interval="0 15 * * 1",
    max_active_runs = 1,
    start_date=datetime(2022, 7, 25)
)


with local_workflow:

    ingest_task = PythonOperator(
        task_id = 'ingest_data',
        python_callable = ingest_weekly_weather_data,
        provide_context = True,
        # database, user, password, host, port,
        op_kwargs = {
            'database': PG_DATABASE,
            'user': PG_USER,
            'password': PG_PASSWORD,
            'host': PG_HOST,
            'port': PG_PORT,
            'locations': ca_zips,
        }
    )

    ingest_task

