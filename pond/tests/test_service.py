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
            patch('pond.repositories.PondRepository.get_pond_by_id'),
            patch('pond.repositories.PondRepository.list_ponds_by_user'),
            patch('pond.repositories.PondRepository.delete_pond'),
            patch('pond.repositories.PondRepository.update_pond')
        ]

        self.mock_create_pond = patchers[0].start()
        self.mock_get_pond_by_id = patchers[1].start()
        self.mock_list_ponds_by_user = patchers[2].start()
        self.mock_delete_pond = patchers[3].start()
        self.mock_update_pond = patchers[4].start()

        self.addCleanup(patchers[0].stop)
        self.addCleanup(patchers[1].stop)
        self.addCleanup(patchers[2].stop)
        self.addCleanup(patchers[3].stop)
        self.addCleanup(patchers[4].stop)

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

    def test_get_pond(self):
        mock_pond = MagicMock()
        self.mock_get_pond_by_id.return_value = mock_pond
        
        pond = PondService.get_pond(self.pond_id)
        
        self.mock_get_pond_by_id.assert_called_once_with(self.pond_id)
        self.assertEqual(pond, mock_pond)

    def test_list_ponds_by_user(self):
        mock_ponds = [MagicMock(), MagicMock()]
        self.mock_list_ponds_by_user.return_value = mock_ponds
        
        ponds = PondService.list_ponds_by_user(self.user)
        
        self.mock_list_ponds_by_user.assert_called_once_with(self.user)
        self.assertEqual(ponds, mock_ponds)

    def test_delete_pond(self):
        PondService.delete_pond(self.pond_id)
        
        self.mock_delete_pond.assert_called_once_with(self.pond_id)
        self.assertTrue(self.mock_delete_pond.called)

    def test_update_pond(self):
        self.mock_update_pond.return_value = MagicMock()
        
        pond = PondService.update_pond(self.pond_id, self.pond_data)
        
        self.mock_update_pond.assert_called_once_with(
            pond=self.mock_get_pond_by_id.return_value,
            name=self.pond_data.name,
            image_name=self.pond_data.image_name,
            length=self.pond_data.length,
            width=self.pond_data.width,
            depth=self.pond_data.depth
        )
        self.assertEqual(pond, self.mock_update_pond.return_value)