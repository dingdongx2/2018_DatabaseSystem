import psycopg2 as pg
import csv

def main():
    db_connect = {
        'host': 'dbapp.hanyang.ac.kr',
        'post': '54321',
        'user': 'u_dblab',
        'dbname': 'db_dblab',
        'password': '1234'
    }

    csv = get_csv('students.csv')
    print(csv)

    connect_string = "host={host} user={user} dbname={dbname} password={password} port={port}".format(**db_connect)
    print(db_connect)

    conn = pg.connect(connect_string)
    # 커서 작성
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    line_count = 0
    for row in csv:
        if(line_count>3):
            sql = f"INSERT INTO students VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}','{row[4]}', '{row[5]}', '{row[6]}')" 
            print(sql)
            cur.execute(sql)
        line_count +=1

    conn.commit() 
    sql = "SELECT * FROM students"
    
    # 수동커밋 필요

    rows = cur.fetchall()

    print(type(rows))
    print(rows)

    for row in rows:
        print(type(row['sid']))
        print(row['sid'])
        print(row['sname'])
    
    pg.close()

def get_csv(filename):
    file_path = 'dbapp_practice'.format(filename)
    try:
        read_file = open(file_path, encoding='utf-8')
        reader = csv.reader(read_file, delimiter-',')
        result = []
        for row in reader:
            print(row)
            result.append(row)
    except:
        return -1
    read_file.close()
    
    return result

if __name__ == '__main__':
    main()
