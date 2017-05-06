from app import db


class Bucketlist(db.Model):
    """this class models the bucketlist table"""
    __tablename__ = 'bucketlist'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(225))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    done = db.Column(db.DateTime,default=False)

    def __init__(self, title):
        """title of the bucket list.Initialize class"""
        self.title = title

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
        return "<Bucklist: {}>".format(self.title)