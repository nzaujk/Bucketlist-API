from datetime import datetime
import os
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import app_config
from app import db


class User(db.Model):
    """for each user w the username and password is stored"""
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.hash_password(password)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(password, self.password_hash)

    def generate_auth_token(self, expiration=1024):
        serializer = Serializer(os.getenv('SECRET'), expires_in=expiration)

        return serializer.dumps({'username': self.username})

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(app_config['SECRET'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            # When token is valid but expired
            return None
        except BadSignature:
            # invalid token
            return None
        user = User.query.get(data['user_id'])
        return user

    def __repr__(self):
        return '<user_id>'.format(self.user_id)


class Bucketlist(db.Model):
    """this class models the bucketlist table"""
    __tablename__ = 'bucketlist'

    bucketlist_id = db.Column(db.Integer,nullable=False, primary_key=True,autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(254))

    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=datetime.now)
    created_by = db.Column(db.Integer,
                           db.ForeignKey("user.user_id"))
    items = db.relationship('BucketListItems',
                            backref='bucketlist',
                            passive_deletes=True)

    def __repr__(self):
        """returning a printable version for the object"""
        return "<Bucketlist: {}>".format(self.title)


class BucketListItems(db.Model):
    """ Models for Items"""
    __tablename__ = "bucketlistitems"
    items_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, onupdate=datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlist.bucketlist_id",
                                                        ondelete='CASCADE'),nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Bucketlist Item {}>".format(self.title)
