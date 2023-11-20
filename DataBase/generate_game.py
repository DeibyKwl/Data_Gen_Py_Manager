from faker import Faker
import mysql.connector
import random
import re
import csv

fake = Faker()
used_ids = set()
used_game_names = set()
reserved_set = {1,2,5,6,8,100}

# this function generates a random game ID, besides 1,2,5,6,8,100
#these numbers are reserved
def generate_game_ID():
    while True:
        game_id = random.randint(1, 1000000)
        if game_id not in used_ids and game_id not in reserved_set:
            used_ids.add(game_id)
            return game_id
        
def generate_game_name(n):
# lists of words to make names from
    adjectives = ["Galaxy", "Neon", "Cyber", "Asteroid", "Pixel", "Laser", "Robo", "Space", "Mystic", "Alien", "Retro", "Crystal", "Jungle", "Time", "Cosmic", "Phantom", "Monster", "Electric", "Sky" , "House of the"]
    nouns = ["Invaders", "Racer", "Ninja", "Blaster", "Pirate", "Quest", "Rebellion", "Warp", "Dragon", "Wizard", "Assault", "Rocket", "Cavern", "Jumper", "Traveler", "Combat", "Fighter", "Mash", "Maze", "Surfer"]
    suffixes = ["3000", "Xtreme", "Showdown", "Pro", "Adventure", "Odyssey", "Saga", "Challenge", "Quest", "Wars", "Force", "Racers", "Escape", "Mania", "Trials", "League", "Elite", "Mayhem", "Escape", "Showdown"]

    game_names = []
    while len(game_names) < n:
        name = f"{random.choice(adjectives)} {random.choice(nouns)} {random.choice(suffixes)}"
        if name not in used_game_names:
            used_game_names.add(name)
            game_names.append(name)

    return game_names

def generate_game_genre():
    genres = ["Fighting", "Shooter", "Platformer", "Racing", "Puzzle", "Sport", "Beat 'em Up", "Light Gun Shooter", "Rhythm Game", "Pinball"]
    num_genres = random.choices([1,2,3,4], [0.1, 0.2, 0.4, 0.3])[0]
    return random.sample(genres, num_genres)

# generate game price from .25 to 2.00 in increments of .25
def generate_game_price():
    return random.randrange(1, 9) / 4

# generate number of players: 1, 2 or 4
def generate_num_players():
    return random.choice([1, 2, 4])

# generate release date from 1975 to today
def generate_release_date():
    return fake.date_between(start_date='-45y', end_date='today')

def generate_type_of_machine():
    type_of_machines = ["Arcade Cabinet", "Pinball Machine", "Racing Simulator", "Claw Machine", "Dance Dance Revolution Machine", "Foosball Table", "Guitar Arcade Unit", "Bubble Hockey Table", "Virtual Pinball Machine", "Arcade Boxing Machine", "Interactive Touchscreen", "Coin Pusher Machine", "Virtual Reality Arcade Pod", "Basketball Shooting Game"]
    return random.choice(type_of_machines)

# arcade_game_names = generate_game_name(10)
# print (arcade_game_names)
# print(generate_release_date())

def generate_and_write_games(num_games):
    used_ids = set()
    used_game_names = set()
    try:
        with open('game.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                used_ids.add(int(row['game_id']))
                used_game_names.add(row['game_name'])
    except FileNotFoundError:
        pass
    for _ in range (num_games):
        write_to_cvs(used_ids, used_game_names)

#we want to generate a csv for the games like with the generateStore.py
def write_to_cvs (used_ids, used_game_names):

    # new game data to CVS 'game.csv'
    with open('game.csv', 'w', newline='') as csvfile:
        fieldnames = ['game_id', 'game_name', 'release_date', 'game_genre', 'num_players', 'type_of_machine', 'game_price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, 11):

            # generate game data
            game_id = generate_game_ID()
            game_name = ' '.join(generate_game_name(1))
            game_genre = ', '.join(generate_game_genre())
            game_price = generate_game_price()
            num_players = generate_num_players()
            release_date = generate_release_date()
            type_of_machine = generate_type_of_machine()

            writer.writerow({'game_id': game_id, 'game_name': game_name, 'release_date': release_date, 'game_genre': game_genre,  'num_players': num_players, 'type_of_machine': type_of_machine, 'game_price': game_price})


generate_and_write_games(10)

#for i in range(9):
#    game_genre = ', '.join(generate_game_genre())
#    print(game_genre)
