# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import requests

token = os.environ['TELEGRAM_TOKEN']
notes = os.environ['PRIVATE_NOTES']

# Commands Callback Function
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Avaiable command:\n/hello\n/price coin_name\n/note")

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))
    
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Please use the available commands, use /start to see any available commands")

def price(bot, update):
    coin = update.message.text[7:]
    if coin == '':
        update.message.reply_text(
            '{}'.format(request('bitcoin')[0]['price_usd']))
    else:
        r_json = request(coin)
        if r_json == 'error':
            bot.send_message(chat_id=update.message.chat_id, text="Sorry, I can't find the coin you looking for")
        else:
            '{}\nBTC {}\nUSD {}'.format(coin, r_json[0]['price_btc'], r_json[0]['price_usd']))
            
def priv_note(bot, update):
    update.message.reply_text(
        '{}'.format(notes))
        
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
updater.dispatcher.add_handler(CommandHandler('note', priv_note))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle()
