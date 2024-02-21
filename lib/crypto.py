#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration
@ File        : crypto.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import sqlite3

import win32crypt


def crypto(password):
    encrypt = win32crypt.CryptProtectData(password.encode('utf-8'))
    return encrypt


def create_db(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(f'''CREATE TABLE {db} (username text , password text)''')
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.close()


def insert_db(db, username, password):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    encrypt = crypto(password)
    cursor.execute(f"INSERT INTO {db}(username,password) VALUES(?,?)", (username, encrypt))
    conn.commit()
    conn.close()


def delete_db(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {db}")
    conn.commit()
    conn.close()


def decrypt(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {db}")
    result = cursor.fetchall()[-1]
    username = result[0]
    password = win32crypt.CryptUnprotectData(result[1])[-1]
    password = password.decode('utf-8')
    return username, password
