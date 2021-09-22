FROM python:3.8.11
FROM python:3.7
RUN pip install 'apache-airflow==2.1.4' && pip install dbt
RUN pip install SQLAlchemy
RUN pip install apache-airflow-providers-postgres
RUN pip install dbt-mysql
RUN pip install mysql-connector-python

RUN mkdir /project
# COPY requirements.txt /project/
# RUN pip install -r /project/requirements.txt 
COPY scripts_airflow/ /project/scripts/
COPY dbt/profiles.yml /root/.dbt/profiles.yml
RUN chmod +x /project/scripts/init.sh
ENTRYPOINT [ "/project/scripts/init.sh" ]