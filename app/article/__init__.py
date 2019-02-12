from flask import Blueprint
from flask_restful import Resource, Api

article = Blueprint('article', __name__)
api = Api(article)

from . import views, models, views, utils
