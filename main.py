import os
import errno
import tempfile
from flask import Flask, request, abort
from janome.tokenizer import Tokenizer
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, TextSendMessage, FollowEvent
)

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET) 

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    # 国名と首都の辞書
    country_dict = {
        "アメリカ" :["ワシントン"],
        "イタリア" :["ローマ"],
        "カナダ" :["オタワ"],
        "コートジボワール" :["ヤムスクロ"],
        "中国": ["北京"],
        "日本": ["東京"],
        "バチカン": ["ありません"],
        "モナコ" :["モナコ"],
        "モンゴル" :["ウランバートル"]
    }

    tokenizer = Tokenizer()
    for token in tokenizer.tokenize(text):
        # 分かち書きで国を受け取った場合
        if token.part_of_speech.split(",")[3] =="国":
            # 辞書にある国は首都を返す、辞書にない国は知りません！
            if token.surface not in country_dict:
                rep_text = f"私は{token.surface}を知りません"
                line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=rep_text))
                break
            else:
                rep_text = f"{token.surface}の首都は{country_dict[token.surface][0]}です"
                line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=rep_text))
                break

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host ='0.0.0.0',port = port)

    