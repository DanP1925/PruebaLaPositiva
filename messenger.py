from flask import request
from pymessenger.bot import Bot
from pymessenger import Button

class Messenger:

    VERIFY_TOKEN = 'TESTINGTOKEN'
    ACCESS_TOKEN = 'EAAGXBJKgLyoBAOKdxLR391IqTyaKKJ7ZAxZAwrfuNgIr0OxhJywUnyIdaN3nSp4ZCmKLGi9ZAiiHTPzBW6ZAW2LIjgp1lK6qG0ZBrfx3vtBV7hbFd7ti8oA12potIB5o1hGqPW4V7ckeT8HNbxEs9Su2pZBbUZCYwuABP5O0XJuHmQZDZD'
    bot = Bot(ACCESS_TOKEN)

    def verify_fb_token(self,token_sent):
        if token_sent == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return 'Invalid verification token'

    def send_message(self,recipient_id,response):
        self.bot.send_text_message(recipient_id,response)
        return "success"

    def send_option_message(self,recipient_id,response,options):
        buttons = []
        for element in options:
            button = Button(title=element ,type='postback', payload='other')
            buttons.append(button)
        self.bot.send_button_message(recipient_id,response,buttons)
        return "success"
