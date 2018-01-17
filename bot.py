# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import requests

token = os.environ['TELEGRAM_TOKEN']
notes = str(os.environ['PRIVATE_NOTES'])

# Commands Callback Function
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Avaiable command:\n/hello\n/p coin_name\n/note")

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))
    
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Please use the available commands, use /start to see any available commands")

def price(bot, update):
    coin = str.lower(update.message.text[3:])
    if coin == '':
        bot.send_message(chat_id=update.message.chat_id, text="Please specifiy the coin name (e.g /p ethereum, /p xlm)")
    else:
        r_json = request(coin)
        if r_json == 'error': # Error, try to check coin with symbol (Limited, only with top 100 coins)
            name, btc, usd, oneH, twentyFourH = find(str.upper(coin))
            if name == 'error':
                bot.send_message(chat_id=update.message.chat_id, text="Sorry, I can't find the coin you looking for")
            else:
                update.message.reply_text(
                '{}\nBTC : {}\nUSD : {}\n% Change 1h : {}\n% Change 24h : {}'.format(name, btc, usd, oneH, twentyFourH))
        else:
            update.message.reply_text(
            '{}\nBTC : {}\nUSD : {}\n% Change 1h : {}\n% Change 24h : {}'.format(r_json[0]['name'], r_json[0]['price_btc'], r_json[0]['price_usd']
                                                          ,r_json[0]['percent_change_1h'], r_json[0]['percent_change_24h']))
            
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

def find(coin):
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=100').json()
    for i in range(0, 100):
        if coin == r[i]['symbol']:
            return r[i]['name'], r[i]['price_btc'], r[i]['price_usd'], r[i]['percent_change_1h'], r[i]['percent_change_24h']
    return 'error', 'error', 'error', 'error', 'error'
        
updater = Updater(token)

# Command
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('p', price))
updater.dispatcher.add_handler(CommandHandler('note', priv_note))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle()
