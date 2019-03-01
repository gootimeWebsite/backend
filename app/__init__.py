# -*- coding: UTF-8 -*-
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth

import os
import sys
import logging
import logging.handlers
from logging.handlers import TimedRotatingFileHandler, SMTPHandler

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, use_native_unicode="utf8")
auth = HTTPTokenAuth()
api = Api(app)
logger = logging.getLogger("flask.app")

logFormatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s")
logger.setLevel(logging.DEBUG)
#logger.handlers = []

fileHandler = TimedRotatingFileHandler(filename="./log/server.log", when='d', interval=1, backupCount=7)
fileHandler.suffix = "%Y-%m-%d-%H-%M.log"
fileHandler.setLevel(level=logging.DEBUG)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(level=logging.ERROR)
streamHandler.setFormatter(logFormatter)
logger.addHandler(streamHandler)

credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
mailHandler = SMTPHandler(
    secure = (),
    mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    fromaddr = 'lixinlong@gootian.com',
    toaddrs = '1298939544@qq.com',
    subject = 'Your Application Failed',
    credentials = credentials
)

mailHandler.setFormatter(logging.Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
'''))
mailHandler.setLevel(logging.ERROR)
logger.addHandler(mailHandler)

from .user import user as user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

from .article import article as article_blueprint
app.register_blueprint(article_blueprint, url_prefix='/article')

from .forum import forum as forum_blueprint
app.register_blueprint(forum_blueprint, url_prefix='/forum')

from app import views, models, error
