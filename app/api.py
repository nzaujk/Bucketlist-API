from flask import g, request
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
                                   help='username cannot be blank')
        self.reqparse.add_argument('email', type=str, required=True,
                                   help='email cannot be blank')

        self.reqparse.add_argument('password', required=True, help='password cannot be blank')
        super(RegisterAPI, self).__init__()

    def post(self):
        """parsing and validating a request"""
        args = self.reqparse.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']
        # check if user already exists

        if username == "": # if user does not enter a user name
            return {'message': 'username cannot be empty'}, 400
        if password == "":
            return {'message': 'password cannot be empty'}, 400
        if email == "":
            return {'message': 'email cannot be empty'}, 400

        # Allow matching of strings  with ilike to enable string to be case insensitive
        if User.query.filter(User.email.ilike(email)).first():
            return {'message': 'email exists'}, 202
        if User.query.filter(User.username.ilike(username)).first() is not None:
            #  status code - request accepted but not processed
            return {
                'message': 'username exists'}, 202

        user = User(username=username,email=email, password=password)
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
                                   help='username cannot be blank')
        self.reqparse.add_argument('password', type=str, required=True,
                                   help='password cannot be blank')
        super(LoginAPI, self).__init__()

    def post(self):
        """Log a user in and return an authentication token."""
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']
        if username and password:
            user = User.query.filter(username=username).first()
        else:
            return {"error": "please enter a username and password."}, 400

        if user and user.verify_password(password):
            token = user.generate_auth_token()
            return {'message': 'login successful', 'token': token.decode('utf-8')}, 200
        # status code - unauthorised
        return {'error': 'invalid username or password'}, 401


bucketlist_items_fields = {
    'item_id': fields.Integer,
    'item_name': fields.String,
    'date_created': fields.String,
    'date_modified': fields.String,
    'is_done': fields.Boolean,
}

bucketlist_fields = {
    'bucketlist_id': fields.Integer,
    'title': fields.String,
    'date_created': fields.String,
    'date_modified': fields.String,
    'bucketlist_items': fields.Nested(bucketlist_items_fields),
    'created_by': fields.Integer
}

user_fields = {
    'user_id': fields.Integer,
    'username': fields.String,
    'bucketlists': fields.Nested(bucketlist_fields)
}


class BucketlistsAPI(Resource):
    """ Create Bucket list URL: /api/v1/bucketlist
        Request method: POST, GET """
    decorators = [auth.login_required]

    def post(self):
        """create bucket lists"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help="Bucket list title cannot be empty")
        self.reqparse.add_argument(
            'description', type=str, default="")

        args = self.reqparse.parse_args()
        title = args['title']
        description = args['description']

        if title == "":
            # if empty bad request status
            return {'error': "Bucket list title cannot be empty"}, 400

        if Bucketlist.query.filter_by(title=title, created_by=g.user.user_id).first() is not None:

            return {'message': 'the bucket list already exists'}, 400
        bucketlist = Bucketlist(title=title, description=description, created_by=g.user.user_id)
        save(bucketlist)
        return {'message': 'bucketlist created successfuly'}, 201

    def get(self):
        """ view all bucket lists """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('page', location="args", type=int, required=False, default=1)
        self.reqparse.add_argument('limit', location="args", type=int, required=False, default=20)
        self.reqparse.add_argument('q', location="args", required=False)

        args = self.reqparse.parse_args()
        page = args['page']
        limit = args['limit']
        search = args['q']

        if limit > 100:
            limit = 100

        if search:
            bucketlists = Bucketlist.query.filter(Bucketlist.created_by == g.user.user_id,
                            Bucketlist.title.like('%' + search + '%')).paginate(page=page,
                            per_page=limit, error_out=False)
            if bucketlists:
                total = bucketlists.pages
                bucketlists = bucketlists.items
                response = {'bucketlists': marshal(bucketlists, bucketlist_fields),
                            'pages': total}
                return response
            else:
                # not found status
                return {'message': "Bucketlist not found"}, 404

        bucketlists = Bucketlist.query.filter_by(created_by=g.user.user_id).paginate(
            page=page,per_page=limit,error_out=False)
        total = bucketlists.pages
        has_next = bucketlists.has_next
        has_previous = bucketlists.has_prev
        if has_next:
            next_page = str(request.url_root) + "api/v1/bucketlists?" + \
                        "limit=" + str(limit) + "&page=" + str(page + 1)
        else:
            next_page = "None"
        if has_previous:
            previous_page = request.url_root + "api/v1/bucketlists?" + \
                            "limit=" + str(limit) + "&page=" + str(page - 1)
        else:
            previous_page = "None"

        bucketlists = bucketlists.items

        response = {'bucketlists': marshal(bucketlists, bucketlist_fields),
                    'pages': total,
                    "has_next": has_next,
                    "total": total,
                    "previous_page": previous_page,
                    "next_page": next_page,
                    'url': "http://127.0.0.1:5000/api/v1/bucketlists?limit=20",
                    'search': "http://127.0.0.1:5000/api/v1/bucketlists?q="
                    }
        return response


class BucketlistAPI(Resource):

    """ Single bucketlist list URL: /api/v1/bucketlist/<int: bucketlist_id>
            Request method: PUT, GET, DELETE """
    decorators = [auth.login_required]

    def get(self, bucketlist_id):

        """ view a single bucket list"""
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id,
                                                created_by=g.user.user_id).first()

        if bucketlist:
            return marshal(bucketlist, bucketlist_fields), 200

        return {'error': "BucketList not found."}, 404

    def put(self, bucketlist_id):
        """ update bucket list"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', location='json')

        args = self.reqparse.parse_args()
        # check if the bucket list exists
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id,
                                                created_by=g.user.user_id).first()

        if not bucketlist:
            return {'error': 'Bucket list not found'}, 404

        if args.title:
            bucketlist.title = args.title
        if args.description:
            bucketlist.description = args.description
        db.session.commit()
        return {'message': 'Bucket list updated successfully'}

    def delete(self, bucketlist_id):
        """ delete bucket list """
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id,
                                                created_by=g.user.user_id).first()
        if bucketlist:
            delete(bucketlist)
            return {'message': 'bucket list deleted'}
        # if not found  return status 404
        return {'error': "bucket list not found"}, 404


class BucketlistItemsAPI(Resource):
    """ Single bucketlist list URL: /api/v1/bucketlist/<int: bucketlist_id>/items
                Request method: POST GET"""
    decorators = [auth.login_required]

    def get(self, bucketlist_id):
        """view items"""
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            return {'error': "bucket list not found."}, 404
        bucketlist_items = BucketListItems.query.filter_by(bucketlist_id=bucketlist_id).all()
        if not bucketlist_items:
            return {'message': 'no items created yet'}, 202

        return {'items': marshal(bucketlist_items, bucketlist_items_fields)}

    def post(self, bucketlist_id):
        """ add new bucketlist item"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_name', type=str, required=True,
                                   help="item name cannot be blank")
        self.reqparse.add_argument('is_done', type=bool)

        args = self.reqparse.parse_args()
        item_name = args['item_name']
        is_done = args['is_done']

        # check if title is null
        if item_name == "":
            # status code - Bad request
            return {'error': "item name cannot be empty"}, 400

        if Bucketlist.query.filter_by(bucketlist_id=bucketlist_id).first() is None:
            # status code - Not found
            return {'error': 'bucket list  not found'}, 404

        # check if item name exists in bucketlist
        if BucketListItems.query.filter_by(item_name=item_name,
                                           bucketlist_id=bucketlist_id).first() is not None:

            return {'error': 'item already exists in the bucketlist'}, 400

        bucketlist_item = BucketListItems(
            item_name=item_name, bucketlist_id=bucketlist_id, is_done=is_done)
        save(bucketlist_item)

        return {'message': 'item has been added succesfully to bucketlist'}, 201


class BucketlistItemAPI(Resource):
    decorators = [auth.login_required]

    def get(self, bucketlist_id=None, item_id=None):
        # check if bucketlist exists
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            return {'error': "bucketlist not found"}, 404

        bucketlist_item = BucketListItems.query.filter_by(bucketlist_id=bucketlist_id,
                                                          item_id=item_id).first()

        if bucketlist_item:
            return marshal(bucketlist_item, bucketlist_items_fields), 200

            # else status code - not found
        return {'error': 'bucket list item not found.'}, 404

    def put(self, bucketlist_id=None, item_id=None):
        """ Update bucketlist item"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item_name', type=str, required=True,
                                   help="name cannot be blank")
        self.reqparse.add_argument('is_done', type=bool)
        args = self.reqparse.parse_args()
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            # status code - not found
            return {'error': "bucketlist not found"}, 404

        bucketlistitem = BucketListItems.query.filter_by(bucketlist_id=bucketlist_id,
                                                         item_id=item_id).first()

        # check if item exists
        if not bucketlistitem:
            return {'error': 'item not found.'}, 404

        if args.item_name:
            bucketlistitem.item_name = args.item_name
        if args.is_done:
            bucketlistitem.is_done = args.is_done
        db.session.commit()

        return {'message': 'item  updated'}, 200

    def delete(self, bucketlist_id=None, item_id=None):
        """ Delete bucket list item"""
        # check if bucketlist exists
        bucketlist = Bucketlist.query.filter_by(bucketlist_id=bucketlist_id).first()
        if not bucketlist:
            return {'error': "bucketList  not found."}, 404

        bucketlist_item = BucketListItems.query.filter_by(bucketlist_id=bucketlist_id,
                                                          item_id=item_id).first()
        # check if item exists
        if not bucketlist_item:
            return {'error': "item not found."}, 404

        delete(bucketlist_item)
        return {'message': 'item deleted'}, 200




