from django.test import TestCase
from ninja.testing import TestClient
from django.contrib.auth.models import User
from .models import Pond, Cycle, FoodSampling
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta
from .api import router

class FoodSamplingAPITest(TestCase):

    def setUp(self):
        start_time = datetime.strptime('2024-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=60)

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
        self.cycle = Cycle.objects.create(
            supervisor = self.user,
            start_date = start_time,
            end_date = end_time,
        )
        self.food_sampling = FoodSampling.objects.create(
            pond=self.pond,
            reporter=self.user,
            cycle=self.cycle,
            food_amount='1',
            date='2024-10-15',
        )
        self.food_sampling_userA = FoodSampling.objects.create(
            pond=self.pond,
            reporter=self.user,
            cycle=self.cycle,
            food_amount='1.5',
            date='2024-10-16'
        )
    
    def test_get_food_sampling(self):
        response = self.client.get(f'/{self.pond.pond_id}/{self.food_sampling.food_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
    
    def test_list_food_samplings(self):
        response = self.client.get(f'/{self.pond.pond_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        expected_data = [
            {"food_id": str(self.food_sampling.food_id), "pond_id": str(self.food_sampling.pond.pond_id), "reporter": str(self.food_sampling.reporter), \
             "food_amount": float(self.food_sampling.food_amount), "date": self.food_sampling.date},
            {"food_id": str(self.food_sampling_userA.food_id), "pond_id": str(self.food_sampling_userA.pond.pond_id), "reporter": str(self.food_sampling_userA.reporter), \
             "food_amount": float(self.food_sampling_userA.food_amount), "date": self.food_sampling_userA.date}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_data)
    
    def test_list_food_sampling_unauthorized(self):
        response = self.client.get(f'/{self.pond.pond_id}/{self.food_sampling.food_id}/', headers={})
        self.assertEqual(response.status_code, 401)