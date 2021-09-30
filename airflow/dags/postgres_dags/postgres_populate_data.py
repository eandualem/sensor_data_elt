from airflow import DAG
from datetime import timedelta
from datetime import datetime as dt
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.email_operator import EmailOperator

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
    'postgres_populate_data',
    default_args=default_args,
    description='An Airflow DAG to populate data',
    schedule_interval="@once",
)

check_file = BashOperator(
    task_id="check_file",
    bash_command="cat /etc/mysql/mysql.cnf",
    retries=2,
    retry_delay=timedelta(seconds=15),
    dag=dag
)

insert_I80_davis = PostgresOperator(
    task_id='insert_I80_davis',
    sql='./postgres_schema/insert_I80_davis.sql',
    postgres_conn_id='postgres_conn_id',
    autocommit=True,
    database="dbtdb",
    dag=dag
)

insert_I80_stations = PostgresOperator(
    task_id='insert_I80_stations',
    sql="./postgres_schema/insert_I80_stations.sql",
    postgres_conn_id='postgres_conn_id',
    autocommit=True,
    database="dbtdb",
    dag=dag
)

insert_richards = PostgresOperator(
    task_id='insert_richards',
    sql="./postgres_schema/insert_richards.sql",
    postgres_conn_id='postgres_conn_id',
    autocommit=True,
    database="dbtdb",
    dag=dag
)

insert_station_summary = PostgresOperator(
    task_id='insert_station_summary',
    sql='./postgres_schema/insert_station_summary.sql',
    postgres_conn_id='postgres_conn_id',
    autocommit=True,
    database="dbtdb",
    dag=dag
)

email = EmailOperator(task_id='send_email',
                      to='eandualem@gmail.com',
                      subject='Daily report generated',
                      html_content=""" <h1>Congratulations! Data populated.</h1> """,
                      dag=dag
                      )

[insert_I80_davis, insert_I80_stations,
    insert_richards, insert_station_summary] >> email
