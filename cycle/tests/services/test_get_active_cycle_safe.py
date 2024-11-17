from unittest.mock import MagicMock, patch
from django.contrib.auth.models import User
from cycle.models import Cycle
from django.test import TestCase
from django.utils import timezone
from cycle.services.cycle_service import CycleService

class TestGetActiveCycleSafeService(TestCase):
    def setUp(self):
        self.supervisor = MagicMock(spec=User)
        self.cycle = MagicMock(spec=Cycle)
        self.cycle.id = 1
        self.cycle.start_date = timezone.now().date()
        self.cycle.end_date = self.cycle.start_date + timezone.timedelta(days = 60)

    @patch('cycle.repositories.cycle_repo.CycleRepo.get_active_cycle_safe')
    def test_get_active_cycle_safe_exists(self, mock_get_active_cycle_safe):
        mock_get_active_cycle_safe.return_value = [self.cycle]
        self.assertEqual([self.cycle], CycleService.get_active_cycle_safe(self.supervisor))

    @patch('cycle.repositories.cycle_repo.CycleRepo.get_active_cycle_safe')
    def test_get_active_cycle_safe_does_not_exist(self, mock_get_active_cycle_safe):
        mock_get_active_cycle_safe.return_value = []
        self.assertEqual([], CycleService.get_active_cycle_safe(self.supervisor))

