# -*- coding: UTF-8 -*-
from app import db
from datetime import datetime

class Article(db.Model):
    __tablename__ = 'article'
    __table_args__ = {
        'mysql_charset' : 'utf8'
    }

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    auther = db.Column(db.String(25), db.ForeignKey('user.username', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    category = db.Column(db.String(50), unique=False, nullable=True)
    content = db.Column(db.Text, nullable=False)
    updatetime = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<ID %r>' % self.id


class Permission:
    POST = 0x0001               #发表文章
    LIKE = 0x0002               #点赞
    COMMENT = 0x0004            #评论
    MANAGE_COMMENT = 0x0008     #管理评论
    ADMINISTER = 0x8000         #管理员


class ArticleRole(db.Model):
    __tablename__ = 'article_roles'
    __table_args__ = {
        'mysql_charset' : 'utf8'
    }

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(64), unique=True, nullable=False)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer, default=0)
    users = db.relationship('User', backref='article_role', lazy='dynamic')

    def __repr__(self):
        return '<ArticleRole %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User' : [Permission.POST, Permission.LIKE, Permission.COMMENT],
            'Administrator' : [Permission.POST, Permission.LIKE, Permission.COMMENT, Permission.MANAGE_COMMENT, Permission.ADMINISTER]
        }

        default_role = 'User'
        for r in roles:
            role = ArticleRole.query.filter_by(name=r).first()
            if role is None:
                role = ArticleRole(name=r)
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
