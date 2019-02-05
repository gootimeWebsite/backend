from app import db, app
from .forum.models import Permission as ForumPermission
from .article.models import Permission as ArticlePermission
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from datetime import datetime, timedelta
import random


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_charset' : 'utf8'
    }

    username = db.Column(db.String(25), primary_key=True, unique=True, nullable=False)
    phonenumber = db.Column(db.String(11), unique=True, nullable=True)
    weixin = db.Column(db.String(30), unique=True, nullable=True)
    qq = db.Column(db.String(12), unique=True, nullable=True)
    articles = db.relationship('Article', backref='Auther', lazy='dynamic')
    article_roleID = db.Column(db.Integer, db.ForeignKey('article_roles.id', ondelete="CASCADE", onupdate="CASCADE"))
    forums = db.relationship('Forum', backref='Auther', lazy='dynamic')
    forum_roleID = db.Column(db.Integer, db.ForeignKey('forum_roles.id', ondelete="CASCADE", onupdate="CASCADE"))
    rand = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return '<Username %r>' % self.username

    def generate_auth_token(self, lifetime=app.config['LIFE_TIME']):
        s = Serializer(app.config['SECRET_KEY'], expires_in = lifetime)
        if lifetime == app.config['LIFE_TIME']:
            self.rand = random.randint(1, 9999)
            db.session.add(self)
            db.session.commit()
        return s.dumps({'username':self.username, 'lifetime':lifetime, 'rand':self.rand})

    @staticmethod
    def verify_auth_token(token, refresh=False):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['username'])
        if not refresh and user.rand != data['rand']:
            return None
        return user

    def forum_can(self, p):
        return self.forum_role is not None and self.forum_role.has_permission(p)

    def forum_is_administrator(self):
        return self.forum_can(ForumPermission.ADMINISTER)

    def article_can(self, p):
        return self.article_role is not None and self.article_role.has_permission(p)

    def article_is_administrator(self):
        return self.article_can(ArticlePermission.ADMINISTER)


class Messages(db.Model):
    __tablename__ = 'messages'
    __table_args__ = {
        'mysql_charset' : 'utf8'
    }

    phonenumber = db.Column(db.String(11), primary_key=True, unique=True, nullable=False)
    message = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return '<Phonenumber %r>' % self.phonenumber
