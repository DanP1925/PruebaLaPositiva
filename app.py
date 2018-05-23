from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAGXBJKgLyoBAAQiWhtEQwbwYP2VsWXtpNZBg87vsPoB7U9VU6ZB0748kUbKyiGs4GbZCiQvTSE6exxEUJBjIRwtUZBSZAeiB06KJXAc3tyul1MsQRZAmoL9TCRO3ayo1tnka6ReS0GN60TlxEQWUSX7lkrPLYbiaWBbj707ajpwZDZD'
VERIFY_TOKEN = 'TESTINGTOKEN'
bot = Bot(ACCESS_TOKEN)

@app.route('/',methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = "Hello World B) !"
                        send_message(recipient_id,response_sent_text)
                    if message['message'].get('attachments'):
                        response_sent_nontext = "Hola Mundo :v !"
                        send_message(recipient_id, response_sent_nontext)
    return "MessageProcessed"

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id,response)
    return "success"

if __name__ == '__main__':
    app.run()

