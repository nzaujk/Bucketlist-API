import json
from tests.base import BaseTestCase
from app.models import User


class TestUser(BaseTestCase):

    def test_registration(self):
        """ Test successful user registration """
        user = {"username": "rachel","email":"rachel@email.com", "password": "password"}
        response = self.client.post('/api/v1/auth/register', data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['message'],'account created', )

    def test_registration_username_cannot_be_empty(self):
        """test registration username field cannot empty"""
        user = {"username": "", 'email': 'emailme@email.com', "password": "password"}
        response = self.client.post('/api/v1/auth/register', data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['message'], 'username cannot be empty')

    def test_registration_email_cannot_be_empty(self):
        """test registration email field cannot empty"""
        user = {"username": "ranchoo", 'email': '', "password": "password"}
        response = self.client.post('/api/v1/auth/register', data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['message'], 'email cannot be empty')

    def test_registration_password_cannot_be_empty(self):
        """test registration password field cannot empty"""
        user = {"username": "miriam", 'email': 'meme@email.com', "password": ""}
        response = self.client.post('/api/v1/auth/register', data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['message'], 'password cannot be empty')

    def test_invalid_email_format_fails(self):
        """test that registration with an invalid email format fails"""
        user = {"username": "sheme", 'email': 'meme@emw.', "password": 'password'}
        response = self.client.post('/api/v1/auth/register', data=json.dumps(user),
                                        content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['error'], 'invalid email format')


    def test_new_user_cannot_register_with_existing_username(self):
        """Test a user cannot register with an existing username"""
        user = {"username": "joenzau",'email': 'joe@email.com', "password": "password"}
        response = self.client.post('/api/v1/auth/register', data=json.dumps(user),
                                    content_type='application/json')
        new_response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 202)
        self.assertIn(new_response_data['message'], 'username exists')

    def test_new_user_cannot_register_with_existing_email(self):
        """Test a user cannot register with an existing email address"""
        user = {"username": "joewaweru",'email': 'myemail@email.com', "password": "password"}
        response = self.client.post('/api/v1/auth/register', data=json.dumps(user),
                                    content_type='application/json')
        new_response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 202)
        self.assertIn(new_response_data['message'], 'email exists')

    def test_user_login(self):
        """Test user can login"""
        user = {'username': 'joenzau','password': 'password'}
        response = self.client.post('/api/v1/auth/login', data=user)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('login successful', str(response_data['message']))

    def test_cannot_login_empty_username_password(self):
        """Test that the required fields are not empty to login"""
        user = {"username": "", "password": ""}
        response = self.client.post('/api/v1/auth/login', data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['error'],'please enter a username and password.')

    def test_wrong_login_credentials_fails(self):
        """Test cannot login with wrong credentials"""
        user = {'username': 'joenzau', 'password': 'invalidpassword'}
        response = self.client.post('/api/v1/auth/login', data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['error'], 'invalid username or password')



