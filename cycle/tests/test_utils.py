from django.test import TestCase
from datetime import date, timedelta
from cycle.utils import is_cycle_active, is_valid_fish_amount, is_valid_period
from unittest.mock import MagicMock

class CycleUtilsTest(TestCase):
    def test_is_cycle_active(self):
        cycle = MagicMock()
        cycle.start_date = date.today()
        cycle.end_date = date.today() + timedelta(days=60)
        
        self.assertTrue(is_cycle_active(cycle))

    def test_is_cycle_active_false(self):
        cycle = MagicMock()
        cycle.start_date = date.today() - timedelta(days=60)
        cycle.end_date = date.today() - timedelta(days=30)
        
        self.assertFalse(is_cycle_active(cycle))
    
    def test_is_valid_fish_amount(self):
        self.assertTrue(is_valid_fish_amount(1))

    def test_is_valid_fish_amount_false(self):
        self.assertFalse(is_valid_fish_amount(0))

    def test_is_valid_period(self):
        start_date = date.today()
        end_date = date.today() + timedelta(days=60)
        
        self.assertTrue(is_valid_period(start_date, end_date))

    def test_is_valid_period_false(self):
        start_date = date.today()
        end_date = date.today() + timedelta(days=59)
        
        self.assertFalse(is_valid_period(start_date, end_date))
