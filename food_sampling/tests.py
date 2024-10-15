from django.test import TestCase
from django.contrib.auth.models import User
from ninja.testing import TestClient
from .models import Pond, FoodSampling
from .api import router
import json
from rest_framework_simplejwt.tokens import AccessToken

class FoodSamplingAPITest(TestCase):
    
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='userA', password='abc123')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
            image_name='test_pond.png',
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.food_sampling = FoodSampling.objects.create(
            pond=self.pond,
            reporter=self.user,
            food_quantity=10,
            sample_date='2024-09-01'
        )
        self.fish_sampling_userA = FoodSampling.objects.create(
            pond=self.pond,
            reporter=self.user,
            food_quantity=10,
            sample_date='2024-09-10'
        )

    def test_add_food_sampling(self):
        response = self.client.post(f'/{self.pond.pond_id}/', data=json.dumps({
            'pond_id': str(self.pond.pond_id),  
            'reporter_id': self.user.id,     
            'food_quantity': 30,
            'sample_date': '2024-09-10'
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)

    def test_add_food_sampling_with_invalid_data(self):
        response = self.client.post(f'/{self.pond.pond_id}/', data=json.dumps({
            'sampling_id': str(self.fish_sampling.sampling_id),
            'pond_id': str(self.pond.pond_id),
            'reporter_id': self.user.id,
            'food_quantity': -30,
            'sample_date': '2024-09-19'
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)