import datetime
import logging
import requests
import collections
import json
from datetime import date as data
from dictionary import default_text as DT

'''
get_headquarters() → returns the headquarters and updates after 12h
get_headquarters_data() → fetches the headquarters and updates it
get_headquarters_rooms() → returns the headquarters from online
get_headquarter_name_by_code(code) → return the name of the headquarter with a given code
get_headquarter_info(code, date) → returns json formatted response from easyroom
get_headquarter_rooms(code, date, info="none") → return the list of rooms for a given headquarter
get_headquarter_events(code, date, info="none") → returns the list of events for a given headquarter in a given day
get_headquarter_times(info) → return the list of times (30 min intervals) from 7:30 to 24:00
get_headquarter_busy_rooms(code, date=data.today().strftime("%d-%m-%Y"), time="none", info="none") → return a list of rooms and busy rooms in a given time of a given day
get_headquarter_room_events(code, room, date=data.today(), info="none") → return the text for the message with listed the activities of a room in a given day
'''

headquarters = {}
last_update_time = None
headquarter_info_cache = {}


def get_headquarters():
    global headquarters, last_update_time

    if not headquarters or (datetime.datetime.now() - last_update_time).total_seconds() > 43200:
        # Fetch new data and update the timestamp
        headquarters = get_headquarters_data()
        last_update_time = datetime.datetime.now()

    return headquarters


def get_headquarters_data():
    
    headquarters = get_headquarters_rooms()[0]
    # headquarters = """{ "headquarters": """ + headquarters + "}"
    try:
        headquarters = json.loads(headquarters)
        logging.info("API - get_headquarters_data - Headquarters aggiornato")
    except:
        logging.info("API - get_headquarters_data - Errore headquarters")
        return (DT["error"])

    return headquarters


def get_headquarters_rooms():
    url = "https://easyacademy.unitn.it/AgendaStudentiUnitn/combo.php?sw=rooms_"
    try:
        response = requests.post(url)
    except:
        return False
    if response.status_code == 200:
        response_text = response.text

        textToDelete = ["var elenco_sedi = ", "var elenco_tipi = ", "var elenco_raggruppamenti_prenotazioni = ",
                        "var elenco_raggruppamenti = "]
        # response_text = response_text.replace('{', '[')
        # response_text = response_text.replace('}', ']')
        response_text = response_text.replace(';', '')
        response_text = response_text.replace(textToDelete[0], "")
        response_text = response_text.replace(textToDelete[1], "")
        response_text = response_text.replace(textToDelete[2], "")
        response_text = response_text.replace(textToDelete[3], "")
        # response_text = response_text.replace('\n', '')
        response_text = response_text.replace('\r', '')
        # response_text = response_text + "}"

        response_text = response_text.split("\n")
        response_text = [value for value in response_text if value != '']

        return response_text
    return False


def get_headquarter_name_by_code(code):
    headquarter = get_headquarters()

    for h in headquarter:
        head = ""
        for key, value in h.items():
            if key == "label":
                head = value
            elif key == "valore":
                if code == value:
                    logging.debug("API - get_headquarter_name_by_code - " + str(head))
                    return head

    logging.info("API - get_headquarter_name_by_code - False")

    return False


def get_headquarter_info(code, date_val=data.today().strftime("%d-%m-%Y")):
    global headquarter_info_cache

    # If it's in the cache for less than 6 h return it
    if (code in headquarter_info_cache and date_val in headquarter_info_cache[code] and
        (datetime.datetime.now() - headquarter_info_cache[code][date_val]['timestamp']).total_seconds() < 21600):
        
        logging.debug("API - get_headquarter_info - Local fetch for code: " + code + " and day: " + str(date_val))
        return headquarter_info_cache[code][date_val]['data']

    cleanup_old_cache_entries()

    fetched_data = get_headquarter_info_from_source(code, date_val)
    if not code in headquarter_info_cache:
        headquarter_info_cache[code] = {}
    headquarter_info_cache[code][date_val] = {
        'timestamp': datetime.datetime.now(),
        'data': fetched_data
    }
    logging.info("API - get_headquarter_info - Online fetch for code: " + code + " and day: " + str(date_val))

    return fetched_data

def get_headquarter_info_from_source(code, date_val):
    data = {
        "form-type": "rooms",
        "sede": code,
        "date": date_val,
        "_lang": "it"
    }

    url = "https://easyacademy.unitn.it/AgendaStudentiUnitn/rooms_call.php"

    response = requests.post(url, data)

    ris = response.json()
    return ris

def cleanup_old_cache_entries():
    global headquarter_info_cache
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)

    for code in list(headquarter_info_cache.keys()):
        for date_val in list(headquarter_info_cache[code].keys()):
            if headquarter_info_cache[code][date_val]['timestamp'] < one_week_ago:
                del headquarter_info_cache[code][date_val]
        # If no dates are left for a code, remove the code entry as well
        if not headquarter_info_cache[code]:
            del headquarter_info_cache[code]


def get_headquarter_rooms(code, date=data.today().strftime("%d-%m-%Y"), info="none"):
    if info == "none":
        area_rooms = get_headquarter_info(code, date)["area_rooms"]
    else:
        area_rooms = info["area_rooms"]
    rooms = area_rooms[code]
    rooms_name = []

    for key in rooms:
        if "/" in key:
            (headquarter, name) = key.split("/")
            if headquarter == code:
                rooms_name.append(name)

    rooms_name.sort()
    return rooms_name


def get_headquarter_events(code, date=data.today().strftime("%d-%m-%Y"), info="none"):
    if info == "none":
        events = get_headquarter_info(code, date)["events"]
    else:
        events = info["events"]

    return events


def get_headquarter_times(info):
    return info["fasce"]


def get_headquarter_busy_rooms(code, date=data.today().strftime("%d-%m-%Y"), time="none", info="none"):
    if info == "none":
        info_local = get_headquarter_info(code, date)
    else:
        info_local = info

    if time == "none":
        time = datetime.datetime.now()

    rooms = get_headquarter_rooms(code, date, info_local)
    events = get_headquarter_events(code, date, info_local)

    busy_rooms = []

    for e in events:
        if e["CodiceSede"] == code:
            ymd = e["Giorno"].split("-")
            hms_start = e["from"].split(":")
            hms_stop = e["to"].split(":")
            time_start = datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]), int(hms_start[0]), int(hms_start[1]))
            time_stop = datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]), int(hms_stop[0]), int(hms_stop[1]))

            if time.time() >= time_start.time() and time.time() <= time_stop.time():
                try:
                    busy_rooms.append(e["CodiceAula"].split("/")[1])
                except Exception:
                    pass

    busy_rooms.sort()

    return rooms, busy_rooms


def get_headquarter_room_events(code, room, date=data.today(), info="none"):
    if info == "none":
        info_local = get_headquarter_info(code, date.strftime("%d-%m-%Y"))
    else:
        info_local = info

    events = get_headquarter_events(code, date, info_local)
    times = get_headquarter_times(info_local)

    room_events = []
    room_times_events = {time["label"]: "Vuoto" for time in times}

    for e in events:
        if e["CodiceSede"] == code and e["CodiceAula"] == str(code + "/" + room):
            room_events.append(e)

    for e in room_events:
        ymd = e["Giorno"].split("-")
        hms_start = e["from"].split(":")
        hms_stop = e["to"].split(":")
        time_event_start = datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]), int(hms_start[0]),
                                             int(hms_start[1]))
        time_event_stop = datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]), int(hms_stop[0]), int(hms_stop[1]))

        (fromH, fromM, _) = e["from"].split(":")
        (toH, toM, _) = e["to"].split(":")

        room_times_events[fromH + ":" + fromM + " - " + toH + ":" + toM] = e["name"]

        for t in times:
            if t["valore"] <= 31:
                (h, m) = t["label"].split(":")
                h = int(h)
                m = int(m)
                if m == 30 and h < 23:
                    h_end = h + 1
                    m_end = 0
                elif m == 0 and h < 23:
                    h_end = h
                    m_end = 30

                time_period_start = datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]), int(h), int(m))
                time_period_stop = datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]), int(h_end), int(m_end))

                if time_period_start.time() >= time_event_start.time() and time_period_stop.time() <= time_event_stop.time():
                    if t["label"] in room_times_events:
                        del room_times_events[t["label"]] 

    room_times_events = collections.OrderedDict(sorted(room_times_events.items()))
    inizio, fine = "", ""
    room_times_events_ordered = {}

    for r in room_times_events:
        if(room_times_events[r] == "Vuoto"):
            if(inizio == ""):
                inizio = r
            else:
                try:
                    fine = (list(room_times_events)[(list(room_times_events.keys()).index(r)) +1]).split(" - ")[0]
                except (ValueError, IndexError):
                    fine = r
        else:
            if(inizio != ""):
                room_times_events_ordered[inizio + " - " + fine] = "Vuoto"
            room_times_events_ordered[r] = room_times_events[r]
            inizio,fine = "", ""

    if(inizio != ""):
        room_times_events_ordered[inizio + " - " + fine] = "Vuoto"
    #room_times_events_ordered = collections.OrderedDict(sorted(room_times_events.items()))

    return room_times_events_ordered

