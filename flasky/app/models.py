from datetime import datetime
from . import db

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(64))
    img = db.Column(db.String(64))
    title = db.Column(db.Text)
    url = db.Column(db.Text)
    html = db.Column(db.Text)
    classify = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

