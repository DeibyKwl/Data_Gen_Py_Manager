
import random
import csv

used_ids = set()
reserved_user_ids = {10,2,1,6}


# generate user id stored separately to avoid collisions

def generate_unique_user_id():
    global used_ids
    while True:
        new_id = random.randint(1, 1000000)
        if new_id not in used_ids and new_id not in reserved_user_ids:
            used_ids.add(new_id)
            return new_id
