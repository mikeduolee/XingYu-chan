from apscheduler.schedulers.blocking import BlockingScheduler
from linebot import LineBotApi
from linebot.models import TextSendMessage
from utils import get_random_reading, load_all_users
import os
from dotenv import load_dotenv

load_dotenv()
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=8, minute=0)
def morning_push():
    users = load_all_users()
    msg = get_random_reading()
    for user_id in users:
        try:
            line_bot_api.push_message(user_id, TextSendMessage(text=msg))
        except Exception as e:
            print(f"Error sending to {user_id}: {e}")

if __name__ == "__main__":
    sched.start()
