#!/usr/bin/python3.5
import sqlite3
import logging
import random
import time
from datetime import date

from flask import Flask, render_template, request, g

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
data = None

DATABASE_NAME = "data.sqlite"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user', methods=['POST'])
def user():
    global data
    con = get_db()
    cur = con.cursor()
    username=request.form['user'].title()
    if request.method == 'POST'and 'result' in request.form:
        result = request.form['result']
        content_id = request.form['content_id']
        cur.execute("INSERT INTO BASELINE (CONTENTID, ISRULE, TIME, USER) VALUES (?, ?, ?, ?)", (content_id, result, time.strftime('%Y-%m-%d %H:%M:%S'), username))
        con.commit()
    cur.execute("SELECT COUNT(ID) FROM BASELINE WHERE USER == (?) AND TIME > (?)", [username, date.fromtimestamp(time.time())])
    num_content = cur.fetchone()[0]
    content_id, content = random.choice(data)
    return render_template('user.html',
                           username=username,
                           content=content,
                           content_id=content_id,
                           num_content=num_content)


def get_db():
    global data
    db = getattr(g, '_database', None)
    if db is None:
        con = sqlite3.connect(DATABASE_NAME)
        cur = con.cursor()
        data = list(cur.execute('SELECT ID, CONTENT FROM DATA'))
        cur.execute(r"CREATE TABLE IF NOT EXISTS BASELINE("
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                    "CONTENTID INTEGER NOT NULL,"
                    "ISPOSITIVE BOOLEAN NOT NULL,"
                    "TIME INTEGER NOT NULL,"
                    "USER STRING NOT NULL)")
        con.commit()
        db = g._database = con
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
	app.run(host='0.0.0.0')
