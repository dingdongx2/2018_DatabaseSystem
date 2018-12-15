from flask import Flask, render_template, redirect, request
from sql import sqlQuery, sqlQuery_
import datetime
import csv
import psycopg2 as pg

conn_str = "dbname=soyoung"

def option(Form, local, opt):
    type = search(local)
    if opt=="edit_id":
        if type=="sellers":
            option_person(Form, local) # Form : name/pwd & local : name
        elif type=="deliveries":
            print("")
        elif type=="customers":
            option_person(Form, local)
    elif opt=="edit_store":
        if type=="sellers":
            option_menu(Form, local)
    elif opt=="edit_tag":
        if type=="sellers":
            option_tag(Form, local)
    elif opt=="save_order":
        option_saveOrder(Form,local)
    elif opt=="order_accept":
        option_accept(Form,local)
    elif opt=="order_decline":
        option_decline(Form,local)


def search(local):
    sql = "SELECT * FROM sellers WHERE local=\'{}\'".format(local)
    personInfo = sqlQuery_(sql)
    if len(personInfo)>=1:
        return "sellers"
    sql = "SELECT * FROM deliveries WHERE local=\'{}\'".format(local)
    personInfo = sqlQuery_(sql)
    if len(personInfo)>=1:
        return "deliveries"
    sql = "SELECT * FROM customers WHERE local=\'{}\'".format(local)
    personInfo = sqlQuery_(sql)
    if len(personInfo)>=1:
        return "customers"
    return None

def option_tag(Form, local):
    type = search(local)
    if Form.get("delete_tag"):
        sqlQuery("DELETE FROM store_tags WHERE sid=%s AND name=%s",(Form.get("sid"),Form.get("tag")))
        print("{} 를 삭제하고 싶음".format(Form.get("tag")))

        # sqlQuery(sql)
    elif Form.get("add_tag"):
        sql = "INSERT INTO store_tags (sid, name) VALUES ({}, \'{}\')".format(Form.get("sid"),Form.get("added_tag"))
        sqlQuery(sql)
        print(sql)

def option_menu(Form, local): # about store
    # TOFIX option_menu으로 함수 이름 바꾸기
    type = search(local)
    if Form.get("changeName"):
        sql = "UPDATE menues SET menu=\'{}\' WHERE menu=\'{}\' AND sid={}".format(Form.get("after_menu"),Form.get("before_menu"),Form.get("sid"))
        sqlQuery(sql)
        print(sql)
    elif Form.get("delete"):
        sql = "DELETE FROM menues WHERE menu=\'{}\' AND sid={}".format(Form.get("before_menu"),Form.get("sid"))
        sqlQuery(sql)
    elif Form.get("add"):
        sql = "INSERT INTO menues (menu, sid) VALUES (\'{}\', {})".format(Form.get("added_menu"),Form.get("sid"))
        sqlQuery(sql)

def option_person(Form, local): # name/pwd change
    type = search(local)
    sql = "SELECT name, passwd FROM {} WHERE local=\'{}\'".format(type,local)
    personInfo = sqlQuery_(sql)

    # print("origin:",list(personInfo[0]))
    # print("after:",Form.get("name"),Form.get("password"))

    if Form.get("save"):
        sql = "UPDATE {} SET name=\'{}\', passwd=\'{}\' WHERE local=\'{}\'".format(type,Form.get("name"),Form.get("password"),local)
        sqlQuery(sql)
        print("edit")
    else:
        print("cancel")

def option_decline(Form, local):
    # did = Form.get("did")
    order_id = Form.get("order_id")
    sqlQuery("""BEGIN TRANSACTION;
        DELETE FROM orders WHERE order_id = %s;
        DELETE FROM basket WHERE order_id = %s;
        END TRANSACTION;""",(order_id, order_id))

def option_accept(Form, local):
    did = Form.get("did")
    order_id = Form.get("order_id")
    sqlQuery("""UPDATE orders SET did=%s, status='delivering' WHERE order_id = %s;""",(did, order_id))

def option_saveOrder(Form, local):
    menu_list = []
    for key in Form.keys():
        if key.startswith('menu_'):
            menu_list.append([key[5:],Form.get(key)])
    print("menu_list:",menu_list)

    if Form.get("payAcc"):
        print("account")
        payment = "account"
    elif Form.get("payCar"):
        print("card")
        payment = "card"

    sqlQuery("""INSERT INTO orders(sid, cid, status, did, payment, timestmp)
        SELECT M.sid, C.cid, 'waiting', NULL, %s, %s
        FROM menues M, customers C
        WHERE C.local=%s AND M.menuid=%s;""",(payment,datetime.datetime.now(),local,menu_list[0][0]))

    conn = pg.connect(conn_str)
    cur = conn.cursor()
    for menu in menu_list:
        cur.execute("""INSERT INTO basket (order_id, menuid, cnt)
            SELECT MAX(O.order_id),%s,%s
            FROM orders O""",(menu[0],menu[1]))
    cur.close()
    conn.commit()
