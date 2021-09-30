#!/usr/bin/env bash

# Setup DB Connection String
AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN
echo "-1---------------------------------------------------------------------------------"


AIRFLOW__WEBSERVER__SECRET_KEY="openssl rand -hex 30"
export AIRFLOW__WEBSERVER__SECRET_KEY
echo "-2---------------------------------------------------------------------------------"

DBT_POSTGRESQL_CONN="postgres://${DBT_POSTGRES_USER}:${DBT_POSTGRES_PASSWORD}@${DBT_POSTGRES_HOST}:${POSTGRES_PORT}/${DBT_POSTGRES_DB}"

cd /dbt && dbt compile
rm -f /airflow/airflow-webserver.pid


sleep 10
airflow db upgrade
airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
echo "-3---------------------------------------------------------------------------------"


sleep 10
airflow connections add 'postgres_conn_id' --conn-uri $DBT_POSTGRESQL_CONN
echo "-4---------------------------------------------------------------------------------"

sleep 10
airflow connections add 'mysql_conn_id'  --conn-uri "mysql://${DBT_MYSQL_USER}:${DBT_MYSQL_PASSWORD}@${DBT_MYSQL_HOST}:${MYSQL_PORT}/${DBT_MYSQL_DB}"
echo "-5---------------------------------------------------------------------------------"

mysql
airflow scheduler & airflow webserver



