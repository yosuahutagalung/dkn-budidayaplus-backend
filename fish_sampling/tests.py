from django.test import TestCase
from django.contrib.auth.models import User
from ninja.testing import TestClient
from .models import Pond, FishSampling
from .api import router
import json

class FishSamplingAPITest(TestCase):
    
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='userA', password='abc123')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
        )
        self.fish_sampling = FishSampling.objects.create(
            pond=self.pond,
            reporter=self.user,
            fish_weight=1.5,
            fish_length=25.0,
            sample_date='2024-09-01'
        )

    def test_add_fish_sampling(self):
        response = self.client.post('/fish-sampling/', data=json.dumps({
            'pond_id': self.pond.id,
            'reporter_id': self.user.id,
            'fish_weight': 2.0,
            'fish_length': 30.0,
            'sample_date': '2024-09-10'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['fish_weight'], 2.0)

    def test_get_fish_sampling(self):
        response = self.client.get(f'/fish-sampling/{self.fish_sampling.sampling_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['fish_weight'], 1.5)

    def test_list_fish_samplings(self):
        response = self.client.get('/fish-sampling/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

    def test_delete_fish_sampling(self):
        response = self.client.delete(f'/fish-sampling/{self.fish_sampling.sampling_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_update_fish_sampling(self):
        response = self.client.put(f'/fish-sampling/{self.fish_sampling.sampling_id}/', data=json.dumps({
            'pond_id': self.pond.id,
            'reporter_id': self.user.id,
            'fish_weight': 2.5,
            'fish_length': 35.0,
            'sample_date': '2024-09-15'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['fish_weight'], 2.5)

