

import os
from app import models
from app.config import Config
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app,db
from flask_restful import Api
from app.api import LoginAPI, RegisterAPI, BucketlistItemsAPI,BucketlistsAPI,BucketlistAPI,BucketlistItemAPI


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
migrate = Migrate(app, db)
manager = Manager(app)


manager.add_command('db', MigrateCommand)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
api = Api(app)
api.add_resource(RegisterAPI, '/api/v1/auth/register', endpoint='register')
api.add_resource(LoginAPI, '/api/v1/auth/login',endpoint='login')
api.add_resource(BucketlistAPI, '/api/v1/bucketlists/<int:id>',endpoint='bucketlist')
api.add_resource(BucketlistsAPI, '/api/v1/bucketlists/',endpoint='bucketlists')
api.add_resource(BucketlistItemsAPI, '/api/v1/bucketlists/<int:id>/items/', endpoint='bucketlist items')
api.add_resource(BucketlistItemAPI, '/api/v1/bucketlists/<int:id>/items/<item_id>', endpoint='bucketlist item')


if __name__ == '__main__':
    manager.run()
