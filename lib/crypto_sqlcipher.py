#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtLoginRegistration
@ File        : crypto.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 将 sqlite3 替换为 pysqlcipher3,实现密码访问
                pysqlcipher3 实现密码访问 SQLite，需要手动安装
                安装看这里：https://www.cnblogs.com/yqbaowo/p/18043628
"""
from pysqlcipher3 import dbapi2 as sqlite3
import win32crypt


def crypto(password):
    encrypt = win32crypt.CryptProtectData(password.encode('utf-8'))
    return encrypt


def create_db(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA key='123456'")  # 密码=123456
    try:
        cursor.execute(f'''CREATE TABLE {db} (username text , password text)''')
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.close()


def insert_db(db, username, password):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA key='123456'")  # 密码=123456
    encrypt = crypto(password)
    cursor.execute(f"INSERT INTO {db}(username,password) VALUES(?,?)", (username, encrypt))
    conn.commit()
    conn.close()


def delete_db(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA key='123456'")  # 密码=123456
    cursor.execute(f"DELETE FROM {db}")
    conn.commit()
    conn.close()


def decrypt(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA key='123456'")  # 密码=123456
    cursor.execute(f"SELECT * FROM {db}")
    result = cursor.fetchall()[-1]
    username = result[0]
    password = win32crypt.CryptUnprotectData(result[1])[-1]
    password = password.decode('utf-8')
    return username, password


if __name__ == '__main__':
    db_ = 'test'
    create_db(db_)
    delete_db(db_)
    insert_db(db_, 'test', '111111')
    print(decrypt(db_))
