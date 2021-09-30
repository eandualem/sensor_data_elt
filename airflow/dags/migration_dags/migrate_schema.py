import os
import sys
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime as dt
from datetime import timedelta
sys.path.insert(0,"/airflow/dags/scripts")
import scripts.mysql_to_postgres as script


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
    'schema_migration_dag',
    default_args=default_args,
    description='Export redash queries',
    schedule_interval='@once',
)

migrate_schema = PythonOperator(
    task_id='MYSQL_to_PostgresSQL',
    python_callable=script.migrate_schema,
    dag=dag
)

migrate_schema