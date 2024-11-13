from unittest.mock import patch, MagicMock
from django.test import TestCase
from datetime import datetime
from food_sampling.services.food_sampling_service import FoodSamplingService
from food_sampling.schemas import FoodSamplingCreateSchema
from ninja.errors import HttpError


class FoodSamplingServiceTest(TestCase):
    
    @patch('food_sampling.repositories.food_sampling_repository.FoodSamplingRepository')
    def setUp(self, MockRepository):
        self.mock_repository = MockRepository()
        self.service = FoodSamplingService(repository=self.mock_repository)
        
        self.mock_pond = MagicMock()
        self.mock_cycle = MagicMock()
        self.mock_reporter = MagicMock()
        self.mock_food_sampling = MagicMock()

        self.mock_repository.get_pond.return_value = self.mock_pond
        self.mock_repository.get_cycle.return_value = self.mock_cycle
        self.mock_repository.get_reporter.return_value = self.mock_reporter

    def test_create_food_sampling_existing_entry(self):
        payload = FoodSamplingCreateSchema(
            food_quantity=20,
            recorded_at=datetime.now()
        )
        self.mock_repository.get_existing_food_sampling.return_value = self.mock_food_sampling
        self.mock_repository.create_food_sampling.return_value = self.mock_food_sampling

        result = self.service.create_food_sampling(
            pond_id='test_pond_id',
            cycle_id='test_cycle_id',
            reporter_id=1,
            payload=payload
        )
    
        self.mock_repository.delete_food_sampling.assert_called_once_with(self.mock_food_sampling)
        self.mock_repository.create_food_sampling.assert_called_once()
        self.assertEqual(result, self.mock_food_sampling)

    def test_create_food_sampling_invalid_quantity(self):
        payload = FoodSamplingCreateSchema(
            food_quantity=-10, 
            recorded_at=datetime.now()
        )
        self.mock_repository.get_existing_food_sampling.return_value = None
        self.mock_repository.create_food_sampling.side_effect = ValueError("Invalid food quantity")

        with self.assertRaises(HttpError) as context:
            self.service.create_food_sampling(
                pond_id='test_pond_id',
                cycle_id='test_cycle_id',
                reporter_id=1,
                payload=payload
            )
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(str(context.exception), self.service.INVALID_FOOD_QUANTITY)
