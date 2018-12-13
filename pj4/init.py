from flask import Flask, render_template, redirect, request
import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv
import json
import base64
# -*- coding: utf-8 -*-

conn_str = "dbname=soyoung"

def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

def sqlQuery(sql):
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    cur.execute(sql)

    cur.close()
    conn.commit()

def sqlQuery_(sql):
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()

    cur.close()
    conn.commit()

def openCsv(filename, jsonExists):
    filename = './csvFiles/' + filename + '.csv'

    with open(filename, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        # contacts.csv, students.csv have [menu]
        menu = next(rdr)
        print(menu)
        res = [menu]

        if jsonExists==1:
            for line in rdr:
                line[5] = json.loads(line[5])
                res.append(line)
        elif jsonExists==2:
            for line in rdr:
                # print(line[5])
                line[5] = json.loads(line[5])
                # print(":",line[5])
                line[6] = json.loads(line[6])
                # line[5] = stringToBase64(line[5])
                # line[6] = stringToBase64(line[6])
                # print(line)
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
    people = openCsv("customers",1)
    menu = people[0]
    people = people[1:]

    # create table
    sql = "CREATE TABLE customers({} VARCHAR, {} VARCHAR, {} VARCHAR, {} VARCHAR, {} VARCHAR, {} VARCHAR, {} FLOAT, {} FLOAT);".format(menu[0],menu[1],menu[2],menu[3],menu[4],menu[5],menu[6],menu[7])
    sqlQuery(sql)

    # insert values
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    for person in people:
        sql = "INSERT INTO customers VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{},{});".format(person[0],person[1],person[2],person[3],person[4],person[5],person[6],person[7])
        # sqlQuery(sql)
        cur.execute(sql)
    cur.close()
    conn.commit()

    sql = "SELECT * FROM customers;"
    sqlQuery(sql)

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
    # sid,address,sname,lat,lng,phone_nums,schedules,seller_id
    stores = openCsv("stores",2)
    menu = stores[0]
    stores = stores[1:]

    # create table
    sql = "CREATE TABLE stores({} INTEGER, {} VARCHAR, {} VARCHAR, {} FLOAT, {} FLOAT, {} VARCHAR, {} VARCHAR, {} INTEGER);".format(menu[0],menu[1],menu[2],menu[3],menu[4],menu[5],menu[6],menu[7])
    sqlQuery(sql)

    # insert values
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    for store in stores:
        # if "'" in store[2]: store[2].replace("'",'')
        # sql = f"INSERT INTO stores VALUES ({store[0]},\'{store[1]}\',\'{store[2]}\',{store[3]},{store[4]},\'{store[5]}\',\'{store[6]}\',{store[7]});"
        # print(sql)
        # cur.execute(sql)
        cur.execute("INSERT INTO stores VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(store[0],store[1],store[2],store[3],store[4],store[5],store[6],store[7]))
    cur.close()
    conn.commit()

    sql = "SELECT * FROM stores;"
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
    sql = "CREATE TABLE menues({} VARCHAR, {} INTEGER);".format(menu[0],menu[1])
    sqlQuery(sql)

    # insert values
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    for m in menues:
        # sql = "INSERT INTO menues VALUES (\'{m[0]}\',{m[1]});",{m[0],m[1]}
        sql = "INSERT INTO menues VALUES (\'{}\',{});".format(m[0],m[1])
        cur.execute(sql)
    cur.close()
    conn.commit()

    sql = "SELECT * FROM menues;"
    sqlQuery(sql)

def init():
    # delete all of database
    # dbName = ["sellers", "customers", "deliveries"]
    dbName = ["sellers","customers","deliveries","banks", "menues", "stores"]
    for name in dbName:
        sql = "Drop Table {};".format(name)
        sqlQuery(sql)
    print("dropped all of database")

init()
putSeller()
# print("sellers fin")
putCustomer()
# print("customers fin")
putDelivery()
putBank()
putMenu()
putStores()
print("fin")
