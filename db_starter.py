import mysql.connector
from configparser import ConfigParser
import json

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


def create_table(config_file, lst_table_descriptions):
    """
    This method takes in the config file path and list of table descriptions and creates tables
    @param lst_table_descriptions: list of table descriptions
    @param config_file:  File Path of the configFile for the database
    """
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # preparing a cursor object
    cursor_object = data_base.cursor()
    for table_description in lst_table_descriptions:
        cursor_object.execute(table_description)


#TODO: make sure to specify which columns will be NULL for all tables (For now only IDs are NULL)
table_description_store = """
CREATE TABLE IF NOT EXISTS store (
    store_id varchar(10) NOT NULL,
    store_name varchar(250),
    website varchar(250),
    city varchar(250),
    address varchar(250), 
    PRIMARY KEY(store_id)
    )
"""

#TODO: for release_date we may change int for date
table_description_games = """
CREATE TABLE IF NOT EXISTS games (
    game_id varchar(10) NOT NULL,
    game_name varchar(250),
    release_date int,
    genre varchar(250),
    num_of_players int, 
    type_of_machine varchar(250),
    PRIMARY KEY(game_id)
)
"""


table_description_store_game = """
CREATE TABLE IF NOT EXISTS store_game (
    store_id varchar(10) NOT NULL,
    game_id varchar(10) NOT NULL,
    game_cost int,
    FOREIGN KEY(store_id) REFERENCES store(store_id),
    FOREIGN KEY(game_id) REFERENCES games(game_id)
)
"""


table_description_store_hours = """
CREATE TABLE IF NOT EXISTS store_hours (
    store_id varchar(10) NOT NULL,
    weekday varchar(250),
    open_time time,
    close_time time,
    FOREIGN KEY(store_id) REFERENCES store(store_id)
)
"""


table_description_user = """
CREATE TABLE IF NOT EXISTS user (
    user_id varchar(10) NOT NULL,
    store_id varchar(10) NOT NULL,
    first_name varchar(250),
    last_name varchar(250),
    email varchar(250),
    PRIMARY KEY(user_id),
    FOREIGN KEY(store_id) REFERENCES store(store_id)
)
"""

# List all table sql creation code here
lst_table_descriptions = [table_description_store, table_description_games,
                          table_description_store_game, table_description_store_hours,
                          table_description_user]

# Start program here
create_db()
create_table(config_file="connectorConfig.json", lst_table_descriptions=lst_table_descriptions)