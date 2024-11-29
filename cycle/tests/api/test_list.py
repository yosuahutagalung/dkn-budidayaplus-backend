from django.http import HttpRequest
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

        self.active_cycle = MagicMock(spec=Cycle)
        self.active_cycle.id = 1
        self.active_cycle.supervisor = self.supervisor
        self.active_cycle.start_date = timezone.now().date()
        self.active_cycle.end_date = self.active_cycle.start_date + timezone.timedelta(days=60)

        self.past_cycle = MagicMock(spec=Cycle)
        self.past_cycle.id = 2
        self.past_cycle.supervisor = self.supervisor
        self.past_cycle.start_date = timezone.now().date() - timezone.timedelta(days=61)
        self.past_cycle.end_date = self.past_cycle.start_date + timezone.timedelta(days=60)

        self.future_cycle = MagicMock(spec=Cycle)
        self.future_cycle.id = 3
        self.future_cycle.supervisor = self.supervisor
        self.future_cycle.start_date = timezone.now().date() + timezone.timedelta(days=61)
        self.future_cycle.end_date = self.future_cycle.start_date + timezone.timedelta(days=60)

        self.stopped_cycle = MagicMock(spec=Cycle)
        self.stopped_cycle.id = 4
        self.stopped_cycle.supervisor = self.supervisor
        self.stopped_cycle.start_date = timezone.now().date() - timezone.timedelta(days=30)
        self.stopped_cycle.end_date = timezone.now().date()
        self.stopped_cycle.is_stopped = True

        self.request = MagicMock(spec=HttpRequest)
        self.request.auth = self.supervisor

    def test_list_cycle(self):
        with patch('cycle.services.cycle_service.CycleService.get_active_cycle_safe', return_value=[self.active_cycle]) as mock_get_active_cycle_safe, \
            patch('cycle.services.cycle_service.CycleService.get_cycle_past_or_future', side_effect=[[self.past_cycle], [self.future_cycle]]) as mock_get_cycle_past_or_future, \
            patch('cycle.services.cycle_service.CycleService.get_stopped_cycle', return_value=[self.stopped_cycle]) as mock_get_stopped_cycles:

            cycles = get_cycle_list(self.request)
            self.assertEqual(cycles['active'], [self.active_cycle])
            self.assertEqual(cycles['past'], [self.past_cycle])
            self.assertEqual(cycles['future'], [self.future_cycle])
            self.assertEqual(cycles['stopped'], [self.stopped_cycle])

            mock_get_active_cycle_safe.assert_called_once()
            mock_get_cycle_past_or_future.assert_any_call(self.supervisor, timezone.now().date(), 'past')
            mock_get_cycle_past_or_future.assert_any_call(self.supervisor, timezone.now().date(), 'future')
            mock_get_stopped_cycles.assert_called_once_with(self.supervisor)

    def test_list_cycle_error(self):
        with patch('cycle.services.cycle_service.CycleService.get_active_cycle_safe', side_effect=Exception('Unexpected error occurred')) as mock_get_active_cycle_safe:
            with self.assertRaises(HttpError) as context:
                get_cycle_list(self.request)
            self.assertEqual(str(context.exception), 'Unexpected error occurred')
            mock_get_active_cycle_safe.assert_called_once()
