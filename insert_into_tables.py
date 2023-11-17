import csv
import os

import mysql.connector
import json

def read_store_csv_file(path_to_store_dir, dic_tuples_store, dic_tuples_store_hours, dic_tuples_user):
    # For store csv files
    with open(path_to_store_dir, newline='', encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        print(path_to_store_dir)
        next(csv_reader)
        
        # Collect data per row
        for row in csv_reader:
            store_id = row[0]
            store_name = row[1]
            website = row[2]
            city = row[3]
            address = row[4]
            list_weekday = row[5].split(",")
            open_time = row[6]
            close_time = row[7]
            user_id = row[8]
            user_first_name = row[9]
            user_last_name = row[10]
            user_email = row[11]

            dic_tuples_store[store_id] = (store_id, store_name, website, city, address)

            dic_tuples_store_hours[store_id] = []
            for weekday in list_weekday:
                dic_tuples_store_hours[store_id].append((store_id, weekday.strip(), open_time, close_time))
            
            dic_tuples_user[store_id] = (user_id, store_id, user_first_name, user_last_name, user_email)
    
    return dic_tuples_store, dic_tuples_store_hours, dic_tuples_user


def read_games_csv_file(path_to_game_dir, dic_tuples_games, dic_tuples_store_game):
    # For games csv files
    with open(path_to_game_dir, newline='', encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        print(path_to_game_dir)
        next(csv_reader)
    
    # Collect data per row
        for row in csv_reader:
            game_id = row[0]
            store_id = row[1]
            game_name = row[2]
            release_date = row[3]
            genre = row[4] #TODO: Maybe genre could be a list.
            num_of_players = row[5]
            type_of_machine = row[6]
            game_cost = row[7]
            
            dic_tuples_games[game_id] = (game_id, game_name, release_date, genre, num_of_players, type_of_machine)

            dic_tuples_store_game[game_id] = (store_id, game_id, game_cost)


    return dic_tuples_games, dic_tuples_store_game


def insert_table(store_dir, game_dir, config_file, store_table, games_table, store_game_table, store_hours_table, user_table):
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
    dic_tuples_store = {}
    dic_tuples_games = {}
    dic_tuples_store_game = {}
    dic_tuples_store_hours = {}
    dic_tuples_user = {}

    # Search through the store csv files
    for store_csv_file in os.listdir(store_dir):
        dic_tuples_store, dic_tuples_store_hours, dic_tuples_user = \
            read_store_csv_file(store_dir + store_csv_file, dic_tuples_store, dic_tuples_store_hours, dic_tuples_user)
    
    # Search through the games csv files
    for game_csv_file in os.listdir(game_dir):
        dic_tuples_games, dic_tuples_store_game = \
           read_games_csv_file(game_dir + game_csv_file, dic_tuples_games, dic_tuples_store_game)
        

    for store_id in dic_tuples_store:
        cursor_object.execute("INSERT INTO "+store_table+" (store_id, store_name, website, city, address)"
                                "values (%s, %s, %s, %s, %s)", (dic_tuples_store[store_id]))
    
    print("PASS")
    
    for store_id in dic_tuples_store_hours:
        for day_hour in dic_tuples_store_hours[store_id]:
            cursor_object.execute("INSERT INTO "+store_hours_table+" (store_id, weekday, open_time, close_time)"
                                    "values (%s, %s, %s, %s)", (day_hour))
    
    print("PASS")

    for user_id in dic_tuples_user:
        cursor_object.execute("INSERT INTO "+user_table+" (user_id, store_id, first_name, last_name, email)"
                                "values (%s, %s, %s, %s, %s)", (dic_tuples_user[user_id]))
    
    print("PASS")
        
    for game_id in dic_tuples_games:
        cursor_object.execute("INSERT INTO "+games_table+" (game_id, game_name, release_date, genre, num_of_players, type_of_machine)"
                                "values (%s, %s, %s, %s, %s, %s)", (dic_tuples_games[game_id]))
    
    print("PASS")
        
    for store_id in dic_tuples_store_game:
        cursor_object.execute("INSERT INTO "+store_game_table+" (store_id, game_id, game_cost)"
                                "values (%s, %s, %s)", (dic_tuples_store_game[store_id]))
    
    print("PASS")

    data_base.commit()
    cursor_object.close()



path_to_game_dir = "game_data/"
path_to_store_dir = "store_data/"
insert_table(path_to_store_dir, path_to_game_dir, "connectorConfig.json", "store", "games", "store_game", "store_hours", "user")