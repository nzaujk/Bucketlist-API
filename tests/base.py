from flask_testing import TestCase
import json
from app.config import app_config
from app import flask_app, db
from app.models import User


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self, app=flask_app):
        """ Initialize app"""
        app.config.from_object(app_config['testing'])
        return app

    def setUp(self):
        self.client = self.create_app().test_client()
        db.create_all()

        # create and add a test user
        new_user = User(username='joenzau', email='myemail@email.com', password='password')
        db.session.add(new_user)
        db.session.commit()

    def get_header(self):
        """ Gets token for user authentication"""
        user = {"username": "joenzau","password": "password"}
        response = self.client.post('/api/v1/auth/login',
                    data=json.dumps(user), content_type='application/json')
        response_data = json.loads(response.get_data(as_text=True))
        token = response_data.get('Authorization')
        return {"Authorization": "token " + token,
                "Accept": 'application/json',
                "Content-Type": 'application/json',
                }

    def tearDown(self):
        """destroy the test db"""
        db.session.remove()
        db.drop_all()

