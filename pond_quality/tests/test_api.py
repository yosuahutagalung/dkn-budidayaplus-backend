from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from pond.models import Pond
from cycle.models import Cycle
from pond_quality.models import PondQuality
from ninja_jwt.tokens import AccessToken
from ninja.testing import TestClient
from pond_quality.api import router
import json, uuid

class PondQualityAPITest(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='081234567890', password='password')

        date_now = datetime.now()
        starting_date = date_now - timedelta(days=30)
        ending_date = starting_date + timedelta(days=60)
        self.cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=starting_date,
            end_date=ending_date
        )

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
            cycle = self.cycle,
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
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_list_pond_qualities_by_pond_invalid_token(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/', headers={"Authorization": "Bearer Invalid Token"})
        self.assertEqual(response.status_code, 401)

    def test_list_pond_qualities_by_pond_invalid_pond(self):
        response = self.client.get(f'/{self.cycle.id}/{uuid.uuid4()}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_list_pond_qualities_by_pond_invalid_cycle(self):
        response = self.client.get(f'{uuid.uuid4()}/{self.pond.pond_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_list_pond_qualities_by_pond_outdated_cycle(self):
        starting_date = datetime.now() - timedelta(days=90)
        ending_date = starting_date + timedelta(days=60)
        cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=starting_date,
            end_date=ending_date
        )
        response = self.client.get(f'/{cycle.id}/{self.pond.pond_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 400)

    def test_add_pond_quality_positive(self):
        response = self.client.post(f'/{self.cycle.id}/{self.pond.pond_id}/', data=json.dumps({
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
        response = self.client.post(f'/{self.cycle.id}/{self.pond.pond_id}/', data=json.dumps({
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
        response = self.client.post(f'/{self.cycle.id}/{uuid.uuid4()}/', data=json.dumps({
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
        response = self.client.post(f'/{self.cycle.id}/{self.pond.pond_id}/', data=json.dumps({
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
        response = self.client.post(f'/{self.cycle.id}/{self.pond.pond_id}/', data=json.dumps({
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
        response = self.client.post(f'/{self.cycle.id}/{self.pond.pond_id}/', data=json.dumps({
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

    def test_add_pond_quality_invalid_cycle(self):
        response = self.client.post(f'{uuid.uuid4()}/{self.pond.pond_id}/', data=json.dumps({
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
    
    def test_add_pond_quality_outdated_cycle(self):
        starting_date = datetime.now() - timedelta(days=90)
        ending_date = starting_date + timedelta(days=60)
        cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=starting_date,
            end_date=ending_date
        )
        response = self.client.post(f'/{cycle.id}/{self.pond.pond_id}/', data=json.dumps({
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
        self.assertEqual(response.status_code, 400)

    def test_get_pond_quality_positive(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['ph_level'], 7.0)

    def test_get_pond_quality_invalid_pond(self):
        response = self.client.get(f'/{self.cycle.id}/{uuid.uuid4()}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_get_pond_quality_invalid_pond_quality(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/{uuid.uuid4()}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_get_pond_quality_invalid_token(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": "Bearer Invalid Token"})
        self.assertEqual(response.status_code, 401)

    def test_get_pond_quality_invalid_user(self):
        user = User.objects.create_user(username='081234567891', password='password')
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(user))}"})
        self.assertEqual(response.status_code, 401)

    def test_get_pond_quality_different_pond(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond2.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)


    def test_get_latest_pond_quality_positive(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/latest', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)

    def test_get_latest_pond_quality_invalid_pond(self):
        response = self.client.get(f'/{self.cycle.id}/{uuid.uuid4()}/latest', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_get_latest_pond_quality_invalid_token(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/latest', headers={"Authorization": "Bearer Invalid Token"})
        self.assertEqual(response.status_code, 401)
    
    def test_get_latest_pond_quality_invalid_user(self):
        user = User.objects.create_user(username='081234567891', password='password')
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/latest', headers={"Authorization": f"Bearer {str(AccessToken.for_user(user))}"})
        self.assertEqual(response.status_code, 401)

    def test_get_latest_pond_quality_not_found(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond2.pond_id}/latest', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)