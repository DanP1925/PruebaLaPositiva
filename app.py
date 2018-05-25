from dblibrary import DbLibrary
from flask import Flask, request
from messenger import Messenger
from musixmatch import MusixMatch
import const
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
                musixmatch = MusixMatch()

                if message.get('message'):
                    recipient_id = message['sender']['id']
                    timestamp = message.get('timestamp')
                    messageText = message['message'].get('text')
                    db_tools.storeMessage(recipient_id,messageText,timestamp)
                    if messageText:
                        if db_tools.isFirstTime(recipient_id):
                            firstTimeVisitor(db_tools,messenger,
                                            recipient_id,timestamp)
                        else:
                            current_state = db_tools.getConversationState(recipient_id)
                            if (current_state == const.findSong):
                                askHowToFind(db_tools,messenger,recipient_id)
                            elif (current_state == const.displayReport):
                                askWhichReport(db_tools,messenger,recipient_id)
                            elif (current_state == const.byAuthor):
                                title, track_id = musixmatch.getSongWithAuthor(messageText)
                                foundSong(db_tools,messenger,musixmatch,
                                        recipient_id,title,track_id)
                            elif (current_state == const.byTitle):
                                title, track_id = musixmatch.getSongWithTitle(messageText)
                                foundSong(db_tools,messenger,musixmatch,
                                        recipient_id,title,track_id)
                            elif (current_state == const.byLyric):
                                title, track_id = musixmatch.getSongWithLyrics(messageText)
                                foundSong(db_tools,messenger,musixmatch,
                                        recipient_id,title,track_id)
                            elif (current_state == const.showMySongs):
                                print("wp")
                            else:
                                returningVisitor(messenger,recipient_id)

                    if message['message'].get('attachments'):
                        messenger.send_message(recipient_id,text.onlyTextMessage)

                elif message.get('postback'):
                    recipient_id = message['sender']['id']
                    timestamp = message.get('timestamp')
                    option = message['postback'].get('title')
                    db_tools.storeMessage(recipient_id,option,timestamp)
                    updateState(db_tools,recipient_id,option)
                    current_state = db_tools.getConversationState(recipient_id)
                    if (current_state == const.findSong):
                        askHowToFind(db_tools,messenger,recipient_id)
                    elif (current_state == const.displayReport):
                        askWhichReport(db_tools,messenger,recipient_id)
                    elif (current_state == const.byAuthor):
                        messenger.send_message(recipient_id,text.inputWords)
                    elif (current_state == const.byTitle):
                        messenger.send_message(recipient_id,text.inputWords)
                    elif (current_state == const.byLyric):
                        messenger.send_message(recipient_id,text.inputWords)
                    elif (current_state == const.showMySongs):
                        print("wp")
                    elif (current_state == const.personsReport):
                        getNumberOfUsers(db_tools,messenger,recipient_id)
                    elif (current_state == const.chatsReport):
                        print("chat")
                    elif (current_state == const.songReport):
                        print("song")


                db_tools.close()
    return "MessageProcessed"

def firstTimeVisitor(db_tools,messenger,recipient_id, timestamp):
    messenger.send_message(recipient_id,text.firstTime)
    db_tools.createNewAccount(recipient_id,timestamp)
    messenger.send_option_message(recipient_id,text.whatCanIDoForYou,
        [text.findSong,text.displayMySongs,text.displayReport])

def askHowToFind(db_tools,messenger,recipient_id):
    messenger.send_option_message(recipient_id,text.howToFind,
        [text.byAuthor,text.byTitle,text.byLyric])
    db_tools.updateConversationState(recipient_id,const.howToFind)

def foundSong(db_tools,messenger, musixmatch, recipient_id, title, track_id):
    if title is not None:
        messenger.send_message(recipient_id,text.foundSong)
        messenger.send_message(recipient_id,title)
        lyrics = musixmatch.getLyricsWithSong(track_id)
        if lyrics is not None:
            messenger.send_message(recipient_id,text.foundLyrics)
            messenger.send_message(recipient_id,lyrics)
        else:
            messenger.send_message(recipient_id,text.noLyrics)
    else:
        messenger.send_message(recipient_id,text.noSong)
    db_tools.updateConversationState(recipient_id,const.greeting)

def returningVisitor(messenger,recipient_id):
    messenger.send_message(recipient_id,text.multipleTimes)
    messenger.send_option_message(recipient_id,text.whatCanIDoForYou,
        [text.findSong,text.displayMySongs,text.displayReport])

def askWhichReport(db_tools,messenger,recipient_id):
    messenger.send_option_message(recipient_id,text.whichReport,
        [text.personsReport,text.chatsReport,text.songsReport])

def updateState(db_tools,recipient_id,option):
    if option == text.findSong:
        db_tools.updateConversationState(recipient_id,const.findSong)
    elif option == text.displayMySongs:
        db_tools.updateConversationState(recipient_id,const.showMySongs)
    elif option == text.displayReport:
        db_tools.updateConversationState(recipient_id,const.displayReport)
    elif option == text.byAuthor:
        db_tools.updateConversationState(recipient_id,const.byAuthor)
    elif option == text.byTitle:
        db_tools.updateConversationState(recipient_id,const.byTitle)
    elif option == text.byLyric:
        db_tools.updateConversationState(recipient_id,const.byLyric)
    elif option == text.personsReport:
        db_tools.updateConversationState(recipient_id,const.personsReport)
    elif option == text.chatsReport:
        db_tools.updateConversationState(recipient_id,const.chatsReport)
    elif option == text.songsReport:
        db_tools.updateConversationState(recipient_id,const.songsReport)

def getNumberOfUsers(db_tools,messenger,recipient_id):
    numberOfUser = db_tools.getNumberOfUsers()
    messenger.send_message(recipient_id,text.resultPersonsReport + 
                            str(numberOfUser) + text.resultPersonsReport2)
    db_tools.updateConversationState(recipient_id,const.resultPersonsReport)

if __name__ == '__main__':
    app.run()

