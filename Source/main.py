#!/usr/bin/env python3

# general purpose library
import os
from datetime import date as data

# my code
import Keyboards as KEYBOARD
import Database as DB
import API
from dictionary import default_text as DT

# telegram bot
import logging
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ParseMode

import telegramcalendar

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
                             parse_mode="MarkdownV2",
                             disable_web_page_preview=True,
                             text=DT['start'],
                             reply_markup=ReplyKeyboardMarkup(
                                 keyboard=KEYBOARD.general_keyboard(),
                                 resize_keyboard=True
                                 # ,one_time_keyboard=True
                             ))


# Reply to user when "\help"
def help(update: Update, context: CallbackContext):
    logging.debug('Main - help - Aiuto')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             parse_mode="MarkdownV2",
                             disable_web_page_preview=True,
                             text=DT['help_text'],
                             reply_markup=ReplyKeyboardMarkup(
                                 keyboard=KEYBOARD.general_keyboard(),
                                 resize_keyboard=True
                                 # ,one_time_keyboard=True
                             ))


############################ Message handlers ############################
def message_handler(update: Update, context: CallbackContext):
    if DT["roomsButton"] in update.message.text:
        rooms(update, context, False)
    elif DT["scheduleButton"] in update.message.text:
        schedule(update, context, False)
    elif DT["settingsButton"] in update.message.text:
        settings(update, context, False)
    elif DT["helpButton"] in update.message.text:
        help(update, context)


def error(update: Update, context: CallbackContext):
    logging.debug('Main - error - Errore')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             parse_mode="MarkdownV2",
                             disable_web_page_preview=True,
                             text=DT['error'],
                             reply_markup=ReplyKeyboardMarkup(
                                 keyboard=KEYBOARD.general_keyboard(),
                                 resize_keyboard=True
                                 , one_time_keyboard=True
                             ))


def rooms(update: Update, context: CallbackContext, query):
    if query:
        id = update.callback_query.message.chat_id
    else:
        id = update.message.chat_id

    text = "Errore"
    reply_markup = KEYBOARD.error_keyboard()

    if DB.check_user(id):
        logging.debug('Main - rooms - Utente gia nel sistema')
        n = DB.number_of_headquarters(id)
        if n == 1:
            logging.debug('Main - rooms - Aule presenti')
            text = DT["selectOptions"]
            already_head = DB.get_user_headquarter(id)
            reply_markup = KEYBOARD.room_headquarter_keyboard(already_head[0][1], id)
        elif n > 1:
            logging.debug('Main - rooms - Aule presenti')
            text = DT['selectHeadquarter']
            reply_markup = KEYBOARD.headquarters_keyboard("sel", id)
        else:
            logging.debug('Main - rooms - Nessuna aula presente')
            text = DT['addHeadquarter']
            reply_markup = KEYBOARD.headquarters_keyboard("add1", id)
    else:
        logging.info('Main - rooms - Nuovo utente')
        text = DT['addHeadquarter']
        reply_markup = KEYBOARD.headquarters_keyboard("add1", id)

    if query:
        update.callback_query.message.edit_text(text,
                                                reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode="MarkdownV2",
                                 disable_web_page_preview=True,
                                 text=text,
                                 reply_markup=reply_markup)


def schedule(update: Update, context: CallbackContext):
    # TODO
    pass


def settings(update: Update, context: CallbackContext, query):
    logging.debug('Main - settings - Impostazioni')
    if query:
        update.callback_query.message.edit_text(text=DT["settings"],
                                                reply_markup=KEYBOARD.settings_keyboard())
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode="MarkdownV2",
                                 disable_web_page_preview=True,
                                 text=DT["settings"],
                                 reply_markup=KEYBOARD.settings_keyboard())


############################ Query handler ############################

def query_handler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    id = update.callback_query.message.chat_id

    logging.debug('Main - query_handler - Id: ' + str(id) + ' - query: ' + query)

    query_split = query.split(";")

    if query_split[0] == "err":
        pass

    elif query_split[0] == DT["roomsButton"]:
        rooms(update, context, True)

    elif query_split[0] == DT["scheduleButton"]:
        schedule(update, context, True)

    elif query_split[0] == DT["settingsButton"]:
        settings(update, context, True)

    elif query_split[0] == "settings":
        if query_split[1] == "headquarter":
            if query_split[2] == "add":
                if query_split[3] == "0":
                    update.callback_query.message.edit_text(DT['addHeadquarter'],
                                                            reply_markup=KEYBOARD.headquarters_keyboard("add", id))

                elif DB.add_user_headquarter(id, query_split[3], API.get_headquarter_name_by_code(query_split[3])):
                    update.callback_query.message.edit_text(DT["headquarterAdded"])

            elif query_split[2] == "rem":
                if query_split[3] == "0":
                    update.callback_query.message.edit_text(DT['remHeadquarter'],
                                                            reply_markup=KEYBOARD.headquarters_keyboard("rem", id))

                elif DB.rem_user_headquarter(id, query_split[3]):
                    update.callback_query.message.edit_text(DT["headquarterRemoved"])

            elif query_split[2] == "sel":
                update.callback_query.message.edit_text(DT["headquarterAddRem"],
                                                        reply_markup=KEYBOARD.settings_headquarter_keyboard())

    elif query_split[0] == "headquarter":
        if query_split[1] == "sel":
            update.callback_query.message.edit_text(DT["selectOptions"],
                                                    reply_markup=KEYBOARD.room_headquarter_keyboard(query_split[2], id))

        elif query_split[1] == "selpl":
            send_rooms_day(update.callback_query.message)

    elif query_split[0] == "date":
        if query_split[1] == "create":
            update.callback_query.message.edit_text(DT["selectDate"],
                                                    reply_markup=telegramcalendar.create_calendar(
                                                        "room;selroom;" + query_split[2] + ";" + query_split[3]))

        else:
            selected, date = telegramcalendar.process_calendar_selection(update, context,
                                                                         "room;selroom;" + query_split[2] + ";" +
                                                                         query_split[3])
            if selected:
                send_rooms_day(update, context, query_split[2], query_split[3], date)

    elif query_split[0] == "room":
        send_rooms_day(update, context, query_split[2], query_split[3])


def send_rooms_day(update: Update, context: CallbackContext, head, room, date="none"):
    if date == "none":
        date = data.today()

    events = API.get_headquarter_room_events(head, room, date)
    text = ""

    for k in events:
        text += "\n" + k + " | " + events[k]

    update.callback_query.message.edit_text(DT['viewResult'] + room + " il " + str(date.day) + "/" + str(date.month) + "/" + str(date.year) + ":" + text,
                                            reply_markup=KEYBOARD.date_room_hedquarter_keyboard(head, room))


############################ Main ############################

if __name__ == '__main__':
    main()
