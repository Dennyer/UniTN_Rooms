#!/usr/bin/env python3

# my code
from dictionary import default_text as DT

# telegram bot
import logging
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import Update

import os

############################ Global variables ############################
keys = {}


############################ Main code ############################
def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    logging.info('Main - main - Caricamento chiavi')
    # load necessary API keys from file
    load_keys()
    logging.info('Main - main - Chiavi caricate')

    # init
    updater = Updater(token=keys["Telegram_key"], use_context=True)
    dispatcher = updater.dispatcher

    # Commands handler
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))

    # Messages handler
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(CallbackQueryHandler(query_handler))

    updater.start_polling()
    updater.idle()


# Loads API keys from "env"
def load_keys():
    keys['Telegram_key'] = os.environ.get('Telegram_key')
    keys['Host_db'] = os.environ.get('Host_db')
    keys['User_db'] = os.environ.get('User_db')
    keys['Password_db'] = os.environ.get('Password_db')
    keys['Database'] = os.environ.get('Database')


############################ Command handlers ############################

# Reply to user when "\start"
def start(update: Update, context: CallbackContext):
    logging.debug('Main - start - Start')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=DT['maintenance'])


# Reply to user when "\help"
def help(update: Update, context: CallbackContext):
    logging.debug('Main - help - Aiuto')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=DT['maintenance'])


############################ Message handlers ############################

def message_handler(update: Update, context: CallbackContext):
    maintenance(update, context)


def maintenance(update: Update, context: CallbackContext):
    logging.debug('Main - maintenance - Manutenzione')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=DT['maintenance'])

############################ Query handler ############################

def query_handler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    id = update.callback_query.message.chat_id

    logging.debug('Main - query_handler - Id: ' + str(id) + ' - query: ' + query)
    maintenance(update, context)

############################ Main ############################

if __name__ == '__main__':
    main()
