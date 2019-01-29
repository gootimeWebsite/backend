from app import db



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

    def __repr__(self):
        return '<Username %r>' % self.username


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
