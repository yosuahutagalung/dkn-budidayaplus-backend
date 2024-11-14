from unittest.mock import patch, MagicMock
from django.test import TestCase
from datetime import datetime
from pond_quality.services.pond_quality_service import PondQualityService
from pond_quality.schemas import PondQualityInput
from ninja.errors import HttpError


class PondQualityServiceTest(TestCase):
    
    @patch('pond_quality.repositories.pond_quality_repository.PondQualityRepository')
    def setUp(self, MockRepository):
        self.mock_repository = MockRepository()
        self.service = PondQualityService(repository=self.mock_repository)
        
        self.mock_pond = MagicMock()
        self.mock_cycle = MagicMock()
        self.mock_reporter = MagicMock()
        self.mock_pond_quality = MagicMock()

        self.mock_repository.get_pond.return_value = self.mock_pond
        self.mock_repository.get_cycle.return_value = self.mock_cycle
        self.mock_repository.get_reporter.return_value = self.mock_reporter

    def test_create_pond_quality_existing_entry(self):
        payload = PondQualityInput(
            image_name = 'test.jpg',
            ph_level = 7.0,
            salinity = 0.0,
            water_temperature = 25.0,
            water_clarity = 0.0,
            water_circulation = 0.0,
            dissolved_oxygen = 0.0,
            orp = 0.0,
            ammonia = 0.0,
            nitrate = 0.0,
            phosphate = 0.0
        )
        self.mock_repository.get_existing_pond_quality.return_value = self.mock_pond_quality
        self.mock_repository.create_pond_quality.return_value = self.mock_pond_quality

        result = self.service.create_pond_quality(
            pond_id='test_pond_id',
            cycle_id='test_cycle_id',
            reporter_id=1,
            payload=payload
        )
    
        self.mock_repository.delete_pond_quality.assert_called_once_with(self.mock_pond_quality)
        self.mock_repository.create_pond_quality.assert_called_once()
        self.assertEqual(result, self.mock_pond_quality)

    def test_create_pond_quality_invalid_ph(self):
        payload = PondQualityInput(
            image_name = 'test.jpg',
            ph_level = 15.0,
            salinity = 0.0,
            water_temperature = 25.0,
            water_clarity = 0.0,
            water_circulation = 0.0,
            dissolved_oxygen = 0.0,
            orp = 0.0,
            ammonia = 0.0,
            nitrate = 0.0,
            phosphate = 0.0
        )
        self.mock_repository.get_existing_pond_quality.return_value = None
        self.mock_repository.create_pond_quality.side_effect = ValueError("Invalid pond quality")

        with self.assertRaises(HttpError) as context:
            self.service.create_pond_quality(
                pond_id='test_pond_id',
                cycle_id='test_cycle_id',
                reporter_id=1,
                payload=payload
            )
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(str(context.exception), self.service.INVALID_POND_QUALITY)