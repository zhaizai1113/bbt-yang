#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import pymysql
from django import db
from flask import Flask
from flask import request
from flask import jsonify
DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = '123456'
DBNAME = 'danmu'
db = pymysql.connect(DBHOST, DBUSER, DBPASS, DBNAME, charset='utf8')
cursor=db.cursor()

try:
    cursor.execute("select * from danmu")
    results=cursor.fetchall
    for row in results:
        name = row[0]
        content = row[1]
        time = row[2]
        print "%s,%s,%s\n" % \(name, content, time )
except:
    print "Error: unable to fecth data"

# 关闭数据库连接
db.close()