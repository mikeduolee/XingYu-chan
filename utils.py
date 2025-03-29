import pandas as pd
import random
import json
import os

FULL_PATH = "xingyu_astrodice_full.csv"
MULTI_PATH = "xingyu_astrodice_multi.csv"
USER_PATH = "user_ids.json"

# 載入兩份資料
df_full = pd.read_csv(FULL_PATH)
df_multi = pd.read_csv(MULTI_PATH)

# 早上自動推播使用完整版
def get_daily_reading():
    row = df_full.sample(1).iloc[0]
    return row["占卜語"]

# 使用者即時互動使用多語氣版
def get_interactive_reading():
    row = df_multi.sample(1).iloc[0]
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
