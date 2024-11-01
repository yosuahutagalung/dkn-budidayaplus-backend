from django.test import TestCase
from django.contrib.auth.models import User
from cycle.models import Cycle
from cycle.services.cycle_service import CycleService
from datetime import date, timedelta

class StopCycleTest(TestCase):
    def setUp(self):
        self.supervisor = User.objects.create_user(username="08123456789", password="test1234")
        self.cycle = Cycle.objects.create(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            supervisor=self.supervisor
        )

    def test_stop_active_cycle(self):
        stopped_cycle = CycleService.stop_cycle(cycle_id=self.cycle.id, supervisor=self.supervisor)
        self.assertEqual(stopped_cycle.status, "STOPPED")
        self.assertEqual(stopped_cycle.end_date, date.today())

    def test_stop_non_active_cycle(self):
        CycleService.stop_cycle(cycle_id=self.cycle.id, supervisor=self.supervisor)
        with self.assertRaises(ValueError) as context:
            CycleService.stop_cycle(cycle_id=self.cycle.id, supervisor=self.supervisor)
        self.assertIn("Hanya siklus yang aktif yang dapat dihentikan", str(context.exception))

    def test_stop_cycle_non_owner(self):
        another_user = User.objects.create_user(username="anotheruser", password="password")
        with self.assertRaises(ValueError) as context:
            CycleService.stop_cycle(cycle_id=self.cycle.id, supervisor=another_user)
        self.assertIn("Siklus tidak ditemukan atau Anda tidak memiliki izin untuk menghentikannya", str(context.exception))
