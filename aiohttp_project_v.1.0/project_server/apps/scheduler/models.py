from sqlalchemy import DateTime, ARRAY, String

from store.gino import db


class Article(db.Model):
    __tablename__ = "article"

    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(128))
    date = db.Column(DateTime)
    tag = db.Column(ARRAY(String(64)))
