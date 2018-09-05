from flask import Flask, render_template, request, redirect, g
import sqlite3


conn = sqlite3.connect("todo.db")
cursor = conn.cursor()
username = 'dodo'
#cursor.execute("INSERT INTO user_list (name, tb) VALUES ('two', 'twotable') ")
# conn.commit()
# cursor.execute("""CREATE TABLE """ + username + """ (
#                 item text,
#                 status integer
#                 )"""
#               )

cursor.execute(""" INSERT INTO """ +username +""" (item, status) VALUES ('dodododo', 1) """)

cursor.execute("SELECT * FROM " + username)
print(cursor.fetchall())
# cursor.execute("DELETE FROM user_list WHERE name = 'two'")
# cursor.execute(""" INSERT INTO user_list ('one', 'onetable') """)
conn.commit()

conn.close()