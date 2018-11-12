# MANAGEMENT DATA THROUGH DB

from flask import Flask, render_template, redirect, request
import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv
from form import contactsForm
from request import option, start
from sql import sqlQuery, sqlQuery_

app = Flask(__name__)

conn_str = "dbname=soyoung"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    sid = request.form.get('sid')
    passwd = request.form.get('passwd')
    print("login! sid:",sid,"/pwd:",passwd)

    sql = f"SELECT sid, password FROM students WHERE sid='{sid}'"
    rows = sqlQuery_(sql)
    print("rows:",rows)

    if len(rows)!=1:
        return render_template("error.html", msg="Wrong ID/Password")
    print(f"{sid}, {passwd}")
    return redirect(f"/{sid}")

@app.route("/<sid>", methods=['POST','GET'])
def portal(sid):
    if request.method == 'POST':
        option(request.form, sid)

    print("sid:",sid)
    conn = pg.connect(conn_str)
    cur = conn.cursor()

    if sid=="admin":
        sql = f"SELECT sid,password,sname,sex,major_id,tutor_id,grade FROM students;"
        students = sqlQuery_(sql)
        # students[0] = students[0].replace(' ','')
        print("\n\n\n",students)

        sql = f"SELECT sid,phone,email FROM contacts;"
        cc = sqlQuery_(sql)
        print("cc:",cc)
        res = []
        for c in cc:
            tmp = []
            for item in c:
                if item != None:
                    tmp.append(item.replace(' ',''))
                else:
                    tmp.append(item);
            res.append(tmp)
        print("://",res)

        head1 = ["학번","비밀번호","이름","전공","학년","지도교수","성적","edit/delete"]
        head2= ["sid","phone","email","edit/delete"]
        context = [head1,head2]
        return render_template("portal_admin.html", con_data = res, context=context, students=students)
    else:
        # EDIT LATER
        sql = f"SELECT sid,password,sname,sex,major_id,tutor_id,grade from students WHERE sid=\'{sid}\';"
        line = sqlQuery_(sql)

        line = list(line[0])
        line[0] = line[0].replace(' ','')
        print("line2:",line)

        sql = f"SELECT sid,phone,email FROM contacts WHERE sid=\'{sid}\';"
        cc = sqlQuery_(sql)
        head = ["학번","이름","전공","학년","지도교수"]
        return render_template("portal.html", stu_data = line, con_data = cc, head=head)

@app.route("/admin/students/edit",methods=['GET','POST'])
def s_edit():
    head = ["sid","password","sname","sex","major_id","tutor_id","grade"]
    sid = request.args.get('sid')

    print("sid::::",sid,"/")
    if sid==None:
        return render_template("s_add.html", head=head)
    sid = sid.replace(' ','')
    sql = f"SELECT sid,password,sname,sex,major_id,tutor_id,grade FROM students WHERE sid=\'{sid}\';"
    line = sqlQuery_(sql)
    line = list(line[0])
    return render_template("s_edit.html",head=head, con_data=line, sid=sid)

@app.route("/<sid>/contacts/edit",methods=['GET','POST'])
def edit(sid):
    phoneNum = request.args.get('phone-num')
    print("phone number:",phoneNum)
    head = ["sid","phone","email","position"]

    if sid.startswith("admin"):
        if phoneNum==None:
            return render_template("add.html", head=head[0:3], owner="admin")

        sql = f"SELECT sid,phone,email FROM contacts WHERE phone=\'{phoneNum}\';"
        line = sqlQuery_(sql)
        line = list(line[0])
        return render_template("s_edit.html", con_data=line, head=head[0:3], sid=sid)
    # students
    else:
        if phoneNum==None:
            return render_template("add.html", head=head, owner=sid)
        print("sid:",sid)
        if sid.startswith("2009003125"): contacts_name = "grass_corp"
        elif sid.startswith("2013004394"): contacts_name = "fire_corp"
        elif sid.startswith("2014005004"): contacts_name = "water_corp"
        else: contacts_name = None
        sql = f"SELECT sid,phone,email,position FROM {contacts_name} WHERE phone=\'{phoneNum}\';"
        line = sqlQuery_(sql)
        line = list(line[0])
        line[1] = line[1].replace(' ','')
        print("\n\n\n",line)
        return render_template("edit.html", con_data=line, head=head, sid=sid)

    return render_template("error.html",msg="error02")

@app.route("/<sid>/contacts")
def contacts(sid):
    sql = f"SELECT sid,password,sname,sex,major_id,tutor_id,grade FROM students WHERE sid=\'{sid}\';"
    line = sqlQuery_(sql)
    line = list(line[0])
    line[0] = line[0].replace(' ','')
    line[1] = line[1].replace(' ','')

    sql = f"SELECT sid,phone,email FROM contacts;"
    hyContacts = sqlQuery_(sql)

    if sid.startswith("2009003125"): contacts_name = "grass_corp"
    elif sid.startswith("2013004394"): contacts_name = "fire_corp"
    elif sid.startswith("2014005004"): contacts_name = "water_corp"
    else: contacts_name = None
    sql = f"SELECT sid,phone,email,position FROM {contacts_name};"
    stuContacts = sqlQuery_(sql)
    # print("\n~~\n",list(stuContacts[0]))
    stu = []
    for stuContact in stuContacts:
        stuContact = list(stuContact)
        stuContact[1] = stuContact[1].replace(' ','')
        stu.append(stuContact)
        # stuContact[1] = list(stuContact[1]).replace(' ','')
    print("stucon~:",stu)

    head = ["sid","phone","email","position","Edit/Delete"]

    return render_template("contacts.html", stu_data = line, con_data = hyContacts, user_data = stu, head=head[0:3], head2=head)
    # return render_template("error.html",msg="error03")

@app.route("/<sid>/count")
def count(sid):
    head = ["domain_name","count"]

    sql = f"SELECT * FROM contacts;"
    lines = sqlQuery_(sql)

    dic = {}
    for line in lines:
        tmp = line[2].split('@')
        if len(tmp)==2:
            if tmp[1] in dic.items():
                dic[tmp[1]]+=1
            else:
                dic[tmp[1]]=1
    domains = []
    for x,y in list(dic.items()):
        domains.append([x,y])
    print(domains)
    return render_template("count.html",head=head,cnt_data=domains)

@app.route("/<sid>/credits")
def credits(sid):
    conn = pg.connect(conn_str)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) #결과물이 딕셔너리 형태로
    sql = f"SELECT cl.name, cl.course_id, cl.year_open as year, cl.credit, cr.grade FROM class cl, creduts cr where cr.sid='{sid}' AND cl.class_id = cr.class_id"

    print(sql)
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        print(row)
    conn.close()
    return render_template("credits.html", credits=rows)

if __name__ == "__main__":
    app.run(debug=True)
