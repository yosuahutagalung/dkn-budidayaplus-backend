from django.test import TestCase
from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from cycle.models import Cycle
from django.utils import timezone

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

