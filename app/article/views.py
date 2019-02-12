# -*- coding: UTF-8 -*-
from flask import *
from flask_restful import Resource
from . import article, api
from app import auth
from .models import Article, Permission, db
from .utils import *
from sqlalchemy.orm import sessionmaker
from datetime import datetime
@api.resource('/<int:id>')
class ArticleInfo(Resource):
    decorators = [auth.login_required]

    '''
    lzm完成
    '''



    """
    @api {get} /forum/:id Get Article Post
    @apiVersion 0.1.0
    @apiName GetArticleID
    @apiGroup Article
    @apiPermission User
    @apiDescription API for user to get a post.

    @apiUse Authorization

    @apiSuccess {String} data Post's data.
    @apiSuccess {String} data.auther Post's auther.
    @apiSuccess {String} data.content Post's content.
    @apiSuccess {String} data.id Post's id.
    @apiSuccess {String} data.title Post's title.
    @apiSuccess {String} data.category Post's category.
    @apiSuccess {String} data.updatetime Post's updatetime.
    @apiSuccess {String} message Post's getting status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "data": {
                "auther": "Tel72250567",
                "title": "Test",
                "content": "This is a test!",
                "category": "test"
                "updatetime": "Sun, 03 Feb 2019 04:26:31 GMT"
                "id": "511053",
            },
            "message": "success"
        }

    @apiUse UnauthorizedError
    @apiUse PostNotFoundError
    """
    def get(self,id):
        ret = {}
        ret_article={}
        post = Article.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            ret_article['auther'] = post.auther
            ret_article['title'] = post.title
            ret_article['content'] = post.content
            ret_article['category'] = post.category
            ret_article['updatetime'] = post.updatetime
            ret_article['id'] = post.id
            ret['message'] = "success"
            ret['data'] = ret_article
            status = 200

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response

    """
    @api {put} /forum/:id Update Article Post
    @apiVersion 0.1.0
    @apiName PutArticleID
    @apiGroup Article
    @apiPermission User
    @apiDescription API for user to update a post.

    @apiUse Authorization
    @apiParam {String} title New title of the post.
    @apiParam {String} content New content of the post.
    @apiParam {String} auther New auther of the post.
    @apiParam {String} category New category of the post.
    @apiSuccess {String} data Post's data.
    @apiSuccess {String} data.auther Post's auther.
    @apiSuccess {String} data.content Post's content.
    @apiSuccess {String} data.id Post's id.
    @apiSuccess {String} data.title Post's title.
    @apiSuccess {String} data.category Post's category.
    @apiSuccess {String} data.updatetime Post's updatetime.
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
    def put(self,id):
        ret = {}
        data = json.loads(request.get_data())
        ret_article={}
        post = Article.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            if post.auther != g.user.username:
                return "Unauthorized Access", 401
            else:
                try:
                    post.title = data['title']
                    post.category = data['category']
                    post.content = data['content']
                    ret_article['auther'] = post.auther
                    ret_article['title'] = data['title']
                    ret_article['content'] = data['content']
                    ret_article['category'] = data['category']
                    ret_article['id'] = post.id
                    post.updatetime = datetime.now()
                    ret_article['updatetime'] = post.updatetime
                    db.session.commit()
                    status = 200
                    ret['data'] = ret_article
                    ret['message'] = "success"
                except:
                    ret['error'] = "InvalidRequest"
                    ret['message'] = "invalid request"
                    status = 400

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response

    """
    @api {patch} /forum/:id Update Article Post
    @apiVersion 0.1.0
    @apiName PatchArticleID
    @apiGroup Article
    @apiPermission User
    @apiDescription API for user to update a part of a post.

    @apiUse Authorization
    @apiParam {String} title New title of the post.
    @apiParam {String} content New content of the post.
    @apiParam {String} auther New auther of the post.
    @apiParam {String} category New category of the post.
    @apiSuccess {String} data Post's data.
    @apiSuccess {String} data.auther Post's auther.
    @apiSuccess {String} data.content Post's content.
    @apiSuccess {String} data.id Post's id.
    @apiSuccess {String} data.title Post's title.
    @apiSuccess {String} data.category Post's category.
    @apiSuccess {String} data.updatetime Post's updatetime.
    @apiSuccess {String} message Post's patching status: 'success'.
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
    def patch(self,id):
        ret = {}
        data = json.loads(request.get_data())
        ret_article={}
        post = Article.query.filter_by(id=id).first()
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
                        post.title = data['title']
                        status = 200
                    if data.__contains__('category'):
                        post.category = data['category']
                        status = 200
                    if data.__contains__('content'):
                        post.content = data['content']
                        status = 200
                    post.updatetime = datetime.now()
                    ret_article['auther'] = post.auther
                    ret_article['title'] = post.title
                    ret_article['content'] = post.content
                    ret_article['category'] = post.category
                    ret_article['updatetime'] = post.updatetime
                    ret_article['id'] = post.id
                    post.updatetime = datetime.now()
                    db.session.commit()
                    if status == 200:
                        ret['data'] = ret_article
                        ret['message'] = "success"
                    else:
                        status = 400
                        ret['error'] = "InvalidRequest"
                        ret['message'] = "invalid request"
                except:
                    ret['error'] = "InvalidRequest"
                    ret['message'] = "invalid request"
                    status = 400

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response

    """
    @api {delete} /forum/:id Delete Article Post
    @apiVersion 0.1.1
    @apiName DeleteArticleID
    @apiGroup Article
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
    def delete(self,id):
        ret = {}

        post = Article.query.filter_by(id=id).first()
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
                except:
                    ret['error'] = "UnknownError"
                    ret['message'] = "unknown error"
                    status = 500

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response


@api.resource('/')
class Article1(Resource):
    decorators = [auth.login_required]

    """
    @api {get} /article Get article homepage
    @apiVersion 0.1.0
    @apiName GetArticle
    @apiGroup Article
    @apiPermission User
    @apiDescription API for user to get article homepage in which the posts are sorted in chronological order.

    @apiUse Authorization

    @apiSuccess {String} data Post's data list.
    @apiSuccess {String} data[i].auther Post's auther.
    @apiSuccess {String} data[i].content Post's content.
    @apiSuccess {String} data[i].id Post's id.
    @apiSuccess {String} data[i].title Post's title.
    @apiSuccess {String} data[i].category Post's category.
    @apiSuccess {String} data[i].updatetime Post's updatetime.
    @apiSuccess {String} message Post's getting status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "data": [
                {
                    "auther": "Tel72250567",
                    "title": "Test",
                    "content": "This is a test!",
                    "category": "test"
                    "updatetime": "Sun, 03 Feb 2019 04:26:31 GMT"
                    "id": "511053",
                },
                {
                    "auther": "Tel72250568",
                    "title": "Test",
                    "content": "This is a test!",
                    "category": "test"
                    "updatetime": "Sun, 03 Feb 2019 04:26:42 GMT"
                    "id": "511057",
                }
            ],
            "message": "success"
        }

    @apiUse UnauthorizedError
    @apiUse PostNotFoundError
    """
    def get(self):
        ret = {}
        ret_article=[]
        post = sorted(Article.query.all(), key=lambda post: post.updatetime, reverse=True)
        if post is None or post == []:
            ret['message'] = "post not found"
            status = 404
        else:
            ret['message'] = "success"
            for item in post:
                ret_article.append({"id":item.id,"auther":item.auther,"title":item.title,"content":item.content,"category":item.category,"updatetime":item.updatetime})
                ret['data'] = ret_article
            status = 200

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response

    """
    @api {post} /forum Create A New Article Post
    @apiVersion 0.1.1
    @apiName PostArticle
    @apiGroup Article
    @apiPermission User
    @apiDescription API for user to create a new post.

    @apiUse Authorization
    @apiParam {String} title The title of the post.
    @apiParam {String} content The content of the post.
    @apiParam {String} title New title of the post.
    @apiParam {String} content New content of the post.
    @apiParam {String} category New category of the post.

    @apiSuccess {String} data Post's data.
    @apiSuccess {String} data.auther Post's auther.
    @apiSuccess {String} data.content Post's content.
    @apiSuccess {String} data.id Post's id.
    @apiSuccess {String} data.title Post's title.
    @apiSuccess {String} data.category Post's category.
    @apiSuccess {String} data.updatetime Post's updatetime.
    @apiSuccess {String} message Post's creation status: 'success'.
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 OK
        {
            "id": "901350",
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
            title = data['title']
            auther = g.user.username
            category = data['category']
            content = str(data['content'])

            article = Article(title=title,auther=auther,category=category,content=content)

            db.session.add(article)
            db.session.commit()
            ret['id'] = article.id
            ret['message'] = "success"
            status = 201
        except:
            status = 400
            ret['error'] = "InvalidRequest"
            ret['message'] = "invalid request"

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response
