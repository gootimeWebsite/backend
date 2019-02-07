# -*- coding: UTF-8 -*-
from flask import *
from flask_restful import Resource
from . import article, api
from app import auth
from .models import Article, db
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
@api.resource('/<int:id>')
class ArticleInfo(Resource):
    decorators = [auth.login_required]

    '''
    lzm完成
    '''
    def get(self,id):
        ret = {}
        ret_article={}
        post = Article.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "not found"
            status = 404
        else:
            ret_article['auther'] = post.auther
            ret_article['title'] = post.title
            ret_article['content'] = post.content
            ret_article['category'] = post.category
            ret_article['updatetime'] = post.updatetime
            ret['message'] = "found"
            ret['data'] = ret_article
            status = 200

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response
        

    def put(self,id):
        ret = {}
        data = json.loads(request.get_data())
        ret_article={}
        post = Article.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            try:
                post.title = data['title']
                post.auther = data['auther']
                post.category = data['category']
                post.content = data['content']
                ret_article['auther'] = data['auther']
                ret_article['title'] = data['title']
                ret_article['content'] = data['content']
                ret_article['category'] = data['category']
                post.updatetime = datetime.now()+timedelta(hours=8)                
                db.session.commit()
                status = 200 
                ret['data'] = ret_article
                ret['message'] = "success"
            except:
                ret['message'] = "fail"
                status = 400

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response

    def patch(self,id):
        ret = {}
        data = json.loads(request.get_data())
        ret_article={}
        post = Article.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "post not found"
            status = 404
        else:
            try:
                if data.__contains__('title'):
                    post.title = data['title']
                if data.__contains__('auther'):
                    post.auther = data['auther']
                if data.__contains__('category'):
                    post.category = data['category']
                if data.__contains__('content'):
                    post.content = data['content']
                ret_article['auther'] = post.auther
                ret_article['title'] = post.title
                ret_article['content'] = post.content
                ret_article['category'] = post.category
                post.updatetime = datetime.now()+timedelta(hours=8)                
                db.session.commit()
                status = 200 
                ret['data'] = ret_article
                ret['message'] = "success"
            except:
                ret['message'] = "fail"
                status = 400

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response

    def delete(self,id):
        ret = {}

        post = Article.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "not found"
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
