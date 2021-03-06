from flask import Flask, render_template, redirect, request
import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv
import json
import base64
# -*- coding: utf-8 -*-

conn_str = "dbname=soyoung"

def sqlQuery(sql, param=None):
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    if param is None:
        cur.execute(sql)
    else:
        cur.execute(sql, param)

    cur.close()
    conn.commit()

def sqlQuery_(sql, param=None):
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    if param is None:
        cur.execute(sql)
    else:
        cur.execute(sql, param)
    rows = cur.fetchall()

    cur.close()
    conn.commit()
    return rows

def openCsv(filename, jsonExists):
    filename = './csvFiles/' + filename + '.csv'

    with open(filename, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        # contacts.csv, students.csv have [menu]
        menu = next(rdr)
        print(menu)
        res = [menu]

        if jsonExists:
            for line in rdr:
                line[5] = json.loads(line[5])
                res.append(line)
        else:
            for line in rdr:
                res.append(line)
    return res
    # res = [[menu1,menu2,..],tmp1,tmp2,tmp3..]

# sellers
def putSeller():
    # sid;name;phone;local;domain;passwd
    people = openCsv("sellers",False)
    menu = people[0]
    people = people[1:]

    # create table
    sql = "CREATE TABLE sellers({} INTEGER, {} VARCHAR, {} VARCHAR, {} VARCHAR, {} VARCHAR, {} VARCHAR);".format(menu[0],menu[1],menu[2],menu[3],menu[4],menu[5])
    sqlQuery(sql)

    # insert values
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    for person in people:
        sql = "INSERT INTO sellers VALUES ({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');".format(person[0],person[1],person[2],person[3],person[4],person[5])
        # sqlQuery(sql)
        cur.execute(sql)
    cur.close()
    conn.commit()

    sql = "SELECT * FROM sellers;"
    sqlQuery(sql)

# customers
def putCustomer():
    # name;phone;local;domain;passwd;payments;lat;lng
    people = openCsv("customers",True)
    menu = people[0]
    people = people[1:]

    # create table
    sqlQuery("""CREATE TABLE customers(
        cid SERIAL PRIMARY KEY,
        name VARCHAR,
        phone VARCHAR,
        local VARCHAR,
        domain VARCHAR,
        passwd VARCHAR,
        payment VARCHAR,
        lat FLOAT,
        lng FLOAT);""")

    # insert values
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    for person in people:
        sql = "INSERT INTO customers (name, phone, local, domain, passwd, payment, lat, lng) VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{},{});".format(person[0],person[1],person[2],person[3],person[4],person[5],person[6],person[7])
        # sqlQuery(sql)
        cur.execute(sql)
    cur.close()
    conn.commit()

# delivery
def putDelivery():
    # did;name;phone;local;domain;passwd;lat;lng;stock
    people = openCsv("delivery",False)
    menu = people[0]
    people = people[1:]

    # create table
    sql = "CREATE TABLE deliveries({} INTEGER, {} VARCHAR, {} VARCHAR, {} VARCHAR, {} VARCHAR, {} VARCHAR, {} FLOAT, {} FLOAT, {} INTEGER);".format(menu[0],menu[1],menu[2],menu[3],menu[4],menu[5],menu[6],menu[7],menu[8])
    sqlQuery(sql)

    # insert values
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    for person in people:
        sql = "INSERT INTO deliveries VALUES ({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{},{},{});".format(person[0],person[1],person[2],person[3],person[4],person[5],person[6],person[7],person[8])
        # sqlQuery(sql)
        cur.execute(sql)
    cur.close()
    conn.commit()

    sql = "SELECT * FROM deliveries;"
    sqlQuery(sql)

def putStores():
    stores = openCsv("stores",True)
    menu = ["sid","address","sname","lat","lng","phone_nums","seller_id","tags"]
    stores = stores[1:]

    # create table
    sql = "CREATE TABLE stores({} INTEGER, {} VARCHAR, {} VARCHAR, {} FLOAT, {} FLOAT, {} VARCHAR, {} INTEGER, {} VARCHAR);".format(menu[0],menu[1],menu[2],menu[3],menu[4],menu[5],menu[6],menu[7])
    sqlQuery(sql)

    sql = """CREATE TABLE store_schedules (
        schedule_id SERIAL PRIMARY KEY,
        sid INTEGER,
        day_no INTEGER,
        holiday BOOLEAN,
        opened INTEGER,
        closed INTEGER
    );"""
    sqlQuery(sql)

    # insert values
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    for store in stores:
        cur.execute("INSERT INTO stores (sid,address,sname,lat,lng,phone_nums,seller_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",(store[0],store[1],store[2],store[3],store[4],store[5],store[7]))
        schedule = json.loads(store[6])
        schedule = json.loads(schedule)
        for day in schedule:
            if not day['holiday']:
                cur.execute("INSERT INTO store_schedules (sid,day_no,holiday,opened,closed) VALUES (%s,%s,%s,%s,%s)",(store[0],day['day'],day['holiday'],day['open'],day['closed']))
            else:
                cur.execute("INSERT INTO store_schedules (sid,day_no,holiday) VALUES (%s,%s,%s)",(store[0],day['day'],day['holiday']))
    cur.close()
    conn.commit()

    sql = """CREATE TABLE store_tags (
        tag_id SERIAL PRIMARY KEY,
        sid INTEGER,
        name VARCHAR
    );"""
    sqlQuery(sql)

# bank
def putBank():
    # bid,code,name
    stores = openCsv("bank",False)
    menu = stores[0]
    stores = stores[1:]

    # create table
    sql = "CREATE TABLE banks({} INTEGER, {} INTEGER, {} VARCHAR);".format(menu[0],menu[1],menu[2])
    sqlQuery(sql)

    # insert values
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    for bank in stores:
        sql = "INSERT INTO banks VALUES ({},{},\'{}\');".format(bank[0],bank[1],bank[2])
        cur.execute(sql)
    cur.close()
    conn.commit()

    sql = "SELECT * FROM banks;"
    sqlQuery(sql)

# menu
def putMenu():
    # menu,sid
    menues = openCsv("menu",False)
    menu = menues[0]
    menues = menues[1:]

    # create table
    sql = """CREATE TABLE menues (
        menuid SERIAL PRIMARY KEY ,
        menu VARCHAR,
        sid INTEGER
    );"""
    sqlQuery(sql)

    sql = """CREATE TABLE basket (
        basket_id SERIAL PRIMARY KEY,
        order_id INTEGER,
        menuid INTEGER,
        cnt INTEGER
    );"""
    sqlQuery(sql)

    # insert values
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    for m in menues:
        sql = "INSERT INTO menues (menu, sid) VALUES (\'{}\',{});".format(m[0],m[1])
        cur.execute(sql)
    cur.close()
    conn.commit()

    sql = "SELECT * FROM menues;"
    sqlQuery(sql)

def putOrder():
    sql = """CREATE TABLE orders(order_id SERIAL PRIMARY KEY,
        sid INTEGER NOT NULL,
        cid INTEGER NOT NULL,
        status VARCHAR NOT NULL,
        did INTEGER,
        payment VARCHAR,
        timestmp TIMESTAMP)"""
    sqlQuery(sql)

def init():
    # delete all of database
    # dbName = ["sellers", "customers", "deliveries"]
    dbName = ["sellers","customers","deliveries","banks", "menues", "stores","store_schedules","store_tags","basket","orders"]
    for name in dbName:
        try:
            sql = "Drop Table {};".format(name)
            sqlQuery(sql)
        except:
            pass
    print("dropped all of database")

init()
putSeller()
print("sellers fin")
putCustomer()
print("customers fin")
putDelivery()
print("deliveries fin")
putBank()
print("banks fin")
putMenu()
print("menues fin")
putStores()
print("stores fin")
putOrder()
print("fin")
