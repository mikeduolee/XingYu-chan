import pandas as pd
import random
import json
import os

DATA_PATH = "xingyu_astrodice_final_from_fuyu.csv"
USER_PATH = "user_ids.json"

# 載入星語姬占星骰資料
df = pd.read_csv(DATA_PATH)

# 統一讀取占卜語（可用於每日推播與即時互動）
def get_reading():
    row = df.sample(1).iloc[0]
    return row["占卜語"]

# 使用者記錄（每日推播會用到）
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
