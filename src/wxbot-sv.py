# coding:utf-8
# by e0e

import threading
from flask import Flask, make_response, request
import itchat

qrSource = ''
def start_flask():
    flaskApp = Flask('itchat')
    @flaskApp.route('/')
    def return_qr():
        if len(qrSource) < 100:
            return qrSource
        else:
            response = make_response(qrSource)
            response.headers['Content-Type'] = 'image/jpeg'
            return response
    flaskApp.run(host='0.0.0.0',port=8289)
flaskThread = threading.Thread(target=start_flask)
flaskThread.setDaemon(True)
flaskThread.start()

def hold_flask():
    flaskApp = Flask('itchat')
    @flaskApp.route('/wx')
    def hello_world():
        global username
        content = request.args.get('content')
        nickname = request.args.get('nickname')
        if not content:            
            content = 'XSS Attention!'
        if (nickname and itchat.search_friends(nickName=nickname)):
            send_to = itchat.search_friends(nickName=nickname)[0]['UserName']
        else:
            send_to = username
            if nickname:
                return "Name Error!"
        print(content)
        print(nickname)
        try:
            itchat.send(content, toUserName=send_to)
        except:
            return 'Error!'
        return 'Hello World!'
    flaskApp.run(host='0.0.0.0',port=2999)
flaskThread_h = threading.Thread(target=hold_flask)
flaskThread_h.setDaemon(True)
flaskThread_h.start()

def qrCallback(uuid, status, qrcode):
    if status == '0':
        global qrSource
        qrSource = qrcode
    elif status == '200':
        qrSource = 'Logged in!'
    elif status == '201':
        qrSource = 'Confirm'

itchat.auto_login(True, qrCallback=qrCallback)
friend_list = itchat.search_friends(nickName='anquantest')
if friend_list:
    username = friend_list[0]['UserName']
else:
    username = ''
itchat.send('Login successfully!!', toUserName=username)
itchat.run()