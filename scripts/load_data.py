import os
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error


class LoadData():

    def __init__(self):
        pass

    def connect(self, dbName=None):
        try:
            conn = mysql.connect(host='localhost',
                                  user=os.getenv("USER"),
                                  password=os.getenv("PASSWORD"),
                                 database=dbName, buffered=True)
            cur = conn.cursor()
            return conn, cur
        except Error as err:
            print("Database connection error: {}".format(err))




if __name__ == "__main__":
    ld = LoadData()
    ld.connect()
    ld.create_db("SensorData")
