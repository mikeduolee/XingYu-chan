from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from utils import get_reading, add_user_if_new
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
        result = get_reading()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="""🌟 星語姬輕聲說：

嗨～我是星語姬，一位聆聽星星低語的小占星師✨  
我能替你擲出三顆星之骰，從中解讀出宇宙給你的悄悄話～

你可以對我說：
🔮「擲骰」—— 開啟一則星之占語  
🌌「幫我占卜」—— 我會讀出此刻的星星訊息給你  
🪐 或者靜靜地想著一個問題，再對我說「占卜」就好～

準備好傾聽星辰的指引了嗎？💫""")

        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
