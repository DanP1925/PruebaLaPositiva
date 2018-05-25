from flask import request
from pymessenger.bot import Bot
from pymessenger import Button

class Messenger:

    VERIFY_TOKEN = 'TESTINGTOKEN'
    ACCESS_TOKEN = 'EAAGXBJKgLyoBAAQiWhtEQwbwYP2VsWXtpNZBg87vsPoB7U9VU6ZB0748kUbKyiGs4GbZCiQvTSE6exxEUJBjIRwtUZBSZAeiB06KJXAc3tyul1MsQRZAmoL9TCRO3ayo1tnka6ReS0GN60TlxEQWUSX7lkrPLYbiaWBbj707ajpwZDZD'
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
