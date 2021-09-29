from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime as dt
from datetime import timedelta
from query_exporter import export_queries

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

export_query = PythonOperator(
    task_id='export_query',
    python_callable=export_queries,
    op_kwargs={'random_base': '3ZlvazduZdG8WpwUHE1zUh2qY6ij34rhGQzDrDV6'},
)

generate_docs
