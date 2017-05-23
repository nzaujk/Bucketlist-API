import os

from app.config import BaseConfig
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import models
from app import app, db

app.config['SQLALCHEMY_DATABASE_URI'] = BaseConfig.SQLALCHEMY_DATABASE_URI
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def createdb(dbname):
    os.system('createdb ' + dbname)
    print("{} created".format(dbname))


@manager.command
def dropdb(dbname):
    os.system('dropdb '+ dbname)

    print("{} deleted".format(dbname))


if __name__ == '__main__':
    manager.run()
