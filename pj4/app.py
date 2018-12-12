from flask import Flask, render_template, jsonify, redirect, request
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
    print("start")

    email = request.form.get('email')
    passwd = request.form.get('passwd')
    tmp = email.split('@')
    print("tmp:",tmp)
    local = tmp[0]
    domain = tmp[1]

    print(email, passwd)
    print("login! id:",local,"/domain:",domain,"/pwd:",passwd,"/")

    trial = 0
    rows = 'a'
    while True:
        if trial == 0:
            sql = f"SELECT local, domain, passwd FROM sellers WHERE local=\'{local}\' AND domain=\'{domain}\' AND passwd=\'{passwd}\';"
            rows = sqlQuery_(sql)
            print("00",rows)
            trial+=1
        elif trial == 1:
            sql = f"SELECT local, domain, passwd FROM deliveries WHERE local=\'{local}\' AND domain=\'{domain}\' AND passwd=\'{passwd}\';"
            rows = sqlQuery_(sql)
            print("01",rows)
            trial+=1
        elif trial == 2:
            sql = f"SELECT local, domain, passwd FROM customers WHERE local=\'{local}\' AND domain=\'{domain}\' AND passwd=\'{passwd}\';"
            rows = sqlQuery_(sql)
            print("02",rows)
            trial+=1
        else:
            return render_template("error.html", msg="Wrong Email/Password")

        if len(rows)>=1:
            break

    print(f"{local}, {passwd}")
    return redirect(f"/{local}")

@app.route("/<local>", methods=['POST','GET'])
def portal(local):
    print("hi",local)
    return render_template("portal.html")

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
