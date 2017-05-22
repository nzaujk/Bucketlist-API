import os
from app.config import app_config

from app import flask_app
from flask_testing import TestCase
basedir = os.path.abspath(os.path.dirname(__file__))


class TestDevelopmentConfig(TestCase):

    def create_app(self):
        flask_app.config.from_object(app_config['development'])
        return flask_app

    def test_app_is_development(self):
        self.assertTrue(flask_app.config['DEBUG'])
        self.assertTrue(flask_app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URL'))
        self.assertTrue(flask_app.config['SECRET_KEY'] == os.getenv('SECRET_KEY'))


class TestTestingConfig(TestCase):
    def create_app(self):
        flask_app.config.from_object(app_config['testing'])
        return flask_app

    def test_app_is_testing(self):
        self.assertTrue(flask_app.config['DEBUG'])
        self.assertTrue(
            flask_app.config['SQLALCHEMY_DATABASE_URI']
            == "postgresql://localhost/test_bucketlist_db")
        self.assertTrue(flask_app.config['SECRET_KEY'] == os.getenv('SECRET_KEY'))

