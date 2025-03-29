from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
from utils import get_random_reading, add_user_if_new
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    add_user_if_new(user_id)
    msg = event.message.text.strip()
    if "擲骰" in msg or "占卜" in msg or "幫我" in msg:
        result = get_random_reading()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="嗨～我可以幫你擲骰占卜，輸入「擲骰」或「占卜」就可以囉！"))

if __name__ == "__main__":
    app.run()
