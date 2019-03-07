from datetime import datetime
from model import db
from .user import User



class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), default="", nullable=False, index=True)
    access = db.Column(db.Integer, default=1, nullable=False, index=True)
    status = db.Column(db.Integer, default=0, nullable=False,index=True)       # publish status
    brief = db.deferred(db.Column(db.Text, default="", nullable=False))
    select_catalog = db.Column(db.Integer, default=0, nullable=False)
    publish_timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False, index=True)
    updatetime = db.Column(db.DateTime, default=datetime.now, nullable=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False, index=True)
    cover = db.Column(db.String(255), default="", nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id,
        ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    catalogs = db.relationship("BookCatalog", backref="book", lazy="dynamic", passive_deletes=True)


class BookCatalog(db.Model):
    __tablename__ = "bookcatalog"

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    title = db.Column(db.String(255), default="", nullable=False, index=True)
    markdown = db.deferred(db.Column(LONGTEXT, default="", nullable=False))
    html = db.deferred(db.Column(LONGTEXT, default="", nullable=False))
    publish_markdown = db.deferred(db.Column(LONGTEXT, default='', nullable=False))
    publish_html = db.deferred(db.Column(LONGTEXT, default='', nullable=False))
    status = db.Column(db.Integer, default=0, nullable = True, index = True)
    abstract = db.deferred(db.Column(db.String(255), default=""))
    publish_order = db.Column(db.Integer, default=0, nullable=True, index = True)
    pos = db.Column(db.Integer, default=0, nullable=False, index=True)
    parent_id = db.Column(db.Integer, default = 0, nullable=False, index=True)
    is_dir = db.Column(db.Boolean, default = False, nullable=False, index=True)
    publish_timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False, index = True)
    first_publish = db.Column(db.DateTime, default=datetime.now, nullable=False, index = True)
    updatetime = db.Column(db.DateTime, default = datetime.now, nullable=False, index=True)
    timestamp = db.Column(db.DateTime, default = datetime.now, nullable=False, index=True)

    book_id = db.Column(db.Integer, db.ForeignKey(Book.id, 
        ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

