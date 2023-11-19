from faker import Faker
import random
import re
import csv
import datetime
from id_manager import generate_unique_user_id


fake = Faker()
used_user_ids = set()


def generate_firstname():
    return fake.first_name()

def generate_lastname():
    return fake.last_name()

#we want email to be firstname.lastname@domain
def generate_email(firstname, lastname):
    return f"{firstname}.{lastname}@{fake.domain_name()}"

#generate user id
# def generate_user_id(used_user_ids):
#     while True:
#         user_id = random.randint(1, 1000000)
#         if user_id not in used_user_ids:
#             used_user_ids.add(user_id)
#             return user_id



def generate_and_write_users(num_users):
    used_user_ids = set()
    try:
        with open('user.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                used_user_ids.add(int(row[0]))
    except:
        pass

    with open('user.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(num_users):
            user_id = generate_unique_user_id()
            firstname = generate_firstname()
            lastname = generate_lastname()
            email = generate_email(firstname, lastname)
            writer.writerow([user_id, firstname, lastname, email])

def write_to_csv(used_ids):
    # new user data
    user_id = generate_unique_user_id()
    firstname = generate_firstname()
    lastname = generate_lastname()
    email = generate_email(firstname, lastname)

    # new user data to CSV 'user.csv'
    with open('user.csv', 'a', newline='') as csvfile:
        fieldnames = ['User_id', 'User_first_name', 'User_last_name', 'User_email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'User_id': user_id, 'User_first_name': firstname, 'User_last_name': lastname, 'User_email': email})

#create a csv file with a varible number of users

generate_and_write_users(10)