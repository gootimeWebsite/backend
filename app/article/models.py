from app import db
from datetime import datetime, timedelta

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
