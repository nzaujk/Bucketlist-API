import os

from app.config import BaseConfig
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import models
from app import flask_app, db

flask_app.config['SQLALCHEMY_DATABASE_URI'] = BaseConfig.SQLALCHEMY_DATABASE_URI
migrate = Migrate(flask_app, db)
manager = Manager(flask_app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
