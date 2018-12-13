from flask import Flask, render_template, jsonify, redirect, request
import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv
from form import contactsForm
from request import option, start, search
from sql import sqlQuery, sqlQuery_

sellers_menu = ["sid","address","sname","lat","lng","phone_nums","schedules","seller_id"]
stores_menu = ["seller_id","name","phone","local","domain","passwd"]
customers_menu = ["name","phone","local","domain","passwd","payments","lat","lng"]
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

    if search(local)==None:
        return render_template("error.html", msg="Wrong Email/Password")

    return redirect("/{}".format(local))

# 2ekle2gw
@app.route("/<local>", methods=['POST','GET'])
def portal(local):
    if request.method == 'POST':
        option(request.form, local)

    print("hi",local)

    conn = pg.connect(conn_str)
    cur = conn.cursor()

    type = search(local)
    if type=="sellers":
        sql = "SELECT * FROM stores WHERE seller_id=(SELECT seller_id FROM sellers WHERE local=\'{}\');".format(local)
        storeInfo = sqlQuery_(sql)
        sql = "SELECT * FROM sellers WHERE local=\'{}\'".format(local)
        personInfo = sqlQuery_(sql)
        if len(personInfo)>=1:
            tmp = []
            for store in storeInfo:
                tmp.append(list(store))
            rows = [[sellers_menu,stores_menu],tmp,list(personInfo[0])]

    elif type=="deliveries":
        sql = f"SELECT * FROM deliveries WHERE local=\'{local}\';"
        rows = sqlQuery_(sql)
        sql = "SELECT * FROM sellers WHERE local=\'{}\'".format(local)
        personInfo = sqlQuery_(sql)
        if len(personInfo)>=1:
            rows = [rows,personInfo]

    elif type=="customers":
        print("customers")
        sql = "SELECT * FROM customers WHERE local=\'{}\'".format(local)
        personInfo = sqlQuery_(sql)
        if len(personInfo)>=1:
            tmp = []
            rows = [customers_menu,list(personInfo[0])]
    else:
        print("error 06")

    return render_template("portal_"+type[0]+".html", info=rows)

@app.route("/<local>/edit",methods=['GET','POST'])
def edit(local):
    # id = request.args.get('local')
    type = search(local)
    # print("id::::",id)
    print("LOCAL::::",local)

    if type=="sellers":
        # print("id:",id)
        head = ["id","pwd"]

        sql = "SELECT * FROM sellers WHERE local=\'{}\'".format(local)
        info = list(sqlQuery_(sql)[0])
        info = [info[3],info[1],info[5]]
        print("ready for edit:",info)
        return render_template("edit_p.html",info=info,head=head)
    elif type=="deliveries":
        return render_template("edit_d.html")
    elif type=="customers":
        head = ["id", "pwd"]
        sql = "SELECT * FROM customers WHERE local=\'{}\'".format(local)
        info = list(sqlQuery_(sql)[0])
        info = [info[2],info[0],info[4]] # [local, name, pwd]
        print("ready for edit:",info)
        return render_template("edit_p.html",info=info,head=head)
    else:
        print("error 02.")
        return render_template("/"+local+".html")

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
