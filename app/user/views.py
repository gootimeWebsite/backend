# -*- coding: UTF-8 -*-
from flask import *
from flask_restful import Resource
from . import user, api, logger
from app import auth

@api.resource('/')
class UserInfo(Resource):
    decorators = [auth.login_required]

    def get(self):
        return "GET UserInfo!"

    def put(self):
        return "PUT UserInfo!"
