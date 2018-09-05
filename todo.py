from flask import Flask, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)

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
#conn.commit()


def dbConn():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE user_list(
                        name varchar(20),
                        tb varchar(20)
                        )"""
                    )
        conn.commit()
        print('Userlist Created')
    except sqlite3.Error as e:
        logging.error("SQL error encountered: " + e.args[0])
        print('Userlist Exists')
    return None

dbConn()

@app.before_request
def before_request():
    g.db = sqlite3.connect("todo.db")

@app.teardown_request
def teardown_request():
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    cursor = g.db.cursor()

    if request.method == 'POST':
        username = request.form['username']
        cursor.execute("SELECT * FROM user_list WHERE name = " + username)
        if(not cursor.fetchone()):
            #reroute to user
            return render_template ('/todo.html', username=username )
        else:
            cursor.execute(" INSERT INTO user_list (name, tb) VALUES (username, username)")
            g.db.commit()
            cursor.execute("""CREATE TABLE """ + username + """ (
                item text,
                status integer
                )"""
              )
            g.db.commit()
            #reroute to user
            return render_template ('/todo.html', username=username, data= )


    return render_template('signin.html')


@app.route('/remove-todo/<username>/<item_id>')
def removeTodo(username, item_id):
    cursor = g.db.cursor()

    data = {'item': item_id }
    cursor.execute("DELETE FROM "+ username + " WHERE item = " + item_id)
    return render_template('/todo.html', username=username)

@app.route('/update-todo/<username>/<item_id>/<status>', methods = ['POST'])
def updateTodo(username, item_id, status):
    cursor = g.db.cursor()
    cursor.execute("UPDATE " + username + " SET status = " + status + " WHERE item = " item_id)
    return render_template('/todo.html', username=username)



if __name__ == '__main__':
    app.run()



