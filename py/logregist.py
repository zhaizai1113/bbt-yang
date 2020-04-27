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
try:
    data = request.get_json()
    username = data['username']
    userpass = data['userpass']
    args = ((username, userpass))
    db = pymysql.connect(DBHOST, DBUSER, DBPASS, DBNAME, charset='utf8')
    print("连接上了")
    cur = db.cursor()
    cur.execute('Insert into `danmuuser` values("%s","%s")', args)
    print("数据插入成功")
    errcode=0
    retu={"errcode":"errcode"}
    response = requests.post('', json=retu, headers=headers)
except pymysql.Error as e:
    print(".."+str(e))
    errcode=404
    retu = {"errcode": "errcode"}
    response = requests.post('', json=retu, headers=headers)