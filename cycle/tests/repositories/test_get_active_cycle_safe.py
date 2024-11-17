from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from cycle.models import Cycle
from django.test import TestCase
from django.utils import timezone
from cycle.repositories.cycle_repo import CycleRepo

class TestGetActiveCycleSafeRepo(TestCase):
    def setUp(self):
        self.cycle = MagicMock(spec=Cycle)
        self.cycle.id = 1
        self.cycle.start_date = timezone.now().date()
        self.cycle.end_date = self.cycle.start_date + timezone.timedelta(days = 60)
        self.supervisor = MagicMock(spec=User)

    @patch('cycle.models.Cycle.objects.filter')
    def test_get_active_cycle_safe_exists(self, mock_filter):
        mock_filter.return_value = [self.cycle]
        self.assertEqual([self.cycle], CycleRepo.get_active_cycle_safe(self.supervisor))

    @patch('cycle.models.Cycle.objects.filter')
    def test_get_active_cycle_safe_does_not_exist(self, mock_filter):
        mock_filter.return_value = []
        self.assertEqual([], CycleRepo.get_active_cycle_safe(self.supervisor))

