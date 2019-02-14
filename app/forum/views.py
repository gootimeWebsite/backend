# -*- coding: UTF-8 -*-
from flask import *
from flask_restful import Resource
from . import forum, api, logger
from .models import Forum, Permission, db
from .utils import *
from app import auth


@api.resource('/')
class ForumHomePage(Resource):
    decorators = [auth.login_required]

    """
    @api {get} /forum/ Get Forum HomePage
    @apiVersion 0.1.1
    @apiName GetForum
    @apiGroup Forum
    @apiPermission User
    @apiDescription API for user to get forum homepage in which the posts are sorted in chronological order.

    @apiUse Authorization

    @apiSuccess {String} data Post's data list.
    @apiSuccess {String} data.auther Post's auther.
    @apiSuccess {String} data.content Post's content.
    @apiSuccess {String} data.id Post's id.
    @apiSuccess {String} data.title Post's title.
    @apiSuccess {String} data.updatetime Post's updatetime.
    @apiSuccess {String} message Post's getting status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "data": [
                {
                    "auther": "Tel72250567",
                    "content": "This is a test!",
                    "id": 511053,
                    "title": "Test",
                    "updatetime": "Sun, 03 Feb 2019 04:26:31 GMT"
                },
                {
                    "auther": "Tel72250567",
                    "content": "This is a PATCH test!",
                    "id": 125421,
                    "title": "Test",
                    "updatetime": "Sat, 02 Feb 2019 22:09:08 GMT"
                }
            ],
            "message": "success"
        }

    @apiUse UnauthorizedError
    @apiUse PostNotFoundError
    @apiUse UnknownError
    """
    def get(self):
        ret = {}
        ret['data'] = []

        posts = sorted(Forum.query.all(), key=lambda post: post.updatetime, reverse=True)
        if posts is None or posts == []:
            status = 404
            ret['message'] = "post not found"
        else:
            for item in posts:
                (ret['message'], data) = item.dict()
                if ret['message'] == "success":
                    status = 200
                    ret['data'].append(data)
                else:
                    status = 500
                    ret['error'] = "UnknownError"
                    break
        logger.info(str(status)+" "+ret['message']) if status == 200 else logger.warning(str(status)+" "+ret['message'])

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response


    """
    @api {post} /forum/ Create A New Forum Post
    @apiVersion 0.1.1
    @apiName PostForum
    @apiGroup Forum
    @apiPermission User
    @apiDescription API for user to create a new post.

    @apiUse Authorization
    @apiParam {String} title The title of the post.
    @apiParam {String} content The content of the post.

    @apiSuccess {String} id Post's id.
    @apiSuccess {String} message Post's creation status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 OK
        {
            "id": 901350,
            "message": "success"
        }

    @apiUse UnauthorizedError
    @apiUse InvalidRequestError
    """
    @permission_required(Permission.POST)
    def post(self):
        ret = {}
        data = json.loads(request.get_data())

        try:
            ret['id'] = Forum().insert(data['title'], g.user.username, data['content'])
            ret['message'] = "success"
            status = 201
        except Exception as e:
            logger.warning(e, exc_info=True)
            ret['error'] = "InvalidRequest"
            ret['message'] = "invalid request"
            status = 400
        logger.info(str(status)+" "+ret['message']) if status == 201 else logger.warning(str(status)+" "+ret['message'])

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response


@api.resource('/<int:id>')
class ForumPost(Resource):
    decorators = [auth.login_required]

    """
    @api {get} /forum/:id Get Forum Post
    @apiVersion 0.1.0
    @apiName GetForumID
    @apiGroup Forum
    @apiPermission User
    @apiDescription API for user to get a post.

    @apiUse Authorization

    @apiSuccess {String} data Post's data.
    @apiSuccess {String} data.auther Post's auther.
    @apiSuccess {String} data.content Post's content.
    @apiSuccess {String} data.id Post's id.
    @apiSuccess {String} data.title Post's title.
    @apiSuccess {String} data.updatetime Post's updatetime.
    @apiSuccess {String} message Post's getting status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "data": {
                "auther": "Tel72250567",
                "content": "This is a test!",
                "id": 901350,
                "title": "Test",
                "updatetime": "Sat, 02 Feb 2019 23:20:46 GMT"
            },
            "message": "success"
        }

    @apiUse UnauthorizedError
    @apiUse PostNotFoundError
    @apiUse UnknownError
    """
    def get(self, id):
        ret = {}

        post = Forum.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            (ret['message'], ret['data']) = post.dict()
            if ret['message'] == "success":
                status = 200
            else:
                status = 500
                ret['error'] = "UnknownError"
        logger.info(str(status)+" "+ret['message']) if status == 200 else logger.warning(str(status)+" "+ret['message'])

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response


    """
    @api {put} /forum/:id Update Forum Post
    @apiVersion 0.1.0
    @apiName PutForumID
    @apiGroup Forum
    @apiPermission User
    @apiDescription API for user to update a post.

    @apiUse Authorization
    @apiParam {String} title New title of the post.
    @apiParam {String} content New content of the post.

    @apiSuccess {String} message Post's putting status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "message": "success"
        }

    @apiUse UnauthorizedError
    @apiUse PostNotFoundError
    @apiUse InvalidRequestError
    """
    @permission_required(Permission.POST)
    def put(self, id):
        ret = {}
        data = json.loads(request.get_data())

        post = Forum.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            if post.auther != g.user.username:
                return "Unauthorized Access", 401
            else:
                try:
                    ret['message'] = post.update(title=data['title'], content=data['content'])
                    status = 200 if ret['message'] == "success" else 500
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
    @api {patch} /forum/:id Update Forum Post
    @apiVersion 0.1.0
    @apiName PatchForumID
    @apiGroup Forum
    @apiPermission User
    @apiDescription API for user to update a part of a post.

    @apiUse Authorization
    @apiParam {String} type The part of the update: 'title', 'content'.
    @apiParam {String} title New title of the post when 'type' = 'title'.
    @apiParam {String} content New content of the post when 'type' = 'content'.

    @apiSuccess {String} message Post's patching status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "message": "success"
        }

    @apiUse UnauthorizedError
    @apiUse PostNotFoundError
    @apiUse InvalidRequestError
    @apiUse UnknownError
    """
    @permission_required(Permission.POST)
    def patch(self, id):
        ret = {}
        data = json.loads(request.get_data())

        post = Forum.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            if post.auther != g.user.username:
                return "Unauthorized Access", 401
            else:
                try:
                    status = 202
                    if data.__contains__('title'):
                        ret['message'] = post.update(title=data['title'])
                        status = 200 if ret['message'] == "success" else 500
                    if data.__contains__('content'):
                        ret['message'] = post.update(content=data['content'])
                        status = 200 if ret['message'] == "success" else 500
                    if status == 202:
                        status = 400
                        ret['error'] = "InvalidRequest"
                        ret['message'] = "invalid request"
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
    @api {delete} /forum/:id Delete Forum Post
    @apiVersion 0.1.1
    @apiName DeleteForumID
    @apiGroup Forum
    @apiPermission User
    @apiDescription API for user to delete a post.

    @apiUse Authorization

    @apiSuccess {String} message Post's deleting status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "message": "success"
        }

    @apiUse UnauthorizedError
    @apiUse PostNotFoundError
    @apiUse UnknownError
    """
    @permission_required(Permission.POST)
    def delete(self, id):
        ret = {}

        post = Forum.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            if post.auther != g.user.username and not g.user.forum_is_administrator():
                return "Unauthorized Access", 401
            else:
                try:
                    db.session.delete(post)
                    db.session.commit()
                    ret['message'] = "success"
                    status = 200
                except Exception as e:
                    logger.warning(e, exc_info=True)
                    ret['error'] = "UnknownError"
                    ret['message'] = "unknown error"
                    status = 500
        logger.info(str(status)+" "+ret['message']) if status == 200 else logger.warning(str(status)+" "+ret['message'])

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response
