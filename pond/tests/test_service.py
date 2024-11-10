from django.test import TestCase
from unittest.mock import MagicMock, patch
import uuid
from pond.services import PondService
from pond.schemas import PondSchema

class PondServiceTest(TestCase):
    def setUp(self):
        self.pond_data = PondSchema(
            name="Test Pond",
            image_name="test_image.jpg",
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.user = MagicMock()
        self.pond_id = uuid.uuid4()

        patchers = [
            patch('pond.repositories.PondRepository.create_pond'),
            patch('pond.repositories.PondRepository.delete_pond')
        ]

        self.mock_create_pond = patchers[0].start()
        self.mock_delete_pond = patchers[1].start()

        self.addCleanup(patchers[0].stop)
        self.addCleanup(patchers[1].stop)

    def test_add_pond(self):
        self.mock_create_pond.return_value = MagicMock()
        
        pond = PondService.add_pond(self.user, self.pond_data)
        
        self.mock_create_pond.assert_called_once_with(
            owner=self.user,
            name=self.pond_data.name,
            image_name=self.pond_data.image_name,
            length=self.pond_data.length,
            width=self.pond_data.width,
            depth=self.pond_data.depth
        )
        self.assertEqual(pond, self.mock_create_pond.return_value)

    def test_delete_pond(self):
        PondService.delete_pond(self.pond_id)
        
        self.mock_delete_pond.assert_called_once_with(self.pond_id)
        self.assertTrue(self.mock_delete_pond.called)