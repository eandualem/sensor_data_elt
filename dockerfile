FROM python:3.8
RUN pip install 'apache-airflow==2.1.4'
RUN pip install dbt
RUN pip install SQLAlchemy
RUN pip install apache-airflow-providers-postgres
RUN pip install apache-airflow-providers-mysql
RUN pip install dbt-mysql
RUN pip install mysql-connector-python
RUN pip install redash_toolbelt

RUN mkdir /project
COPY scripts/airflow/init.sh /project/scripts/
COPY dbt/profiles.yml /root/.dbt/profiles.yml
RUN chmod +x /project/scripts/init.sh
ENTRYPOINT [ "/project/scripts/init.sh" ]