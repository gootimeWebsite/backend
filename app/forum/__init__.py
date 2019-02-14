# -*- coding: UTF-8 -*-
from flask import Blueprint
from flask_restful import Resource, Api
import logging

forum = Blueprint('forum', __name__)
api = Api(forum)
logger = logging.getLogger("flask.app.forum")

from . import views, models, views, utils
