from flask import g
from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource, reqparse, marshal, fields

from app import db
from app.models import User, BucketListItems, Bucketlist

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    # authenticate by token
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


class RegisterAPI(Resource):
    """
    Register a new user. URL: /api/v1/auth/register/
    Request method: POST
    """

    def __init__(self):
        """initializing parsers"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='username cannot be blank', location='json')

        self.reqparse.add_argument('password', required=True, help='password cannot be blank',
                                   location='json')
        super(RegisterAPI, self).__init__()

    def post(self):
        """parsing and validating a request"""
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']

        # check if parameters are null
        if username == "" or password == "":
            return {'message': 'cannot send an empty entry'}, 400

        if User.query.filter_by(username=username).first() is not None:
            #  status code - request accepted but not processed

            return {
                'message': 'username exists'}, 202

        new_user = User(username=username, password=password)
        new_user.hash_password(password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'account created'}, 201


class LoginAPI(Resource):
    """
    User login URL: /api/v1/auth/login/
    Request method: POST
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='username cannot be blank', location='json')
        self.reqparse.add_argument('password', required=True,
                                   help='password cannot be blank', location='json')
        super(LoginAPI, self).__init__()

    def post(self):
        """Log a user in and return an authentication token."""
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']

        if password == "" or username == "":
            # bad request
            return {'error': "Username or Password can't be empty"}, 400
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            token = user.generate_auth_token().decode("utf-8")
            return {'token': token}, 200

        # status code - unauthorised
        return {'error': 'invalid username or password'}, 401


bucketlist_items_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.String,
    'date_modified': fields.String,
    'done': fields.Boolean,
}

bucketlist_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.String,
    'date_modified': fields.String,
    'bucketlist_items': fields.Nested(bucketlist_items_fields),
    'created_by': fields.String
}

# users_fields = {
#     'user_id': fields.Integer,
#     'username': fields.String,
#     'bucketlists': fields.Nested(bucketlist_fields)
# }


class BucketlistsAPI(Resource):
    """this resource shows all and adds bucketlists."""
    decorators = [auth.login_required]

    def post(self, bucketlist_id):
        """create a new bucketlist"""

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help="Bucket list title cannot be empty")
        self.reqparse.add_argument(
            'description', type=str, default="")

        args = self.reqparse.parse_args()
        title = args['title']
        description = args['description']
        user_id = g.user.user_id
        if title == "":
            # bad request status
            return {'error': "Bucket list title cannot be empty"}, 400

        if Bucketlist.query.filter_by(title=title, created_by=user_id).first() is not None:
            # accepted status but cannot be created
            return {'message': 'The bucket list already exists'}, 202
        bucketlist = Bucketlist(title=title, description=description, created_by=user_id)
        db.session.add(bucketlist)
        db.session.commit()
        # created
        return {'message': 'bucketlist created successfuly'}, 201

    def get(self):
        """ View all bucketlists"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('page', location="args", type=int, required=False, default=1)
        self.reqparse.add_argument('limit', location="args", type=int, required=False, default=20)
        self.reqparse.add_argument('q', location="args", required=False)

        user_id = g.user.user_id
        args = self.reqparse.parse_args()
        page = args['page']
        limit = args['limit']
        search = args['q']

        if limit > 100:
            limit = 100

        if search:
            bucketlists = Bucketlist.query.filter(
                Bucketlist.created_by == user_id,
                Bucketlist.title.like('%' + search + '%')).paginate(page=page, per_page=limit, error_out=False)
            if bucketlists:
                total = bucketlists.pages
                bucketlists = bucketlists.items
                response = {'bucketlists': marshal(bucketlists, BucketlistsAPI),
                            'pages': total}
                return response
            else:
                # not found status
                return {'message': "Bucketlist not found"}, 404

        bucketlists = Bucketlist.query.filter_by(created_by=user_id).paginate(
            page=page,per_page=limit,error_out=False)

        total = bucketlists.pages
        bucketlists = bucketlists.items

        response = {'bucketlists': marshal(bucketlists, bucketlist_fields),
                    'pages': total,
                    'url': "http://address/api/v1.0/bucketlists/?page=",
                    'search': "http://address/api/v1.0/bucketlists/?q="
                    }
        return response


class BucketlistAPI(Resource):
    decorators = [auth.login_required]

    def get(self, bucketlist_id):
        """ view a single bucket list"""
        user_id = g.user.user_id
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id,
                                                created_by=user_id).first()

        if bucketlist:
            # if bucketlist exists :status code ok
            return marshal(bucketlist, bucketlist_fields), 200
            # if not return not found

        return {'error': "BucketList not found."}, 404

    def put(self, bucketlist_id):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', location='json')

        user_id = g.user.user_id
        args = self.reqparse.parse_args()
        # check if the bucket list exists
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id,
                                                created_by=user_id).first()

        if not bucketlist:
            return {'error': 'Bucket list not found'}, 404

        if args.title:
            bucketlist.title = args.title
        if args.description:
            bucketlist.description = args.description
        db.session.commit()
        return {'message': 'Bucket list updated succcessfully'}

    def delete(self, bucketlist_id):
        user_id = g.user.user_id
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id,
                                                created_by=user_id).first()
        # check if bucket exists
        if bucketlist:
            db.session.delete(bucketlist)
            db.session.commit()
            return {'message': 'bucket list deleted'}
        # not found status
        return {'error': "Bucket list not found"}, 404


class BucketlistItemsAPI(Resource):
    decorators = [auth.login_required]

    def get(self, bucketlist_id):
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            return {'error': "Bucket list not found."}, 404
        bucketlist_items = BucketListItems.query.filter_by(bucketlist_id=bucketlist_id).all()
        if not bucketlist_items:
            return {'message': "No Items created yet"}

        return {'items': marshal_with(bucketlist_items, bucketlist_items_fields)}

    def delete(self):
        pass


class BucketlistItemAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

