from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from ninja_extra.testing import TestClient
from .models import Pond
from .controller import PondController
import json, uuid


class PondAPITest(TestCase):
    def setUp(self):
        self.client = TestClient(PondController)
        self.user = User.objects.create_user(username='08123456789', password='12345')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
            image_name='test_image.jpg',
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.pond_omar = Pond.objects.create(
            owner=self.user,
            name='Test Pond Omar',
            image_name='test_image_omar.jpg',
            length=40.0,
            width=60.0,
            depth=3.0
        )
    
    def test_add_pond(self):
        response = self.client.post('/', data=json.dumps({
            'name': 'New Pond',
            'image_name': 'new_image.jpg',
            'length': 500.0,
            'width': 500.0,
            'depth': 2.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'New Pond')

    def test_add_pond_no_name(self):
        response = self.client.post('/', data=json.dumps({
            'image_name': 'new_image.jpg',
            'length': 500.0,
            'width': 500.0,
            'depth': 2.0
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
        response = self.client.get("/", headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})

        expected_data = [
            {
                "pond_id": str(self.pond.pond_id), 
                "name": self.pond.name,
                "image_name" : self.pond.image_name, 
                "owner": self.pond.owner.username, 
                "length": self.pond.length, 
                "width": self.pond.width, 
                "depth": self.pond.depth
            },
            {
                "pond_id": str(self.pond_omar.pond_id),
                "name": self.pond_omar.name,
                "image_name" : self.pond_omar.image_name,
                "owner": self.pond_omar.owner.username, 
                "length": self.pond_omar.length, 
                "width": self.pond_omar.width, 
                "depth": self.pond_omar.depth
            },
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_data)

    def test_list_ponds_by_user_invalid_token(self):
        response = self.client.get("/", headers={"Authorization": "Bearer Invalid Token"})
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
            'length': 400.0,
            'width': 300.0,
            'depth': 2.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Updated Pond')

    def test_update_pond_not_found(self):
        response = self.client.put(f'/{uuid.uuid4()}/', data=json.dumps({
            'name': 'Updated Pond',
            'image_name': 'updated_image.jpg',
            'length': 400.0,
            'width': 300.0,
            'depth': 2.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_update_pond_no_name(self):
        response = self.client.put(f'/{self.pond.pond_id}/', data=json.dumps({
            'image_name': 'updated_image.jpg',
            'length': 400.0,
            'width': 300.0,
            'depth': 2.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 422)

    def test_update_pond_blank_image_name(self):
        response = self.client.put(f'/{self.pond.pond_id}/', data=json.dumps({
            'name': 'Updated Pond',
            'image_name': '',
            'length': 400.0,
            'width': 300.0,
            'depth': 2.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.pond.image_name, 'test_image.jpg')
        self.assertEqual(response.json()['image_name'], 'test_image.jpg')

class PondModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='081234567890', password='password')

        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
            image_name='pond_image.jpg',
            length=10.0,
            width=5.0,
            depth=2.0
        )

    def test_str_method(self):
        self.assertEqual(str(self.pond), 'Test Pond')