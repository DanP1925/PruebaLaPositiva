from dblibrary import DbLibrary
from flask import Flask, request
from messenger import Messenger
import text

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def receive_message():
    messenger = Messenger()
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return messenger.verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                db_tools = DbLibrary() 
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    timestamp = message.get('timestamp')
                    messageText = message['message'].get('text')
                    if messageText:
                        if db_tools.isFirstTime(recipient_id):
                            messenger.send_message(recipient_id,text.firstTime)
                            db_tools.createNewAccount(recipient_id,timestamp)
                        else:
                            messenger.send_message(recipient_id,text.multipleTimes)

                        messenger.send_option_message(recipient_id,text.whatCanIDoForYou,
                            [text.findSong,text.displayMySongs,text.displayReport])
                        db_tools.storeMessage(recipient_id,messageText,timestamp)
                    if message['message'].get('attachments'):
                        messenger.send_message(recipient_id,text.onlyTextMessage)

                elif message.get('postback'):
                    recipient_id = message['sender']['id']
                    timestamp = message.get('timestamp')
                    option = message['postback'].get('title')
                    if option == text.findSong:
                        print("Buscar canciones")
                    elif option == text.displayMySongs:
                        print("Muestrame mis canciones")
                    db_tools.storeMessage(recipient_id,option,timestamp)
                db_tools.close()

    return "MessageProcessed"

if __name__ == '__main__':
    app.run()

