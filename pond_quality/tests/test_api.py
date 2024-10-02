from django.test import TestCase
from django.contrib.auth.models import User
from pond.models import Pond
from pond_quality.models import PondQuality
from ninja_jwt.tokens import AccessToken
from ninja.testing import TestClient
from pond_quality.api import router
import json, uuid

class PondQualityAPITest(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='081234567890', password='password')
        self.pond = Pond.objects.create(
            owner = self.user,
            name = 'Test Pond',
            image_name = 'test.jpg',
            length = 1.0,
            width = 1.0,
            depth = 1.0
        )
        self.pond2 = Pond.objects.create(
            owner = self.user,
            name = 'Test Pond 2',
            image_name = 'test.jpg',
            length = 1.0,
            width = 1.0,
            depth = 1.0
        )
        self.pond_quality = PondQuality.objects.create(
            pond = self.pond,
            reporter = self.user,
            image_name = 'test.jpg',
            ph_level = 7.0,
            salinity = 0.0,
            water_temperature = 25.0,
            water_clarity = 0.0,
            water_circulation = 0.0,
            dissolved_oxygen = 0.0,
            orp = 0.0,
            ammonia = 0.0,
            nitrate = 0.0,
            phosphate = 0.0
        )

    def test_list_pond_qualities_by_pond(self):
        response = self.client.get(f'/{self.pond.pond_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_list_pond_qualities_by_pond_invalid_token(self):
        response = self.client.get(f'/{self.pond.pond_id}/', headers={"Authorization": "Bearer Invalid Token"})
        self.assertEqual(response.status_code, 401)

    def test_list_pond_qualities_by_pond_invalid_pond(self):
        response = self.client.get(f'/{uuid.uuid4()}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    
    def test_add_pond_quality_positive(self):
        response = self.client.post(f'/{self.pond.pond_id}/', data=json.dumps({
            'image_name': 'test.jpg',
            'ph_level': 7.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['pond'], str(self.pond.pond_id))
        self.assertEqual(data['image_name'], 'test.jpg')
        self.assertEqual(data['ph_level'], 7.0)

    def test_add_pond_quality_no_image_name(self):
        response = self.client.post(f'/{self.pond.pond_id}/', data=json.dumps({
            'ph_level': 7.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)

    def test_add_pond_quality_invalid_pond(self):
        response = self.client.post(f'/{uuid.uuid4()}/', data=json.dumps({
            'image_name': 'test.jpg',
            'ph_level': 7.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_add_pond_quality_invalid_token(self):
        response = self.client.post(f'/{self.pond.pond_id}/', data=json.dumps({
            'image_name': 'test.jpg',
            'ph_level': 7.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": "Bearer Invalid Token"})
        self.assertEqual(response.status_code, 401)

    def test_add_pond_quality_no_ph_level(self):
        response = self.client.post(f'/{self.pond.pond_id}/', data=json.dumps({
            'image_name': 'test.jpg',
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 422)

    def test_add_pond_quality_no_salinity(self):
        response = self.client.post(f'/{self.pond.pond_id}/', data=json.dumps({
            'image_name': 'test.jpg',
            'ph_level': 7.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 422)


    def test_delete_pond_quality_positive(self):
        response = self.client.delete(f'/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())

    def test_delete_pond_quality_invalid_pond(self):
        response = self.client.delete(f'/{uuid.uuid4()}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_delete_pond_quality_invalid_token(self):
        response = self.client.delete(f'/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": "Bearer Invalid Token"})
        self.assertEqual(response.status_code, 401)

    def test_delete_pond_quality_invalid_pond_quality(self):
        deleted_id = self.pond_quality.id
        self.client.delete(f'/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str (AccessToken.for_user(self.user))}"})
        response = self.client.delete(f'/{self.pond.pond_id}/{deleted_id}/', headers={"Authorization": f"Bearer {str (AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)
        
    def test_delete_pond_quality_invalid_user(self):
        user = User.objects.create_user(username='081234567891', password='password')
        response = self.client.delete(f'/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(user))}"})
        self.assertEqual(response.status_code, 401)

    def test_delete_pond_quality_different_pond(self):
        response = self.client.delete(f'/{self.pond2.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)


    def test_get_pond_quality_positive(self):
        response = self.client.get(f'/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['ph_level'], 7.0)

    def test_get_pond_quality_invalid_pond(self):
        response = self.client.get(f'/{uuid.uuid4()}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_get_pond_quality_invalid_pond_quality(self):
        response = self.client.get(f'/{self.pond.pond_id}/{uuid.uuid4()}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_get_pond_quality_invalid_token(self):
        response = self.client.get(f'/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": "Bearer Invalid Token"})
        self.assertEqual(response.status_code, 401)

    def test_get_pond_quality_invalid_user(self):
        user = User.objects.create_user(username='081234567891', password='password')
        response = self.client.get(f'/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(user))}"})
        self.assertEqual(response.status_code, 401)

    def test_get_pond_quality_different_pond(self):
        response = self.client.get(f'/{self.pond2.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    
    def test_update_pond_quality_positive(self):
        response = self.client.put(f'/{self.pond.pond_id}/{self.pond_quality.id}/', data=json.dumps({
            'image_name': 'test.jpg',
            'ph_level': 8.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        updated_data = PondQuality.objects.get(id=self.pond_quality.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_data.ph_level, 8.0)

    def test_update_pond_quality_blank_image(self):
        response = self.client.put(f'/{self.pond.pond_id}/{self.pond_quality.id}/', data=json.dumps({
            'image_name': '',
            'ph_level': 8.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        updated_data = PondQuality.objects.get(id=self.pond_quality.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_data.image_name, 'test.jpg')

    def test_update_pond_quality_no_image(self):
        response = self.client.put(f'/{self.pond.pond_id}/{self.pond_quality.id}/', data=json.dumps({
            'ph_level': 8.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        updated_data = PondQuality.objects.get(id=self.pond_quality.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_data.image_name, 'test.jpg')

    def test_update_pond_quality_invalid_pond(self):
        response = self.client.put(f'/{uuid.uuid4()}/{self.pond_quality.id}/', data=json.dumps({
            'image_name': 'test.jpg',
            'ph_level': 8.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_update_pond_quality_invalid_pond_quality(self):
        response = self.client.put(f'/{self.pond.pond_id}/{uuid.uuid4()}/', data=json.dumps({
            'image_name': 'test.jpg',
            'ph_level': 8.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_update_pond_quality_invalid_token(self):
        response = self.client.put(f'/{self.pond.pond_id}/{self.pond_quality.id}/', data=json.dumps({
            'image_name': 'test.jpg',
            'ph_level': 8.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": "Bearer Invalid Token"})
        self.assertEqual(response.status_code, 401)

    def test_update_pond_quality_invalid_user(self):
        user = User.objects.create_user(username='081234567891', password='password')
        response = self.client.put(f'/{self.pond.pond_id}/{self.pond_quality.id}/', data=json.dumps({
            'image_name': 'test.jpg',
            'ph_level': 8.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(user))}"})
        self.assertEqual(response.status_code, 401)

    def test_update_pond_different_pond(self):
        response = self.client.put(f'/{self.pond2.pond_id}/{self.pond_quality.id}/', data=json.dumps({
            'image_name': 'test.jpg',
            'ph_level': 8.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)