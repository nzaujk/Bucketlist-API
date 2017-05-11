import unittest
from flask_testing import TestCase
import json
from app import create_app, db
from tests.base import BaseTestCase


class Bucketlist(BaseTestCase, TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Climb Mount Kenya'}

        with self.app.app_context():
            # create the tables
            db.create_all()

    def test_create_bucketlist(self):
        """Test API can POST request"""
        response = self.client.post('/bucketlists/', data=json.dumps(self.bucketlist),
                                    headers=self.fetch_token())
        self.assertEqual(response.status_code, 201)
        self.assertIn("Climb Mount Kenya", str(response.data))

    def test_view_bucketlist(self):
        """Test API can GET request"""
        pass

    def test_edit_bucketlist(self):
        """Test API can PUT request"""
        pass

    def test_public_cannot_add_bucketlist(self):
        """Test authentication is required to add a bucketlist"""
        pass

    def test_must_be_Loggedin_view_bucketlist(self):
        """Test authentication is required to access bucketlists"""
        pass

    def test_delete_bucketlist(self):
        """Test API can DELETE """
        pass

    def test_duplicate_buckelist_not_allowed(self):
        """Tests that a user cannot input an existing bucket list"""
        pass







if __name__ == '__main__':
    unittest.main()
