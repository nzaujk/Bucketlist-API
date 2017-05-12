

import os
from instance.config import *
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, app
from app import models

# app.config.from_pyfile('config.py')

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

db.create_all()

if __name__ == '__main__':
    manager.run()
