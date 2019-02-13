from ..models import User, db
from ..forum.models import ForumRole
from ..article.models import ArticleRole
import json

class UserManager:

    def __init__(self):
        pass


    def dict(self, user):
        ret = {}
        try:
            ret['username'] = user.username
            ret['phonenumber'] = user.phonenumber
            ret['weixin'] = user.weixin
            ret['qq'] = user.qq
            ret['status'] = "success"
        except:
            logger.error("User.dict()", exc_info = True)
            ret['status'] = "error"
        return ret


    def insert(self, username, phonenumber, weixin, qq, default=True):
        try:
            if default:
                article_role = ArticleRole.query.filter_by(default=True).first()
                forum_role = ForumRole.query.filter_by(default=True).first()
                user = User(username=username, phonenumber=phonenumber, weixin=weixin, qq=qq, article_roleID=article_role.id, forum_roleID=forum_role.id)
            else:
                user = User(username=username, phonenumber=phonenumber, weixin=weixin, qq=qq)
            db.session.add(user)
            db.session.commit()
            return user
        except:
            logger.error("User.insert()", exc_info = True)
            return None


    def update(self, user, username, phonenumber, weixin, qq):
        try:
            user.username = username
            user.phonenumber = phonenumber
            user.weixin = weixin
            user.qq = qq
            db.session.add(user)
            db.session.commit()
            return "success"
        except:
            logger.error("User.update()", exc_info = True)
            return "error"


    def search(self, data, type):
        try:
            if type == "username":
                user = User.query.filter_by(username=data).first()
            elif type == "phonenumber":
                user = User.query.filter_by(phonenumber=data).first()
            elif type == "weixin":
                user = User.query.filter_by(weixin=data).first()
            elif type == "qq":
                user = User.query.filter_by(qq=data).first()
            else:
                return None
            return user
        except:
            logger.error("User.search()", exc_info = True)
            return None


    def delete(self, user):
        try:
            db.session.delete(user)
            db.session.commit()
            return "success"
        except:
            logger.error("User.delete()", exc_info = True)
            return "error"


usermanager = UserManager()
