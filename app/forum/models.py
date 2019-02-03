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
