
import random
import csv

used_ids = set()

# generate user id stored separately to avoid collisions

def generate_unique_user_id():
    global used_ids
    while True:
        new_id = random.randint(1, 1000000)
        if new_id not in used_ids:
            used_ids.add(new_id)
            return new_id