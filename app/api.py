from flask import g
from flask_httpauth import HTTPTokenAuth

from flask_restful import Resource, reqparse, marshal, fields
from app import db

from app.models import User, BucketListItems, Bucketlist
from app.models import save, delete


auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    # authenticate by token
    user = User.verify_auth_token(token)
    if user:
        g.user = user
        return True
    return False


class RegisterAPI(Resource):
    """
    Register a new user. URL: /api/v1/auth/register/
    Request method: POST
    """

    def __init__(self):
        """initializing parsers"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='username is blank')
        self.reqparse.add_argument('email', type=str, required=True,
                                   help='email is blank')

        self.reqparse.add_argument('password', required=True, help='password is blank')
        super(RegisterAPI, self).__init__()

    def post(self):
        """parsing and validating a request"""
        args = self.reqparse.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']
        # check if user already exists

        if username == "":
            return {'message': 'username cannot be empty'}, 400
        if password == "":
            return {'message': 'password cannot be empty'}, 400
        if email == "":
            return {'message': 'email cannot be empty'}, 400

        if User.query.filter_by(email=email).first() is not None:
            return {'message': 'email exists'}, 202
        if User.query.filter_by(username=username).first() is not None:
            #  status code - request accepted but not processed
            return {
                'message': 'username exists'}, 202

        user = User(username='username',email='email', password='password')
        user.hash_password(password)
        save(user)
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
        if username and password:
            user = User.query.filter_by(username=username).first()
        else:
            return {"error": "please enter a username and password."}, 400

        if user and user.verify_password(password):
            token = user.generate_auth_token()
            return {'message': 'login successful', 'token': token.decode('utf-8')}, 200
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

user_fields = {
    'user_id': fields.Integer,
    'username': fields.String,
    'bucketlists': fields.Nested(bucketlist_fields)
}


class BucketlistsAPI(Resource):
    """this resource shows all and adds bucketlists."""
    # decorators = [auth.login_required]

    def post(self):
        """create a new bucketlist"""

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help="Bucket list title cannot be empty")
        self.reqparse.add_argument(
            'description', type=str, default="")

        args = self.reqparse.parse_args()
        title = args['title']
        description = args['description']

        if title == "":
            # bad request status
            return {'error': "Bucket list title cannot be empty"}, 400

        if Bucketlist.query.filter_by(title=title, created_by=g.user.id).first() is not None:

            return {'message': 'The bucket list already exists'}, 400
        bucketlist = Bucketlist(title=title, description=description, created_by=g.user.id)
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
    # decorators = [auth.login_required]

    def get(self, id):
        """ view a single bucket list"""
        user_id = g.user.id
        bucketlist = Bucketlist.query.filter_by(id=id,
                                                created_by=user_id).first()

        if bucketlist:
            # bucketlist exists return status code ok
            return marshal(bucketlist, bucketlist_fields), 200
            # if not, return not found 404

        return {'error': "BucketList not found."}, 404

    def put(self, id):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', location='json')

        user_id = g.user.id
        args = self.reqparse.parse_args()
        # check if the bucket list exists
        bucketlist = Bucketlist.query.filter_by(id=id,
                                                created_by=user_id).first()

        if not bucketlist:
            return {'error': 'Bucket list not found'}, 404

        if args.title:
            bucketlist.title = args.title
        if args.description:
            bucketlist.description = args.description
        db.session.commit()
        return {'message': 'Bucket list updated successfully'}

    def delete(self, id):
        user_id = g.user.user_id
        bucketlist = Bucketlist.query.filter_by(id=id,
                                                created_by=user_id).first()
        # check if bucket list exists
        if bucketlist:
            delete(bucketlist)
            return {'message': 'bucket list deleted'}
        # if not found  return status 404
        return {'error': "Bucket list not found"}, 404


class BucketlistItemsAPI(Resource):
    # decorators = [auth.login_required]

    def get(self, id):
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            return {'error': "Bucket list not found."}, 404
        bucketlist_items = BucketListItems.query.filter_by(id=id).all()
        if not bucketlist_items:
            return {'message': "No Items created yet"}

        return {'items': marshal(bucketlist_items, bucketlist_items_fields)}


class BucketlistItemAPI(Resource):
    # decorators = [auth.login_required]

    def get(self, id, item_id):
        # check if bucketlist exists
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            # status code - not found
            return {'error': "bucketlist not found"}, 404

        bucketlist_item = BucketListItems.query.filter_by(id=id, item_id=item_id).first()

        if bucketlist_item:
            # status code - ok
            return marshal(bucketlist_item, bucketlist_items_fields), 200

            # else status code - not found
        return {'error': "BucketListItem with id {} not found.".format(item_id)}, 404

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

