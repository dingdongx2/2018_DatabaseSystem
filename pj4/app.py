from flask import Flask, render_template, jsonify, redirect, request
import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv
import json
from form import contactsForm
from request import option, search
from sql import sqlQuery, sqlQuery_
import datetime

stores_menu = ["sid","address","sname","lat","lng","phone_nums","seller_id","tags"]
sellers_menu = ["seller_id","name","phone","local","domain","passwd"]
customers_menu = ["cid","name","phone","local","domain","passwd","payments","lat","lng"]
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
    # if request.method == 'POST':
    #     option(request.form, local, "edit_id")
    if local == 'favicon.ico':
        return ''
    print("hi",local)

    conn = pg.connect(conn_str)
    cur = conn.cursor()

    type = search(local)
    print("type:",type)
    if type=="sellers":
        storeInfo = sqlQuery_("""SELECT * FROM stores WHERE seller_id=(SELECT seller_id FROM sellers S WHERE S.local=%s);""",(local,))
        personInfo = sqlQuery_("""SELECT * FROM sellers WHERE local=%s""",(local,))
        if len(personInfo)>=1:
            tmp = []
            for store in storeInfo:
                tmp.append(list(store))
            rows = [[stores_menu,sellers_menu],tmp,list(personInfo[0])]

        try:
            order_list = sqlQuery_("""SELECT order_id, status FROM orders WHERE sid = (SELECT sid FROM stores WHERE seller_id=(SELECT seller_id FROM sellers WHERE local=%s));""",(local,))[0]
        except IndexError:
            order_list = []
        print("~:",order_list)
        return render_template("portal_s.html", info=rows,order_list=order_list)

    elif type=="deliveries":
        sql = f"SELECT * FROM deliveries WHERE local=\'{local}\';"
        rows = sqlQuery_(sql)
        sql = "SELECT * FROM sellers WHERE local=\'{}\'".format(local)
        personInfo = sqlQuery_(sql)
        if len(personInfo)>=1:
            rows = [rows,personInfo]
        return render_template("portal_d.html", info=rows)

    elif type=="customers":
        if request.method == 'POST':
            option(request.form, local, "delivery_fin")
            return redirect("/"+local)

        print("customers")
        personInfo = sqlQuery_("SELECT * FROM customers WHERE local=%s",(local,))
        if len(personInfo)>=1:
            rows = [customers_menu,list(personInfo[0])]

        try:
            orderComplete = sqlQuery_("""SELECT O.order_id, S.sname, M.menu, O.payment, O.timestmp
                FROM orders O, stores S, menues M, basket B
                WHERE O.cid = %s
                    AND O.order_id = B.order_id AND B.menuid = M.menuid
                    AND O.sid = S.sid
                    AND O.status = 'completed'
                ORDER BY O.timestmp DESC;""",(rows[1][0],))
        except IndexError:
            orderComplete = []

        print(".:",orderComplete)

        try:
            orderWaiting = sqlQuery_("""SELECT O.order_id, S.sname, M.menu, O.payment, O.timestmp, O.status
                FROM orders O, stores S, menues M, basket B
                WHERE O.cid = %s
                    AND O.status = 'waiting'
                    AND B.menuid = M.menuid
                    AND O.order_id = B.order_id AND O.sid=S.sid
                ORDER BY O.timestmp DESC;""",(rows[1][0],))
        except IndexError:
            orderWaiting = []

        try:
            orderDelivering = sqlQuery_("""SELECT O.order_id, S.sname, M.menu, O.payment, O.timestmp, O.status, D.name
                FROM orders O, stores S, menues M, basket B, deliveries D
                WHERE O.cid = %s
                    AND O.status = 'delivering'
                    AND B.menuid = M.menuid
                    AND O.order_id = B.order_id AND O.sid=S.sid
                    AND D.did=O.did
                ORDER BY O.timestmp DESC;""",(rows[1][0],))
        except IndexError:
            orderDelivering = []

        print("...:",orderWaiting)
        print("//",orderDelivering)

        return render_template("portal_c.html", info=rows,orderComplete=orderComplete,orderWaiting=orderWaiting,orderDelivering=orderDelivering)
    else:
        print("error 06")

    row = []
    return render_template("portal_"+type[0]+".html", info=rows)

@app.route("/<local>/order",methods=['GET','POST'])
def newOrder(local):
    if request.method == 'POST':
        option(request.form, local, "save_order")
        return redirect("/"+local)

    try:
        tmp = sqlQuery_("""SELECT cid,lat,lng FROM customers WHERE local=%s""",(local,))[0]
    except IndexError:
        return redirect('/')

    customer_info = []
    for t in tmp:
        customer_info.append(t)
    print("customer:",customer_info)
    dt = datetime.datetime.now()
    print("~~~~~~~:",dt.hour)
    if dt.hour==0:
        timeNow = 2400+dt.minute
    else:
        timeNow = dt.hour*100+dt.minute

    near_stores = sqlQuery_("""SELECT S.sid, (S.lat - C.lat)^2 + (S.lng - C.lng)^2 as distance, S.sname
        FROM stores S, customers C, store_schedules SS
        WHERE S.sid = SS.sid
            AND day_no = %s AND SS.holiday = false AND SS.opened <= %s AND SS.closed >= %s
            AND C.cid = %s
        ORDER BY distance ASC
        limit 100;""",(dt.weekday(),timeNow,timeNow,customer_info[0], ) )
    print(near_stores)

    return render_template("orderMenu.html",local=local,near_stores=near_stores)

@app.route("/<local>/order/<sid>",methods=['GET','POST'])
def orderWithId(local,sid):
    menu_list = sqlQuery_("""SELECT M.menuid, M.menu FROM menues M, stores S WHERE S.sid=%s AND M.sid = S.sid;""",(sid,))
    q = sqlQuery_("""SELECT payment FROM customers WHERE local=%s""",(local,))
    payment_list = json.loads(q[0][0])
    tmp = [[],[]]
    print(";",payment_list)
    # print(len(payment_list))
    print(tmp)
    return render_template("storeInfo.html",menu_list=menu_list,local=local,payment_list=payment_list)

@app.route("/<local>/order/result",methods=['GET','POST'])
def searchResult(local):
    store_results = None
    if request.method == 'POST':
        res = request.form.get('address')
        if res:
            store_results = sqlQuery_("""SELECT sid, NULL, sname
                FROM stores WHERE address LIKE %s""",('%%'+res+'%%',))

        res = request.form.get('tag')
        if res:
            store_results = sqlQuery_("""SELECT T.sid, NULL, S.sname
                FROM stores S, store_tags T
                WHERE T.name LIKE %s AND T.sid=S.sid""",('%%'+res+'%%',))

        res = request.form.get('store_name')
        if res:
            store_results = sqlQuery_("""SELECT sid, NULL, sname
                FROM stores WHERE sname LIKE %s""",('%%'+res+'%%',))

    if store_results is None:
        store_results = []
    return render_template("searchResult.html",store_results=store_results,local=local)

@app.route("/<local>/edit",methods=['GET','POST'])
def edit(local):
    # id = request.args.get('local')
    type = search(local)
    print("LOCAL::::",local)

    if request.method == 'POST':
        option(request.form, local, "edit_id")
        return redirect('/' + local)

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
        info = [info[3],info[1],info[5]] # [local, name, pwd]
        print("ready for edit:",info)
        return render_template("edit_p.html",info=info,head=head)
    else:
        print("error 02.")
        return render_template("/"+local+".html")

@app.route("/<local>/store",methods=['GET','POST'])
def store(local):
    if request.method == 'POST':
        print("10")
        if request.form.get('tags'):
            option(request.form, local, "edit_tag")
        elif request.form.get('accept'):
            option(request.form, local, "order_accept")
        elif request.form.get('decline'):
            option(request.form, local, "order_decline")
        else:
            print("request!!!!")
            print("before:",request.form.get('before_menu'))
            print("after:",request.form.get('after_menu'))
            option(request.form, local, "edit_store")

    sid = request.args.get('sid') # sid : store num
    print("sid:",sid)
    print("local:",local)

    menues = sqlQuery_("""SELECT menu from menues WHERE sid=%s""",(sid,))
    menu_list = []
    for menu in menues: menu_list.append(menu[0])

    tags = sqlQuery_("""SELECT name from store_tags WHERE sid=%s""",(sid,))

    oids = sqlQuery_("SELECT order_id, status FROM orders WHERE sid = %s",(sid,))
    print(oids)
    # order_list = []
    # for id in oids: order_list.append(id[0])
    # print(order_list)

    if tags:
        res = []
        for t in tags: res.append(t[0])
        return render_template("manage.html",menu_list = menu_list, sid=sid, local=local, tag_list=res, order_list=oids)
    else:
        return render_template("manage.html",menu_list = menu_list, sid=sid, local=local, tag_list=[],order_list=oids)

@app.route("/<local>/store/order",methods=['GET','POST'])
def checkOrder(local):
    if request.method == 'POST':
        print("00")

    order_id = request.form.get("order_id")
    sid = request.form.get("sid")
    print("order_id:",order_id)
    menu_info = sqlQuery_("""SELECT M.menu, B.cnt
        FROM menues M, basket B, orders O
        WHERE O.order_id = %s
            AND O.order_id = B.order_id
            AND B.menuid = M.menuid;""",(order_id,))
    print("menu_list:",menu_info)

    deliver_info = sqlQuery_("""SELECT D.did, D.name, (D.lat - S.lat)^2 + (D.lng - S.lng)^2 AS distance
        FROM deliveries D, stores S
        WHERE D.stock < 5 AND S.sid = %s
        ORDER BY distance ASC
        limit 5;""",(sid,))
    print("deliver_info:",deliver_info)
    print("local:",local)

    order_status = sqlQuery_("""SELECT status FROM orders WHERE order_id=%s""",(order_id,))

    return render_template("sellerOrder.html",menu_info=menu_info,local=local,sid=sid,order_id=order_id,deliver_info=deliver_info,order_status=order_status)

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
