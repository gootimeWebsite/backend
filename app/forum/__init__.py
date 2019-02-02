from flask import Blueprint
from flask_restful import Resource, Api

forum = Blueprint('forum', __name__)
api = Api(forum)

from . import views, models, views
