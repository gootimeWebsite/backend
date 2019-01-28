# -*- coding: UTF-8 -*-
from flask import *
from app import app
from .models import *
from .user.manager import usermanager
from .textMessage import TextMessage
import random, json


login_status = [200, 403, 500, 403, 403]
login_message = ["登陆成功", "用户不存在", "未知错误", "缺少短信验证码", "短信验证码错误"]
@app.route('/login', methods = ['POST'])
def login():
    ret = {}
    data = json.loads(request.get_data())

    if data['type'] == 'phone':
        m = Messages.query.filter_by(phonenumber=data['phonenumber']).first()
        if m is None:
            status = 3
        elif m.message != data['message']:
            status = 4
        else:
            db.session.delete(m)
            db.session.commit()
            user = usermanager.search(data['phonenumber'], "phonenumber")
            if user is None:
                username = "Tel" + str(random.randint(10000000, 99999999))
                while usermanager.search(username, "username") is not None:
                    username = "Tel" + str(random.randint(10000000, 99999999))
                login = usermanager.insert(username, data['phonenumber'], "", "")
                if login == "success":
                    status = 0
                else:
                    print (login, username)
                    status = 2
            else:
                username = user.username
                status = 0
    elif data['type'] == 'weixin':
        #微信登录
        pass
    elif data['type'] == 'qq':
        #qq登录
        pass
    else:
        status = 2
    ret['message'] = login_message[status]

    if status == 0:
        session['username'] = username

    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = login_status[status]
    return response


logout_status = [200, 403, 403]
logout_message = ["登出成功", "错误用户", "用户未登录"]
@app.route('/logout', methods = ['POST'])
def logout():
    ret = {}
    data = json.loads(request.get_data())

    if session.get('username') is not None:
        if session.get('username') == data['username']:
            session.pop('username')
            status = 0
        else:
            status = 1
    else:
        status = 2
    ret['message'] = logout_message[status]

    if status == 0:
        return redirect(url_for('index'))
    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = logout_status[status]
    return response


@app.route('/message/<phonenumber>', methods = ['POST'])
def message(phonenumber):
    message = TextMessage.TextMessage()
    businessID = str(random.randint(100000,999999))
    lastTextMessage = str(random.randint(100000,999999))
    dic = {}
    dic['code'] = lastTextMessage
    #text = message.sendSMS(businessID, phonenumber, dic) #发送短信验证码接口

    m = Messages.query.filter_by(phonenumber=phonenumber).first()
    if m is None:
        m = Messages(phonenumber=phonenumber, message=lastTextMessage)
    else:
        m.message = lastTextMessage
    db.session.add(m)
    db.session.commit()

    response = make_response()
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = 202
    return response


@app.route('/', defaults={'path': ''})
@app.route('/')
def index():
    return 'Hello World!'
