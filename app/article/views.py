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
            ret['message'] = "not found error"
            status = 404
        else:
            ret_article['auther'] = post.auther
            ret_article['title'] = post.title
            ret_article['content'] = post.content
            ret_article['category'] = post.category
            ret_article['updatetime'] = post.updatetime
            ret['message'] = "success"
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
            ret['message'] = "request error"
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
                ret['message'] = "put error"
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
            ret['message'] = "request error"
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
                ret['message'] = "patch error"
                status = 400

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response

    def delete(self,id):
        ret = {}

        post = Article.query.filter_by(id=id).first()
        if post is None:
            ret['message'] = "not found error"
            status = 404
        else:
            try:
                db.session.delete(post)
                db.session.commit()
                ret['message'] = "success"
                status = 200
            except:
                ret['message'] = "delete error"
                status = 400

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response
    
    
@api.resource('/')
class Article1(Resource):
    decorators = [auth.login_required]
    def get(self):
        ret = {}
        ret_article=[]
        post = Article.query.all()
        if post is None or post == []:
            ret['message'] = "not found error"
            status = 404
        else:
            ret['message'] = "success"
            for item in post:
                ret_article.append({"auther":item.auther,"title":item.title,"content":item.content,"category":item.category,"updatetime":item.updatetime})
                ret['data'] = ret_article
            status = 200

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response
    def post(self):
        ret = {}
        ret_article={}
        data = json.loads(request.get_data())
        try:
            title = data['title']
            auther = data['auther']
            category = data['category']
            content = str(data['content'])
            
            article = Article(title=title,auther=auther,category=category,content=content)

            db.session.add(article)
            db.session.commit()
            ret_article['auther'] = auther
            ret_article['title'] = title
            ret_article['content'] = content
            ret_article['category'] = category
            ret['message'] = "success"
            ret['data'] = ret_article
            status = 201
        except:
            status = 400
            ret['message'] = "post error"

        response = make_response(json.dumps(ret))
        response.headers['Content-Type'] = 'application/json;charset=utf8'
        response.status_code = status
        return response
