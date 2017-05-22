import os
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired) # for creating tokens


from datetime import datetime
from app.config import app_config
from app import db


class User(db.Model):
    """for each user w the username and password is stored"""

    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(254), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.hash_password(password)
        self.email = email

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

    def generate_auth_token(self, expiration=3600):
        serializer = Serializer(os.getenv('SECRET_KEY'), expires_in=expiration)
        token = serializer.dumps({"user_id": self.user_id})
        return token

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(os.getenv('SECRET_KEY'))
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            # When token is valid but expired
            return None
        except BadSignature:
            # invalid token
            return None
        user = User.query.get(data["user_id"])
        return user

    def __repr__(self):
        return "<User: {}>" .format(self.username)


class Bucketlist(db.Model):
    """this class models the bucketlist table"""
    __tablename__ = 'bucketlist'

    bucketlist_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(254))

    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=datetime.now)
    created_by = db.Column(db.Integer,
                           db.ForeignKey('user.user_id'))
    user = db.relationship('User')
    items = db.relationship('BucketListItems')

    def __repr__(self):
        """returning a printable version for the object"""
        return "<Bucketlist: {}>".format(self.title)


class BucketListItems(db.Model):
    """ Models for Items"""
    __tablename__ = 'bucketlistitems'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, onupdate=datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('User')
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.bucketlist_id',
                                                        ondelete='CASCADE'))
    is_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Bucketlist Item {}>'.format(self.title)


def save(record):
    db.session.add(record)
    db.session.commit()


def delete(record):
    db.session.delete(record)
    db.session.commit()


def update():
    db.session.commit()


