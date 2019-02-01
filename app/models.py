from app import db, app
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
    rulesID = db.Column(db.Integer, db.ForeignKey('rules.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False, default=1)
    articles = db.relationship('Article', backref='Auther', lazy='dynamic')
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


class Rules(db.Model):
    __tablename__ = 'rules'
    __table_args__ = {
        'mysql_charset' : 'utf8'
    }

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user = db.relationship('User', backref='rules', lazy='dynamic')

    def __repr__(self):
        return '<ID %r>' % self.id


class Access(db.Model):
    __tablename__ = 'access'
    __table_args__ = {
        'mysql_charset' : 'utf8'
    }

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    action = db.Column(db.Text, nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<ID %r>' % self.id


class Messages(db.Model):
    __tablename__ = 'messages'
    __table_args__ = {
        'mysql_charset' : 'utf8'
    }

    phonenumber = db.Column(db.String(11), primary_key=True, unique=True, nullable=False)
    message = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return '<Phonenumber %r>' % self.phonenumber


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
    updatetime = db.Column(db.DateTime, default=datetime.now()+timedelta(hours=8))

    def __repr__(self):
        return '<ID %r>' % self.id
