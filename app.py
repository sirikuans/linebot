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
import oil_price

app = Flask(__name__)

line_bot_api = LineBotApi('zJpp5I1+RnkZ0hipU9suQMvxBEPis5aZyICsBI6aetecVdBOvXwDT17hsqaRjSxxM1+MBCzQVmyTZ6Sbzonq8plbtlg58gt1ebG34kSsXy8R0owIidmZPDs2BLNrRUSTH8eHZsZHs6+8JEVb5uTrqAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3b48e125e82f410a2a4a4945eeaffe41')

@app.route("/",methods=['GET'])
def default_action():
    return 'Hello World'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'ราคาน้ำมัน':
        l = oil_price.get_prices()
        s = ""
        for p in l:
            s += "%s %.2f บาท\n"%(p[0],p[1])

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=s))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text+'คะ'))

if __name__ == "__main__":
    app.run()