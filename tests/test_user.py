import json
import unittest
from flask_testing import TestCase

from tests.base import BaseTestCase


class TestUser(BaseTestCase, TestCase):
    def test_user_login(self):
        """Test user login POST"""
        user = {"username": "user1", "password": "1234"}
        response = self.client.post('/auth/login', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('Authorization', response_data)

    def test_user_password_authentication(self):
        """Test that password is valid"""
        pass

    def test_new_user_not_already_registered(self):
        """Test a new user cannot exist in the system"""
        pass

    def test_username_is_valid_character(self):
        """Test that a username is not a number or invalid character"""
        pass

    def test_user_required_fields_to_register(self):
        """Test that the required fields are not empty to register"""
        pass

    def test_wrong_credentials_fails(self):
        """Test cannot login with wrong credentials"""
        pass

    def test_log_out(self):
        """Test that a user can logout"""
        pass


if __name__ == '__main__':
    unittest.main()
