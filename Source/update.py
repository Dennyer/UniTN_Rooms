#!/usr/bin/env python3

# general purpose library
import os

# my code
import Database as DB
import API
from dictionary import default_text as DT

# telegram bot
import logging
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import Update

############################ Global variables ############################
keys = {}

############################ Main code ############################
def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    logging.info('Main - main - Caricamento chiavi')
    # load necessary API keys from file
    load_keys()
    logging.info('Main - main - Chiavi caricate')
    logging.info('Main - main - Connessione DB')
    DB.db_connect(keys["Host_db"], keys["User_db"], keys["Password_db"], keys["Database"])
    logging.info('Main - main - DB connesso')

    API.get_headquarters()

    # init
    updater = Updater(token=keys["Telegram_key"], use_context=True)
    dispatcher = updater.dispatcher

    # Commands handler
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('send_update_notification', update))

    # Messages handler
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(CallbackQueryHandler(query_handler))

    updater.start_polling()
    updater.idle()


# Loads API keys from "keys.cfg"
def load_keys():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "keys.cfg"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path) as myfile:
        for line in myfile:
            name, var = line.partition("=")[::2]
            keys[name.strip()] = var[:-1]
        myfile.close()

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

def update(update: Update, context: CallbackContext):
    logging.debug('Main - update - Notifica aggiornamento')
    users = DB.get_users()

    for user in users:
        context.bot.send_message(chat_id=user[0],
                             text=DT["update"] + update.message.text.replace("/send_update_notification ", "").capitalize())

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