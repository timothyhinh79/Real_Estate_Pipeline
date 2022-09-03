import sys
sys.path.append('/opt/airflow/dags/code/')

import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingest_lasd_crimes_data_script import ingest_crimes_data_to_postgres

PG_HOST = os.getenv('POSTGRES_HOST')
PG_USER = os.getenv('POSTGRES_USER')
PG_PASSWORD = os.getenv('POSTGRES_PASSWORD')
PG_PORT = os.getenv('POSTGRES_PORT')
PG_DATABASE = os.getenv('POSTGRES_DB')

lasd_last30days_url = 'http://shq.lasdnews.net/CrimeStats/CAASS/PART_I_AND_II_CRIMES.csv'
last30days_output_file = '/opt/airflow/dags/data/lasd_crimes_data_last30days.csv'

lasd_ytd_url = 'http://shq.lasdnews.net/CrimeStats/CAASS/PART_I_AND_II_CRIMES-YTD.csv'
ytd_output_file = '/opt/airflow/dags/data/lasd_crimes_data_ytd.csv'

last30days_workflow = DAG(
    "CrimesIngestionDAG",
    max_active_runs = 1,
    schedule_interval="0 10 * * 5", # every Friday at 3 PM PST
    start_date = datetime(2022,8,19)
)


with last30days_workflow:

    curl_task = BashOperator(
        task_id='curl',
        bash_command=f'curl -sSL {lasd_last30days_url} > {last30days_output_file}'
    )

    ingest_to_postgres_task = PythonOperator(
        task_id='ingest_to_postgres',
        python_callable = ingest_crimes_data_to_postgres,
        op_kwargs = {
            'input': last30days_output_file,
            'source_file': 'last_30_days',
            'schema': 'development',
            'table': 'crimes',
            'database': PG_DATABASE,
            'user': PG_USER,
            'password': PG_PASSWORD,
            'host': PG_HOST,
            'port': PG_PORT
        }
    )

    curl_task >> ingest_to_postgres_task


ytd_workflow = DAG(
    "CrimesIngestionDAG_YTD",
    max_active_runs = 1,
    schedule_interval="0 10 * * 5#3", # every third Friday of the month at 3 PM PST
    start_date = datetime(2022,7,14)
)


with ytd_workflow:

    curl_task = BashOperator(
        task_id='curl',
        bash_command=f'curl -sSL {lasd_ytd_url} > {ytd_output_file}'
    )

    ingest_to_postgres_task = PythonOperator(
        task_id='ingest_to_postgres',
        python_callable = ingest_crimes_data_to_postgres,
        op_kwargs = {
            'input': ytd_output_file,
            'source_file': 'year_to_date',
            'database': PG_DATABASE,
            'schema': 'development',
            'table': 'crimes',
            'user': PG_USER,
            'password': PG_PASSWORD,
            'host': PG_HOST,
            'port': PG_PORT
        }
    )

    curl_task >> ingest_to_postgres_task