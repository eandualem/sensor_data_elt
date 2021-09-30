import os
import sys
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime as dt
from datetime import timedelta
sys.path.insert(0,"/airflow/dags/scripts")
import scripts.query_exporter as script


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
    'redash_query_exporter_dag',
    default_args=default_args,
    description='Export redash queries',
    schedule_interval='@once',
)

export_queries = PythonOperator(
    task_id='export_query',
    python_callable=script.export_queries,
    op_kwargs={
      'redash_url': 'http://localhost:5000',
      'api_key': '3ZlvazduZdG8WpwUHE1zUh2qY6ij34rhGQzDrDV6'
    },
    dag=dag
)

export_queries