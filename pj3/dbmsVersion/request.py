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

    info = []
    get_sid = Form.get(head[0])
    get_phone_num = Form.get(head[1])
    get_email = Form.get(head[2])

    info.append(get_sid)
    info.append(get_phone_num)
    info.append(get_email)
    if not sid.startswith("admin"):
        get_pos = Form.get(head[3])
        info.append(get_pos)
    print("after info : ",get_sid, get_phone_num, get_email)
    print("after info2 :",info)

    if sid.startswith("admin"):
        if Form.get('save'):
            saveRequest2(info, sid)
        elif Form.get('delete'):
            delRequest2(info, sid)
        elif Form.get('add'):
            addRequest2(info, sid)
        else:
            print("error")
    else:
        if Form.get('save'):
            saveRequest2(info, sid)
        elif Form.get('delete'):
            delRequest2(info, sid)
        elif Form.get('add'):
            addRequest2(info, sid)
        else:
            print("error")

def saveRequest1(info, sid, head):
    sql = f"UPDATE students SET {head[0]}=\'{info[0]}\', {head[1]}=\'{info[1]}\',{head[2]}=\'{info[2]}\',{head[3]}=\'{info[3]}\',{head[4]}={info[4]},{head[5]}=\'{info[5]}\',{head[6]}={info[6]} WHERE sid=\'{sid}\';"
    sqlQuery(sql)

    # contacts_name = "students.csv"
    # with open(contacts_name,'r') as f:
    #     rdr = csv.reader(f)
    #     new_lines = []
    #     for line in rdr:
    #         if line[1]!=info[1]:
    #             new_lines.append(line)
    #         else:
    #             new_lines.append(info)
    # with open(contacts_name,'w') as f:
    #     w = csv.writer(f, delimiter=',')
    #     w.writerows(new_lines)
    print("save!")

def delRequest1(info, sid, head):
    contacts_name = "students.csv"
    with open(contacts_name,'r') as f:
        rdr = csv.reader(f)
        new_lines = []
        for line in rdr:
            if line[1]!=info[1]:
                new_lines.append(line)
    with open(contacts_name,'w') as f:
        w = csv.writer(f, delimiter=',')
        w.writerows(new_lines)
    print("delete!")

def addRequest1(info, sid, head):
    info[0] = info[0]+'\t'
    contacts_name = "students.csv"
    with open(contacts_name,'a') as f:
        f.write(','.join(info)+'\n')

def saveRequest2(info, sid):
    if sid.startswith("admin"): contacts_name = "contacts.csv"
    elif sid.startswith("2009003125"): contacts_name = "Grass_corp.csv"
    elif sid.startswith("2013004394"): contacts_name = "Fire_corp.csv"
    elif sid.startswith("2014005004"): contacts_name = "Water_corp.csv"
    else: contacts_name = None

    with open(contacts_name,'r') as f:
        rdr = csv.reader(f)
        new_lines = []
        for line in rdr:
            if line[1]!=info[1]:
                new_lines.append(line)
            else:
                new_lines.append(info)
    with open(contacts_name,'w') as f:
        w = csv.writer(f, delimiter=',')
        w.writerows(new_lines)
    print("save!")

def delRequest2(info, sid):
    if sid.startswith("admin"): contacts_name = "contacts.csv"
    elif sid.startswith("2009003125"): contacts_name = "Grass_corp.csv"
    elif sid.startswith("2013004394"): contacts_name = "Fire_corp.csv"
    elif sid.startswith("2014005004"): contacts_name = "Water_corp.csv"
    else: contacts_name = None

    with open(contacts_name,'r') as f:
        rdr = csv.reader(f)
        new_lines = []
        for line in rdr:
            if line[1]!=info[1]:
                new_lines.append(line)
    with open(contacts_name,'w') as f:
        w = csv.writer(f, delimiter=',')
        w.writerows(new_lines)
    print("delete!")

def addRequest2(info, sid):
    if sid.startswith("admin"): contacts_name = "contacts.csv"
    elif sid.startswith("2009003125"): contacts_name = "Grass_corp.csv"
    elif sid.startswith("2013004394"): contacts_name = "Fire_corp.csv"
    elif sid.startswith("2014005004"): contacts_name = "Water_corp.csv"
    else: contacts_name = None

    info[0] = info[0]+'\t'
    if sid.startswith("admin"):
        contacts_name = "contacts.csv"
        with open(contacts_name,'a') as f:
            f.write(','.join(info[0:3])+'\n')
    else:
        if sid.startswith("2009003125"): contacts_name = "Grass_corp.csv"
        elif sid.startswith("2013004394"): contacts_name = "Fire_corp.csv"
        elif sid.startswith("2014005004"): contacts_name = "Water_corp.csv"
        else: contacts_name = None
        with open(contacts_name,'a') as f:
            f.write(','.join(info)+'\n')

def start(sid):
    if sid.startswith("2009003125"): contacts_name = "Grass_corp.csv"
    elif sid.startswith("2013004394"): contacts_name = "Fire_corp.csv"
    elif sid.startswith("2014005004"): contacts_name = "Water_corp.csv"
    else: contacts_name = None
    return contacts_name
