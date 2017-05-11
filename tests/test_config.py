from instance.config import app_config
from app import app
from flask_testing import TestCase


class TestDevelopmentConfig(TestCase):

    def create_app(self):
        app.config.from_object(app_config["development"])
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] ==
                        "postgresql://postgres:root@localhost/bucketlist_db"
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object(app_config['testing'])
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == "postgresql://postgres:root@localhost/test_db"
        )
