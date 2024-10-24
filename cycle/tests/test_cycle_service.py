from django.test import TestCase
from unittest.mock import MagicMock, patch
from cycle.schemas import CycleInput, PondFishAmountInput
from cycle.services.cycle_service import CycleService
from datetime import date, timedelta
import uuid


class CycleServiceTest(TestCase):
    def setUp(self):
        self.data_input = CycleInput(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            pond_fish_amount=[
                PondFishAmountInput(pond_id=uuid.uuid4(), fish_amount=10),
            ]
        )
        self.supervisor = MagicMock()

        patchers = [
            patch('cycle.repositories.cycle_repo.CycleRepo.is_active_cycle_exist'),
            patch('cycle.repositories.pond_fish_amount_repo.PondFishAmountRepo.bulk_create'),
            patch('cycle.repositories.cycle_repo.CycleRepo.create')
        ]
        
        self.mock_is_active_cycle_exist = patchers[0].start()
        self.mock_bulk_create_pfa = patchers[1].start()
        self.mock_create_cycle = patchers[2].start()

        self.addCleanup(patchers[0].stop)
        self.addCleanup(patchers[1].stop)
        self.addCleanup(patchers[2].stop)

    def test_create_cycle(self):
        self.mock_is_active_cycle_exist.return_value = False
        self.mock_create_cycle.return_value = MagicMock()

        cycle = CycleService.create_cycle(self.supervisor, self.data_input)

        self.assertEqual(self.mock_bulk_create_pfa.call_count, 1)
        self.assertEqual(self.mock_create_cycle.call_count, 1)
        self.assertEqual(cycle, self.mock_create_cycle.return_value)
        self.mock_bulk_create_pfa.assert_called_with(self.data_input.pond_fish_amount, self.mock_create_cycle.return_value)
        self.mock_is_active_cycle_exist.assert_called_with(self.supervisor, self.data_input.start_date, self.data_input.end_date)
        self.mock_create_cycle.assert_called_with(self.data_input.start_date, self.data_input.end_date, self.supervisor)


    def test_create_active_cycle_exists(self):
        self.mock_is_active_cycle_exist.return_value = True

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(self.supervisor, self.data_input)

        self.assertEqual(self.mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(self.mock_create_cycle.call_count, 0)
        self.assertEqual(self.mock_is_active_cycle_exist.call_count, 1)
        self.assertEqual(str(context.exception), "Anda sudah memiliki siklus yang aktif")
        self.mock_is_active_cycle_exist.assert_called_with(self.supervisor, self.data_input.start_date, self.data_input.end_date)


    def test_create_invalid_date_lt(self):
        self.mock_is_active_cycle_exist.return_value = False
        self.data_input.end_date -= timedelta(days=30)

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(self.supervisor, self.data_input)

        self.assertEqual(self.mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(self.mock_create_cycle.call_count, 0)
        self.assertEqual(str(context.exception), "Periode siklus harus 60 hari")


    def test_create_invalid_date_gt(self):
        self.mock_is_active_cycle_exist.return_value = False
        self.data_input.end_date += timedelta(days=1)

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(self.supervisor, self.data_input)

        self.assertEqual(self.mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(self.mock_create_cycle.call_count, 0)
        self.assertEqual(str(context.exception), "Periode siklus harus 60 hari")


    def test_create_invalid_fish_amount(self):
        self.mock_is_active_cycle_exist.return_value = False
        self.data_input.pond_fish_amount[0].fish_amount = 0

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(self.supervisor, self.data_input)

        self.assertEqual(str(context.exception), "Jumlah ikan harus lebih dari 0")
        self.assertEqual(self.mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(self.mock_create_cycle.call_count, 0)
        self.assertEqual(self.mock_is_active_cycle_exist.call_count, 1)


    @patch('cycle.repositories.cycle_repo.CycleRepo.get_cycle_by_id')
    def test_get_cycle_by_id(self, mock_get):
        mock_get.return_value = MagicMock()

        mock_cycle_id = str(uuid.uuid4())
        cycle = CycleService.get_cycle_by_id(mock_cycle_id)

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(cycle, mock_get.return_value) 
        mock_get.assert_called_with(mock_cycle_id)


    @patch('cycle.repositories.cycle_repo.CycleRepo.get_cycle_by_id')
    def test_get_cycle_by_id_not_exist(self, mock_get):
        mock_get.return_value = None
        mock_cycle_id = str(uuid.uuid4())

        with self.assertRaises(ValueError) as context:
            CycleService.get_cycle_by_id(mock_cycle_id)
        
        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(str(context.exception), "Siklus tidak ditemukan")
        mock_get.assert_called_with(mock_cycle_id)


    @patch('cycle.repositories.cycle_repo.CycleRepo.get_active_cycle')
    def test_get_active_cycle(self, mock_get):
        mock_get.return_value = MagicMock()

        cycle = CycleService.get_active_cycle(self.supervisor)

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(cycle, mock_get.return_value)
        mock_get.assert_called_with(self.supervisor)
    

    @patch('cycle.repositories.cycle_repo.CycleRepo.get_active_cycle')
    def test_get_active_cycle_not_exist(self, mock_get):
        mock_get.return_value = None

        with self.assertRaises(ValueError) as context:
            CycleService.get_active_cycle(self.supervisor)

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(str(context.exception), "Siklus tidak ditemukan")
        mock_get.assert_called_with(self.supervisor)