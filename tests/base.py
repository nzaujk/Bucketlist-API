from flask_testing import TestCase
import json
from instance.config import app_config
from app import db, app
from app.models import User


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object(app_config["testing"])
        self.client = app.test_client
        return app

    def setUp(self):
        """Run this instructions before executing the tests."""
        self.client = self.create_app().test_client
        username = User(username='user1', password='1234')
        db.session.add(username)
        db.create_all()
        db.session.commit()

    def fetch_token(self):
        """ fetch token for authentication"""
        user = {"username": "user1", "password": "1234"}
        get_token = self.client.post('/auth/login', data=json.dumps(user),
                                     content_type='application/json')
        response_data = json.loads(get_token.get_data(as_text=True))
        token = response_data.get("Authorization")
        return token


    def tearDown(self):
        db.session.remove()
        db.drop_all()
