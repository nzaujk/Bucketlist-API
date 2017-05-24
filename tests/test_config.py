import os
from app.config import app_config

from app import app
from flask_testing import TestCase
basedir = os.path.abspath(os.path.dirname(__file__))


class TestDevelopmentConfig(TestCase):

    def create_app(self):
        app.config.from_object(app_config['development'])
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URL'))
        self.assertTrue(app.config['SECRET_KEY'] == os.getenv('SECRET_KEY'))


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object(app_config['testing'])
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI']
            == "postgresql://localhost/test_bucketlist_db")
        self.assertTrue(app.config['SECRET_KEY'] == os.getenv('SECRET_KEY'))


class ProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object(app_config['production'])
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI']
            == "postgresql://localhost/default")
        self.assertTrue(app.config['SECRET_KEY'] == os.getenv('SECRET_KEY'))
