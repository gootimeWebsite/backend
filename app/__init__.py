from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, use_native_unicode="utf8")

from .user import user as user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

from app import views, models
