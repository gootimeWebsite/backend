# -*- coding: UTF-8 -*-
from flask import *
from . import app, auth, logger
from .models import *
from .user.manager import usermanager
from .textMessage import TextMessage
import random, json, re


@auth.verify_token
def verify_token(token):
    logger.info(request.method+" "+request.path)
    if request.path == "/token":
        user = User.verify_auth_token(token, True)
    else:
        user = User.verify_auth_token(token)
    if not user:
        logger.warning("Unauthorized Access")
        return False
    g.user = user
    return True


    """
    @api {post} /login User Login
    @apiVersion 0.1.1
    @apiName Login
    @apiGroup General
    @apiDescription API for user to login.

    @apiParam {String} type The way user login: 'phone', 'weixin', 'qq'.

    @apiParam {String} phonenumber User's phnoe number when 'type' == 'phone'.
    @apiParam {String} message User's text message when 'type' == 'phone'.

    @apiSuccess {String} message User's login status: 'success'.
    @apiSuccess {String} username User's username.
    @apiSuccess {String} token User's access token.
    @apiSuccess {String} rftoken User's refresh token to get access token.
    @apiSuccess {Number} expires Access token's expires time(s).

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "message": "success",
            "username": "Tel11893460",
            "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTU0ODc3NDMzNiwiZXhwIjoxNTQ4NzgxNTM2fQ.eyJ1c2VybmFtZSI6IlRlbDExODkzNDYwIiwibGlmZXRpbWUiOjcyMDAsInJhbmQiOjU5OTR9.Iw6cZ_qnDMpxthxYuHKAldOzzk5QuairvzsnzZmDIIU",
            "rftoken": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTU0ODc3NDMzNiwiZXhwIjoxNTUxMzY2MzM2fQ.eyJ1c2VybmFtZSI6IlRlbDExODkzNDYwIiwibGlmZXRpbWUiOjI1OTIwMDAsInJhbmQiOjU5OTR9.81CvEk63uxCTIEhgvfYf52fpU3keeFu5zKDNhvw__H8",
            "expires": 7200
        }

    @apiError NeedMessage Need text message to login when 'type' == 'phone'.
    @apiError WrongMessage Wrong text message when 'type' == 'phone'.

    @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 BAD REQUEST
        {
            "error": "WrongMessage",
            "message": "wrong message"
        }

    @apiUse InvalidRequestError
    @apiUse UnknownError
    """
login_status = [200, 201, 500, 400, 400, 400]
login_message = ["success", "success", "unknown error", "need message", "wrong message", "invalid request"]
login_error = ["", "", "UnknownError", "NeedMessage", "WrongMessage", "InvalidRequest"]
@app.route('/login', methods = ['POST'])
def login():
    logger.info(request.method+" "+request.path)
    ret = {}
    data = json.loads(request.get_data())

    try:
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
            status = 5
    except:
        status = 5
    ret['message'] = login_message[status]

    if status == 0 or status == 1:
        logger.info("200 "+ret['message'])
        ret['username'] = username
        ret['rftoken'] = user.generate_auth_token(app.config['LONG_LIFE_TIME']).decode('ascii')
        ret['token'] = user.generate_auth_token().decode('ascii')
        ret['expires'] = app.config['LIFE_TIME']
    else:
        logger.warning(str(login_status[status])+" "+ret['message'])
        ret['error'] = login_error[status]

    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = login_status[status]
    return response


    """
    @api {get} /token Get Token
    @apiVersion 0.1.1
    @apiName Token
    @apiGroup General
    @apiPermission User
    @apiDescription API for user to get token with rftoken.

    @apiUse Authorization

    @apiSuccess {String} token User's access token.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
             "message": "success",
             "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTU0ODg0NjYxNywiZXhwIjoxNTQ4ODUzODE3fQ.eyJ1c2VybmFtZSI6IlRlbDExODkzNDYwIiwibGlmZXRpbWUiOjcyMDAsInJhbmQiOjU0MzB9.HzF56MKEBqftIipLkMhP0sJI43U5RqNK2E5lS2PLDCM"
        }

    @apiUse UnauthorizedError
    """
@app.route('/token', methods = ['GET'])
@auth.login_required
def token():
    ret = {}
    ret['message'] = "success"
    ret['token'] = g.user.generate_auth_token().decode('ascii')

    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = 200

    logger.info("200 "+ret['message'])
    return response


    """
    @api {post} /logout User Logout
    @apiVersion 0.1.0
    @apiName Logout
    @apiGroup General
    @apiPermission User
    @apiDescription API for user to logout.

    @apiUse Authorization

    @apiSuccess {String} message User's logout status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "message": "success"
        }

    @apiUse UnauthorizedError
    """
logout_status = [200, 400]
logout_message = ["success", "invalid request"]
@app.route('/logout', methods = ['POST'])
@auth.login_required
def logout():
    ret = {}

    status = 0
    ret['message'] = logout_message[status]

    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = logout_status[status]

    logger.info("200 "+ret['message'])
    return response


    """
    @api {post} /message Get Text Message
    @apiVersion 0.1.0
    @apiName Message
    @apiGroup General
    @apiDescription API for user to get text message.

    @apiParam {String} phonenumber User's phnoe number.

    @apiSuccess {String} message Text message sending status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 202 OK
        {
            "message": "success"
        }

    @apiUse InvalidRequestError
    """
message_status = [202, 400]
message_message = ["success", "invalid request"]
@app.route('/message', methods = ['POST'])
def message():
    logger.info(request.method+" "+request.path)
    ret = {}
    data = json.loads(request.get_data())

    try:
        phonenumber = data['phonenumber']
        if not re.fullmatch('\d{11}', phonenumber):
            status = 1
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
            status = 0
    except:
        status = 1
    ret['message'] = message_message[status]
    logger.info("202 "+ret['message']) if status == 0 else logger.warning("400 "+ret['message'])

    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = message_status[status]
    return response


@app.route('/', defaults={'path': ''})
@app.route('/')
def index():
    logger.info(request.method+" "+request.path)

    logger.info("404 Not Found")
    return "Not Found",404
