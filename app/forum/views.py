# -*- coding: UTF-8 -*-
from flask import *
from flask_restful import Resource
from . import forum, api
from .models import Forum, db
from app import auth

@api.resource('/')
class ForumHomePage(Resource):
    decorators = [auth.login_required]

    def get(self):
        return "GET ForumHomePage!"


    def post(self):
        ret = {}
        data = json.loads(request.get_data())

        try:
            ret['id'] = Forum().insert(data['title'], data['auther'], data['content'])
            ret['message'] = "success"
            status = 201
        except:
            ret['message'] = "bad request"
            status = 400

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response


@api.resource('/<int:id>')
class ForumPost(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        ret = {}

        post = Forum.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            (ret['message'], ret['data']) = post.dict()
            status = 200 if ret['message'] == "success" else 500

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response


    def put(self, id):
        ret = {}
        data = json.loads(request.get_data())

        post = Forum.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            try:
                ret['message'] = post.update(title=data['title'], content=data['content'])
                status = 200 if ret['message'] == "success" else 500
            except:
                ret['message'] = "bad request"
                status = 400

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response


    def patch(self, id):
        ret = {}
        data = json.loads(request.get_data())

        post = Forum.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            try:
                if data['type'] == "title":
                    ret['message'] = post.update(title=data['title'])
                    status = 200 if ret['message'] == "success" else 500
                elif data['type'] == "content":
                    ret['message'] = post.update(content=data['content'])
                    status = 200 if ret['message'] == "success" else 500
                else:
                    ret['message'] = "unknown error"
                    status = 500
            except:
                ret['message'] = "bad request"
                status = 400

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response


    def delete(self, id):
        ret = {}

        post = Forum.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            try:
                db.session.delete(post)
                db.session.commit()
                ret['message'] = "success"
                status = 200
            except:
                ret['message'] = "bad request"
                status = 400

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response
