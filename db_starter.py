import mysql.connector
import json
import os

def create_db():
    with open("connectorConfig.json", "r") as f:
        config = json.load(f)

    connection_config = config["mysql"]
    dataBase = mysql.connector.connect(host=connection_config["host"],
                                       user=connection_config["user"],
                                       passwd=connection_config["passwd"])

    # preparing a cursor object
    cursorObject = dataBase.cursor()

    # creating database
    cursorObject.execute("CREATE DATABASE IF NOT EXISTS arcade")
    dataBase.close()

def create_table(config_file, table_dir):

    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # preparing a cursor object
    cursor_object = data_base.cursor()

    # List of table creation scripts ordered by dependency
    # Hardcoded for now but we will change later
    table_creation_order = [
        'table_games.sql',
        'table_game_genre.sql',
        'table_store.sql',
        'table_store_hours.sql',
        'table_store_game.sql',
        'table_user.sql',
        # Add any other tables in the order they should be created
    ]

    # Execute the SQL files in the defined order
    for table_sql_file in table_creation_order:
        with open(os.path.join(table_dir, table_sql_file), "r") as f:
            table_query = f.read()
            try:
                cursor_object.execute(table_query)
                data_base.commit()  # Commit changes
            except mysql.connector.Error as err:
                print(f"Error: '{err}' occurred while executing {table_sql_file}")
                data_base.rollback()  # Roll back in case of error
                break  # Stop the execution as there was an error

    cursor_object.close()
    data_base.close()

# Start program here
create_db()
create_table(config_file="connectorConfig.json", table_dir="table/")
