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
        response_data = json.loads(str(response.get_data))
        self.assertIn('Authorization', response_data)

    def test_user_password_authentication(self):
        """Test that password is valid"""
        pass

    def test_user_required_fields_to_register(self):
        """Test that the required fields are not empty to register"""
        pass





if __name__ == '__main__':
    unittest.main()
