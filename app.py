from dblibrary import DbLibrary
from flask import Flask, request
from messenger import Messenger
from musixmatch import MusixMatch
import const
from datetime import datetime
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
                            # Search Song
                            if (current_state == const.findSong):
                                askHowToFind(db_tools,messenger,recipient_id)
                            elif (current_state == const.byAuthor):
                                title, author, track_id = musixmatch.getSongWithAuthor(messageText)
                                foundSong(db_tools,messenger,musixmatch,
                                        recipient_id,title,author,track_id,timestamp)
                                messenger.send_option_message(recipient_id,text.addFavorites,
                                        [text.yes,text.no])
                                db_tools.updateConversationState(recipient_id,const.addFavorite)
                            elif (current_state == const.byTitle):
                                title, author, track_id = musixmatch.getSongWithTitle(messageText)
                                foundSong(db_tools,messenger,musixmatch,
                                        recipient_id,title,author,track_id,timestamp)
                                messenger.send_option_message(recipient_id,text.addFavorites,
                                        [text.yes,text.no])
                                db_tools.updateConversationState(recipient_id,const.addFavorite)
                            elif (current_state == const.byLyric):
                                title, author, track_id = musixmatch.getSongWithLyrics(messageText)
                                foundSong(db_tools,messenger,musixmatch,
                                        recipient_id,title,author,track_id,timestamp)
                                messenger.send_option_message(recipient_id,text.addFavorites,
                                        [text.yes,text.no])
                                db_tools.updateConversationState(recipient_id,const.addFavorite)
                            # My Songs
                            elif (current_state == const.showMySongs):
                                showSongs(db_tools,messenger,recipient_id)
                            # Reports
                            elif (current_state == const.displayReport):
                                askWhichReport(db_tools,messenger,recipient_id)
                            #Other
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
                    # Search Songs
                    if (current_state == const.findSong):
                        askHowToFind(db_tools,messenger,recipient_id)
                    elif (current_state == const.byAuthor):
                        messenger.send_message(recipient_id,text.inputWords)
                    elif (current_state == const.byTitle):
                        messenger.send_message(recipient_id,text.inputWords)
                    elif (current_state == const.byLyric):
                        messenger.send_message(recipient_id,text.inputWords)
                    elif (current_state == const.yes):
                        db_tools.updateFavoriteSong(recipient_id)
                        messenger.send_message(recipient_id,"Listo")
                        db_tools.updateConversationState(recipient_id,const.greeting)
                    elif (current_state == const.no):
                        messenger.send_message(recipient_id,"Para la proxima sera :)")
                        db_tools.updateConversationState(recipient_id,const.greeting)
                        
                    # My Songs
                    elif (current_state == const.showMySongs):
                        showSongs(db_tools,messenger,recipient_id)
                    # Reports
                    elif (current_state == const.displayReport):
                        askWhichReport(db_tools,messenger,recipient_id)
                    elif (current_state == const.personsReport):
                        getNumberOfUsers(db_tools,messenger,recipient_id)
                    elif (current_state == const.chatsReport):
                        getChatsPerDay(db_tools,messenger,recipient_id)
                    elif (current_state == const.songReport):
                        getTopSongs(db_tools,messenger,recipient_id)


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

def foundSong(db_tools,messenger, musixmatch, recipient_id, title, author, track_id,timestamp):
    if title is not None:
        messenger.send_message(recipient_id,text.foundSong)
        messenger.send_message(recipient_id,title + ' ' + author)
        db_tools.storeSong(title,author,track_id,recipient_id,timestamp)
        lyrics = musixmatch.getLyricsWithSong(track_id)
        if lyrics is not None:
            messenger.send_message(recipient_id,text.foundLyrics)
            messenger.send_message(recipient_id,lyrics)
        else:
            messenger.send_message(recipient_id,text.noLyrics)
    else:
        messenger.send_message(recipient_id,text.noSong)

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
        db_tools.updateConversationState(recipient_id,const.songReport)
    elif option == text.yes:
        db_tools.updateConversationState(recipient_id,const.yes)
    elif option == text.no:
        db_tools.updateConversationState(recipient_id,const.no)

def getNumberOfUsers(db_tools,messenger,recipient_id):
    numberOfUser = db_tools.getNumberOfUsers()
    messenger.send_message(recipient_id,text.resultPersonsReport + 
                            str(numberOfUser) + text.resultPersonsReport2)
    db_tools.updateConversationState(recipient_id,const.greeting)

def getChatsPerDay(db_tools,messenger,recipient_id):
    topChats = db_tools.getMessageNumberPerDay()
    for chat in topChats:
        messenger.send_message(recipient_id, text.resultChatReport + str(datetime.date(chat[1]))
                                + text.resultChatReport2 + str(chat[0]) + text.resultChatReport3)
    db_tools.updateConversationState(recipient_id,const.greeting)

def showSongs(db_tools,messenger,recipient_id):
    mySongs = db_tools.getMyTopSongs(recipient_id)
    i = 1
    for song in mySongs:
        fullMessage = str(i) + ". " + song[1] + "-" + song[2]
        messenger.send_message(recipient_id,fullMessage) 
        i+=1
    db_tools.updateConversationState(recipient_id,const.greeting)

def getTopSongs(db_tools,messenger,recipient_id):
    topSongs = db_tools.getTopSongs()
    i = 1
    for song in topSongs:
        fullMessage = str(i) + ". " + song[1] + "-" + song[2]
        messenger.send_message(recipient_id,fullMessage) 
        i+=1
    db_tools.updateConversationState(recipient_id,const.greeting)

if __name__ == '__main__':
    app.run()

