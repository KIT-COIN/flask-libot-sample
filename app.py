from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# import sentencepiece as spm

from SentensePiece import reply


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

line_bot_api = LineBotApi(app.config['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['CHANNEL_SECRET'])


@app.route("/")
def say_hello():
    return "Hello"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # sp = spm.SentencePieceProcessor()

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ここで文章生成
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text="メッセージありがとう！"))

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text="返信考え中！"))

    try:
        reply_text = reply()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text))
    except BaseException:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="返信失敗..."))
    finally:
        print("aaa")


if __name__ == "__main__":
    app.run()
