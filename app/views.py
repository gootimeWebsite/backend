# -*- coding: UTF-8 -*-
from flask import *
from app import app, auth
from .models import *
from .user.manager import usermanager
from .access import accessmanager
from .textMessage import TextMessage
import random, json


@auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


login_status = [200, 201, 500, 403, 403, 400]
login_message = ["登陆成功", "登陆成功", "未知错误", "缺少短信验证码", "短信验证码错误", "无效请求"]
@app.route('/login', methods = ['POST'])
def login():
    ret = {}
    data = json.loads(request.get_data())

    if accessmanager.auth(1, "POST", "/login") is False:
        status = 5
    else:
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
                    user = usermanager.insert(username, data['phonenumber'], "", "")
                    if user is not None:
                        status = 1
                    else:
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

    if status == 0 or status == 1:
        ret['username'] = username
        ret['token'] = user.generate_auth_token().decode('ascii')
        ret['rftoken'] = user.generate_auth_token(app.config['LONG_LIFE_TIME']).decode('ascii')

    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = login_status[status]
    return response


@app.route('/token', methods = ['GET'])
@auth.login_required
def token():
    ret = {}
    ret['token'] = g.user.generate_auth_token().decode('ascii')

    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = 200
    return response


logout_status = [200, 400]
logout_message = ["登出成功", "无效请求"]
@app.route('/logout', methods = ['POST'])
@auth.login_required
def logout():
    ret = {}
    data = json.loads(request.get_data())

    if accessmanager.auth(1, "POST", "/logout") is False:
        status = 1
    else:
        status = 0
    ret['message'] = logout_message[status]

    if status == 0:
        return redirect(url_for('index'))
    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = logout_status[status]
    return response


@app.route('/message/<phonenumber>', methods = ['POST'])
def message(phonenumber):
    if accessmanager.auth(1, "POST", "/message") is False:
        status = 400
    else:
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
        status = 202

    response = make_response()
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = status
    return response


@app.route('/', defaults={'path': ''})
@app.route('/')
def index():
    return 'Hello World!'
