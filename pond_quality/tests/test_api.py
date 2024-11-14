import uuid, json
from unittest.mock import patch
from django.test import TestCase
from ninja.testing import TestClient
from django.contrib.auth.models import User
from pond.models import Pond
from cycle.models import Cycle
from pond_quality.models import PondQuality
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta
from pond_quality.api import router
from ninja.errors import HttpError

class PondQualityAPITest(TestCase):

    def setUp(self):
        date_now = datetime.now()
        start_date = date_now - timedelta(days=30)
        end_date = start_date + timedelta(days=60)

        self.client = TestClient(router)
        self.user = User.objects.create_user(username='081234567890', password='abc123')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
            image_name='test_pond.png',
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.pondB = Pond.objects.create(
            owner=self.user,
            name='Test Pond B',
            image_name='test_pondB.png',
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.cycle = Cycle.objects.create(
            supervisor = self.user,
            start_date = start_date,
            end_date = end_date,
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
            phosphate = 0.0,
            recorded_at = datetime.now()
        )
        self.pond_quality_userA = PondQuality.objects.create(
            pond = self.pond,
            reporter = self.user,
            cycle = self.cycle,
            image_name = 'test.jpg',
            ph_level = 9.0,
            salinity = 0.0,
            water_temperature = 25.0,
            water_clarity = 0.0,
            water_circulation = 0.0,
            dissolved_oxygen = 0.0,
            orp = 0.0,
            ammonia = 0.0,
            nitrate = 0.0,
            phosphate = 0.0,
            recorded_at = datetime.now() - timedelta(days=1)
        )
    
    def test_get_pond_quality(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
    
    def test_get_pond_quality_cycle_not_active(self): 
        start_date = datetime.now()
        end_date = start_date + timedelta(days=60)
        cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=start_date,
            end_date=end_date
        )
        response = self.client.get(f'/{cycle.id}/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)
    
    def test_get_pond_quality_different_cycle(self):
        starting_date = datetime.now()
        ending_date = starting_date + timedelta(days=60)
        cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=starting_date,
            end_date=ending_date
        )
        response = self.client.get(f'/{cycle.id}/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)
    
    def test_get_pond_quality_invalid_pond(self):
        response = self.client.get(f'/{self.cycle.id}/{uuid.uuid4()}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)
    
    def test_get_pond_quality_different_pond(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pondB.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)
    
    def test_get_pond_quality_invalid_pond_quality(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/{uuid.uuid4()}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)
    
    def test_get_pond_quality_invalid_user(self):
        user = User.objects.create_user(username='081234567891', password='admin1234')
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/{self.pond_quality.id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(user))}"})
        self.assertEqual(response.status_code, 401)
    
    def test_list_pond_qualitys(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['pond_qualitys']), 2)

    def test_list_pond_quality_unauthorized(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/{self.pond_quality.id}/', headers={})
        self.assertEqual(response.status_code, 401)
    
    def test_list_pond_quality_by_invalid_cycle(self):
        response = self.client.get(f'{uuid.uuid4()}/{self.pond.pond_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)
    
    def test_list_pond_quality_by_invalid_pond(self):
        response = self.client.get(f'/{self.cycle.id}/{uuid.uuid4()}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)
    
    def test_get_latest_pond_quality(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/latest', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
    
    def test_get_latest_pond_quality_invalid_pond(self):
        response = self.client.get(f'/{self.cycle.id}/{uuid.uuid4()}/latest', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)
    
    def test_get_latest_pond_quality_invalid_user(self):
        user = User.objects.create_user(username='081234567891', password='abc123')
        response = self.client.get(f'/{self.cycle.id}/{self.pond.pond_id}/latest', headers={"Authorization": f"Bearer {str(AccessToken.for_user(user))}"})
        self.assertEqual(response.status_code, 401)
    
    def test_get_latest_pond_quality_cycle_not_active(self):
        start_date = datetime.now() - timedelta(days=90)
        end_date = start_date + timedelta(days=60)
        cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=start_date,
            end_date=end_date
        )
        response = self.client.get(f'/{cycle.id}/{self.pond.pond_id}/latest', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 400)
    
    def test_get_latest_pond_quality_not_found(self):
        response = self.client.get(f'/{self.cycle.id}/{self.pondB.pond_id}/latest', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)
    
    def test_add_pond_quality(self):
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
            'phosphate': 0.0,
            'recorded_at': datetime.now().isoformat()
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)

    def test_add_pond_quality_with_invalid_data(self):
        response = self.client.post(f'/{self.cycle.id}/{self.pond.pond_id}/', data=json.dumps({
            'image_name': 'test.jpg',
            'ph_level': 15.0,
            'salinity': 0.0,
            'water_temperature': 25.0,
            'water_clarity': 0.0,
            'water_circulation': 0.0,
            'dissolved_oxygen': 0.0,
            'orp': 0.0,
            'ammonia': 0.0,
            'nitrate': 0.0,
            'phosphate': 0.0,
            'recorded_at': datetime.now().isoformat()
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
    
    def test_add_pond_quality_with_pond_not_found(self):
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
            'phosphate': 0.0,
            'recorded_at': datetime.now().isoformat()
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 500)
    
    def test_add_pond_quality_with_cycle_not_found(self):
        response = self.client.post(f'/{uuid.uuid4()}/{self.pond.pond_id}/', data=json.dumps({
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
            'phosphate': 0.0,
            'recorded_at': datetime.now().isoformat()
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 500)
    
    def test_add_pond_quality_already_existing(self):
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
            'phosphate': 0.0,
            'recorded_at': datetime.now().isoformat()
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PondQuality.objects.filter(cycle=self.cycle, pond=self.pond).count(), 2)

    @patch('pond_quality.api.pond_quality_service.create_pond_quality')
    def test_add_pond_quality_with_service_error(self, mock_create_pond_quality):
        # Configure the mock to raise an HttpError
        mock_create_pond_quality.side_effect = HttpError(400, "Mocked service error")
        
        response = self.client.post(
            f'/{self.cycle.id}/{self.pond.pond_id}/',
            data=json.dumps({
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
                'phosphate': 0.0,
                'recorded_at': datetime.now().isoformat()
            }),
            content_type='application/json',
            headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"}
        )
        
        # Verify the response status and content
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], "Mocked service error")