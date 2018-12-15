from flask import Flask, render_template, redirect, request
import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv

conn_str = "dbname=soyoung"

def sqlQuery(sql, param=None):
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    if param is None:
        cur.execute(sql)
    else:
        cur.execute(sql, param)

    cur.close()
    conn.commit()

def sqlQuery_(sql, param=None):
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    if param is None:
        cur.execute(sql)
    else:
        cur.execute(sql, param)
    rows = cur.fetchall()

    cur.close()
    conn.commit()
    return rows
