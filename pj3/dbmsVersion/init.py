from flask import Flask, render_template, redirect, request
import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv

conn_str = "dbname=soyoung"

def sqlQuery(sql):
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    cur.execute(sql)
    # rows = cur.fetchall()
    # print(rows)
    cur.close()
    conn.commit()

def sqlQuery_(sql):
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()
    print(rows)

    cur.close()
    conn.commit()

def openCsv(filename, firstline):
    filename = filename + '.csv'

    with open(filename, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)

        # contacts.csv, students.csv have [menu]
        if firstline == True:
            menu = next(rdr)
            res = [menu]
        else:
            res = []

        for line in rdr:
            tmp = []
            for l in line:
                tmp.append(l.replace(' ',''))
            res.append(tmp)
    return res

def putStudents():
    students = openCsv("students",True)
    menu = students[0]
    students = students[1:]

    # print("students:",students)
    # create table
    sql = f"CREATE TABLE students({menu[0]} CHAR(15), {menu[1]} CHAR(15), {menu[2]} CHAR(10), {menu[3]} CHAR(10), {menu[4]} INTEGER, {menu[5]} CHAR(15), {menu[6]} INTEGER);"
    sqlQuery(sql)
    # insert values
    for student in students:
        sql = f"INSERT INTO students VALUES (\'{student[0]}\',\'{student[1]}\',\'{student[2]}\',\'{student[3]}\',{student[4]},\'{student[5]}\',{student[6]});"
        sqlQuery(sql)

    # print("\nSTUDENTS\n")
    sql = f"SELECT * FROM students;"
    sqlQuery_(sql)

def putContacts():
    contacts = openCsv("contacts",True)
    menu = contacts[0]
    contacts = contacts[1:]

    # print("contacts:",contacts)
    # create table
    sql = f"CREATE TABLE contacts({menu[0]} CHAR(15), {menu[1]} CHAR(15), {menu[2]} CHAR(30));"
    sqlQuery(sql)
    # insert values
    for contact in contacts:
        sql = f"INSERT INTO contacts VALUES (\'{contact[0]}\',\'{contact[1]}\',\'{contact[2]}\');"
        sqlQuery(sql)

def putPerson(filename):
    person = openCsv(filename,False)
    sql = f"CREATE TABLE {filename}(sid CHAR(15), phone CHAR(15), email CHAR(30), position CHAR(5));"
    sqlQuery(sql)
    for p in person:
        sql = f"INSERT INTO {filename} VALUES (\'{p[0]}\',\'{p[1]}\',\'{p[2]}\',\'{p[3]}\');"
        sqlQuery(sql)


putStudents()
putContacts()
putPerson("Grass_corp")
putPerson("Fire_corp")
putPerson("Water_corp")
