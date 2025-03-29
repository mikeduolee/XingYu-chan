import pandas as pd
import random
import json
import os

DATA_PATH = "fuyu_astrodice_readings.csv"
USER_PATH = "user_ids.json"

df = pd.read_csv(DATA_PATH)

def get_random_reading():
    row = df.sample(1).iloc[0]
    return row["占卜語"]

def add_user_if_new(user_id):
    users = load_all_users()
    if user_id not in users:
        users.append(user_id)
        with open(USER_PATH, "w") as f:
            json.dump(users, f)

def load_all_users():
    if not os.path.exists(USER_PATH):
        return []
    with open(USER_PATH, "r") as f:
        return json.load(f)
