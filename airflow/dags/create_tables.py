from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from datetime import datetime as dt
from datetime import timedelta


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
    'create_tables',
    default_args=default_args,
    description='An Airflow DAG to create tables',
    schedule_interval=timedelta(days=1),
)

mysql_task = MySqlOperator(
    task_id='create_table_mysql_external_file',
    mysql_conn_id='mysql_conn_id',
    sql='I80_davis_schema.sql',
    dag=dag,
)

mysql_task1 = MySqlOperator(
    task_id='create_table_mysql_external_file2',
    mysql_conn_id='mysql_conn_id',
    sql='I80_stations_schema.sql',
    dag=dag,
)

mysql_task >> mysql_task1
