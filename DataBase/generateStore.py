from faker import Faker
import mysql.connector
import random
import re
import csv
import datetime
import generateUser
from id_manager import generate_unique_user_id

fake = Faker()
used_ids = set()
used_website = set()
reserved_set = {1,2,3,4}

#note store and arcade are interchangeable for most cases in the program
# ok stores consist of
#  store_id, store_name, website, city, address

#this function generates a random store_id
#we need to generate a random store_id for each arcade, and make sure its not in use
#I want the ids in the form of 000005, 000026, etc
def generate_store_id(used_ids):
    while True:
        store_id = random.randint(1, 1000000)
        if store_id not in used_ids and store_id not in reserved_set:
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


#function to generate random arcade addresses, but we just want it to generate the street name and number
def generate_store_address():
    return fake.street_address()

#function to generate random arcade hours in the form of "9:00am to 9:00 pm" open atleast for 8 hours
def generate_city():
    return fake.city()

#function to generate what days the arcade is open
#we want a random amount of days open, but at least 4 days, even added weights so 6 and 7 are more common
def generate_days_open():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    num_days = random.choices([4, 5, 6, 7], weights=[0.1, 0.2, 0.4, 0.3])[0]
    return random.sample(days, num_days)



#oh we want to use military time for the hours
def generate_store_hours():
    # Generate a random start hour between 9 (9 AM) and 15 (3 PM)
    start_hour = random.randint(9, 15)

    # Generate a random end hour, at least 8 hours after start, but not later than 23 (11 PM)
    end_hour = random.randint(start_hour + 8, 23)

    # Format the hours
    formatted_start_hour = f"{start_hour:02d}:00"
    formatted_end_hour = f"{end_hour:02d}:00"

    # we want to return both the open hour and the close hour, separately
    return formatted_start_hour, formatted_end_hour

#once we get the two hours from the store

    


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


# hours are returned in two parts, we need to write it to the csv
def write_to_csv(used_ids, used_websites):
    # new store data
    store_id = generate_store_id(used_ids)
    store_name = generate_store_name()
    store_website = generate_store_website(store_name, used_websites)
    store_city = generate_city()
    store_address = generate_store_address()
    store_weekdays = generate_days_open()
    store_open_hour, store_close_hour = generate_store_hours()

    # Check if a user should be reused
    reuse_user = random.randint(1, 20) == 1

    if reuse_user:
        # Select a random existing user
        with open('user.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_users = list(reader)
            random_user = random.choice(existing_users)

        # Set store user values to existing user values
        store_user_id = random_user['user_id']
        store_user_first_name = random_user['firstname']
        store_user_last_name = random_user['lastname']
        store_user_email = random_user['email']
    else:
        # Generate new user values
        store_user_id = generate_unique_user_id()
        store_user_first_name = generateUser.generate_firstname()
        store_user_last_name = generateUser.generate_lastname()
        store_user_email = generateUser.generate_email(store_user_first_name, store_user_last_name)

    # new store data to CSV 'store.csv'
    with open('store.csv', 'a', newline='') as csvfile:
        fieldnames = ['Store_id', 'Store_name', 'Website', 'City', 'Address', 'Weekday', 'Open_time', 'Close_time', 'User_id', 'User_first_name', 'User_last_name', 'User_email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'Store_id': store_id, 'Store_name': store_name, 'Website': store_website, 'City': store_city,
                          'Address': store_address, 'Weekday': store_weekdays, 'Open_time': store_open_hour, 'Close_time': store_close_hour,
                          'User_id': store_user_id,'User_first_name': store_user_first_name, 'User_last_name': store_user_last_name, 'User_email': store_user_email})

    # also make a user for each store if not reusing an existing user
    if not reuse_user:
        with open('user.csv', 'a', newline='') as csvfile:
            fieldnames = ['user_id', 'firstname', 'lastname', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'user_id': store_user_id, 'firstname': store_user_first_name, 'lastname': store_user_last_name, 'email': store_user_email})

    

    # new store data to CSV 'store.csv'
    with open('store.csv', 'a', newline='') as csvfile:
        fieldnames = ['Store_id', 'Store_name', 'Website', 'City', 'Address', 'Weekday', 'Open_time', 'Close_time', 'User_id', 'User_first_name', 'User_last_name', 'User_email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'Store_id': store_id, 'Store_name': store_name, 'Website': store_website, 'City': store_city,
                          'Address': store_address, 'Weekday': store_weekdays, 'Open_time': store_open_hour, 'Close_time': store_close_hour,
                          'User_id': store_user_id,'User_first_name': store_user_first_name, 'User_last_name': store_user_last_name, 'User_email': store_user_email})

    #also make a user for each store
    with open('user.csv', 'a', newline='') as csvfile:
        fieldnames = ['user_id', 'firstname', 'lastname', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'user_id': store_user_id, 'firstname': store_user_first_name, 'lastname': store_user_last_name, 'email': store_user_email})

#we need to generate a user for each store, that we will store in the store cvs file aswell


# generate and write 20 stores
generate_and_write_stores(20)

# print (generate_store_address(),",", generate_city())
# print (generate_store_id(used_ids))


