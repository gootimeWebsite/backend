# -*- coding: UTF-8 -*-
from flask import *
from . import user

@user.route('/', methods = ['GET', 'POST'])
def user_info():
    pass
