from sqlalchemy import DateTime

from store.gino import db


class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    first_name = db.Column(
        db.String(64),
    )
    last_name = db.Column(
        db.String(64),
    )
    created = db.Column(DateTime)


class Session(db.Model):
    __tablename__ = "session"

    id = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(64), nullable=False)
