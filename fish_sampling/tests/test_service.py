from unittest.mock import patch, MagicMock
from django.test import TestCase
from datetime import date
from fish_sampling.services import FishSamplingService
from fish_sampling.schemas import FishSamplingCreateSchema
from ninja.errors import HttpError

class FishSamplingServiceTest(TestCase):
    
    @patch('fish_sampling.repositories.FishSamplingRepository')
    def setUp(self, MockRepository):
        self.mock_repository = MockRepository()
        self.service = FishSamplingService(repository=self.mock_repository)
        
        self.mock_pond = MagicMock()
        self.mock_cycle = MagicMock()
        self.mock_reporter = MagicMock()
        self.mock_fish_sampling = MagicMock()

        self.mock_cycle.start_date = date(2024, 1, 1)
        self.mock_cycle.end_date = date(2024, 12, 31)
        
        self.mock_repository.get_pond.return_value = self.mock_pond
        self.mock_repository.get_cycle.return_value = self.mock_cycle
        self.mock_repository.get_reporter.return_value = self.mock_reporter

    def test_create_fish_sampling_existing_entry(self):
        payload = FishSamplingCreateSchema(
            fish_weight=10,
            fish_length=20,
        )

        self.mock_repository.get_existing_fish_sampling.return_value = self.mock_fish_sampling
        self.mock_repository.create_fish_sampling.return_value = self.mock_fish_sampling
        
        result = self.service.create_fish_sampling(
            pond_id='test_pond_id',
            cycle_id='test_cycle_id',
            reporter_id=1,
            payload=payload
        )
    
        self.mock_repository.delete_fish_sampling.assert_called_once_with(self.mock_fish_sampling)
        self.mock_repository.create_fish_sampling.assert_called_once()
        self.assertEqual(result, self.mock_fish_sampling)

    def test_create_fish_sampling_invalid_weight_length(self):
        payload = FishSamplingCreateSchema(
            fish_weight=-10, 
            fish_length=0, 
        )
        self.mock_repository.get_existing_fish_sampling.return_value = None
        with self.assertRaises(HttpError) as context:
            self.service.create_fish_sampling(
                pond_id='test_pond_id',
                cycle_id='test_cycle_id',
                reporter_id=1,
                payload=payload
            )
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(str(context.exception), self.service.INVALID_FISH_MEASUREMENTS)
    
    def test_create_fish_sampling_cycle_not_active(self):
        today = date(2024, 6, 15) 
        self.mock_cycle.start_date = date(2024, 1, 1)
        self.mock_cycle.end_date = date(2024, 5, 31) 
        self.mock_repository.get_cycle.return_value = self.mock_cycle

        payload = FishSamplingCreateSchema(
            fish_weight=10,
            fish_length=20,
        )

        self.mock_repository.get_existing_fish_sampling.return_value = None
        self.mock_repository.get_pond.return_value = self.mock_pond
        self.mock_repository.get_reporter.return_value = self.mock_reporter

        with self.assertRaises(HttpError) as context:
            self.service.create_fish_sampling(
                pond_id='test_pond_id',
                cycle_id='test_cycle_id',
                reporter_id=1,
                payload=payload
            )
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(str(context.exception), self.service.CYCLE_NOT_ACTIVE)
    
    def test_create_fish_sampling_value_error(self):
        payload = FishSamplingCreateSchema(
            fish_weight=10,
            fish_length=20,
        )

        self.mock_repository.create_fish_sampling.side_effect = ValueError

        with self.assertRaises(HttpError) as context:
            self.service.create_fish_sampling(
                pond_id='test_pond_id',
                cycle_id='test_cycle_id',
                reporter_id=1,
                payload=payload
            )
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(str(context.exception), self.service.INVALID_FISH_MEASUREMENTS)
    
    def test_get_latest_fish_sampling_success(self):
        self.mock_repository.get_latest_fish_sampling.return_value = self.mock_fish_sampling
        
        result = self.service.get_latest_fish_sampling(
            cycle_id='test_cycle_id', 
            pond_id='test_pond_id', 
            user=None
        )
        
        self.mock_repository.get_latest_fish_sampling.assert_called_with(self.mock_pond, self.mock_cycle)
        self.assertEqual(result, self.mock_fish_sampling)

    def test_get_latest_fish_sampling_not_found(self):
        self.mock_repository.get_latest_fish_sampling.return_value = None
        
        with self.assertRaises(HttpError) as context:
            self.service.get_latest_fish_sampling(
                cycle_id='test_cycle_id', 
                pond_id='test_pond_id', 
                user=None
            )
        
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(str(context.exception), self.service.DATA_NOT_FOUND)
    
    def test_get_latest_fish_sampling_cycle_not_active(self):
        today = date(2024, 6, 15)
        self.mock_cycle.start_date = date(2024, 1, 1)
        self.mock_cycle.end_date = date(2024, 5, 31)
        self.mock_repository.get_cycle.return_value = self.mock_cycle

        with self.assertRaises(HttpError) as context:
            self.service.get_latest_fish_sampling(
                cycle_id='test_cycle_id', 
                pond_id='test_pond_id', 
                user=None
            )
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(str(context.exception), self.service.CYCLE_NOT_ACTIVE)

    def test_list_fish_samplings_success(self):
        self.mock_repository.list_fish_samplings.return_value = [self.mock_fish_sampling]
        
        result = self.service.list_fish_samplings(
            cycle_id='test_cycle_id', 
            pond_id='test_pond_id', 
            user=None
        )
        
        self.mock_repository.list_fish_samplings.assert_called_with(self.mock_cycle, self.mock_pond)
        self.assertEqual(result, [self.mock_fish_sampling])

    def test_list_fish_samplings_no_data(self):
        self.mock_repository.list_fish_samplings.return_value = []
        
        result = self.service.list_fish_samplings(
            cycle_id='test_cycle_id', 
            pond_id='test_pond_id', 
            user=None
        )
        
        self.mock_repository.list_fish_samplings.assert_called_with(self.mock_cycle, self.mock_pond)
        self.assertEqual(result, [])
    
    def test_list_fish_samplings_cycle_not_active(self):
        today = date(2024, 6, 15)  
        self.mock_cycle.start_date = date(2024, 1, 1)
        self.mock_cycle.end_date = date(2024, 5, 31)
        self.mock_repository.get_cycle.return_value = self.mock_cycle

        with self.assertRaises(HttpError) as context:
            self.service.list_fish_samplings(
                cycle_id='test_cycle_id',
                pond_id='test_pond_id',
                user=None
            )
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(str(context.exception), self.service.CYCLE_NOT_ACTIVE)