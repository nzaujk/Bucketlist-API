import json
from tests.base import BaseTestCase


class TestUser(BaseTestCase):

    def test_registration(self):
        """ Test successful user registration """
        user = {"username": "Joe", "password": "password"}
        response = self.client.post('api/v1/auth/register', data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['message'], 'account created')

    def test_username_exists(self):
        """Test a username already exists"""
        user = {"username": "Joe", "password": "password"}
        response = self.client.post('api/v1/auth/register', data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 202)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['message'], 'username exists')

    def test_registration_empty_fields_fails(self):
        """test empty fields cannot be registered"""
        user = {"username": "", "password": ""}
        response = self.client.post('api/v1/auth/register', data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['message'], 'cannot send an empty entry')

    def test_user_login(self):
        """Test user login POST"""
        user = {"username": "Joe", "password": "password"}
        response = self.client.post('api/v1/auth/login', data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('token', response_data)

    def test_user_password_authentication(self):
        """Test that password is valid"""
        pass

    def test_cannot_login_empty_username_password(self):
        """Test that the required fields are not empty to login"""
        user = {"username": "", "password": ""}
        response = self.client.post('api/v1/auth/login', data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['error'],'Username or Password cant be empty', )

    def test_wrong_login_credentials_fails(self):
        """Test cannot login with wrong credentials"""
        user = {'username': 'Mike', 'password': 'invalid'}
        response = self.client.post('api/v1/auth/login', data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn(response_data['error'], 'invalid username or password')



