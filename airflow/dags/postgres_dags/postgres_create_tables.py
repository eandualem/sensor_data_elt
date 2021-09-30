from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.email_operator import EmailOperator
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
    'postgres_create_tables',
    default_args=default_args,
    description='An Airflow DAG to create tables',
    schedule_interval='@once',
)

create_I80_davis_table = PostgresOperator(
    task_id='create_table_I80_davis',
    sql='./postgres_schema/I80_davis_schema.sql',
    postgres_conn_id='postgres_conn_id',
    autocommit=True,
    database="dbtdb",
    dag=dag,
)

create_I80_stations_table = PostgresOperator(
    task_id='create_table_I80_stations',
    sql='./postgres_schema/I80_stations_schema.sql',
    postgres_conn_id='postgres_conn_id',
    autocommit=True,
    database="dbtdb",
    dag=dag,
)

create_richards_table = PostgresOperator(
    task_id='create_table_richards',
    sql='./postgres_schema/richards_schema.sql',
    postgres_conn_id='postgres_conn_id',
    autocommit=True,
    database="dbtdb",
    dag=dag,
)

create_station_summary_table = PostgresOperator(
    task_id='create_table_station_summary',
    sql='./postgres_schema/station_summary_schema.sql',
    postgres_conn_id='postgres_conn_id',
    autocommit=True,
    database="dbtdb",
    dag=dag,
)

email = EmailOperator(task_id='send_email',
                      to='eandualem@gmail.com',
                      subject='Daily report generated',
                      html_content=""" <h1>Congratulations! The tables are created.</h1> """,
                      dag=dag,
                      )

[create_I80_davis_table, create_I80_stations_table,
    create_richards_table, create_station_summary_table] >> email
