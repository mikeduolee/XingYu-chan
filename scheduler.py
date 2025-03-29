from utils import get_reading, load_all_users
from linebot import LineBotApi
from dotenv import load_dotenv
import os
import time

load_dotenv()
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))

def push_daily_message():
    users = load_all_users()
    message = get_reading()
    for user_id in users:
        try:
            line_bot_api.push_message(user_id, TextSendMessage(text=message))
        except Exception as e:
            print(f"❌ 推播失敗: {user_id} - {str(e)}")

if __name__ == "__main__":
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == "08:00":
            from linebot.models import TextSendMessage
            print("🌞 發送每日星語中...")
            push_daily_message()
            time.sleep(60)  # 避免重複發送
        else:
            time.sleep(30)
