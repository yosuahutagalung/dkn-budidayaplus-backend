from django.test import TestCase
from unittest.mock import patch, MagicMock
from cycle.services.cycle_service import CycleService
from cycle.repositories.cycle_repo import CycleRepo

class CycleServiceTest(TestCase):
    
    @patch.object(CycleRepo, 'get_cycle_by_id')
    def test_get_cycle_by_id_success_with_stub(self, mock_get_cycle_by_id):
        class StubCycle:
            def __init__(self, id):
                self.id = id
                self.start_date = "2024-01-01"
                self.end_date = "2024-03-01"
                self.supervisor = MagicMock()

        mock_get_cycle_by_id.return_value = StubCycle('valid_id')

        cycle = CycleService.get_cycle_by_id('valid_id')
        
        self.assertEqual(cycle.id, 'valid_id')
        self.assertEqual(cycle.start_date, "2024-01-01")
        self.assertEqual(cycle.end_date, "2024-03-01")

    @patch.object(CycleRepo, 'get_cycle_by_id')
    def test_get_cycle_by_id_not_found_with_stub(self, mock_get_cycle_by_id):
        mock_get_cycle_by_id.return_value = None
        
        with self.assertRaises(ValueError) as context:
            CycleService.get_cycle_by_id('invalid_id')
        
        self.assertEqual(str(context.exception), "Siklus tidak ditemukan")