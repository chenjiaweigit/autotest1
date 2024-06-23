#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import psycopg2
import pymysql
from common.yaml_util1 import load_ini

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
mysql_data = load_ini(data_file_path)['mysql']
pg_data = load_ini(data_file_path)['postgresql']

# DB_CONF = {
#     "host": data["MYSQL_HOST"],
#     "port": int(data["MYSQL_PORT"]),
#     "username": data["MYSQL_USER"],
#     "password": data["MYSQL_PASSWD"],
#     "database": data["MYSQL_DB"]
# }

mysql_host = mysql_data["mysql_host"]
mysql_port = int(mysql_data["mysql_port"])
mysql_username = mysql_data["mysql_user"]
mysql_password = mysql_data["mysql_passwd"]
mysql_database = mysql_data["mysql_db"]
pg_host = pg_data["pg_host"]
pg_port = int(pg_data["pg_port"])
pg_username = pg_data["pg_user"]
pg_password = pg_data["pg_passwd"]
pg_database = pg_data["pg_db"]


def my_sql_database():

    mydb = pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_username,
        passwd=mysql_password,
        db=mysql_database,
        charset='utf8'
    )
    mycursor = mydb.cursor()
    sql = "select * from jg_staff where staff_name = 'xxx'"
    # mycursor.execute("SHOW DATABASES")
    mycursor.execute(sql)
    print(mycursor.fetchall())
    # for x in mycursor:
    #     print(x)


def pg_sql_database():

    conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            user=pg_username,
            password=pg_password,
            database=pg_database
    )
    cur = conn.cursor()
    sql = "select module, name, method, address_url, data, except_pt," \
          " except_code, except_result, non_null_assert from test_case"
    cur.execute(sql)
    # print(cur.fetchall()) #打印结果
    return cur.fetchall()

# print(pg_sql_database())