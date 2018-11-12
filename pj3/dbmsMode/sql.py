from flask import Flask, render_template, redirect, request
import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv

conn_str = "dbname=soyoung"

def sqlQuery(sql):
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    cur.execute(sql)
    # rows = cur.fetchall()
    # print(rows)
    cur.close()
    conn.commit()

def sqlQuery_(sql):
    conn = pg.connect(conn_str)
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()
    # print(rows)

    cur.close()
    conn.commit()
    return rows
