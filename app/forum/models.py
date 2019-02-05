from app import db
from datetime import datetime, timedelta
import random

class Forum(db.Model):
    __tablename__ = 'forum'
    __table_args__ = {
        'mysql_charset' : 'utf8'
    }

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    auther = db.Column(db.String(25), db.ForeignKey('user.username', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    updatetime = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<ID %r>' % self.id

    def dict(self):
        ret = {}
        try:
            ret['id'] = self.id
            ret['title'] = self.title
            ret['auther'] = self.auther
            ret['content'] = self.content
            ret['updatetime'] = self.updatetime
            return ("success", ret)
        except:
            return ("unknown error", ret)

    def insert(self, title, auther, content):
        self.id = random.randint(100000, 999999)
        self.title = title
        self.auther = auther
        self.content = content
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self, title=None, content=None):
        try:
            if title:
                self.title = title
            if content:
                self.content = content
            self.updatetime = datetime.now()
            db.session.add(self)
            db.session.commit()
            return "success"
        except:
            return "unknown error"


class Permission:
    POST = 0x0001               #发帖
    LIKE = 0x0002               #点赞顶帖
    COMMENT = 0x0004            #评论跟帖
    MANAGE_COMMENT = 0x0008     #管理评论
    ADMINISTER = 0x8000         #管理员


class ForumRole(db.Model):
    __tablename__ = 'forum_roles'
    __table_args__ = {
        'mysql_charset' : 'utf8'
    }

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(64), unique=True, nullable=False)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer, default=0)
    users = db.relationship('User', backref='forum_role', lazy='dynamic')

    def __repr__(self):
        return '<ForumRole %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User' : [Permission.POST, Permission.LIKE, Permission.COMMENT],
            'Administrator' : [Permission.POST, Permission.LIKE, Permission.COMMENT, Permission.MANAGE_COMMENT, Permission.ADMINISTER]
        }

        default_role = 'User'
        for r in roles:
            role = ForumRole.query.filter_by(name=r).first()
            if role is None:
                role = ForumRole(name=r)
            role.reset_permissions()
            for p in roles[r]:
                role.add_permissions(p)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def has_permission(self, p):
        return self.permissions & p == p

    def add_permissions(self, p):
        if not self.has_permission(p):
            self.permissions += p

    def remove_permissions(self, p):
        if self.has_permission(p):
            self.permissions -= p

    def reset_permissions(self):
        self.permissions = 0
