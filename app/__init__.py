from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_restful import Api
from instance.config import app_config
from app.api import LoginAPI, RegisterAPI,BucketlistAPI, BucketlistsAPI, \
    BucketlistItemsAPI, BucketlistItemAPI


app = Flask(__name__)
api = Api(app)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config.from_object(app_config['parent'])

api.add_resource(RegisterAPI, '/auth/register')
api.add_resource(LoginAPI, '/auth/login')
api.add_resource(BucketlistAPI, '/bucketlists/api/v1.0/')
api.add_resource(BucketlistsAPI, '/bucketlists/api/v1.0/<id>')
api.add_resource(BucketlistItemsAPI, '/bucketlists/api/v1.0/<id>/items/')
api.add_resource(BucketlistItemAPI, '/bucketlists/api/v1.0/<id>/items/<item_id>')

# if __name__ == '__main__':
#     db.init_app(app)
#     app.run()