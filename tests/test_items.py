import json
from tests.base import BaseTestCase


class BucketlistItems(BaseTestCase):

    def test_add_new_item_in_bucketlist(self):
        """Test user can add new item to bucketlist"""
        # add bucket list
        data = {'title': 'Wild Adventures'}
        response = self.client.post('/api/v1/bucketlists', data=data,
                                    headers=self.get_header())
        self.assertEqual(response.status_code, 201)
        # add item
        item = {'item_name': 'Mount Kenya hike', 'is_done': False}
        item_response = self.client.post('api/v1/bucketlists/1/items', data=item,
                                         headers=self.get_header())
        self.assertEqual(item_response.status_code, 201)

    def test_delete_item_in_bucketlist(self):
        """Test item is deleted from bicketlist"""
        # add bucket list
        data = {"title": "Travel Diaries", "description": "4 countries per year"}
        self.client.post('/api/v1/bucketlists', data=data, headers=self.get_header())
        # add item
        item = {'item_name': 'Mount Kenya hike', 'is_done': False}
        self.client.post('api/v1/bucketlists/1/items', data=item,
                         headers=self.get_header())
        # delete item
        response_item = self.client.delete('/api/v1/bucketlists/1/items/1',
                                           headers=self.get_header())
        self.assertEqual(response_item.status_code, 200)

    def test_cannot_perform_delete_request_if_backet_list_does_not_exist(self):
        """delete request fails for none existing bucketlist"""
        response_item = self.client.delete('/api/v1/bucketlists/1/items/1',
                                           headers=self.get_header())
        self.assertEqual(response_item.status_code, 404)

    def test_cannot_perform_delete_request_if_item_does_not_exist(self):
        """delete request fails for none existing bucketlist"""
        # add bucket list
        data = {"title": "Travel Diaries", "description": "4 countries per year"}
        self.client.post('/api/v1/bucketlists', data=data, headers=self.get_header())

        response_item = self.client.delete('/api/v1/bucketlists/1/items/1',
                                           headers=self.get_header())
        self.assertEqual(response_item.status_code, 404)

    def test_lists_all_bucketlist_items(self):
        """Test that a user can view all bucketlists"""
        # add bucket list
        data = {'title': 'Mountain Climbing'}
        self.client.post('/api/v1/bucketlists', data=data,
                         headers=self.get_header())
        # add items to bucket list
        items = {'item_name': 'Mount Kenya Hike', 'is_done': False}
        self.client.post('/api/v1/bucketlists/1/items', data=items,
                         headers=self.get_header())
        view_all = self.client.get('/api/v1/bucketlists/1/items/1', data=data,
                                   headers=self.get_header())
        self.assertEqual(view_all.status_code, 200)

    def test_view_single_bucketlist_item(self):
        """Test that a user can select a single bucketlist"""
        # add bucket list
        data = {'title': 'Road Trips'}
        self.client.post('/api/v1/bucketlists', data=data,
                         headers=self.get_header())
        # add item
        data = {'item_name': 'Addis Road trip', 'is_done': False}
        self.client.post('/api/v1/bucketlists/1/items', data=data,
                         headers=self.get_header())

        response = self.client.get('/api/v1/bucketlists/1/items', data=data,
                                   headers=self.get_header())
        self.assertEqual(response.status_code, 200)

    def test_cannot_view_empty_items(self):
        """if user requests to view items in an empty bucket list"""
        # add bucket list
        data = {'title': 'Road Trips'}
        self.client.post('/api/v1/bucketlists', data=data,
                         headers=self.get_header())
        # view item in empty bucket list
        response = self.client.get('/api/v1/bucketlists/1/items',headers=self.get_header())

        self.assertEqual(response.status_code, 404)

    def test_item_name_cannot_be_empty(self):
        """Test that an items name cannot be empty"""
        # add bucket list
        bucket_list = {"title": "Road Trips"}
        self.client.post('/api/v1/bucketlists', data=bucket_list,
                         headers=self.get_header())
        # add items
        add_items = {'item_name': '', 'is_done': False}
        response = self.client.post('/api/v1/bucketlists/1/items', data=add_items,
                         headers=self.get_header())
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("item name cannot be empty", response_data['error'])

    def test_cannot_add_items_to_none_existing_bucket_list(self):
        """Test api cannot add items before bucket list has been created"""
        # add items
        add_items = {'item_name': 'Road trips', 'is_done': False}
        response = self.client.post('/api/v1/bucketlists//items', data=add_items,
                         headers=self.get_header())
        self.assertEqual(response.status_code, 404)

    def test_api_rejects_duplicate_items(self):
        """Test api rejects duplicate item entries"""
        # add bucket list
        bucket_list = {"title": "Road Trips"}
        self.client.post('/api/v1/bucketlists', data=bucket_list,
                         headers=self.get_header())
        # add items
        add_items = {'item_name': 'Bale Mountains', 'is_done': True}
        first_response = self.client.post('/api/v1/bucketlists/1/items', data=add_items,
                         headers=self.get_header())
        self.assertEqual(first_response.status_code, 201)

        response = self.client.post('/api/v1/bucketlists/1/items', data=add_items,
                                    headers=self.get_header())
        self.assertEqual(response.status_code, 400)









