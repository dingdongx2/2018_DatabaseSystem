# MANAGEMENT DATA THROUGH FILE

from flask import Flask, render_template, redirect, request
import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    sid = request.form.get('sid')
    passwd = request.form.get('passwd')

    with open('students.csv','r',encoding='utf-8') as f:
        rdr = csv.reader(f)
        # for line in rdr:
        #     print(line)
        tmp = "none"
        for line in rdr:
            if line[0].startswith(sid) and line[1].startswith(passwd):
                return redirect(f"/{sid}")
                tmp = line[1]
                print("exists")
    return render_template("error.html",msg="Wrong ID/Password")

@app.route("/<sid>", methods=['POST','GET'])
def portal(sid):
    if request.method == 'POST':
        get_sid = request.form.get('sid')
        get_phone_num = request.form.get('phone_num')
        get_email = request.form.get('email')
        print(get_sid, get_phone_num, get_email)
        if request.form.get('save'):
            with open('contacts.csv','r') as f:
                rdr = csv.reader(f)
                new_lines = []
                for line in rdr:
                    # print(line)
                    if line[1]!=get_phone_num:
                        new_lines.append(line)
                    else:
                        new_lines.append([get_sid,get_phone_num,get_email])
            with open('contacts.csv','w') as f:
                w = csv.writer(f, delimiter=',')
                w.writerows(new_lines)
            print("save!")

        elif request.form.get('delete'):
            with open('contacts.csv','r') as f:
                rdr = csv.reader(f)
                new_lines = []
                for line in rdr:
                    if line[1]!=get_phone_num:
                        new_lines.append(line)
            with open('contacts.csv','w') as f:
                w = csv.writer(f, delimiter=',')
                w.writerows(new_lines)
            print("delete!")

    with open('students.csv','r',encoding='utf-8') as f:
        rdr = csv.reader(f)
        # tmp = 0
        for line in rdr:
            if line[0].startswith("admin"):
                with open('contacts.csv','r',encoding='utf-8') as c:
                    cc = csv.reader(c)
                    next(cc)
                    return render_template("portal_admin.html", stu_data = line, con_data = cc)

                # return render_template("portal_admin.html", stu_data = line)
            elif line[0].startswith(sid):
                return render_template("portal.html", stu_data = line)
    return render_template("error.html",msg="error01")
    # return render_template("portal.html", stu_data = rows[0])

@app.route("/<sid>/contacts/edit",methods=['POST', 'GET'])
def edit(sid):
    # if request.method == 'POST':
    #     print('post\n\n')
    # if request.method == 'GET':
    #     phoneNum = request.args.get('phone-num')
    #     print("phone number:",phoneNum)
    phoneNum = request.form.get('phone-num')
    print("phone number:",phoneNum)
    if phoneNum==None:
        return render_template("edit.html", con_data=[None,None,None])

    with open('contacts.csv','r',encoding='utf-8') as c:
        rdr = csv.reader(c)
        next(rdr)
        for line in rdr:
            if line[1]==phoneNum:
                return render_template("edit.html", con_data=line)
    return render_template("error.html",msg="error02")
    # return render_template("portal.html")

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
