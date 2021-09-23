from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

from airflow.utils.dates import datetime
from airflow.utils.dates import timedelta

default_args = {
    'owner': 'elias',
    'depends_on_past': False,
    'start_date': datetime(2021, 10, 21),
    'email': ['eandualem@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'populate_data_dag',
    default_args=default_args,
    description='An Airflow DAG to invoke simple dbt commands',
    schedule_interval=timedelta(days=1),
)

mysql_task = MySqlOperator(
    task_id='create_table_mysql_external_file',
    mysql_conn_id='mysql_conn_id',
    sql='create table if not exists dbtdb.sensor_data(sense_id int NOT NULL PRIMARY KEY,date Date, time Time, station_id int, col3 float, col4 float, col5 float, col6 float, col7 float, col8 float, col9 float, col10 float, col11 float, col12 float, col13 float, col14 float, col15 float, col16 float, col17 float, col18 float, col19 float, col20 float, col21 float, col22 float, col23 float, col24 float, col25 float, col26 float)',
    dag=dag
)


# [END howto_operator_mysql_external_file]

mysql_task 
