import mysql.connector
import logging
import time
from mysql.connector import Error


'''
db_connect(host, user, passwd, db) → connects to DB
check_db() → just to see if it's still connected to the DB, in case it is not reconnects
check_user(id) → check if user exists else it creates it
user_exists(id) → check if the user exists
create_user(id) → creates the user with a given id
number_of_headquarters(id) → return the number of headquarters for a give id
add_user_headquarter(id, code, name) → adds to the user a headquarter
rem_user_headquarter(id, code) → removes from the user a headquarter
get_user_headquarter(id) → get the list of headquarters for a given id
'''

mydb = ""
host, user, passwd, db = "","","",""


def db_connect(h, u, p, d):
    global mydb, host, user, passwd, db

    host, user, passwd, db = h, u, p, d
    retries = 5  # Number of times to retry connecting
    delay = 5  # Delay in seconds between retries

    for n in range(retries):
        try:
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=passwd,
                database=db
            )
            if mydb.is_connected():
                logging.debug('DB - db_connect - Successfully connected to the database')
                return mydb
        except Error as e:
            logging.debug('DB - db_connect - failed, retrying in ' + str(delay) + ' error: ' + str(e) )
        
        time.sleep(delay)

    logging.debug('DB - db_connect - Failed to connect to the database after multiple retries')
    return None


def check_db():
    try:
        mycursor = mydb.cursor()
        request = """SELECT id FROM userdata LIMIT 1"""
        mycursor.execute(request)
        mycursor.close()
    except Exception:
        db_connect(host, user, passwd, db)

def check_user(id):
    logging.debug('DB - check_user - Controllo utente')
    if user_exists(id):
        logging.debug('DB - check_user - Utente esiste')
        return True
    logging.debug('DB - check_user - Nuovo utente')
    create_user(id)
    return False


def user_exists(id):
    check_db()
    mycursor = mydb.cursor()
    request = """SELECT id FROM userdata WHERE id = (%s)"""
    val = [str(id)]
    mycursor.execute(request, val)
    res = mycursor.fetchall()
    mycursor.close()

    if not res:
        logging.debug('DB - user_exists - Utente non esiste - richiesta: ' + request)
        return False

    logging.debug('DB - user_exists - Utente esiste - richiesta: ' + request)
    return True


def create_user(id):
    check_db()
    mycursor = mydb.cursor()
    request = """INSERT INTO userdata (id) VALUES (%s)"""
    val = [str(id)]
    try:
        mycursor.execute(request, val)
        mydb.commit()
        mycursor.close()
    except Exception as e:
        logging.debug('DB - create_user - error: ' + str(e))
        return True
    res = abs(mycursor.rowcount)

    if res == 1:
        logging.debug('DB - create_user - Utente creato - richiesta: ' + request)
        return True

    logging.debug('DB - create_user - Utente NON creato - richiesta: ' + request)
    return False


def number_of_headquarters(id):
    check_db()
    mycursor = mydb.cursor()
    request = """SELECT id FROM headquarter WHERE id = """ + str(id)
    mycursor.execute(request)
    res = mycursor.fetchall()
    mycursor.close()

    if not res:
        logging.debug('DB - number_of_headquarters - Non ci sono sedi - richiesta: ' + request)
        return 0

    logging.debug('DB - number_of_headquarters - Ci sono ' + str(mycursor.rowcount) + ' sedi - richiesta: ' + request)
    return abs(mycursor.rowcount)


def add_user_headquarter(id, code, name):
    logging.debug("DB - add_user_headquarter - " + str(id) + " - " + str(code) + " - " + str(name))
    check_db()
    mycursor = mydb.cursor()
    request = """INSERT INTO headquarter (id, name_headquarter, code) VALUES (%s, %s, %s)"""
    val = [str(id), str(name), str(code)]
    try:
        mycursor.execute(request, val)
        mydb.commit()
        mycursor.close()
    except Exception as e:
        logging.debug('DB - add_user_headquarter - error: ' + str(e))
        return False

    res = abs(mycursor.rowcount)

    if res == 1:
        logging.debug('DB - add_user_headquarter - Sede aggiunta - richiesta: ' + request)
        return True

    logging.debug('DB - add_user_headquarter - Sede non aggiunta - richiesta: ' + request)
    return False


def rem_user_headquarter(id, code):
    check_db()
    mycursor = mydb.cursor()
    request = """DELETE FROM headquarter WHERE id = %s AND code = %s"""
    val = [str(id), str(code)]
    try:
        mycursor.execute(request, val)
        mydb.commit()
        mycursor.close()
    except Exception as e:
        logging.debug('DB - rem_user_headquarter - error: ' + str(e))
        return True

    res = abs(mycursor.rowcount)

    if abs(res) == 1:
        logging.debug('DB - rem_user_headquarter - Sede rimossa - richiesta: ' + request)
        return True

    logging.debug('DB - rem_user_headquarter - Sede non rimossa - richiesta: ' + request)
    return False


def get_user_headquarter(id):
    check_db()
    mycursor = mydb.cursor()
    request = """SELECT id, code, name_headquarter FROM headquarter WHERE id = """ + str(id)
    mycursor.execute(request)
    res = mycursor.fetchall()
    mycursor.close()

    logging.debug('DB - get_user_headquarter - Lista di sedi: ' + str(res) + ' - richiesta: ' + request)

    return res

def get_users():
    check_db()
    mycursor = mydb.cursor()
    request = """SELECT id FROM userdata"""
    mycursor.execute(request)
    res = mycursor.fetchall()
    mycursor.close()

    logging.debug('DB - get_user_headquarter - Lista di sedi: ' + str(res) + ' - richiesta: ' + request)

    return res