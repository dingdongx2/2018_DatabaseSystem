from flask import Flask, render_template, redirect, request
import csv

def option(Form, sid):
    head = ["sid","phone","email","position"]
    # head = ["sid","phone","email"]
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
            saveRequest(info, sid)
        elif Form.get('delete'):
            delRequest(info, sid)
        elif Form.get('add'):
            addRequest(info, sid)
        else:
            print("error")
    else:
        if Form.get('save'):
            saveRequest(info, sid)
        elif Form.get('delete'):
            delRequest(info, sid)
        elif Form.get('add'):
            addRequest(info, sid)
        else:
            print("error")

def saveRequest(info, sid):
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

def delRequest(info, sid):
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

def addRequest(info, sid):
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
