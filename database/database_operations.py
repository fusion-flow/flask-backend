# database_operations.py

import sqlite3

def connect_db():
    return sqlite3.connect('database/fusionFlow_db.db')

def get_cursor(conn):
    return conn.cursor()

def close_connection(conn):
    conn.close()

def select_data_by_intent(intents):
    conn = connect_db()
    cursor = get_cursor(conn)

    result_urls = {}

    for intent in intents:
        cursor.execute("SELECT url FROM urlMapping WHERE intent=?", (intent,))
        urls = cursor.fetchone()
        if(urls):
            result_urls[intent] = urls[0]

    close_connection(conn)
    return result_urls
