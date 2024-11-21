from django.test import TestCase
from cycle.services.cycle_service import CycleService
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from cycle.models import Cycle
from django.utils import timezone

class TestGetFutureOrPastCycleService(TestCase):
    def setUp(self):
        self.supervisor = MagicMock(spec=User)
        self.supervisor.id = 1
        self.supervisor.username = 'agus'

        self.cycle = MagicMock(spec=Cycle)
        self.cycle.id = 1
        self.cycle.supervisor = self.supervisor
        self.cycle.start_date = timezone.now().date()
        self.cycle.end_date = self.cycle.start_date + timezone.timedelta(days=60)

        self.cycle2 = MagicMock(spec=Cycle)
        self.cycle2.id = 2
        self.cycle2.supervisor = self.supervisor
        self.cycle2.start_date = timezone.now().date() - timezone.timedelta(days=61)
        self.cycle2.end_date = self.cycle2.start_date + timezone.timedelta(days=60)

        self.cycle3 = MagicMock(spec=Cycle)
        self.cycle3.id = 3
        self.cycle3.supervisor = self.supervisor
        self.cycle3.start_date = timezone.now().date() + timezone.timedelta(days=61)
        self.cycle3.end_date = self.cycle3.start_date + timezone.timedelta(days=60)

    @patch('cycle.repositories.cycle_repo.CycleRepo.get_cycle_past_or_future')
    def test_get_cycle_past(self, mock_get):
        mock_get.return_value = [self.cycle2]

        cycles = CycleService.get_cycle_past_or_future(self.supervisor, timezone.now().date(), 'past')
        mock_get.assert_called_once()
        self.assertEqual(len(cycles), 1)
        self.assertEqual(cycles[0].id, self.cycle2.id)

    @patch('cycle.repositories.cycle_repo.CycleRepo.get_cycle_past_or_future')
    def test_get_cycle_future(self, mock_get):
        mock_get.return_value = [self.cycle3]

        cycles = CycleService.get_cycle_past_or_future(self.supervisor, timezone.now().date(), 'future')
        mock_get.assert_called_once()
        self.assertEqual(len(cycles), 1)
        self.assertEqual(cycles[0].id, self.cycle3.id)

