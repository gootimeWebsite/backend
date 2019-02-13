from flask import Blueprint
from flask_restful import Resource, Api
import logging

user = Blueprint('user', __name__)
api = Api(user)
logger = logging.getLogger("flask.app.user")

from . import views, manager
