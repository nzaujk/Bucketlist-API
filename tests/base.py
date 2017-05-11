from flask_testing import TestCase
import json
from instance.config import app_config
from app import db, app
from app.models import User


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object(app_config["testing"])
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
        response = self.client.post('/auth/login', data=json.dumps(user),
                               content_type='application/json')
        response_data = json.loads(str(response.get_data))
        token = response_data.get("Authorization")
        return {"Authorization": "token " + token,
                "Accept": 'application/json',
                "Content-Type": 'application/json',
                }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
