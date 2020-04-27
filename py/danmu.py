#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import pymysql
import time
from django import db
from flask import Flask
from flask import request
from flask import jsonify
from gevent import monkey
from flask import Flask, render_template
from werkzeug.debug import DebuggedApplication
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource
DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = '123456'
DBNAME = 'danmu'
monkey.patch_all()
# AC自动机算法
class node(object):
    def __init__(self):
        self.next = {}
        self.fail = None
        self.isWord = False
        self.word = ""

class ac_automation(object):

    def __init__(self):
        self.root = node()

    # 添加敏感词函数
    def addword(self, word):
        temp_root = self.root
        for char in word:
            if char not in temp_root.next:
                temp_root.next[char] = node()
            temp_root = temp_root.next[char]
        temp_root.isWord = True
        temp_root.word = word

    # 失败指针函数
    def make_fail(self):
        temp_que = []
        temp_que.append(self.root)
        while len(temp_que) != 0:
            temp = temp_que.pop(0)
            p = None
            for key,value in temp.next.item():
                if temp == self.root:
                    temp.next[key].fail = self.root
                else:
                    p = temp.fail
                    while p is not None:
                        if key in p.next:
                            temp.next[key].fail = p.fail
                            break
                        p = p.fail
                    if p is None:
                        temp.next[key].fail = self.root
                temp_que.append(temp.next[key])

    # 查找敏感词函数
    def search(self, content):
        p = self.root
        result = []
        currentposition = 0

        while currentposition < len(content):
            word = content[currentposition]
            while word in p.next == False and p != self.root:
                p = p.fail

            if word in p.next:
                p = p.next[word]
            else:
                p = self.root

            if p.isWord:
                result.append(p.word)
                p = self.root
            currentposition += 1
        return result

    # 加载敏感词库函数
    def parse(self, path):
        with open(path,encoding='utf-8') as f:
            for keyword in f:
                self.addword(str(keyword).strip())

    # 敏感词替换函数
    def words_replace(self, text):
        """
        :param ah: AC自动机
        :param text: 文本
        :return: 过滤敏感词之后的文本
        """
        result = list(set(self.search(text)))
        for x in result:
            m = text.replace(x, '*' * len(x))
            text = m
        return text

data = request.get_json()
username = data['username']
content = data['content']
localtime = time.asctime(time.localtime(time.time()))
#websocket
if __name__ == '__main__':

    ah = ac_automation()
    path='C:/Users/AZUMATOGAKU/Desktop/c++/PY/弹幕/sensitive_words.txt'
    ah.parse(path)
    text2 = ah.words_replace(content)
args = ((username, text2,localtime))
flask_app = Flask(__name__)
flask_app.debug = True


class ChatApplication(WebSocketApplication):
    def on_open(self):
        print("Some client connected!")

    def on_message(self, message):
        if message is None:
            return

        message = json.loads(message)

        if message['msg_type'] == 'message':
            self.broadcast(message)
        elif message['msg_type'] == 'update_clients':
            self.send_client_list(message)

    def send_client_list(self, message):
        current_client = self.ws.handler.active_client
        current_client.nickname = message['nickname']

        self.ws.send(json.dumps({
            'msg_type': 'update_clients',
            'clients': [
                getattr(client, 'nickname', 'anonymous')
                for client in self.ws.handler.server.clients.values()
            ]
        }))

    def broadcast(self, message):
        for client in self.ws.handler.server.clients.values():
            client.ws.send(json.dumps({
                'msg_type': 'message',
                'nickname': message['nickname'],
                'message': message['message']
            }))

    def on_close(self, reason):
        print("Connection closed!")


@flask_app.route('/index.html')
def index():
    return render_template('index.html')

server = WebSocketServer(
    ('0.0.0.0', 8000),

    Resource([
        ('^/chat', ChatApplication),
        ('^/.*', DebuggedApplication(flask_app))
    ]),

    debug=False,

)
for client in server.clients.values():
    client.ws.send(("text2"))
server.serve_forever()
try:

    db = pymysql.connect(DBHOST, DBUSER, DBPASS, DBNAME, charset='utf8')
    print("连接上了")
    cur = db.cursor()
    cur.execute('Insert into `danmus` values("%s","%s","%s")', args)
    print("数据插入成功")
    errcode=0
    retu={"errcode":"errcode"}
    response = requests.post('/', json=retu, headers=headers)
except pymysql.Error as e:
    print(".."+str(e))
    errcode=404
    retu = {"errcode": "errcode"}
    response = requests.post('', json=retu, headers=headers)