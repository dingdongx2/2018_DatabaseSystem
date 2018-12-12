from flask import Flask, render_template, jsonify, redirect
import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv
from form import contactsForm
from request import option, start
from sql import sqlQuery, sqlQuery_

app = Flask(__name__)

conn_str = "dbname=soyoung"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    sid = request.form.get('sid')
    passwd = request.form.get('passwd')
    print("login! sid:",sid,"/pwd:",passwd,"/")

    sql = f"SELECT sid, password FROM students WHERE sid=\'{sid}\' AND password=\'{passwd}\';"
    rows = sqlQuery_(sql)
    print("rows:",rows)

    if len(rows)!=1:
        return render_template("error.html", msg="Wrong ID/Password")
    print(f"{sid}, {passwd}")
    return redirect(f"/{sid}")

@app.route('/p/<page_name>')
def static_page(page_name):
    return render_template(f'{page_name}.html')

@app.route('/split')
def f_split():
    strings = request.args.get("param1")

    print(strings)
    return jsonify(strings)

if __name__ == '__main__':
    app.run(debug=True)
