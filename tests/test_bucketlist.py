import json
from tests.base import BaseTestCase


class Bucketlist(BaseTestCase):
    def setUp(self):
        self.bucket_list = {"title": "Travel Diaries", "description": "4 countries per year",
                            "created by": "Joe"}
        self.bucket_list_items = {'title': 'Climb Mount Kenya', 'title': "Get to D1",
                           "title": "Go to Ertaale"}
        self.bucket_list_item = {"title": 'Climb mount Kenya'}

    def test_create_bucket_list(self):
        """Test API can POST request"""

        response = self.client.post("api/v1/bucketlists/", data=self.bucket_list,
                                 headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertTrue("bucketlist created successfuly" in response_data["message"])
        self.assertIn(self.bucketlist["title"], response.data)
        self.assertIn(self.bucketlist["description"], response.data)
        self.assertIn(self.bucketlist["created by"], response.data)

    def test_cannot_add_bucket_list_without_title(self):
        """test that one cannot add a bucket list without a title"""
        no_title = {'': 'Visit Lake Turkana',
                    'description':'By end of the year',
                    'created by': 'Joe'}
        response = self.client.post('api/v1/bucketlists/', data=no_title,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Bucket list title cannot be empty",
                      response.get_data(as_text=True))

    def test_duplicate_bucketlist_not_allowed(self):
        """Tests that a user cannot input an existing bucket list title"""
        user = {'title':'Climb Mount Kenya'}
        response = self.client.post('/api/v1/bucketlists/1', data=json.dumps(user),
                                    headers=self.get_token())
        self.assertEqual(response.status_code, 400)

    def test_edit_bucketlist(self):
        """Test API can PUT request"""
        updated_bucketlist = {'Activity': 'Climb Mount Kenya by end of the year'}
        response = self.client.post('/api/v1/bucketlists/1',data=json.dumps(self.bucket_list),
                                      headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        new_response = self.client().put('/api/v1/bucketlists/1',data=json.dumps(updated_bucketlist),
                               headers=self.get_token())
        self.assertEqual(new_response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("Bucketlist updated",response_data['message'])

    def test_unauthenitcated_cannot_add_bucketlist(self):
        """Test authentication is required to add a bucketlist"""
        response = self.client.post('/api/v1/bucketlists/', data=json.dumps(self.bucket_list))
        self.assertEqual(response.status_code, 401)

    # def test_must_be_Loggedin_view_bucketlist(self):
    #     """Test authentication is required to access bucketlists"""
    #     pass
    #
    def test_delete_bucketlist(self):
        """Test API can DELETE """
        response = self.client.post('/api/v1/bucketlists/',data=json.dumps(self.bucket_list),
                                      headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        response_item = self.client.delete('/bucketlists/1')
        self.assertEqual(response_item.status_code, 200)
        # check for the item if it exists. If delete is successful it returns status 404
        result = self.client.get('/api/v1/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def test_delete_item_in_bucketlist(self):
        """Test item is deleted from bicketlist"""
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    data=json.dumps(self.bucket_list),
                                    headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        response_item = self.client.delete('/api/v1/bucketlists/1/items/1')
        self.assertEqual(response_item.status_code, 200)
        # check for the item if it exists. If delete is successful it returns status 404
        result = self.client.get('/api/v1/bucketlists/1/items/1')
        self.assertEqual(result.status_code, 404)

    def test_cannot_delete_not_exists(self):
        """If a delete attempt is done to a none existing file"""
        result = self.client.get('/api/v1/bucketlists/1')
        self.assertEqual(result.status_code, 404)
        response_data = json.loads(result.get_data(as_text=True))
        self.assertIn("Bucketlist doesn't exist",response_data['error'])

    def test_lists_all_bucketlist_items(self):
        """Test that a user can view all bucketlists"""
        response = self.client.get('/api/v1/bucketlists/1/items/', data=json.dumps(self.bucket_list_items_),
                                   headers=self.get_token())
        self.assertEqual(response.status_code, 200)

    def test_lists_single_bucketlist_item(self):
        """Test that a user can select a single bucketlist"""
        self.client.post('/api/v1/bucketlists/1/items/1', data=json.dumps(self.bucket_list_item),
                         headers=self.get_token())
        response = self.client.get('/api/v1/bucketlists/1/items/1', headers=self.get_token())
        self.assertEqual(response.status_code, 200)

    def test_create_new_item_in_bucketlist(self):
        """Test user can add new item to bucketlist"""
        response = self.client.post('/api/v1/bucketlists/1/items/1',
                                    data=json.dumps(self.bucket_list),
                                    headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        self.assertIn("Climb Mount Kenya", response.get_data(as_text=True))
