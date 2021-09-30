import os
import glob


def convert_sql(sql_satement, target_path, file_name):

  postgres_sql = sql_satement.lower()
  postgres_sql = postgres_sql.replace(";", "")
  postgres_sql = postgres_sql.strip()

  postgres_sql = postgres_sql.replace("ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci".lower(), "")
  postgres_sql = postgres_sql.replace("ENGINE=InnoDB DEFAULT CHARSET=utf8".lower(), "")
  postgres_sql = postgres_sql.replace("double".lower(), "double precision")

  postgres_sql = postgres_sql.replace("`", "")
  postgres_sql = postgres_sql.strip() + ";"

  if postgres_sql.split()[0] == 'load':
    # to do load handler
    pass
  if postgres_sql.split()[0] == 'create':
     with open(f'{target_path}/{file_name}', 'w', encoding = 'utf-8') as _file:
      _file.write(postgres_sql)

def migrate_schema(src_path="/airflow/dags/mysql_dags/mysql_schema/", tgt_path="/airflow/dags/postgres_dags/postgres_schema/"):
  sql_files = glob.glob(f'{src_path}*.sql')
  for sql_file in sql_files:
    file_name = sql_file.split("/")[-1]
    with open(sql_file, encoding = 'utf-8') as _file:
      convert_sql(_file.read(), tgt_path, file_name=file_name)