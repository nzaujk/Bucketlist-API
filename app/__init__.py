from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_restful import Api
from app.config import app_config

app = Flask(__name__)
app.config.from_object(app_config['development'])
db = SQLAlchemy(app)


from app.api import LoginAPI,RegisterAPI,BucketlistsAPI,\
    BucketlistAPI,BucketlistItemsAPI,BucketlistItemAPI

api = Api(app=app, prefix='/api/v1')

api.add_resource(RegisterAPI, '/auth/register', endpoint='register')
api.add_resource(LoginAPI, '/auth/login', endpoint='login')
api.add_resource(BucketlistAPI, '/bucketlists/<int:id>', endpoint='bucketlist')
api.add_resource(BucketlistsAPI, '/bucketlists/', endpoint='bucketlists')
api.add_resource(BucketlistItemsAPI, '/bucketlists/<int:id>/items', endpoint='bucketlist items')
api.add_resource(BucketlistItemAPI, '/bucketlists/<int:id>/items/<item_id>', endpoint='bucketlist item')

