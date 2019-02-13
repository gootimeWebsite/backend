from flask import Blueprint
from flask_restful import Resource, Api
import logging

article = Blueprint('article', __name__)
api = Api(article)
logger = logging.getLogger("flask.app.article")

from . import views, models, views, utils
