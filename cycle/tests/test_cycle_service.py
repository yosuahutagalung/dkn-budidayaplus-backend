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


    @patch('cycle.repositories.cycle_repo.CycleRepo.is_active_cycle_exist') 
    @patch('cycle.repositories.pond_fish_amount_repo.PondFishAmountRepo.bulk_create')  
    @patch('cycle.repositories.cycle_repo.CycleRepo.create')
    def test_create_cycle(self, mock_create_cycle, mock_bulk_create_pfa, mock_is_active_cycle_exist):
        mock_is_active_cycle_exist.return_value = False
        mock_create_cycle.return_value = MagicMock()

        cycle = CycleService.create_cycle(MagicMock(), self.data_input)

        self.assertEqual(mock_bulk_create_pfa.call_count, 1)
        self.assertEqual(mock_create_cycle.call_count, 1)
        self.assertEqual(cycle, mock_create_cycle.return_value)


    @patch('cycle.repositories.cycle_repo.CycleRepo.is_active_cycle_exist') 
    @patch('cycle.repositories.pond_fish_amount_repo.PondFishAmountRepo.bulk_create')  
    @patch('cycle.repositories.cycle_repo.CycleRepo.create')
    def test_create_active_cycle_exists(self, mock_create_cycle, mock_bulk_create_pfa, mock_is_active_cycle_exist):
        mock_is_active_cycle_exist.return_value = True

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(MagicMock(), self.data_input)

        self.assertEqual(mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(mock_create_cycle.call_count, 0)
        self.assertEqual(mock_is_active_cycle_exist.call_count, 1)
        self.assertEqual(str(context.exception), "Anda sudah memiliki siklus yang aktif")


    @patch('cycle.repositories.cycle_repo.CycleRepo.is_active_cycle_exist') 
    @patch('cycle.repositories.pond_fish_amount_repo.PondFishAmountRepo.bulk_create')  
    @patch('cycle.repositories.cycle_repo.CycleRepo.create')
    def test_create_invalid_date_lt(self, mock_create_cycle, mock_bulk_create_pfa, mock_is_active_cycle_exist):
        mock_is_active_cycle_exist.return_value = False

        data_input = CycleInput(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            pond_fish_amount=[
                PondFishAmountInput(pond_id=uuid.uuid4(), fish_amount=10),
            ]
        )

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(MagicMock(), data_input)

        self.assertEqual(mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(mock_create_cycle.call_count, 0)
        self.assertEqual(str(context.exception), "Periode siklus harus 60 hari")


    @patch('cycle.repositories.cycle_repo.CycleRepo.is_active_cycle_exist') 
    @patch('cycle.repositories.pond_fish_amount_repo.PondFishAmountRepo.bulk_create')  
    @patch('cycle.repositories.cycle_repo.CycleRepo.create')
    def test_create_invalid_date_gt(self, mock_create_cycle, mock_bulk_create_pfa, mock_is_active_cycle_exist):
        mock_is_active_cycle_exist.return_value = False

        data_input = CycleInput(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=61),
            pond_fish_amount=[
                PondFishAmountInput(pond_id=uuid.uuid4(), fish_amount=10),
            ]
        )

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(MagicMock(), data_input)

        self.assertEqual(mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(mock_create_cycle.call_count, 0)
        self.assertEqual(str(context.exception), "Periode siklus harus 60 hari")
    

    @patch('cycle.repositories.cycle_repo.CycleRepo.is_active_cycle_exist') 
    @patch('cycle.repositories.pond_fish_amount_repo.PondFishAmountRepo.bulk_create')  
    @patch('cycle.repositories.cycle_repo.CycleRepo.create')
    def test_create_invalid_fish_amount(self, mock_create_cycle, mock_bulk_create_pfa, mock_is_active_cycle_exist):
        mock_is_active_cycle_exist.return_value = False

        data_input = CycleInput(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            pond_fish_amount=[
                PondFishAmountInput(pond_id=uuid.uuid4(), fish_amount=-10),
            ]
        )

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(MagicMock(), data_input)

        self.assertEqual(str(context.exception), "Jumlah ikan harus lebih dari 0")
        self.assertEqual(mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(mock_create_cycle.call_count, 0)
        self.assertEqual(mock_is_active_cycle_exist.call_count, 1)
