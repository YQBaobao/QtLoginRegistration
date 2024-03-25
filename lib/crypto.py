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


def create_db(db, table):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(f'CREATE TABLE {table} (username text , password text)')
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.close()


def insert_db(db, table, username, password):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    encrypt = crypto(password)
    cursor.execute(f"INSERT INTO {table}(username,password) VALUES(?,?)", (username, encrypt))
    conn.commit()
    conn.close()


def delete_db(db, table):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table}")
    conn.commit()
    conn.close()


def decrypt(db, table):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    result = cursor.fetchall()[-1]
    username = result[0]
    password = win32crypt.CryptUnprotectData(result[1])[-1]
    password = password.decode('utf-8')
    return username, password


if __name__ == '__main__':
    db_ = 'test1.db'
    table_ = 'test'
    create_db(db_, table_)
    delete_db(db_, table_)
    insert_db(db_, table_, 'test', '111111')
    print(decrypt(db_, table_))
