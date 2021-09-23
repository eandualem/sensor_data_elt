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
    schedule_interval=timedelta(days=1),
)

check_file = BashOperator(
    task_id="check_file",
    bash_command="shasum /var/lib/mysql-files/I80_stations.csv",
    retries=2,
    retry_delay=timedelta(seconds=15),
    dag=dag
)


insert = MySqlOperator(
    task_id='insert_I80_davis',
    mysql_conn_id="mysql_conn_id",
    sql="""LOAD DATA INFILE '/var/lib/mysql-files/I80_sample.txt' INTO TABLE I80Davis FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS
           (date, time, station_id, @vcol3, @vcol4, @vcol5, @vcol6, @vcol7, @vcol8, @vcol9, @vcol10, @vcol11, @vcol12, @vcol13, @vcol14, @vcol15, @vcol16, @vcol17, @vcol18, @vcol19, @vcol20, @vcol21, @vcol22, @vcol23, @vcol24, @vcol25, @vcol26) SET 
           col3 = NULLIF( @vcol3, ''), 
           col4 = NULLIF( @vcol4, ''), 
           col5 = NULLIF( @vcol5, ''), 
           col6 = NULLIF( @vcol6, ''), 
           col7 = NULLIF( @vcol7, ''), 
           col8 = NULLIF( @vcol8, ''), 
           col9 = NULLIF( @vcol9, ''), 
           col10 = NULLIF( @vcol10, ''), 
           col11 = NULLIF( @vcol11, ''), 
           col12 = NULLIF( @vcol12, ''), 
           col13 = NULLIF( @vcol13, ''), 
           col14 = NULLIF( @vcol14, ''),
           col15 = NULLIF( @vcol15, ''), 
           col16 = NULLIF( @vcol16, ''), 
           col17 = NULLIF( @vcol17, ''), 
           col18 = NULLIF( @vcol18, ''), 
           col19 = NULLIF( @vcol19, ''), 
           col20 = NULLIF( @vcol20, ''), 
           col21 = NULLIF( @vcol21, ''), 
           col22 = NULLIF( @vcol22, ''), 
           col23 = NULLIF( @vcol23, ''), 
           col24 = NULLIF( @vcol24, ''), 
           col25 = NULLIF( @vcol25, ''), 
           col26 = NULLIF( @vcol26, '');""",
    dag=dag
)

insert1 = MySqlOperator(
    task_id='insert_I80_stations',
    mysql_conn_id="mysql_conn_id",
    sql="LOAD DATA INFILE '/var/lib/mysql-files/I80_stations.csv' INTO TABLE I80Stations FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS (ID,Fwy,Dir,District,County,City,@vState_PM,Abs_PM,Latitude,Longitude,@vLength,Type,Lanes,Name,User_ID_1,User_ID_2,User_ID_3,User_ID_4) SET Length = NULLIF( @vLength, ''), State_PM = NULLIF( @vState_PM, '');",
    dag=dag
)

email = EmailOperator(task_id='send_email',
                      to='eandualem@gmail.com',
                      subject='Daily report generated',
                      html_content=""" <h1>Congratulations! Your store reports are ready.</h1> """,
                      dag=dag
                      )

insert >> email
