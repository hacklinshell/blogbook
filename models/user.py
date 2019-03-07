from datetime import datetime
from model import db

class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False, index=True, default="")
    nickname = db.Column(db.String(255), nullable = False, default="")
    password =  db.Column(db.String(255), default="")
    avatar = db.Column(db.String(255),  default="")
    updatetime = db.Column(db.DateTime, default = datetime.now, nullable=False)
    timestamp = db.Column(db.DateTime, default = datetime.now, nullable=False)
    books = db.relationship("Book", backref="user", lazy="dynamic")
     