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
            return None


    def verify(self, username):
        """
        0 : 验证成功
        1 : 用户不存在
        2 : 未知错误
        """
        try:
            user = User.query.filter_by(username=username).first()
            if user is None:
                return 1
            return 0
        except:
            return 2


    def delete(self, user):
        try:
            db.session.delete(user)
            db.session.commit()
            return "success"
        except:
            return "error"


usermanager = UserManager()
