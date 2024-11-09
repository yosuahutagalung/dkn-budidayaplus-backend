from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from pond.models import Pond
from cycle.models import Cycle
from fish_sampling.models import FishSampling
from django.utils.timezone import make_aware

class FishSamplingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='081234567890', password='password')
        self.pond = Pond.objects.create(
            owner = self.user,
            name = 'Test Pond',
            image_name = 'test.jpg',
            length = 1.0,
            width = 1.0,
            depth = 1.0
        )
        starting_date = make_aware(datetime.strptime('2024-09-01', '%Y-%m-%d'))
        ending_date = starting_date + timedelta(days=60)
        self.cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=starting_date,
            end_date=ending_date
        )
        self.fish_sampling = FishSampling.objects.create(
            pond = self.pond,
            reporter = self.user,
            cycle = self.cycle,
            fish_weight = 1.5,
            fish_length = 25.0,
            recorded_at = make_aware(datetime.now())
        )

    def test_str_method(self):
        self.assertEqual(str(self.fish_sampling), str(self.fish_sampling.sampling_id))
