# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import requests

token = os.environ['TELEGRAM_TOKEN']
notes = str(os.environ['PRIVATE_NOTES'])
host = os.environ['URL_HOST']

# Commands Callback Function
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Avaiable command:\n/hello\n/p coin_name\n/cal amount coin_name\n/note\n/s moneyspend")

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
                '{}\nɃ {}\n$ {}\n% Change 1h : {}\n% Change 24h : {}'.format(name, btc, usd, oneH, twentyFourH))
        else:
            update.message.reply_text(
            '{}\nɃ {}\n$ {}\n% Change 1h : {}\n% Change 24h : {}'.format(r_json[0]['name'], r_json[0]['price_btc'], r_json[0]['price_usd']
                                                          ,r_json[0]['percent_change_1h'], r_json[0]['percent_change_24h']))
            
def calculate(bot, update):
    total_coin = str.lower(update.message.text[5:])
    total_coin = total_coin.split()
    coin = ''
    if len(total_coin) != 2:
        bot.send_message(chat_id=update.message.chat_id, text="Please use the right format (e.g /cal 10 eth, /cal 0.22 monero)")
        return
    while True:
        try:
            total = float(total_coin[0])
            coin = total_coin[1]
            break
        except ValueError:
            bot.send_message(chat_id=update.message.chat_id, text="Please use the right format (e.g /cal 10 eth, /cal 0.22 monero)")
            return
    r_json = request(coin)
    if r_json == 'error': # Error, try to check coin with symbol (Limited, only with top 100 coins)
        name, btc, usd, oneH, twentyFourH = find(str.upper(coin))
        if name == 'error':
            bot.send_message(chat_id=update.message.chat_id, text="Sorry, I can't find the coin you looking for")
        else:
            update.message.reply_text(
                'Ƀ {}\n$ {}'.format(total*float(btc), total*float(usd)))
    else:
        update.message.reply_text(
            'Ƀ {}\n$ {}'.format(total*float(r_json[0]['price_btc']), total*float(r_json[0]['price_usd'])))

def spend(bot, update):
    total_spend = 0
    while True:
        try:
            total_spend = int(update.message.text[3:])
            break
        except ValueError:
            bot.send_message(chat_id=update.message.chat_id, text="Please use the right format (e.g /s 2000)")
            return
        
    r = requests.post(host, data={'spend': total_spend})
    if r.status_code == 200:
        bot.send_message(chat_id=update.message.chat_id, text="Berhasil!")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Gagal!")
    
def priv_note(bot, update): # Private note
    update.message.reply_text('{}'.format(notes))
        
# Other Functions
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

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('p', price)) # /p eth
updater.dispatcher.add_handler(CommandHandler('cal', calculate)) # /cal 10 eth
updater.dispatcher.add_handler(CommandHandler('note', priv_note))
updater.dispatcher.add_handler(CommandHandler('s', spend))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle()

# ex post requests query
# requests.post("http://localhost/duidQ/bot.php", data={'duid': 1000})
