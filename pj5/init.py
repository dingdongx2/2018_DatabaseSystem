import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv
import xlrd

conn_str = "dbname=soyoung"

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

def openCsv(filename):
    filename = filename + '.xlsx'

    with open(filename, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)

        menu = next(rdr)
        res = [menu]

        for line in rdr:
            tmp = []
            for l in line:
                tmp.append(l.replace(' ',''))
            res.append(tmp)
    return res

def opens(name):
    filename = name+".txt"
    print(filename)

    res = []
    with open(filename) as f:
        for line in f:
            # print(line)
            # res.append(line.split())
            if line.startswith('building_id'):
                tmp = line.replace('\n','').split('\t',3)
                res.append(tmp)
            else:
                tmp = line.replace('\n','').split('\t',3)
                tmp[0] = int(tmp[0])
                tmp[3] = int(tmp[3])
                res.append(tmp)
    print(res)
    return res

def putRoom():
    rooms = opens("room")
    # rooms = openCsv("room")
    menu = rooms[0]
    rooms = rooms[1:]
    for i in menu: print(i)

    sql = f"CREATE TABLE room({menu[0]} INTEGER, {menu[1]} INTEGER, {menu[2]} INTEGER);"
    sqlQuery(sql)

    for room in rooms:
        sql = f"INSERT INTO room VALUES({room[0]},{room[1]},{room[2]});"
        sqlQuery(sql)

def putBuilding():
    buildings = opens("building")
    menu = buildings[0]
    buildings = buildings[1:]
    # for i in menu: print(i)
    for building in buildings: print(building)

    sql = f"CREATE TABLE building({menu[0]} INTEGER, {menu[1]} CHAR[10], {menu[2]} CHAR[10], {menu[3]} INTEGER);"
    sqlQuery(sql)

    for building in buildings:
        sql = f"INSERT INTO building VALUES(\'{building[0]}\',\'{building[1]}\',\'{building[2]}\',\'{building[3]}\');"
        sqlQuery(sql)

def init():
    # delete all of database
    dbName = ["room","building","course","instructor","credits","class","time","major","student"]
    for name in dbName:
        sql = f"Drop Table {name};"
        sqlQuery(sql)
    print("drop all of database")

# init()
# putRoom()
putBuilding()
# print("fin")
