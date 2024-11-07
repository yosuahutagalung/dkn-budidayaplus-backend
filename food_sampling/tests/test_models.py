from django.test import TestCase
from ninja.testing import TestClient
from django.contrib.auth.models import User
from pond.models import Pond
from cycle.models import Cycle
from food_sampling.models import FoodSampling
from datetime import datetime, timedelta
from food_sampling.api import router

class FoodSamplingModelTest(TestCase):
    
    def setUp(self):
        start_time = datetime.strptime('2024-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=60)

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
        self.cycle = Cycle.objects.create(
            supervisor = self.user,
            start_date = start_time,
            end_date = end_time,
        )
        self.food_sampling = FoodSampling.objects.create(
            pond=self.pond,
            reporter=self.user,
            cycle=self.cycle,
            food_quantity='1.0',
            recorded_at = datetime.now(),
        )

    def test_str_method(self):
        expected_str = f"Food Sampling for {self.pond.name} on {self.food_sampling.sample_date}"
        self.assertEqual(str(self.food_sampling), expected_str)