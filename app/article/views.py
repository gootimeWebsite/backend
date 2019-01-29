# -*- coding: UTF-8 -*-
from flask import *
from flask_restful import Resource
from . import article, api
from app import auth

@api.resource('/')
class ArticleInfo(Resource):
    decorators = [auth.login_required]

    '''
    lzm完成
    '''
    def get(self):
        return "GET ArticleInfo!"

    def post(self):
        return "POST ArticleInfo!"

    def put(self):
        return "PUT ArticleInfo!"

    def patch(self):
        return "PATCH ArticleInfo!"

    def delete(self):
        return "DELETE ArticleInfo!"
