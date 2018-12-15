from flask import Flask, render_template, redirect, request
from sql import sqlQuery, sqlQuery_
import csv

def option(Form, local, opt):
    type = search(local)
    if opt=="edit_id":
        print(Form.get("name"))
        print("local:",local,"\n\n\n")
        if type=="sellers":
            print("request:seller")
            option_person(Form, local) # Form : name/pwd & local : name
        elif type=="deliveries":
            print("")
        elif type=="customers":
            option_person(Form, local)
        else:
            print("error 07")
    elif opt=="edit_store":
        if type=="sellers":
            option_store(Form, local)
        else:
            print("error 08")
    elif opt=="edit_tag":
        if type=="sellers":
            option_tag(Form, local)
        else:
            print("error 09")

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
        sql = "SELECT tags FROM stores WHERE sid={}".format(Form.get("sid"))
        tag_list = list(sqlQuery_(sql)[0])[0].replace('"','').replace(' ','')[1:][:-1].split(",")
        print("01:",tag_list)
        print("{} 를 삭제하고 싶음".format(Form.get("tag")))
        tag_list.remove(Form.get("tag"))
        print("02:",tag_list)
        sql = "UPDATE stores SET tags=\'{}\' WHERE sid={}".format(str(tag_list).replace("'",'"'),Form.get("sid"))
        sqlQuery(sql)
        print(sql)

        # sqlQuery(sql)
    elif Form.get("add_tag"):
        sql = "SELECT tags FROM stores WHERE sid={}".format(Form.get("sid"))
        tag_list = list(sqlQuery_(sql)[0])[0].replace('"','').replace(' ','')[1:][:-1].split(",")
        print("01:",tag_list)
        print("{} 를 추가하고 싶음".format(Form.get("added_tag")))
        if tag_list[0] == None:
            tag_list = [Form.get("added_tag")]
        else:
            tag_list.append(Form.get("added_tag"))
        print("02:",tag_list)
        sql = "UPDATE stores SET tags=\'{}\' WHERE sid={}".format(str(tag_list).replace("'",'"'),Form.get("sid"))
        sqlQuery(sql)
        print(sql)

def option_store(Form, local): # about store
    type = search(local)
    if Form.get("changeName"):
        sql = "UPDATE menues SET menu=\'{}\' WHERE menu=\'{}\' AND sid={}".format(Form.get("after_menu"),Form.get("before_menu"),Form.get("sid"))
        sqlQuery(sql)
        print(sql)
    elif Form.get("delete"):
        sql = "DELETE FROM menues WHERE menu=\'{}\' AND sid={}".format(Form.get("before_menu"),Form.get("sid"))
        sqlQuery(sql)
    elif Form.get("add"):
        sql = "INSERT INTO menues VALUES (\'{}\', {})".format(Form.get("added_menu"),Form.get("sid"))
        sqlQuery(sql)

def option_person(Form, local): # name/pwd change
    type = search(local)
    sql = "SELECT name, passwd FROM {} WHERE local=\'{}\'".format(type,local)
    personInfo = sqlQuery_(sql)

    print("origin:",list(personInfo[0]))
    print("after:",Form.get("name"),Form.get("password"))

    if Form.get("save"):
        sql = "UPDATE {} SET name=\'{}\', passwd=\'{}\' WHERE local=\'{}\'".format(type,Form.get("name"),Form.get("password"),local)
        sqlQuery(sql)
        print("edit")
    else:
        print("cancel")
