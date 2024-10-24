import uuid
from django.test import TestCase
from unittest.mock import patch, MagicMock
from cycle.schemas import PondFishAmountInput
from cycle.models import Cycle
from cycle.services.pond_fish_amount_service import PondFishAmountService


class TestPondFishAmountService(TestCase):
    @patch('cycle.repositories.pond_fish_amount_repo.PondFishAmountRepo.bulk_create')
    def test_bulk_create_pond_fish_amount(self, mock_bulk_create):
        data = [
            PondFishAmountInput(pond_id=uuid.uuid4(), fish_amount=100),
            PondFishAmountInput(pond_id=uuid.uuid4(), fish_amount=150),
        ]
        
        mock_cycle = MagicMock(spec=Cycle)

        PondFishAmountService.bulk_create(data, mock_cycle)

        self.assertEqual(mock_bulk_create.call_count, 1)
    

    @patch('cycle.repositories.pond_fish_amount_repo.PondFishAmountRepo.bulk_create')
    def test_bulk_create_pond_fish_amount_invalid_amount(self, mock_bulk_create):
        data = [
            PondFishAmountInput(pond_id=uuid.uuid4(), fish_amount=0),
        ]

        mock_cycle = MagicMock(spec=Cycle)
        
        with self.assertRaises(ValueError) as context:
            PondFishAmountService.bulk_create(data, mock_cycle)

        self.assertEqual(str(context.exception), "Jumlah ikan harus lebih dari 0")
        self.assertEqual(mock_bulk_create.call_count, 0)


    @patch('cycle.repositories.pond_fish_amount_repo.PondFishAmountRepo.bulk_update')
    def test_bulk_update_pond_fish_amount(self, mock_bulk_update):
        data = [
            PondFishAmountInput(pond_id=uuid.uuid4(), fish_amount=200),
            PondFishAmountInput(pond_id=uuid.uuid4(), fish_amount=250),
        ]

        mock_cycle = MagicMock(spec=Cycle)

        PondFishAmountService.bulk_update(data, mock_cycle)

        self.assertEqual(mock_bulk_update.call_count, 1)


    @patch('cycle.repositories.pond_fish_amount_repo.PondFishAmountRepo.bulk_update')
    def test_bulk_update_pond_fish_amount_invalid_amount(self, mock_bulk_update):
        data = [
            PondFishAmountInput(pond_id=uuid.uuid4(), fish_amount=-50),
        ]

        mock_cycle = MagicMock(spec=Cycle)

        with self.assertRaises(ValueError) as context:
            PondFishAmountService.bulk_update(data, mock_cycle)

        self.assertEqual(str(context.exception), "Jumlah ikan harus lebih dari 0")
        self.assertEqual(mock_bulk_update.call_count, 0)
