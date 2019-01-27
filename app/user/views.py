# -*- coding: UTF-8 -*-
from flask import *
from . import user

@user.route('/login', methods = ['GET', 'POST'])
def login():
    pass


@user.route('/register', methods = ['GET', 'POST'])
def login():
    pass
