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

    # conn = pg.connect(conn_str)
    # cur = conn.cursor()
    sql = f"SELECT sid, password FROM students WHERE sid='{sid}'"
    rows = sqlQuery_(sql)
    print("rows:",rows)
    print(rows[0])
    # cur.execute(sql)

    # rows = cur.fetchall()
    if len(rows)!=1:
        return render_template("error.html", msg="Wrong ID/Password")
    # conn.close()
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

        sql = f"SELECT sid,phone,email FROM contacts;"
        cc = sqlQuery_(sql)

        head1 = ["학번","비밀번호","이름","전공","학년","지도교수","edit/delete"]
        head2= ["sid","phone","email","edit/delete"]
        context = [head1,head2]
        # with open('students.csv','r',encoding='utf-8') as f:
        #     rdr = csv.reader(f)
        #     next(rdr)
        #     students = []
        #     for line in rdr:
        #         line[0] = line[0].replace(' ','')
        #         students.append(line)
        #     with open('contacts.csv','r',encoding='utf-8') as c:
        #         cc = csv.reader(c)
        #         next(cc)
        #         return render_template("portal_admin.html", con_data = cc, context=context, students=students)
        return render_template("portal_admin.html", con_data = cc, context=context, students=students)
    else:
        # EDIT LATER
        sql = f"SELECT sid,password,sname,sex,major_id,tutor_id,grade from students WHERE sid=\'{sid}\';"
        line = sqlQuery_(sql)

        sql = f"SELECT sid,phone,email FROM contacts WHERE sid=\'{sid}\';"
        cc = sqlQuery_(sql)
        # print(sql)
        # cur.execute(sql)

    #     with open('students.csv','r',encoding='utf-8') as f:
    #         rdr = csv.reader(f)
    #         for line in rdr:
    #             if line[0].startswith(sid):
    #                 with open('contacts.csv','r',encoding='utf-8') as c:
    #                     cc = csv.reader(c)
    #                     next(cc)
    #                     line[0] = line[0].replace(' ','')
    #                     print("???:",line)
    #                     return render_template("portal.html", stu_data = line, con_data = cc)
    # return render_template("error.html",msg="error01")
        render_template("portal.html", stu_data = line, con_data = cc)

# 여기 수정차례
@app.route("/admin/students/edit",methods=['GET','POST'])
def s_edit():
    head = ["sid","password","sname","sex","major_id","tutor_id","grade"]
    sid = request.args.get('sid')

    sid = sid.replace(' ','')
    print("sid::::",sid,"/")
    if sid==None:
        return render_template("s_add.html", head=head)

    sql = f"SELECT sid,password,sname,sex,major_id,tutor_id,grade from students WHERE sid=\'{sid}\';"
    line = sqlQuery_(sql)
    line = list(line[0])
    return render_template("s_edit.html",head=head, con_data=line, sid=sid)

    # with open('students.csv','r',encoding='utf-8') as f:
    #     rdr = csv.reader(f)
    #     next(rdr)
    #     for line in rdr:
    #         if line[0].replace(' ','') == sid:
    #             return render_template("s_edit.html",head=head, con_data=line, sid=sid)

@app.route("/<sid>/contacts/edit",methods=['GET','POST'])
def edit(sid):
    phoneNum = request.args.get('phone-num')
    print("phone number:",phoneNum)
    head = ["sid","phone","email","position"]

    if sid.startswith("admin"):
        if phoneNum==None:
            return render_template("add.html", head=head[0:3], owner="admin")
        with open('contacts.csv','r',encoding='utf-8') as c:
            rdr = csv.reader(c)
            next(rdr)
            for line in rdr:
                if line[1]==phoneNum:
                    return render_template("edit.html", con_data=line, head=head[0:3], sid=sid)
    # students
    else:
        if phoneNum==None:
            return render_template("add.html", head=head, owner=sid)

        with open(start(sid),'r',encoding='utf-8') as userC:
            userCon = csv.reader(userC)
            for line in userCon:
                if line[1].replace(' ','')==phoneNum.replace(' ',''):
                    return render_template("edit.html", con_data=line, head=head, sid=sid)

    return render_template("error.html",msg="error02")

@app.route("/<sid>/contacts")
def contacts(sid):
    with open('students.csv','r',encoding='utf-8') as f:
        rdr = csv.reader(f)
        for line in rdr:
            if line[0].startswith(sid):
                with open('contacts.csv','r',encoding='utf-8') as c:
                    cc = csv.reader(c)
                    next(cc)

                    with open(start(sid), 'r', encoding='utf-8') as userC:
                        userCon = csv.reader(userC)
                        line[0]=line[0].replace(' ','')
                        head = ["sid","phone","email","position","Edit/Delete"]
                        return render_template("contacts.html", stu_data = line, con_data = cc, user_data = userCon, head=head[0:3], head2=head)
    return render_template("error.html",msg="error03")

@app.route("/<sid>/count")
def count(sid):
    head = ["domain_name","count"]
    with open('contacts.csv','r') as f:
        rdr = csv.reader(f)
        next(rdr)
        dic = {}
        for line in rdr:
            tmp = line[2].split('@')
            if len(tmp)==2:
                # print(tmp[0],tmp[1])
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
