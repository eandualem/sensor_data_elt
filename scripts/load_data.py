import os
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error


class LoadData():

    def __init__(self):
        pass

    def connect(self, db_name=None):
        try:
            conn = mysql.connect(host='localhost',
                                  user=os.getenv("USER"),
                                  password=os.getenv("PASSWORD"),

                                 database=db_name, buffered=True)
            cur = conn.cursor()
            return conn, cur
        except Error as err:
            print("Database connection error: {}".format(err))

    def create_db(self, db_name: str) -> None:
        try:
            conn, cur = self.connect()
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            conn.commit()
            cur.close()
        except Error as err:
            print("Error : {}".format(err))

    def create_tables(self, db_name: str, sql_file: str) -> None:
        conn, cur = self.connect(db_name)
        fd = open(sql_file, 'r')
        read_sql_file = fd.read()
        fd.close()

        sqlCommands = read_sql_file.split(';')
        for command in sqlCommands:
            try:
                res = cur.execute(command)
            except Exception as ex:
                print("Command skipped: ", ex)
        conn.commit()
        cur.close()
        return

    def csv_db(self):



if __name__ == "__main__":
    ld = LoadData()
    # ld.create_db("SensorData")
    # ld.create_tables("SensorData", "I80_stations_schema.sql")
    ld.create_tables("SensorData", "I80_davis_schema.sql")
