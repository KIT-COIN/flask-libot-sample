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

# from SentensePiece import reply


line_bot_api = LineBotApi(
    'BBRbzcN0GjBelHIlfA0QkwsCGqN5kNVJcH9m5kEO//OPT74Ml0i5YAjHeEWUHU1HmAUfsJ/7bn6mQ1v1yQQSTIkZBnCdDDTrCrpqV3jORXuEy2oiPUXsLSbgjd6LHz1kdFnvcJxIWbpj0qrrlXewiwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('21a4d78b5cd16fe7b22580095a364185')

app = Flask(__name__)


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

    # text = reply()

    # print(text)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
