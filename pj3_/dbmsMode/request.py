from flask import Flask, render_template, redirect, request
from sql import sqlQuery, sqlQuery_
import csv

def option(Form, sid):
    print(Form.get("sname"))
    print("sid:",sid,"\n\n\n")
    if sid == "admin":
        if Form.get("sname") != None:
            print("option1")
            option1(Form, sid)
        else:
            option2(Form, sid)
    else:
        option2(Form, sid)

# students
def option1(Form, sid):
    head = ["sid","password","sname","sex","major_id","tutor_id","grade"]
    print("func option, input : ", head, sid)
    info = [Form.get(head[x]) for x in range(7)]
    print(info)

    if Form.get('save'):
        saveRequest1(info, sid, head)
    elif Form.get('delete'):
        delRequest1(info, sid, head)
    elif Form.get('add'):
        addRequest1(info, sid, head)
    else:
        print("error")

def option2(Form, sid):
    head = ["sid","phone","email","position"]
    print("func option, input : ", head, sid)

    get_sid = Form.get(head[0])
    get_phone_num = Form.get(head[1])
    get_email = Form.get(head[2])

    info = [get_sid,get_phone_num,get_email]

    if not sid.startswith("admin"):
        get_pos = Form.get(head[3])
        info.append(get_pos)
    print("after info : ",get_sid, get_phone_num, get_email)
    print("after info2 :",info)

    if sid.startswith("admin"):
        if Form.get('save'):
            saveRequest2(info, sid, head[0:3])
        elif Form.get('delete'):
            delRequest2(info, sid, head[0:3])
        elif Form.get('add'):
            addRequest2(info, sid, head[0:3])
        else:
            print("error")
    else:
        if Form.get('save'):
            saveRequest2(info, sid, head)
        elif Form.get('delete'):
            delRequest2(info, sid, head)
        elif Form.get('add'):
            addRequest2(info, sid, head)
        else:
            print("error")

def saveRequest1(info, sid, head):
    sql = f"UPDATE students SET {head[0]}=\'{info[0]}\', {head[1]}=\'{info[1]}\',{head[2]}=\'{info[2]}\',{head[3]}=\'{info[3]}\',{head[4]}={info[4]},{head[5]}=\'{info[5]}\',{head[6]}={info[6]} WHERE sid=\'{info[0]}\';"
    print("saverequest1 sid:",info[0])
    sqlQuery(sql)

    print("save!")

def delRequest1(info, sid, head):
    sql = f"DELETE FROM students WHERE sid=\'{info[0]}\';"
    sqlQuery(sql)
    print("delete!")

def addRequest1(info, sid, head):
    # info[0] = info[0]+'\t'
    sql = f"INSERT INTO students VALUES (\'{info[0]}\', \'{info[1]}\', \'{info[2]}\', \'{info[3]}\', \'{info[4]}\', \'{info[5]}\', \'{info[6]}\');"
    sqlQuery(sql)
    print("add!")

def saveRequest2(info, sid, head):
    if sid.startswith("admin"): contacts_name = "contacts"
    elif sid.startswith("2009003125"): contacts_name = "grass_corp"
    elif sid.startswith("2013004394"): contacts_name = "fire_corp"
    elif sid.startswith("2014005004"): contacts_name = "water_corp"
    else: contacts_name = None

    print("contacts_name:",contacts_name)

    if contacts_name == "contacts":
        sql = f"UPDATE {contacts_name} SET {head[0]}=\'{info[0]}\',{head[1]}=\'{info[1]}\',{head[2]}=\'{info[2]}\' WHERE sid=\'{info[0]}\';"
        sqlQuery(sql)
        print("save!")

    elif contacts_name != None:
        sql = f"UPDATE {contacts_name} SET {head[0]}=\'{info[0]}\',{head[1]}=\'{info[1]}\',{head[2]}=\'{info[2]}\',{head[3]}=\'{info[3]}\' WHERE sid=\'{info[0]}\';"
        sqlQuery(sql)
        print("save!")

def delRequest2(info, sid, head):
    if sid.startswith("admin"): contacts_name = "contacts"
    elif sid.startswith("2009003125"): contacts_name = "grass_corp"
    elif sid.startswith("2013004394"): contacts_name = "fire_corp"
    elif sid.startswith("2014005004"): contacts_name = "water_corp"
    else: contacts_name = None

    sql = f"DELETE FROM {contacts_name} WHERE sid=\'{info[0]}\';"
    sqlQuery(sql)
    print("delete!")

def addRequest2(info, sid, head):
    if sid.startswith("admin"): contacts_name = "contacts"
    elif sid.startswith("2009003125"): contacts_name = "grass_corp"
    elif sid.startswith("2013004394"): contacts_name = "fire_corp"
    elif sid.startswith("2014005004"): contacts_name = "water_corp"
    else: contacts_name = None

    print("contacts_name:",contacts_name)
    if sid.startswith("admin"):
        sql = f"INSERT INTO {contacts_name} VALUES (\'{info[0]}\', \'{info[1]}\', \'{info[2]}\');"
        sqlQuery(sql);
        print("add!")
    else:
        sql = f"INSERT INTO {contacts_name} VALUES (\'{info[0]}\', \'{info[1]}\', \'{info[2]}\', \'{info[3]}\');"
        sqlQuery(sql);
        print("add!")

def start(sid):
    if sid.startswith("2009003125"): contacts_name = "grass_corp.csv"
    elif sid.startswith("2013004394"): contacts_name = "fire_corp.csv"
    elif sid.startswith("2014005004"): contacts_name = "water_corp.csv"
    else: contacts_name = None
    return contacts_name
