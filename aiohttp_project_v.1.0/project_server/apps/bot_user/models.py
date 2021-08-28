from sqlalchemy import DateTime, Time

from store.gino import db


class User(db.Model):
    __tablename__ = "users"

    def __init__(self, **kw):
        super().__init__(**kw)
        self._subscriptions = {}

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    chat_id = db.Column(db.Integer())
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    created = db.Column(DateTime)
    is_banned = db.Column(db.String(8))

    @property
    def subscriptions(self):
        return self._subscriptions


class Subscriptions(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    tag = db.Column(db.String(64))
    schedule = db.Column(Time)
    last_update = db.Column(DateTime)
