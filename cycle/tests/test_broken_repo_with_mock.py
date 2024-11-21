from cycle.models import Cycle
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from cycle.repositories.cycle_repo import CycleRepo
from unittest.mock import patch, MagicMock

class BrokenRepoNoMockTest(TestCase):
    def setUp(self):
        self.user = MagicMock(spec=User)
        self.cycle = MagicMock(spec=Cycle)
        self.cycle.start_date = timezone.now().date()
        self.cycle.end_date = timezone.now().date()
        self.cycle.supervisor = self.user

        self.cycle2 = MagicMock(spec=Cycle)
        self.cycle2.start_date = timezone.now().date() + timezone.timedelta(days=61)
        self.cycle2.end_date = timezone.now().date() + timezone.timedelta(days=121)
        self.cycle2.supervisor = self.user

        self.cycle_list = [self.cycle, self.cycle2]

    @patch('cycle.repositories.cycle_repo.CycleRepo.get_active_cycle')
    def test_get_cycle_active(self, mock_get_active_cycle):
        mock_get_active_cycle.return_value = [cycle for cycle in self.cycle_list if cycle.start_date <= timezone.now().date() and cycle.end_date >= timezone.now().date()][0]
        cycle = CycleRepo.get_active_cycle(self.user)
        self.assertEqual(cycle, self.cycle)
