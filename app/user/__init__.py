from flask import Blueprint
from flask_restful import Resource, Api

user = Blueprint('user', __name__)
api = Api(user)

from . import views, manager
