from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from ninja.testing import TestClient
from .models import Pond
from .api import router
import json, uuid


class PondAPITest(TestCase):
    
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='08123456789', password='12345')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
            image_name='test_image.jpg',
            volume=1000.0
        )
        self.pond_omar = Pond.objects.create(
            owner=self.user,
            name='Test Pond Omar',
            image_name='test_image_omar.jpg',
            volume=6969.0
        )
    
    def test_add_pond(self):
        response = self.client.post('/', data=json.dumps({
            'name': 'New Pond',
            'image_name': 'new_image.jpg',
            'volume': 500.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'New Pond')

    def test_add_pond_no_name(self):
        response = self.client.post('/', data=json.dumps({
            'image_name': 'new_image.jpg',
            'volume': 500.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 422)

    def test_get_pond(self):
        response = self.client.get(f'/{self.pond.pond_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Test Pond')

    def test_get_pond_not_found(self):
        response = self.client.get(f'/{uuid.uuid4()}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_list_ponds_by_user(self):
        token = str(AccessToken.for_user(self.user))
        response = self.client.get("/", headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})

        expected_data = [
                    {"id": str(self.pond.pond_id), "name": self.pond.name, "owner": self.pond.owner.username},
                    {"id": str(self.pond_omar.pond_id), "name": self.pond_omar.name, "owner": self.pond_omar.owner.username},
                ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_data)

    def test_list_ponds_by_user_invalid_token(self):
        response = self.client.get("/", headers={"Authorization": f"Bearer Invalid Token"})
        self.assertEqual(response.status_code, 401)

    def test_delete_pond(self):
        response = self.client.delete(f'/{self.pond.pond_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_delete_pond_not_found(self):
        response = self.client.delete(f'/{uuid.uuid4()}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_update_pond(self):
        response = self.client.put(f'/{self.pond.pond_id}/', data=json.dumps({
            'name': 'Updated Pond',
            'image_name': 'updated_image.jpg',
            'volume': 1500.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Updated Pond')

    def test_update_pond_not_found(self):
        response = self.client.put(f'/{uuid.uuid4()}/', data=json.dumps({
            'name': 'Updated Pond',
            'image_name': 'updated_image.jpg',
            'volume': 1500.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)