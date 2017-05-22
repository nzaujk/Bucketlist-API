import json
from tests.base import BaseTestCase


class BucketlistItems(BaseTestCase):
    def test_add_new_item_in_bucketlist(self):
        """Test user can add new item to bucketlist"""
        item = {'item_name': 'Mount Kenya hike', 'is_done': False}
        response = self.client.post('api/v1/bucketlists/1/items/', data=item,
                                    headers=self.get_header())
        self.assertEqual(response.status_code, 201)
        response_data = response.get_data(as_text=True)
        self.assertIn('item has been added succesfully to bucketlist', response_data['message'])

    def test_delete_item_in_bucketlist(self):
        """Test item is deleted from bicketlist"""
        data= {"item_1": "Travel Diaries", "item_2": "Addis"}
        response = self.client.post('/api/v1/bucketlists/1/items',
                                    data=data,
                                    headers=self.get_header())
        self.assertEqual(response.status_code, 201)
        response_item = self.client.delete('/api/v1/bucketlists/1/items/1')
        self.assertEqual(response_item.status_code, 200)
        # check for the item if it exists. If delete is successful it returns status 404
        result = self.client.get('/api/v1/bucketlists/1/items/1')
        self.assertEqual(result.status_code, 404)

    def test_lists_all_bucketlist_items(self):
        """Test that a user can view all bucketlists"""
        data = {'title': 'Climb Mount Kenya', 'title': "Get to D1",
         "title": "Go to Ertaale"}
        response = self.client.post('/api/v1/bucketlists/1/items', data=data,
                                    headers=self.get_header())
        self.assertEqual(response.status_code, 201)
        view = self.client.get('/api/v1/bucketlists/1/items', data=data,
                                   headers=self.get_header())
        self.assertEqual(view.status_code, 200)

    def test_lists_single_bucketlist_item(self):
        """Test that a user can select a single bucketlist"""
        data = {'item': 'Go to hawaasa'}
        self.client.post('/api/v1/bucketlists/1/items/1', data=data,
                         headers=self.get_header())
        response = self.client.get('/api/v1/bucketlists/1/items/1', headers=self.get_header())
        self.assertEqual(response.status_code, 200)

