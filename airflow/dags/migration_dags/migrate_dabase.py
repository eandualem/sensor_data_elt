import os
import sys
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime as dt
from datetime import timedelta
sys.path.insert(0,"/airflow/dags/scripts")
import scripts.migration_operator as script

default_args = {
    'owner': 'elias',
    'depends_on_past': False,
    'email': ['eandualem@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'start_date': dt(2021, 9, 13),
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'database_migrator_dag',
    default_args=default_args,
    description='Migrate database from MYSQL to PostgressSQL',
    schedule_interval='@once',
)

sql = "SELECT * FROM station_info LIMIT 100;"
database_migrator = script.MigrationOperator(
    task_id='station_info_migrator',
    source_conn_id='mysql_conn_id',
    destination_conn_id='postgres_conn_id',
    destination_table="station_info",
    sql=sql,
    dag=dag
)

database_migrator