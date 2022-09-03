from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import datetime
from airflow.utils.dates import timedelta
from airflow.contrib.operators.ssh_operator import SSHOperator

with DAG(
    dag_id='dbt_dag',
    start_date=datetime(2022, 9, 1),
    description='An Airflow DAG to invoke simple dbt commands',
    max_active_runs = 1,
    schedule_interval="0 11 * * 5", # every Friday at 4 PM PST
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt-postgres && dbt run',
    )

    # dbt_test = BashOperator(
    #     task_id='dbt_test',
    #     bash_command='dbt test'
    # )

    dbt_run #>> dbt_test