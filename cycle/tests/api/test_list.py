from django.http import HttpRequest
from django.test import TestCase
from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from ninja.errors import HttpError
from cycle.models import Cycle
from django.utils import timezone
from cycle.api import get_cycle_list

class TestListCycleAPI(TestCase):
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

        self.request = MagicMock(spec=HttpRequest)
        self.request.auth = self.supervisor

    def test_list_cycle(self):
        with patch('cycle.services.cycle_service.CycleService.get_active_cycle_safe', return_value=[self.cycle]) as mock_get_active_cycle_safe, \
            patch('cycle.services.cycle_service.CycleService.get_cycle_past_or_future', side_effect=[[self.cycle2], [self.cycle3]]) as mock_get_cycle_past_or_future:
            cycles = get_cycle_list(self.request)
            self.assertEqual(cycles['active'], [self.cycle])
            self.assertEqual(cycles['past'], [self.cycle2])
            self.assertEqual(cycles['future'], [self.cycle3])

            mock_get_active_cycle_safe.assert_called_once()
            mock_get_cycle_past_or_future.assert_any_call(self.supervisor, timezone.now().date(), 'past')
            mock_get_cycle_past_or_future.assert_any_call(self.supervisor, timezone.now().date(), 'future')

    def test_list_cycle_error(self):
        with patch('cycle.services.cycle_service.CycleService.get_active_cycle_safe', side_effect=Exception('Unexpected error occured')) as mock_get_active_cycle_safe:
            with self.assertRaises(HttpError) as context:
                get_cycle_list(self.request)
                self.assertEqual(str(context.exception), 'Unexpected error occured')

            mock_get_active_cycle_safe.assert_called_once()

