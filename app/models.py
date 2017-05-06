from app import db
from passlib.apps import custom_app_context as pwd_context

from app import db


class User(db.Model):
    """for each user w the username and password is stored
    the passord is encrypted with passlib module"""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        """the function takes a plain password as argument
        stores a hash of it with the user."""
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """takes a plain password as argument and returns True
        if the password is correct"""
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<user_id {}>'.format(self.user_id)


class Bucketlist(db.Model):
    """this class models the bucketlist table"""
    __tablename__ = 'bucketlist'

    bucketlist_id = db.Column(db.Integer,nullable=False, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer,
                           db.ForeignKey("users.user_id",
                                         ondelete='CASCADE'), nullable=False)
    items = db.relationship('BucketListItems',
                            backref='bucketlist',
                            passive_deletes=True)

    def __init__(self, name):
        """title of the bucket list.Initialize class"""
        self.name = name

    def save(self):
        """add new bucketlist to the database."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """get all the bucketlists in a single query"""
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """returning a printable version for the object"""
        return "<Bucketlist: {}>".format(self.name)


class BucketListItems(db.Model):
    """ Models for Items"""
    __tablename__ = "bucketlistitems"
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        "bucketlist.bucketlist_id", ondelete='CASCADE'), nullable=False)

    status = db.Column(db.Boolean,default=False)