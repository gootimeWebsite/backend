from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, use_native_unicode="utf8")
auth = HTTPTokenAuth()
api = Api(app)

from .user import user as user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

from .article import article as article_blueprint
app.register_blueprint(article_blueprint, url_prefix='/article')

from .forum import forum as forum_blueprint
app.register_blueprint(forum_blueprint, url_prefix='/forum')

from app import views, models, access
