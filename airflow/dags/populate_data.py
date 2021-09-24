from airflow import DAG
from datetime import timedelta
from datetime import datetime as dt
from airflow.operators.bash_operator import BashOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
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
    'populate_data',
    default_args=default_args,
    description='An Airflow DAG to populate data',
    schedule_interval="@once",
)

check_file = BashOperator(
    task_id="check_file",
    bash_command="shasum /var/lib/mysql-files/I80_stations.csv",
    retries=2,
    retry_delay=timedelta(seconds=15),
    dag=dag
)

insert_I80_davis = MySqlOperator(
    task_id='insert_I80_davis',
    mysql_conn_id="mysql_conn_id",
    sql='./insert_I80_davis.sql',
    dag=dag
)

insert_I80_stations = MySqlOperator(
    task_id='insert_I80_stations',
    mysql_conn_id="mysql_conn_id",
    sql="./insert_I80_stations.sql",
    dag=dag
)

email = EmailOperator(task_id='send_email',
                      to='eandualem@gmail.com',
                      subject='Daily report generated',
                      html_content=""" <h1>Congratulations! Data populated.</h1> """,
                      dag=dag
                      )

[insert_I80_davis, insert_I80_stations] >> email
