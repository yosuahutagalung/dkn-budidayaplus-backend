from django.test import TestCase
from cycle.models import Cycle
from datetime import date, timedelta
from django.contrib.auth.models import User
from cycle.repositories.cycle_repo import CycleRepo
import uuid

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
    
    def test_get_active_cycle(self):
        active_cycle = Cycle.objects.create(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            supervisor=self.user
        )

        cycle = CycleRepo.get_active_cycle(self.user)

        self.assertEqual(active_cycle, cycle)

    def test_get_active_cycle_not_exist(self):
        cycle = CycleRepo.get_active_cycle(self.user)

        self.assertIsNone(cycle)

    def test_get_cycle_by_id(self):
        cycle = Cycle.objects.create(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            supervisor=self.user
        )

        cycle_by_id = CycleRepo.get_cycle_by_id(cycle.id)
        
        self.assertEqual(cycle, cycle_by_id)
    
    def test_get_cycle_by_id_not_exist(self):
        ex_id = uuid.uuid4()
        cycle_by_id = CycleRepo.get_cycle_by_id(str(ex_id))

        self.assertIsNone(cycle_by_id)

    def test_stop_cycle(self):
        cycle = Cycle.objects.create(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            supervisor=self.user,
            status="ACTIVE"
        )
        stopped_cycle = CycleRepo.stop_cycle(cycle)

        cycle.refresh_from_db()
        
        self.assertEqual(stopped_cycle.status, "STOPPED")
        self.assertEqual(stopped_cycle.end_date, date.today())

    def test_stop_cycle_already_stopped(self):
        cycle = Cycle.objects.create(
            start_date=date.today() - timedelta(days=70),
            end_date=date.today() - timedelta(days=10),
            supervisor=self.user,
            status="STOPPED"
        )

        stopped_cycle = CycleRepo.stop_cycle(cycle)
        cycle.refresh_from_db()
        
        self.assertEqual(stopped_cycle.status, "STOPPED")
        self.assertEqual(stopped_cycle.end_date, date.today() - timedelta(days=10))