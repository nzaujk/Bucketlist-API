# from flask import g
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, reqparse, marshal, fields

# from app.models import User
# from app import app


auth = HTTPBasicAuth()


# @app.route('/api/token')
# @auth.login_required
# def get_auth_token():
#     token = g.user.generate_auth_token()
#     return {'token': token}

# decorators = [auth.login_required]
#
# def verify_password(token):
#     user = User.verify_auth_token(token)
#     if not user:
#         return False
#     g.user = user
#     return True


class RegisterAPI(Resource):
    """user registration """

    def post(self):
        pass


class LoginAPI(Resource):
    """login through token authentication"""

    def login(self):
        pass

class BucketlistsAPI(Resource):
    decorators = [auth.login_required]

    def get(self):

        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class BucketlistAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class BucketlistItemsAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

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
