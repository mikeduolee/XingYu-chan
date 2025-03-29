from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
import os
import random
from utils import get_reading, add_user_if_new

load_dotenv()
app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

def get_question_intro(user_message):
    intros = [
        "🌟 星語姬輕聲說：\n\n我聽見了你心裡的聲音：",
        "🌟 星語姬輕聲說：\n\n星星們正在傾聽你的問題…",
        "🌟 星語姬輕聲說：\n\n啊～這顆星星好像對你悄悄說了點什麼，我來幫你翻譯看看吧～\n\n你問的是："
    ]
    intro = random.choice(intros)
    return f"{intro}「{user_message}」\n\n如果你準備好了～請對我說「擲骰」，我就會幫你揭開答案喔！💫"

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

    if "擲骰" in msg or "占卜" in msg:
        reply = get_reading()
    elif msg.startswith("問題："):
        reply = get_question_intro(msg)
    else:
        reply = (
            "🌟 星語姬輕聲說：\n\n"
            "嗨～我是星語姬，一位聆聽星星低語的小占星師✨\n"
            "我能替你擲出三顆星之骰，從中翻譯宇宙的訊息～\n\n"
            "你可以對我說：\n"
            "🔮 擲骰｜📩 幫我占卜\n\n"
            "🌌 或是輸入你心中的問題（請以「問題：」開頭），我會傾聽，再等你說出「擲骰」，讓星星替你作出回應～💫\n"
        )

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
