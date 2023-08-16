import datetime
from datetime import date as data

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

import API
import Database as DB
from dictionary import default_text as DT


def general_keyboard():
    keyboard = [[KeyboardButton(DT["roomsButton"])],
                [KeyboardButton(DT["settingsButton"]), KeyboardButton(DT["helpButton"])]]

    '''keyboard = [[KeyboardButton(DT["roomsButton"]), KeyboardButton(DT["scheduleButton"])],
                [KeyboardButton(DT["settingsButton"]), KeyboardButton(DT["helpButton"])]]'''

    return keyboard


def error_keyboard():
    keyboard = [[InlineKeyboardButton(DT["error"], callback_data="err;err")]]
    return InlineKeyboardMarkup(keyboard)


def headquarters_keyboard(action, id):
    keyboard = []

    if action == "add" or action == "add1":
        headquarter = API.get_headquarters()
        already_head = DB.get_user_headquarter(id)

        for h in headquarter:
            head = ""
            code = ""

            skip = True

            for key, value in h.items():
                for ah in already_head:
                    if key == "valore" and ah[1] == value:
                        skip = False

                if skip:
                    if key == "label":
                        head = value
                    elif key == "valore":
                        code = "settings;headquarter;add;" + value
            if skip:
                keyboard.append([InlineKeyboardButton(head, callback_data=code)])

        if action == 'add':
            keyboard.append([InlineKeyboardButton(DT["backButton"], callback_data="settings;headquarter;sel")])

    elif action == "rem":
        headquarter = DB.get_user_headquarter(id)
        for h in headquarter:
            head = h[2]
            code = "settings;headquarter;rem;" + h[1]

            keyboard.append([InlineKeyboardButton(head, callback_data=code)])

        keyboard.append([InlineKeyboardButton(DT["backButton"], callback_data="settings;headquarter;sel")])

    elif action == "sel":
        headquarter = DB.get_user_headquarter(id)
        for h in headquarter:
            head = h[2]
            code = "headquarter;" + action + ";" + h[1]

            keyboard.append([InlineKeyboardButton(head, callback_data=code)])

    return InlineKeyboardMarkup(keyboard)


def settings_keyboard():
    keyboard = [[InlineKeyboardButton(DT["headquarterButton"], callback_data="settings;headquarter;sel")]]
    return InlineKeyboardMarkup(keyboard)


def settings_headquarter_keyboard():
    keyboard = [[InlineKeyboardButton(DT["addButton"], callback_data="settings;headquarter;add;0")],
                [InlineKeyboardButton(DT["removeButton"], callback_data="settings;headquarter;rem;0")],
                [InlineKeyboardButton(DT["backButton"], callback_data=DT["settingsButton"])]]
    return InlineKeyboardMarkup(keyboard)


def room_headquarter_keyboard(code, id):
    rooms, busy_rooms = API.get_headquarter_busy_rooms(code, data.today().strftime("%d-%m-%Y"),
                                                       datetime.datetime.now())
    keyboard = []
    cont = 0
    temp = []

    for r in rooms:
        if r in busy_rooms:
            temp.append(InlineKeyboardButton("❌" + r, callback_data="room;selroom;" + code + ";" + r))
        else:
            temp.append(InlineKeyboardButton("✅" + r, callback_data="room;selroom;" + code + ";" + r))

        cont += 1

        if cont == 3:
            cont = 0
            keyboard.append(temp)
            temp = []

    n = DB.number_of_headquarters(id)
    if n > 1:
        if temp != []:
            temp.append(InlineKeyboardButton(DT["backButton"], callback_data=DT["roomsButton"]))
            keyboard.append(temp)
        else:
            keyboard.append([InlineKeyboardButton(DT["backButton"], callback_data=DT["roomsButton"])])
    else:
        if temp != []:
            keyboard.append(temp)

    return InlineKeyboardMarkup(keyboard)


def date_room_hedquarter_keyboard(code, room):
    keyboard = [[InlineKeyboardButton(DT["backButton"], callback_data="headquarter;sel;"+code), InlineKeyboardButton(DT["dateButton"], callback_data="date;create;" + str(code) + ";" + str(room))]]
    return InlineKeyboardMarkup(keyboard)

def back_keyboard(prev):
    keyboard = [[InlineKeyboardButton(DT["backButton"], callback_data=prev)]]
    return InlineKeyboardMarkup(keyboard)
