from faker import Faker
import mysql.connector
import random
import re
import csv
import datetime

fake = Faker()
used_ids = set()
used_website = set()

#note store and arcade are interchangeable for most cases in the program
# ok stores consist of
#  store_id, store_name, website, city, address

#this function generates a random store_id
#we need to generate a random store_id for each arcade, and make sure its not in use
def generate_store_id(used_ids):
    while True:
        store_id = fake.random_int(min=1, max=9999)
        if store_id not in used_ids:
            used_ids.add(store_id)
            return store_id

#function to generate random store(arcade) names
def generate_store_name():
    # Lists of themed words
    adjectives = ['Glowing', 'Golden', 'Time-Warp', 'Mystic', 'Retro', 'Virtual', 'Neon', 'Pixelated', 'Retro', 'Electric', 'Cosmic', 'Digital', 'Cyber', 'High Voltage', 'Laser', 'Dry-Dry', 'Arcane', 'Enchanted', 'Epic', 'Fantastic', 'Magical', 'Mythical', 'Legendary', 'Spectacular', 'Wonderful']

    nouns = ['Joystick', 'Pixel', 'Quest', 'Playground', 'Realm', 'Night', 'Domain', 'Dungeon', 'Kingdom', 'Empire', 'Emporium', 'Asylum', 'Haven', 'Station', 'Loft', 'Groove', 'Refuge', 'Den', 'Club', 'Garage', 'Alley', 'Circuit', 'Zone', 'Galaxy', 'Oasis', 'Lab', 'Labrynth', 'Matrix', 'Dimension', 'Expanse', 'Sanctuary']

    # Randomly choose from each list
    chosen_adjective = random.choice(adjectives)
    chosen_noun = random.choice(nouns)


    storename = f'{chosen_adjective} {chosen_noun} Arcade'
    return storename


#url should have something to do with the name of the store
#function to generate random arcade websites
def generate_store_website(store_name, used_websites):
    while True:
        url_friendly_name = re.sub(r'\s+', '', store_name).lower().replace('arcade', '')
        website = f'www.{url_friendly_name}.com'
        if website not in used_websites:
            used_websites.add(website)
            return website


#function to generate random arcade addresses
def generate_store_address():
    return fake.address()

#function to generate random arcade hours in the form of "9:00am to 9:00 pm" open atleast for 8 hours


def generate_store_hours():
    # Generate a random start hour between 9 AM (9) and 3 PM (15)
    start_hour = random.randint(9, 15)

    # Generate a random end hour, at least 8 hours after start, but not later than 11 PM (23)
    end_hour = random.randint(start_hour + 8, 23)

    # Convert hours to 12-hour format and format them
    formatted_start_hour = f"{start_hour if start_hour <= 12 else start_hour - 12}{'am' if start_hour < 12 else 'pm'}"
    formatted_end_hour = f"{end_hour if end_hour <= 12 or end_hour == 24 else end_hour - 12}{'am' if end_hour < 12 or end_hour == 24 else 'pm'}"

    return f"{formatted_start_hour}-{formatted_end_hour}"



    
    


  

#function to generate random arcade cities
# def generate_store_city():
#     return fake.city()


# # Generate store data
# store_name = generate_store_name()
# store_website = generate_store_website(store_name)
# store_id = generate_store_id()
# store_address = generate_store_address()
# store_city = generate_store_city()

# print("Generating fake data...")
# print(store_id, "\n", store_name, "\n", store_website, "\n", store_address, store_city)

def generate_and_write_stores(num_stores):
    used_ids = set()
    used_websites = set()
    try:
        with open('store.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                used_ids.add(int(row['store_id']))
                used_websites.add(row['website'])
    except FileNotFoundError:
        pass

    for _ in range(num_stores):
        write_to_csv(used_ids, used_websites)


def write_to_csv(used_ids, used_websites):
    # new store data
    store_id = generate_store_id(used_ids)
    store_name = generate_store_name()
    store_website = generate_store_website(store_name, used_websites)
    store_address = generate_store_address()

    # new store data to CSV 'store.csv'
    with open('store.csv', 'a', newline='') as csvfile:
        fieldnames = ['store_id', 'store_name', 'website', 'city', 'address']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'store_id': store_id, 'store_name': store_name, 'website': store_website, 'address': store_address})

# generate and write 20 stores
# generate_and_write_stores(20)
print(generate_store_hours())
