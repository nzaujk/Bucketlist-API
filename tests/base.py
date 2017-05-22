from flask_testing import TestCase
import json
from app.config import app_config
from app import app, db
from app.models import User, save


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self, app=app):
        """ Initialize app"""
        app.config.from_object(app_config['testing'])
        db.create_all()
        return app

    def setUp(self):
        self.client = self.create_app().test_client()
        # create and add a test user
        new_user = User(username='joenzau', email='myemail@email.com', password='password')
        save(new_user)


    def get_header(self):
        """ Gets token for user authentication"""
        new_user = User(username='jojo', email='jojo@email.com', password='password')
        save(new_user)
        user = {"username": "jojo", "password": "password"}
        response = self.client.post('/api/v1/auth/login',data=json.dumps(user),
                                    content_type='application/json')
        response_data = json.loads(response.get_data(as_text=True))
        token = response_data['token']
        print(response_data)
        return {'authorization': 'token ' + token}



    def tearDown(self):
        """destroy the test db"""
        db.session.remove()
        db.drop_all()

