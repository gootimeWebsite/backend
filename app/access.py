from app import db
from .models import Access
from flask import request

class AccessManager:

    def __init__(self):
        pass


    def auth(self, id, method, path):
        action = method + " " + path
        access = Access.query.filter_by(action=action).first()
        if access is None or access.rank > id:
            return False
        return True


accessmanager = AccessManager()
