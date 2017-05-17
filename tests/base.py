from flask_testing import TestCase
import json

from app.config import app_config
from app import app, db
from app.models import User


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object(app_config["testing"])
        return app

    def setUp(self):
        """Run this instructions before executing the tests."""
        self.client = self.create_app().test_client()
        db.create_all()

        user = User(username='Joe', password='password')
        db.session.add(user)
        db.session.commit()

    def get_token(self):
        """ get authentication token """
        user = {"username": "Joe", "password": "password"}
        response = self.client.post('api/v1/auth/login/', data=json.dumps(user),
                                    content_type='application/json')
        response_data = json.loads(response.get_data(as_text=True))
        token = response_data.get('token')
        return {'token': token}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

