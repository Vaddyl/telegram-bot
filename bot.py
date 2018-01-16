# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import requests

token = os.environ['TELEGRAM_TOKEN']

# Commands Callback Function
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Avaiable command:\n/hello\n/price")

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))
    
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Please use the available command, use /start command to see any available command")

def price(bot, update):
    update.message.reply_text(
        '{}'.format('bitcoin')[0]['price_usd']))
        
# Other Function
def request(coin):
    url = 'https://api.coinmarketcap.com/v1/ticker/' + coin
    r = requests.get(url)
    while True:
        try:
            r.json()['error']
            return 'error'
        except TypeError:
            return r.json()

updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('price', price))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle()
