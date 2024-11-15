from datetime import datetime, timedelta
from django.test import TestCase
from pond.models import Pond
from cycle.models import Cycle
from django.contrib.auth.models import User
from fish_sampling.models import FishSampling
from fish_sampling.repositories import FishSamplingRepository

class FishSamplingRepositoryTest(TestCase):
    def setUp(self):
        date_now = datetime.now()
        start_date = date_now - timedelta(days=30)
        end_date = start_date + timedelta(days=60)

        self.user = User.objects.create(username="testuser", password="password")
        
        self.pond = Pond.objects.create(
            owner=self.user,
            name="Test Pond",
            length=10.0,
            width=5.0,
            depth=3.0
        )
        
        self.cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=start_date,
            end_date=end_date,
        )

        self.fish_sampling = FishSampling.objects.create(
            pond=self.pond,
            cycle=self.cycle,
            reporter=self.user,
            fish_weight=20.0,
            fish_length=30.0,
            recorded_at=datetime.now()
        )

    def test_create_fish_sampling(self):
        fish_weight = 1.5
        fish_length = 20.0
        recorded_at = datetime.now()
        fish_sampling = FishSamplingRepository.create_fish_sampling(
            pond=self.pond,
            cycle=self.cycle,
            reporter=self.user,
            fish_weight=fish_weight,
            fish_length=fish_length,
            recorded_at=recorded_at
        )

        self.assertEqual(fish_sampling.pond, self.pond)
        self.assertEqual(fish_sampling.cycle, self.cycle)
        self.assertEqual(fish_sampling.reporter, self.user)
        self.assertEqual(fish_sampling.fish_weight, fish_weight)
        self.assertEqual(fish_sampling.fish_length, fish_length)
    
    def test_get_latest_fish_sampling(self):
        latest_sampling = FishSamplingRepository.get_latest_fish_sampling(self.pond, self.cycle)
        self.assertEqual(latest_sampling, self.fish_sampling)
    
    def test_get_latest_fish_sampling_no_data(self):
        self.fish_sampling.delete()
        latest_sampling = FishSamplingRepository.get_latest_fish_sampling(self.pond, self.cycle)
        self.assertIsNone(latest_sampling)

    def test_list_fish_samplings(self):
        samplings = FishSamplingRepository.list_fish_samplings(self.cycle, self.pond)
        self.assertEqual(len(samplings), 1)
        self.assertEqual(samplings[0], self.fish_sampling)