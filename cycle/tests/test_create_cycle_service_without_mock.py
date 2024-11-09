from django.test import TestCase
from cycle.services.cycle_service import CycleService
from cycle.models import Cycle
from datetime import date, timedelta
from django.contrib.auth.models import User
from uuid import uuid4

class CycleServiceTest(TestCase):
    def setUp(self):
        self.supervisor = User.objects.create_user(username='08123456789', password='admin1234')
        self.cycle = Cycle.objects.create(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            supervisor=self.supervisor
        )

    def test_get_cycle_by_id(self):
        cycle = CycleService.get_cycle_by_id(self.cycle.id)
        self.assertEqual(cycle, self.cycle)

    def test_get_cycle_by_id_not_found_with_stub(self):
        with self.assertRaises(ValueError) as context:
            CycleService.get_cycle_by_id(uuid4())
        
        self.assertEqual(str(context.exception), "Siklus tidak ditemukan")