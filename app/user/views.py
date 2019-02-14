# -*- coding: UTF-8 -*-
from flask import *
from flask_restful import Resource
from . import user, api, logger
from app import app, auth
from .manager import usermanager
from .utils import DuplicateException

import re

@api.resource('/')
class UserInfo(Resource):
    decorators = [auth.login_required]

    """
    @api {get} /user/ Get User Information
    @apiVersion 0.1.1
    @apiName GetUserInfo
    @apiGroup User
    @apiPermission User
    @apiDescription API for user to get user's information.

    @apiUse Authorization

    @apiSuccess {String} data User's information.
    @apiSuccess {String} data.username User's username.
    @apiSuccess {String} data.phonenumber User's phonenumber.
    @apiSuccess {String} data.weixin User's weixin.
    @apiSuccess {String} data.qq User's qq.
    @apiSuccess {String} data.articles User's articles list.
    @apiSuccess {String} data.articles.auther User's article's auther.
    @apiSuccess {String} data.articles.id User's article's id.
    @apiSuccess {String} data.articles.category User's article's category.
    @apiSuccess {String} data.articles.content User's article's content.
    @apiSuccess {String} data.articles.title User's article's title.
    @apiSuccess {String} data.articles.updatetime User's article's updatetime.
    @apiSuccess {String} data.posts User's posts list.
    @apiSuccess {String} data.posts.auther User's post's auther.
    @apiSuccess {String} data.posts.content User's post's content.
    @apiSuccess {String} data.posts.id User's post's id.
    @apiSuccess {String} data.posts.title User's post's title.
    @apiSuccess {String} data.posts.updatetime User's post's updatetime.
    @apiSuccess {String} message UserInfo's getting status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "data": {
                "articles": [
                    {
                        "auther": "Tel72250567",
                        "category": "Test",
                        "content": "This is a test!",
                        "id": 2,
                        "title": "Test",
                        "updatetime": "Thu, 14 Feb 2019 12:02:00 GMT"
                    }
                ],
                "phonenumber": "17799163760",
                "posts": [
                    {
                        "auther": "Tel72250567",
                        "content": "This is a test!",
                        "id": 260164,
                        "title": "Test",
                        "updatetime": "Wed, 13 Feb 2019 21:03:36 GMT"
                    }
                ],
                "qq": null,
                "username": "Tel72250567",
                "weixin": null
            },
            "message": "success"
        }

    @apiUse UnauthorizedError
    @apiUse InvalidRequestError
    @apiUse UnknownError
    """
    def get(self):
        ret = {}
        ret['data'] = {}
        status = 202
        ret['message'] = "accepted"

        try:
            ret['data']['username'] = g.user.username
            ret['data']['phonenumber'] = g.user.phonenumber
            ret['data']['weixin'] = g.user.weixin
            ret['data']['qq'] = g.user.qq
            status = 200
            ret['message'] = "success"

            ret['data']['articles'] = []
            articles = sorted(g.user.articles, key=lambda article: article.updatetime, reverse=True)
            for article in articles:
                ret['data']['articles'].append({"id":article.id,"auther":article.auther,"title":article.title,"content":article.content,"category":article.category,"updatetime":article.updatetime})

            ret['data']['posts'] = []
            posts = sorted(g.user.forums, key=lambda post: post.updatetime, reverse=True)
            for post in posts:
                (message, data) = post.dict()
                if message == "success":
                    ret['data']['posts'].append(data)
                else:
                    status = 500
                    ret['error'] = "UnknownError"
                    ret['message'] = "unknown error"
                    break
        except Exception as e:
            logger.warning(e, exc_info=True)
            ret['error'] = "InvalidRequest"
            ret['message'] = "invalid request"
            status = 400
        logger.info(str(status)+" "+ret['message']) if status == 200 else logger.warning(str(status)+" "+ret['message'])

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response


    """
    @api {put} /user/ Update User Information
    @apiVersion 0.1.1
    @apiName PutUserInfo
    @apiGroup User
    @apiPermission User
    @apiDescription API for user to update user's information.

    @apiUse Authorization

    @apiParam {String} username User's new username.
    @apiParam {String} phonenumber User's new phonenumber.

    @apiSuccess {String} token User's new access token.
    @apiSuccess {String} rftoken User's new refresh token to get access token.
    @apiSuccess {Number} expires New access token's expires time(s).
    @apiSuccess {String} message User's updating status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "expires": 7200,
            "message": "success",
            "rftoken": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTU1MDEyMTAyMSwiZXhwIjoxNTUyNzEzMDIxfQ.eyJ1c2VybmFtZSI6ImFkaWwiLCJsaWZldGltZSI6MjU5MjAwMCwicmFuZCI6MzQ5NX0.KWNTuzp7xtUhAYjMn_dXe8eDuLKLbtpq9aTObXVJRMo",
            "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTU1MDEyMTAyMSwiZXhwIjoxNTUwMTI4MjIxfQ.eyJ1c2VybmFtZSI6ImFkaWwiLCJsaWZldGltZSI6NzIwMCwicmFuZCI6MTA4N30.ZAUU-ko1VlgV6iTLxCmjwdbtmX1lZn24Kqj4KJf7mAo"
        }

    @apiError DuplicateUsername Duplicate username.
    @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 BAD REQUEST
        {
            "error": "DuplicateUsername",
            "message": "username already exist"
        }

    @apiError DuplicatePhonenumber Duplicate phonenumber.
    @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 BAD REQUEST
        {
            "error": "DuplicatePhonenumber",
            "message": "phonenumber already exist"
        }

    @apiUse UnauthorizedError
    @apiUse InvalidRequestError
    @apiUse UnknownError
    """
    def put(self):
        ret = {}
        data = json.loads(request.get_data())
        status = 202
        ret['message'] = "accepted"

        try:
            phonenumber = data['phonenumber']
            if not re.fullmatch('\d{11}', phonenumber):
                raise Exception("Phonenumber do not match.")
            user = usermanager.search(phonenumber, "phonenumber")
            if user and user.phonenumber != g.user.phonenumber:
                raise DuplicateException("phonenumber")
            else:
                ret['message'] = usermanager.update(user=g.user, phonenumber=phonenumber)
                if ret['message'] == "success":
                    status = 200
                else:
                    status = 500
                    ret['error'] = "UnknownError"

            username = data['username']
            user = usermanager.search(username, "username")
            if user and user.username != g.user.username:
                raise DuplicateException("username")
            else:
                ret['message'] = usermanager.update(user=g.user, username=username)
                if ret['message'] == "success":
                    status = 200
                    ret['rftoken'] = g.user.generate_auth_token(app.config['LONG_LIFE_TIME']).decode('ascii')
                    ret['token'] = g.user.generate_auth_token().decode('ascii')
                    ret['expires'] = app.config['LIFE_TIME']
                else:
                    status = 500
                    ret['error'] = "UnknownError"
        except DuplicateException as e:
            logger.warning(e, exc_info=True)
            ret['error'] = "Duplicate" + e.typename.capitalize()
            ret['message'] = e.typename + " already exist"
            status = 400
        except Exception as e:
            logger.warning(e, exc_info=True)
            ret['error'] = "InvalidRequest"
            ret['message'] = "invalid request"
            status = 400
        logger.info(str(status)+" "+ret['message']) if status < 300 else logger.warning(str(status)+" "+ret['message'])

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response


    """
    @api {patch} /user/ Update User Information
    @apiVersion 0.1.1
    @apiName PatchUserInfo
    @apiGroup User
    @apiPermission User
    @apiDescription API for user to update user's information.

    @apiUse Authorization

    @apiParam {String} username User's new username.
    @apiParam {String} phonenumber User's new phonenumber.

    @apiSuccess {String} token User's new access token.
    @apiSuccess {String} rftoken User's new refresh token to get access token.
    @apiSuccess {Number} expires New access token's expires time(s).
    @apiSuccess {String} message User's updating status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "expires": 7200,
            "message": "success",
            "rftoken": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTU1MDEyMTAyMSwiZXhwIjoxNTUyNzEzMDIxfQ.eyJ1c2VybmFtZSI6ImFkaWwiLCJsaWZldGltZSI6MjU5MjAwMCwicmFuZCI6MzQ5NX0.KWNTuzp7xtUhAYjMn_dXe8eDuLKLbtpq9aTObXVJRMo",
            "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTU1MDEyMTAyMSwiZXhwIjoxNTUwMTI4MjIxfQ.eyJ1c2VybmFtZSI6ImFkaWwiLCJsaWZldGltZSI6NzIwMCwicmFuZCI6MTA4N30.ZAUU-ko1VlgV6iTLxCmjwdbtmX1lZn24Kqj4KJf7mAo"
        }

    @apiError DuplicateUsername Duplicate username.
    @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 BAD REQUEST
        {
            "error": "DuplicateUsername",
            "message": "username already exist"
        }

    @apiError DuplicatePhonenumber Duplicate phonenumber.
    @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 BAD REQUEST
        {
            "error": "DuplicatePhonenumber",
            "message": "phonenumber already exist"
        }

    @apiUse UnauthorizedError
    @apiUse InvalidRequestError
    @apiUse UnknownError
    """
    def patch(self):
        ret = {}
        data = json.loads(request.get_data())
        status = 202
        ret['message'] = "accepted"

        try:
            if data.__contains__('phonenumber'):
                phonenumber = data['phonenumber']
                if not re.fullmatch('\d{11}', phonenumber):
                    raise Exception("Phonenumber do not match.")
                user = usermanager.search(phonenumber, "phonenumber")
                if user and user.phonenumber != g.user.phonenumber:
                    raise DuplicateException("phonenumber")
                else:
                    ret['message'] = usermanager.update(user=g.user, phonenumber=phonenumber)
                    if ret['message'] == "success":
                        status = 200
                    else:
                        status = 500
                        ret['error'] = "UnknownError"

            if data.__contains__('username'):
                username = data['username']
                user = usermanager.search(username, "username")
                if user and user.username != g.user.username:
                    raise DuplicateException("username")
                else:
                    ret['message'] = usermanager.update(user=g.user, username=username)
                    if ret['message'] == "success":
                        status = 200
                        ret['rftoken'] = g.user.generate_auth_token(app.config['LONG_LIFE_TIME']).decode('ascii')
                        ret['token'] = g.user.generate_auth_token().decode('ascii')
                        ret['expires'] = app.config['LIFE_TIME']
                    else:
                        status = 500
                        ret['error'] = "UnknownError"
            if status == 202:
                raise Exception("Empty data.")
        except DuplicateException as e:
            logger.warning(e, exc_info=True)
            ret['error'] = "Duplicate" + e.typename.capitalize()
            ret['message'] = e.typename + " already exist"
            status = 400
        except Exception as e:
            logger.warning(e, exc_info=True)
            ret['error'] = "InvalidRequest"
            ret['message'] = "invalid request"
            status = 400
        logger.info(str(status)+" "+ret['message']) if status < 300 else logger.warning(str(status)+" "+ret['message'])

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response
