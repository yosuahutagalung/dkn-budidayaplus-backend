from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from cycle.models import Cycle, CycleFishDistribution
from pond.models import Pond

class CycleModelTest(TestCase):
    def setUp(self):
        starting_date = datetime.strptime('2024-09-01', '%Y-%m-%d')
        ending_date = starting_date + timedelta(days=60)

        self.user = User.objects.create_user(username='08123456789', password='12345')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
            image_name='test_image.jpg',
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=starting_date,
            end_date=ending_date
        )
        self.cycle_fish_distribution = CycleFishDistribution.objects.create(
            cycle=self.cycle,
            pond=self.pond,
            fish_amount = 10,
        )

    def test_str_method(self):
        self.assertEqual(str(self.cycle_fish_distribution), str(self.cycle_fish_distribution.id))

    def test_save_valid_fish_amount(self):
        cycle_fish_distribution = CycleFishDistribution.objects.create(
            cycle=self.cycle,
            pond=self.pond,
            fish_amount = 10,
        )
        self.assertEqual(cycle_fish_distribution.fish_amount, 10)

    def test_save_invalid_fish_amount(self):
        with self.assertRaises(ValidationError):
            CycleFishDistribution.objects.create(
                cycle=self.cycle,
                pond=self.pond,
                fish_amount = -10,
            )
