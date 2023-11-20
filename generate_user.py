from faker import Faker
import random
import re
import csv
import datetime
from id_manager import generate_unique_user_id


fake = Faker()
used_user_ids = set()
reserved_user_ids = {10,2,1,6}

#make a first name
def generate_firstname():
    return fake.first_name()

#makea last name
def generate_lastname():
    return fake.last_name()


# we want email to be firstname.lastname@domain
def generate_email(firstname, lastname):
    return f"{firstname}.{lastname}@{fake.domain_name()}"

#using generate_unique_user_id() from id_manager.py, and the above functions, generate a new user
def generate_new_user():
    firstname = generate_firstname()
    lastname = generate_lastname()
    email = generate_email(firstname, lastname)
    user_id = generate_unique_user_id()
    return user_id, firstname, lastname, email

#generate a user from the existing user.csv
def get_existing_user():
    with open('user.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            used_user_ids.add(int(row['User_id']))
    return random.choice(list(used_user_ids))

#write the user to user.csv
def write_user_to_csv(user_id, firstname, lastname, email):
    with open('store_data/user.csv', 'a', newline='') as csvfile:
        fieldnames = ['User_id', 'User_first_name', 'User_last_name', 'User_email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({
            'User_id': user_id,
            'User_first_name': firstname,
            'User_last_name': lastname,
            'User_email': email
        })

#generate 5 users
def generate_and_write_users(num_users):
    for _ in range(num_users):
        user_id, firstname, lastname, email = generate_new_user()
        write_user_to_csv(user_id, firstname, lastname, email)


