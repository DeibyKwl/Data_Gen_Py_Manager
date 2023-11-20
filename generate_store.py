from faker import Faker
import mysql.connector
import random
import re
import csv
import datetime
import generate_user
# from id_manager import generate_unique_user_id
import os
import os


fake = Faker()
used_ids = set()
used_website = set()
reserved_set = {1,2,3,4}


#so the goal of generateStore.py is to generate random arcade data
#the store.csv will contain information that includes the:
# store_id, store_name, website, city, address, weekday, open_time, close_time, user_id, user_first_name, user_last_name, user_email

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
    adjectives = [
        'Glowing', 'Golden', 'Time-Warp', 'Mystic', 'Retro', 'Virtual', 'Neon', 'Pixelated', 'Electric', 
        'Cosmic', 'Digital', 'Cyber', 'High Voltage', 'Laser', 'Dry-Dry', 'Arcane', 'Enchanted', 'Epic', 'Fantastic', 
        'Magical', 'Mythical', 'Legendary', 'Spectacular', 'Wonderful', 'World', 'Planet', 'Base', 'Portal', 'Chamber', 
        'Domain', 'Terminal', 'Blazing', 'Stellar', 'Thundering', 'Infinity', 'Quantum', 'Neon-Lit', 'Turbocharged', 
        'Galactic', 'Interstellar', 'Flashing', 'Shimmering', 'Radiant', 'Illustrious', 'Twinkling', 'Phantom', 
        'Dazzling', 'Prismatic', 'Hyper', 'Virtual', 'Cosmic', 'Astral', 'Dynamic', 'Kinetic', 'Invincible', 'Sonic', 
        'Ultra', 'Mega', 'Supercharged', 'Hypersonic', 'Nova', 'Eclipse', 'Starlit', 'Moonlit', 'Sunlit', 'Luminous', 
        'Vibrant', 'Sparkling', 'Hologram', 'Futuristic', 'Celestial', 'Meteoric', 'Solar', 'Lunar', 'Astro', 'Nebula', 
        'Pulsar', 'Polaris', 'Interdimensional', 'Twilight', 'Dawn', 'Dusk', 'Aurora', 'Zenith'
    ]

    nouns = [
        'Joystick', 'Pixel', 'Quest', 'Playground', 'Realm', 'Night', 'Domain', 'Dungeon', 'Kingdom', 'Empire', 
        'Emporium', 'Asylum', 'Haven', 'Station', 'Loft', 'Groove', 'Refuge', 'Den', 'Club', 'Garage', 'Alley', 
        'Circuit', 'Zone', 'Galaxy', 'Oasis', 'Lab', 'Labrynth', 'Matrix', 'Dimension', 'Expanse', 'Sanctuary', 
        'Nexus', 'Odyssey', 'Arena', 'Pavilion', 'Fortress', 'Hub', 'Parlor', 'World', 'Planet', 'Base', 'Portal', 
        'Chamber', 'Domain', 'Terminal', 'Complex', 'Center', 'Sphere', 'Gateway', 'Coliseum', 'Hangout', 'Lounge', 
        'Suite', 'Lair', 'Hideout', 'Shelter', 'Shrine', 'Vault', 'Plaza', 'Terrace', 'Domain', 'Grotto', 'Citadel', 
        'Castle', 'Palace', 'Garden', 'Grove', 'Island', 'Tower', 'Spire', 'Keep', 'Estate', 'Pavilion', 'Realm', 
        'Waterscape', 'Dreamscape', 'Mindscape', 'Vortex', 'Horizon', 'Void', 'Chasm', 'Cosmos', 'Arcade', 
        'Battleground', 'Beacon', 'Cove', 'Enclave', 'Gateway', 'Glade', 'Hinterland', 'Junction', 'Labyrinth', 
        'Mirage', 'Observatory', 'Pinnacle', 'Retreat', 'Sanctum', 'Sphere', 'Thicket', 'Underworld', 'Vestibule', 
        'Wonderland', 'Zenith'
    ]

    # Remove duplicates by converting to sets and back to lists
    adjectives = list(set(adjectives))
    nouns = list(set(nouns))

    # Randomly choose from each list
    chosen_adjective = random.choice(adjectives)
    chosen_adjective2 = random.choice(adjectives)
    chosen_noun = random.choice(nouns)
    storename = f'{chosen_adjective} {chosen_adjective2} {chosen_noun} Arcade'
    return storename

#url should have something to do with the name of the store
#function to generate random arcade websites
def generate_store_website(store_name, used_websites):
    url_friendly_name = re.sub(r'\s+', '', store_name).lower().replace('arcade', '')
    base_website = f'www.{url_friendly_name}'

    try:
        website = f'{base_website}.com'
        if website not in used_websites:
            used_websites.add(website)
            return website
        else:
            count = 1
            while True:
                modified_website = f'{base_website}{count}.com'
                if modified_website not in used_websites:
                    used_websites.add(modified_website)
                    return modified_website
                count += 1
    except Exception as e:
        print(f"Error generating store website: {e}")
        return None



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

#NOTE: up to here we have functions that generate all the store specific data
# we will need user information  when making the store.csv

#generate all the store data
def generate_store_data(used_ids, used_websites):
    store_id = generate_store_id(used_ids)
    store_name = generate_store_name()
    store_website = generate_store_website(store_name, used_websites)
    store_city = generate_city()
    store_address = generate_store_address()
    store_weekdays = generate_days_open()
    store_open_hour, store_close_hour = generate_store_hours()

    return store_id, store_name, store_website, store_city, store_address, store_weekdays, store_open_hour, store_close_hour


#we need to generate the user data for the store.csv
def call_generate_user():
    user_id, firstname, lastname, email = generate_user.generate_new_user()
    return user_id, firstname, lastname, email

# we need a function to determine if the user does not need to be generate and instead use an existing user
#this should read all parts of the existing user.csv (User_id, User_first_name, User_last_name, User_email)
def get_existing_user():
    # Empty list to store all users
    users = []

    # Check user.csv, inside the store_data folder for existing users
    #with open(os.path.join('store_data', 'user.csv'), 'r', newline='') as csvfile:
    with open('user.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            users.append(row)

    # If the list is not empty
    if users:
        # Random user from the list
        random_user = random.choice(users)
        return random_user
    else:
        return None

def write_store_to_csv(store_id, store_name, store_website, store_city, store_address, store_weekdays, store_open_hour, store_close_hour, user_data):
    # Check if the store_data folder exists, create it if it doesn't
    if not os.path.exists('store_data'):
        os.makedirs('store_data')

    # Check if the store.csv file exists, create it if it doesn't
    if not os.path.exists('store_data/store.csv'):
        with open('store_data/store.csv', 'a', newline='') as csvfile:
            fieldnames = ['Store_id', 'Store_name', 'Store_website', 'Store_city', 'Store_address', 'Store_weekdays', 'Store_open_hour', 'Store_close_hour', 'User_id', 'User_first_name', 'User_last_name', 'User_email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    
    #if not os.path.exists('store_data/user.csv'):
    #    with open('store_data/user.csv', 'w', newline='') as csvfile:
    #        fieldnames = ['User_id', 'User_first_name', 'User_last_name', 'User_email']
    #        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #        writer.writeheader()

    with open('store_data/store.csv', 'a', newline='') as csvfile:
        fieldnames = ['Store_id', 'Store_name', 'Store_website', 'Store_city', 'Store_address', 'Store_weekdays', 'Store_open_hour', 'Store_close_hour', 'User_id', 'User_first_name', 'User_last_name', 'User_email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Prepare the store data
        store_data = {
            'Store_id': store_id,
            'Store_name': store_name,
            'Store_website': store_website,
            'Store_city': store_city,
            'Store_address': store_address,
            'Store_weekdays': ', '.join(store_weekdays),
            'Store_open_hour': store_open_hour,
            'Store_close_hour': store_close_hour,
            'User_id': user_data['User_id'],
            'User_first_name': user_data['User_first_name'],
            'User_last_name': user_data['User_last_name'],
            'User_email': user_data['User_email']
        }

        # Write the store data
        writer.writerow(store_data)

def generate_and_write_stores(num_stores):
    for i in range(num_stores):
        if random.randint(1, 20) == 1:
            # print(f"Store {i+1}: Attempting to reuse existing user")
            user_data = get_existing_user()
            if user_data is None:  
                # print(f"Store {i+1}: No existing user found, generating a new one")
                user_id, firstname, lastname, email = call_generate_user()
                user_data = {'User_id': user_id, 'User_first_name': firstname, 'User_last_name': lastname, 'User_email': email}
                generate_user.write_user_to_csv(user_id, firstname, lastname, email)
            else:
                # print(f"Store {i+1}: Reusing user: {user_data['User_id']}")
                pass
        else:
            # print(f"Store {i+1}: Generating new user")
            user_id, firstname, lastname, email = call_generate_user()
            user_data = {'User_id': user_id, 'User_first_name': firstname, 'User_last_name': lastname, 'User_email': email}
            generate_user.write_user_to_csv(user_id, firstname, lastname, email)

        store_id, store_name, store_website, store_city, store_address, store_weekdays, store_open_hour, store_close_hour = generate_store_data(used_ids, used_website)
        write_store_to_csv(store_id, store_name, store_website, store_city, store_address, store_weekdays, store_open_hour, store_close_hour, user_data)
        # print(f"Store {i+1}: Store data written to CSV")

# generate and write n stores
generate_and_write_stores(1000)