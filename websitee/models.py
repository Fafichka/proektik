from sqlalchemy import func
from . import db
from flask_login import UserMixin


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    date_join = db.Column(db.DateTime(timezone=True), default=func.now())
    new_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    ava = db.relationship('Userava')


class Userava(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(150000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))