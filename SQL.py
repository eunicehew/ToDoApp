from flask import Flask, render_template, request, redirect, g
import sqlite3


conn = sqlite3.connect("todo.db")
cursor = conn.cursor()
username = 'eunicehew'
#cursor.execute("INSERT INTO user_list (name, tb) VALUES ('two', 'twotable') ")
# conn.commit()
# cursor.execute("""CREATE TABLE """ + username + """ (
#                 item text,
#                 status integer
#                 )"""
#               )

cursor.execute(""" INSERT INTO """ +username +""" (item, status) VALUES ('dodododo', 0) """)

cursor.execute("SELECT * FROM " + username)
print(cursor.fetchall())
# cursor.execute("DELETE FROM user_list WHERE name = 'two'")
# cursor.execute(""" INSERT INTO user_list ('one', 'onetable') """)
conn.commit()

conn.close()


#  cursor.execute("""CREATE TABLE user_list(
#                 name varchar(20),
#                 tb varchar(20)
#                 )"""
#               )
#  cursor.execute("""CREATE TABLE todo_list(
#                 item varchar(20),
#                 status integer
#                 )"""
#               )
#   conn.commit()
