# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import requests

token = os.environ['TELEGRAM_TOKEN']

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Avaiable command:\n/hello\n/price [coin]")

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))
    
def uknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Please use the available command, use /start command to see any available command")
    
def request(coin):
    def req():
    url = 'https://api.coinmarketcap.com/v1/ticker/' + coi 
    r = requests.get(url)
    while True:
        try:
            r.json()['error']
            return 'error'
        except TypeError:
            return r.json()

updater = Updater(token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(MessageHandler(Filters.command, uknown))

updater.start_polling()
updater.idle()
