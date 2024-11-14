from django.test import TestCase
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from food_sampling.models import FoodSampling
from pond.models import Pond
from cycle.models import Cycle
from food_sampling.repositories.food_sampling_repository import FoodSamplingRepository

class FoodSamplingRepositoryTest(TestCase):
    
    def setUp(self):
        date_now = datetime.now()
        start_date = date_now - timedelta(days=30)
        end_date = start_date + timedelta(days=60)

        self.user = User.objects.create_user(username='user', password='pass')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Pond',
            image_name='pond.png',
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=start_date,
            end_date=end_date,
        )
        self.food_sampling = FoodSampling.objects.create(
            pond=self.pond,
            reporter=self.user,
            cycle=self.cycle,
            food_quantity=1.0,
            recorded_at=datetime.now()
        )

    def test_get_pond(self):
        pond = FoodSamplingRepository.get_pond(self.pond.pond_id)
        self.assertEqual(pond, self.pond)
    
    def test_get_cycle(self):
        cycle = FoodSamplingRepository.get_cycle(self.cycle.id)
        self.assertEqual(cycle, self.cycle)
    
    def test_get_existing_food_sampling(self):
        existing_food_sampling = FoodSamplingRepository.get_existing_food_sampling(
            cycle=self.cycle,
            pond=self.pond,
            today=datetime.now().date()
        )
        self.assertEqual(existing_food_sampling, self.food_sampling)
    
    def test_create_food_sampling(self):
        new_food_sampling = FoodSamplingRepository.create_food_sampling(
            pond=self.pond,
            reporter=self.user,
            cycle=self.cycle,
            food_quantity=2,
            recorded_at=datetime.now()
        )
        self.assertIsNotNone(new_food_sampling)
        self.assertEqual(new_food_sampling.food_quantity, 2.0)
    
    def test_delete_food_sampling(self):
        FoodSamplingRepository.delete_food_sampling(self.food_sampling)
        with self.assertRaises(FoodSampling.DoesNotExist):
            FoodSampling.objects.get(sampling_id=self.food_sampling.sampling_id)

    def test_get_food_sampling_by_id(self):
        food_sampling = FoodSamplingRepository.get_food_sampling_by_id(self.food_sampling.sampling_id)
        self.assertEqual(food_sampling, self.food_sampling)
    
    def test_get_latest_food_sampling(self):
        latest_sampling = FoodSamplingRepository.get_latest_food_sampling(self.pond, self.cycle)
        self.assertEqual(latest_sampling, self.food_sampling)
    
    
