import sqlite3
import os
from aiogram.utils.markdown import hbold

def check_table():
    try:
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        # Создаем таблицу Users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER,
        username TEXT,
        money INTEGER,
        oblaka INTEGER,
        purchases INTEGER,
        admin INTEGER,
        discount INTEGER,
        referal INTEGER,
        server TEXT,
        price REAL,
        use_discount TEXT,
        inviting_user TEXT,
        user_invited TEXT
        )
        ''')
        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()
    except:
        print("Database: FAIL")

def add_new_user(id, username):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT telegram_id FROM users''')
    users = cursor.fetchall()
    for user in users:
        if id in user:
            connection.commit()
            connection.close()
            return f"Привет {hbold(username)}! Давно не виделись!"
    if str(id) in os.getenv("ADMIN_IDS"): admin = 1
    else: admin = 0
    cursor.execute('''INSERT INTO users (telegram_id, username, money, oblaka, purchases, admin, discount, 
    referal, server, price, use_discount, inviting_user, user_invited) 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (id, username, 0, 1, 0, admin, 0, 0, "no", 0, "no", "no", "no"))
    connection.commit()
    connection.close()
    return f"Привет {hbold(username)}! Приятно познакомиться!"

def user_info(id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM users WHERE telegram_id = {id}''')
    users = cursor.fetchall()
    connection.commit()
    connection.close()
    return list(users[0])

def add_discount_oblaka(id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET oblaka = 0, discount = 20 WHERE telegram_id = {id}')
    connection.commit()
    connection.close()

def server_choosing(text, price, server, id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET server = "{server}", price = {price}, use_discount = "{text}" '
                   f'WHERE telegram_id = {id}')
    connection.commit()
    connection.close()

def all_telegram_id():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM users''')
    users = cursor.fetchall()
    connection.commit()
    connection.close()
    return list(users)

def add_referal_to_user(inviting_user, id):
    inviting_user = inviting_user.replace("rf", "")
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f'''SELECT inviting_user FROM users WHERE telegram_id = {id}''')
    is_inviting_user = cursor.fetchall()
    if "no" in is_inviting_user[0]:
        cursor.execute(f'UPDATE users SET inviting_user = "{inviting_user}" WHERE telegram_id = {id}')
        connection.commit()
        connection.close()
        return f"Вы успешно активировали реферальный код! (rf{inviting_user})"
    else:
        connection.commit()
        connection.close()
        return f"Вы уже активировали реферальный код! (rf{inviting_user})"


def add_referal_discount(id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET referal = 10 WHERE telegram_id = {id}')
    connection.commit()
    connection.close()

def add_referal_discount_new_user(id, user_invite):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET user_invited = "{user_invite}" WHERE telegram_id = {id}')
    connection.commit()
    connection.close()