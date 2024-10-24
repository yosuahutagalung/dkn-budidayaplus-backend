from django.test import TestCase
from cycle.models import Cycle
from datetime import date, timedelta
from django.contrib.auth.models import User
from cycle.repositories.cycle_repo import CycleRepo

class CycleRepoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='08123456789', password='test1234')
    
    def test_create_cycle(self):
        cycle = CycleRepo.create(
            start=date.today(),
            end=date.today() + timedelta(days=60),
            supervisor=self.user
        )

        self.assertEqual(Cycle.objects.count(), 1)
        self.assertEqual(Cycle.objects.get(), cycle)

    def test_is_active_cycle_exist(self):
        Cycle.objects.create(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            supervisor=self.user
        )

        active_cycle_exist = CycleRepo.is_active_cycle_exist(
            supervisor=self.user,
            start=date.today(),
            end=date.today() + timedelta(days=60)
        )

        self.assertTrue(active_cycle_exist)

    def test_is_active_cycle_not_exist(self):
        active_cycle_exist = CycleRepo.is_active_cycle_exist(
            supervisor=self.user,
            start=date.today(),
            end=date.today() + timedelta(days=60)
        )

        self.assertFalse(active_cycle_exist)