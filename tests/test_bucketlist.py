import json
from tests.base import BaseTestCase


class Bucketlist(BaseTestCase):
    def setUp(self):
        self.bucket_list = {"title": "Travel Diaries", "description": "4 countries per year"}
        self.bucket_list_items = {'title': 'Climb Mount Kenya', 'title': "Get to D1",
                           "title": "Go to Ertaale"}
        self.bucket_list_item = {"title": 'Mountain Climbing'}

    def test_create_bucket_list(self):
        """Test API can POST request"""
        data = {"title": "Travel Diaries", "description": "4 countries per year"}
        response = self.client.post('/api/v1/bucketlists/', data=data,
                                    headers=self.get_header())
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        print(response_data)
        self.assertTrue("bucketlist created successfuly",response_data["message"])

    def test_cannot_add_bucket_list_without_title(self):
        """test that one cannot add a bucket list without a title"""
        no_title = {'': 'Visit Lake Turkana',
                    'description':'By end of the year'}
        response = self.client.post('/api/v1/bucketlists/', data=no_title,
                                    headers=self.get_header())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Bucket list title cannot be empty",
                      response.get_data(as_text=True))

    def test_duplicate_bucketlist_not_allowed(self):
        """Tests that a user cannot input an existing bucket list title"""
        user = {'title':'Go to Hannover'}
        self.client.post('/bucketlists/', data=json.dumps(user),
                                    headers=self.get_header())
        new_response = self.client.post('/bucketlists/', data=json.dumps(user),
                                    headers=self.get_header())
        self.assertEqual(new_response.status_code, 400)
        new_response_data = json.loads(new_response.get_data(as_text=True))
        self.assertIn("'The bucket list alread exists'", new_response_data['message'])

    def test_update_bucketlist(self):
        """Test API can PUT request"""
        data = {'title':'Visit Hannover'}
        response = self.client.post('/api/v1/bucketlists/', data=json.dumps(data),
                                      headers=self.get_header())
        self.assertEqual(response.status_code, 201)
        update = {'title': 'Go to Enterprise Europe Network'}
        new_response = self.client().put('/api/v1/bucketlists/1',
                            data=update, headers=self.get_header())
        self.assertEqual(new_response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("Bucketlist updated",response_data['message'])

    def test_unauthenitcated_cannot_add_bucketlist(self):
        """Test authentication is required to add a bucketlist"""
        response = self.client.post('/api/v1/bucketlists/', data=json.dumps(self.bucket_list))
        self.assertEqual(response.status_code, 401)

    def test_delete_bucketlist(self):
        """Test API can DELETE """
        data = {"title": "Sunset Beach"}
        response = self.client.post('/api/v1/bucketlists/',data=data,
                                      headers=self.get_header())
        # self.assertEqual(response.status_code, 201)
        response_item = self.client.delete('/api/v1/bucketlists/1',data=data,
                                      headers=self.get_header())
        self.assertEqual(response_item.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('bucket list deleted', response_data['message'])

    def test_cannot_delete_none_existing(self):
        """If a delete attempt is done to a none existing file"""
        result = self.client.delete('/api/v1/bucketlists/1', headers=self.get_header())
        self.assertEqual(result.status_code, 404)
        response_data = json.loads(result.get_data(as_text=True))
        self.assertIn("bucketlist doesn't exist",response_data['error'])
