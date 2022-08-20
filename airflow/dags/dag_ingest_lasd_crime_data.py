import sys
sys.path.append('/opt/airflow/dags/code/')

from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingest_lasd_crimes_data_script import ingest_crimes_data_to_postgres

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

lasd_url = 'http://shq.lasdnews.net/CrimeStats/CAASS/PART_I_AND_II_CRIMES.csv'
output_file = '/opt/airflow/dags/data/lasd_crimes_data.csv'

local_workflow = DAG(
    "CrimesIngestionDAG",
    max_active_runs = 1,
    schedule_interval="@once",
    start_date = datetime(2022,8,19)
)


with local_workflow:

    curl_task = BashOperator(
        task_id='curl',
        bash_command=f'curl -sSL {lasd_url} > {output_file}'
    )

    ingest_to_postgres_task = PythonOperator(
        task_id='ingest_to_postgres',
        python_callable = ingest_crimes_data_to_postgres,
        op_kwargs = {
            'input': output_file,
            'database': PG_DATABASE,
            'user': PG_USER,
            'password': PG_PASSWORD,
            'host': PG_HOST,
            'port': PG_PORT
        }
    )

    curl_task >> ingest_to_postgres_task