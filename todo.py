from flask import Flask, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)

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

#dbConn()

@app.before_request
def before_request():
    g.db = sqlite3.connect("todo.db")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def login():
    cursor = g.db.cursor()
    if request.method == 'POST':
        username = request.form['username']
        try:
            cursor.execute("SELECT * FROM " + username)
            g.db.commit()
            data = cursor.fetchall()
            print(data)
            return render_template ('/todo.html', username=username, data = data)
        except:
            cursor.execute("INSERT INTO user_list (name, tb) VALUES ('" + username+"', '"+username+"')")
            g.db.commit()
            cursor.execute("""CREATE TABLE IF NOT EXISTS """ + username + """ (
                item text,
                status integer
                )"""
            )
            g.db.commit()
            data=cursor.fetchall() 
            return render_template ('/todo.html', username=username, data = data)
    return render_template('signin.html')


@app.route('/todo', methods=['GET', 'POST'])
def todo():    #how to make for specific user and table????
    cursor = g.db.cursor()
    username = request.form['username']
    itemId = request.form['add']
    cursor = g.db.cursor()
    g.db.row_factory = sqlite3.Row
    g.db.commit()
    todolist = g.db.row_factory

    # todolist = dict(zip(item, status))
    return render_template('/todo.html', username=username, data = data, todolist=todolist)


@app.route('/add-todo', methods=['GET', 'POST'])
def addTodo():
    if request.method == 'POST':
        username = request.form['username']
        itemId = request.form['add']
        cursor = g.db.cursor()
        cursor.execute("INSERT INTO " + username + "(item, status) VALUES ('" + itemId + "', '0' )")
        g.db.commit()
        # cursor.execute("DELETE FROM user_list WHERE name = 'eunicehew'")
        # cursor.execute("SELECT * FROM user_list WHERE name = 'eunicehew'")
        # cursor.execute("SELECT * FROM user_list WHERE name = '" + username + "'")
        # cursor.execute("DELETE FROM " + username + " WHERE status = '0'")
        cursor.execute("SELECT * FROM " + username) #gets todolist from user 
        g.db.commit()
        data = cursor.fetchall() 
        # print(data)
        return render_template('/todo.html', username=username, data = data)
    return EnvironmentError

@app.route('/remove-todo', methods=['GET', 'POST'])
def removeTodo():
    username = request.form['username']
    itemId = request.form['remove']
    cursor = g.db.cursor()
    cursor.execute("DELETE FROM " + username + " WHERE item = '" + item_id + "'")
    g.db.commit()
    return render_template('/todo.html', username=username)

@app.route('/update-todo', methods = ['POST'])
def updateTodo():
    username = request.form['username']
    itemId = request.form['complete']
    cursor = g.db.cursor()
    cursor.execute("SELECT " + status + " FROM " + username + " WHERE item = '" + item_id + "'")
    g.db.commit()
    currStatus = cursor.fetchone()
    if currStatus == 1:
        currStatus = 0
    else:
        currStatus = 1
    cursor.execute("UPDATE " + username + " SET status = '" + currStatus + "' WHERE item = '" + item_id + "'")
    conn.commit()
    cursor.execute("SELECT * FROM user_list WHERE name = '" + username + "'")
    data = cursor.fetchall()
    return render_template('/todo.html', username=username, data=data)


@app.route('/logout')
def logout():
    return redirect('/')


# @app.route('/add/<username>')
# def addToDo(username):
#     cursor = g.db.cursor()
#     cursor.execute("INSERT INTO "+ username + " (item, status) VALUES (" + item + ", 0)")
#     g.db.commit()
#     return render_template('/todo.html', username=username)

# @app.route('/complete/<username>')
# def completeToDo(username):
#     cursor = g.db.cursor()
#     cursor.execute("UPDATE "+ username + " SET status = 1 WHERE item = " + item)
#     g.db.commit()
#     return render_template('/todo.html', username=username)

# @app.route('/remove/<username>')
# def removeToDo(username):
#     cursor = g.db.cursor()
#     cursor.execute("DELETE FROM "+ username + " WHERE item = " + item_id)
#     g.db.commit()
#     return render_template('/todo.html', username=username)


# @app.route('/remove-todo/<username>/<item_id>')
# def removeTodo(username, item_id):
#     cursor = g.db.cursor()
#     data = {'item': item_id }
#     cursor.execute("DELETE FROM "+ username + " WHERE item = " + item_id)
#     g.db.commit()
#     return render_template('/todo.html', username=username)

# @app.route('/update-todo/<username>/<item_id>/<status>', methods = ['POST'])
# def updateTodo(username, item_id, status):
#     cursor = g.db.cursor()
#     cursor.execute("UPDATE " + username + " SET status = " + status + " WHERE item = " item_id)
#     g.db.commit()
#     return render_template('/todo.html', username=username)



if __name__ == '__main__':
    app.run()



