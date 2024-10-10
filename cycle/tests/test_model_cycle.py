from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cycle.models import Cycle

class CycleModelTest(TestCase):
    def setUp(self):
        starting_date = datetime.strptime('2024-09-01', '%Y-%m-%d').date()
        ending_date = starting_date + timedelta(days=60)

        self.user = User.objects.create_user(username='08123456789', password='12345')
        self.cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=starting_date,
            end_date=ending_date
        )

    def test_str_method(self):
        self.assertEqual(str(self.cycle), str(self.cycle.id))

    def test_start_date_after_end_date(self):
        starting_date = datetime.strptime('2024-09-01', '%Y-%m-%d')
        ending_date = starting_date - timedelta(days=60)

        with self.assertRaises(ValidationError):
            Cycle.objects.create(
                supervisor=self.user,
                start_date=starting_date,
                end_date=ending_date
            )

    def test_end_date_not_60_days_after_start_date(self):
        starting_date = datetime.strptime('2024-09-01', '%Y-%m-%d')
        ending_date = starting_date + timedelta(days=59)

        with self.assertRaises(ValidationError):
            Cycle.objects.create(
                supervisor=self.user,
                start_date=starting_date,
                end_date=ending_date
            )
            
    def test_date_valid(self):
        starting_date = datetime.strptime('2024-09-01', '%Y-%m-%d')
        ending_date = starting_date + timedelta(days=60)

        cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=starting_date,
            end_date=ending_date
        )

        self.assertEqual(cycle.start_date, starting_date)
        self.assertEqual(cycle.end_date, ending_date)

    def test_is_active_within_date_range(self):
        today = datetime.strptime('2024-10-01', '%Y-%m-%d').date()
        with self.settings(DATE_OVERRIDE=today):
            self.assertTrue(self.cycle.is_active)

    def test_is_active_outside_date_range(self):
        start = datetime.strptime('2025-10-20', '%Y-%m-%d').date()
        end = start + timedelta(days=60)
        cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=start,
            end_date=end
        )
        self.assertFalse(cycle.is_active)