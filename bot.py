# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler
import os

#           Config vars
token = os.environ['TELEGRAM_TOKEN']

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

updater = Updater(token)
updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
