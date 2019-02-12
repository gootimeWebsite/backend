from flask import *
from .models import Permission
from functools import wraps

def permission_required(p):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user.article_can(p):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
