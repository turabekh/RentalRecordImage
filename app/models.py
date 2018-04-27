from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask_login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),
                      nullable=False, unique=True, index=True)
    username = db.Column(db.String(64),
                         nullable=False, unique=True, index=True)
    is_agent = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    bio = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    checkins = db.relationship('Checkin', lazy='dynamic', backref='customer')
    checkouts = db.relationship('Checkout', lazy='dynamic', backref='customer')
    messages = db.relationship('Message', lazy='dynamic', backref='customer')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or \
               hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Checkin(db.Model):
    __tablename__ = "checkins"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    car_number = db.Column(db.String(128),
                      nullable=False, index=True)
    agent_name = db.Column(db.String(128), nullable=True)
    add_info = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    photo_1 = db.Column(db.String(255))
    photo_2 = db.Column(db.String(255))
    photo_3 = db.Column(db.String(255))
    photo_4 = db.Column(db.String(255))
    photo_5 = db.Column(db.String(255))
    photo_6 = db.Column(db.String(255))

class Checkout(db.Model):
    __tablename__ = "checkouts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    car_number = db.Column(db.String(128),
                      nullable=False, index=True)
    agent_name = db.Column(db.String(128), nullable=True)
    add_info = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    photo_1 = db.Column(db.String(255))
    photo_2 = db.Column(db.String(255))
    photo_3 = db.Column(db.String(255))
    photo_4 = db.Column(db.String(255))
    photo_5 = db.Column(db.String(255))
    photo_6 = db.Column(db.String(255))
    

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    content = db.Column(db.Text())





