from app import db

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_charset':'utf8'
    }

    username = db.Column(db.String(25), primary_key=True, unique=True, nullable=False)
    phonenumber = db.Column(db.String(11), unique=True, nullable=True)
    weixin = db.Column(db.String(30), unique=True, nullable=True)
    qq = db.Column(db.String(12), unique=True, nullable=True)

    def __repr__(self):
        return '<Username %r>' % self.username


class Messages(db.Model):
    __tablename__ = 'messages'
    __table_args__ = {
        'mysql_charset':'utf8'
    }
    phonenumber = db.Column(db.String(11), primary_key=True, unique=True, nullable=False)
    message = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return '<Phonenumber %r>' % self.phonenumber
