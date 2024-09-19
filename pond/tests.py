from django.test import TestCase
from django.contrib.auth.models import User
from ninja.testing import TestClient
from .models import Pond
from .api import router
import json

class PondAPITest(TestCase):
    
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
            image_name='test_image.jpg',
            volume=1000.0
        )
    
    def test_add_pond(self):
        response = self.client.post('/ponds/', data=json.dumps({
            'owner_id': self.user.id,
            'name': 'New Pond',
            'image_name': 'new_image.jpg',
            'volume': 500.0
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'New Pond')

    def test_get_pond(self):
        response = self.client.get(f'/ponds/{self.pond.pond_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Test Pond')

    def test_list_ponds(self):
        response = self.client.get('/ponds/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

    def test_delete_pond(self):
        response = self.client.delete(f'/ponds/{self.pond.pond_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_update_pond(self):
        response = self.client.put(f'/ponds/{self.pond.pond_id}/', data=json.dumps({
            'name': 'Updated Pond',
            'image_name': 'updated_image.jpg',
            'volume': 1500.0
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Updated Pond')