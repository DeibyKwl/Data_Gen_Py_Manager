import mysql.connector
from configparser import ConfigParser
import json
import os

def create_db():
    with open("connectorConfig.json", "r") as f:
        config = json.load(f)

    connection_config = config["mysql"]
    dataBase = mysql.connector.connect(host=connection_config["host"],
    user = connection_config["user"],
    passwd = connection_config["passwd"])

    # preparing a cursor object
    cursorObject = dataBase.cursor()

    # creating database
    cursorObject.execute("CREATE DATABASE IF NOT EXISTS arcade")


def create_table(config_file, table_dir):

    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # preparing a cursor object
    cursor_object = data_base.cursor()

    # Inserting the sql commands one by one
    for table_sql_file in os.listdir(table_dir):
        with open(table_dir+table_sql_file, "r") as f:
            table_query = f.read()
            cursor_object.execute(table_query)

# Start program here
create_db()
create_table(config_file="connectorConfig.json", table_dir="table/")