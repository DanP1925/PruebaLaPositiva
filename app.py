from dblibrary import DbLibrary
from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Button
import text

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
                    timestamp = message['timestamp']
                    messageText = message['message'].get('text')
                    if messageText:
                        db_tools = DbLibrary() 
                        if db_tools.isFirstTime(recipient_id):
                            send_message(recipient_id,text.firstTime)
                            db_tools.createNewAccount(recipient_id,timestamp)
                        else:
                            send_message(recipient_id,text.multipleTimes)
                        send_option_message(recipient_id,text.whatCanIDoForYou,
                                            [text.findSong,
                                            text.displayMySongs,
                                            text.displayReport])
                        db_tools.storeMessage(recipient_id,messageText,timestamp)
                        db_tools.close()
                    if message['message'].get('attachments'):
                        send_message(recipient_id,text.onlyTextMessage)
                elif message.get('postback'):
                    option = message['postback'].get('title')
                    if option == text.findSong:
                        print("Buscar canciones")
                    elif option == text.displayMySongs:
                        print("Muestrame mis canciones")
    return "MessageProcessed"

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id,response)
    return "success"

def send_option_message(recipient_id, response, options):
    buttons = []
    for element in options:
        button = Button(title=element ,type='postback', payload='other')
        buttons.append(button)
    bot.send_button_message(recipient_id,response,buttons)
    return "success"

if __name__ == '__main__':
    app.run()

