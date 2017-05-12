import unittest
from flask_testing import TestCase
import json
from app import app, db
from tests.base import BaseTestCase


class Bucketlist(BaseTestCase, TestCase):
    def setUp(self):
        self.bucketlist = {'Activity': 'Climb Mount Kenya'}
        self.listitems = {'Activity1': 'Climb Mount Kenya', 'Activity2': "Get to D1",
                          "Activity3": "Go to Ertaale"}
        self.bucketlist_item = {"Activity": ['Bungee Jumping','Sky Diving', 'Snockeling']}

    def test_create_bucketlist(self):
        """Test API can POST request"""
        response = self.client.post('/bucketlists/api/v1.0/', data=json.dumps(self.bucketlist),
                                    headers=self.fetch_token())
        self.assertEqual(response.status_code, 201)
        self.assertIn("Climb Mount Kenya", response.get_data(as_text=True))

    def test_view_bucketlist(self):
        """Test API can GET request"""
        response = self.client.get('/bucketlists/api/v1.0/', data=json.dumps(self.bucketlist),
                                    headers=self.fetch_token())
        self.assertEqual(response.status_code, 200)

    def test_duplicate_buckelist_not_allowed(self):
        """Tests that a user cannot input an existing bucket list"""
        response = self.client.post('/bucketlists/api/v1.0/', data=json.dumps(self.bucketlist),
                                    headers=self.fetch_token())
        self.assertEqual(response.status_code, 202)

    def test_edit_bucketlist(self):
        """Test API can PUT request"""
        updated_bucketlist = {'Activity': 'Climb Mount Kenya by end of the year'}
        response = self.client.post('/bucketlists/api/v1.0/',data=json.dumps(self.bucketlist),
                                      headers=self.fetch_token())
        self.assertEqual(response.status_code, 201)
        new_response = self.client().put('/bucketlists/api/v1.0/1',data=json.dumps(updated_bucketlist),
                               headers=self.fetch_token() )
        self.assertEqual(new_response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("Bucketlist updated",response_data['message'])

    def test_unauthenitcated_cannot_add_bucketlist(self):
        """Test authentication is required to add a bucketlist"""
        response = self.client.post('/bucketlists/', data=json.dumps(self.bucketlist))

        self.assertEqual(response.status_code, 401)

    def test_must_be_Loggedin_view_bucketlist(self):
        """Test authentication is required to access bucketlists"""
        pass

    def test_delete_bucketlist(self):
        """Test API can DELETE """
        response = self.client.post('/bucketlists/api/v1.0/',data=json.dumps(self.bucketlist),
                                      headers=self.fetch_token())
        self.assertEqual(response.status_code, 201)
        response_item = self.client.delete('/bucketlists/1')
        self.assertEqual(response_item.status_code, 200)
        # check for the item if it exists. If delete is successful it returns status 404
        result = self.client.get('/bucketlists/api/v1.0/1')
        self.assertEqual(result.status_code, 404)

    def test_delete_item_in_bucketlist(self):
        """Test item is deleted from bicketlist"""
        response = self.client.post('/bucketlists/api/v1.0/1/items/',
                                    data=json.dumps(self.bucketlist),
                                    headers=self.fetch_token())
        self.assertEqual(response.status_code, 201)
        response_item = self.client.delete('/bucketlists/api/v1.0/1/items/1')
        self.assertEqual(response_item.status_code, 200)
        # check for the item if it exists. If delete is successful it returns status 404
        result = self.client.get('/bucketlists/api/v1.0/1/items/1')
        self.assertEqual(result.status_code, 404)

    def test_cannot_delete_not_exists(self):
        """If a delete attempt is done to a none existing file"""
        result = self.client.get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)
        response_data = json.loads(result.get_data(as_text=True))
        self.assertIn("Bucketlist doesn't exist",response_data['error'])

    def test_lists_all_bucketlists(self):
        """Test that a user can view all bucketlists"""
        response = self.client.get('bucketlists/api/v1.0/<id>/items/', data=json.dumps(self.listitems),
                                   headers=self.fetch_token())
        self.assertEqual(response.status_code, 200)

    def test_lists_single_bucketlist(self):
        """Test that a user can select a single bucketlist"""
        self.client.post('/bucketlists/api/v1.0/1/items/1', data=json.dumps(self.bucketlist_item),
                         headers=self.fetch_token())
        response = self.client.get('/bucketlists/api/v1.0/1/items/1', headers=self.fetch_token())
        self.assertEqual(response.status_code, 200)

    def test_create_new_item_in_bucketlist(self):
        """Test user can add new item to bucketlist"""
        response = self.client.post('/bucketlists/api/v1.0/1/items/1',
                                    data=json.dumps(self.bucketlist),
                                    headers=self.fetch_token())
        self.assertEqual(response.status_code, 201)
        self.assertIn("Climb Mount Kenya", response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
