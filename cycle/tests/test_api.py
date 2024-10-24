import uuid
import json

from django.test import TestCase
from cycle.api import router
from ninja.testing import TestClient
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from cycle.models import Cycle
from ninja_jwt.tokens import AccessToken
from datetime import date
from cycle.schemas import CycleInput

class CycleAPITest(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='08123456789', password='admin1234')
        self.data_input = CycleInput(
            start_date='2024-10-23',
            end_date='2024-12-22',
            pond_fish_amount=[
                {
                    'pond_id': f"{uuid.uuid4()}",
                    'fish_amount': 10
                },
                {
                    'pond_id': f"{uuid.uuid4()}",
                    'fish_amount': 20
                }
            ]
        )
        
    @patch('cycle.services.cycle_service.CycleService.create_cycle')
    def test_create_cycle(self, mock_create_cycle):
        mock_cycle = MagicMock(spec=Cycle)
        mock_cycle.id = uuid.uuid4()  
        mock_cycle.start_date = date(2024, 10, 23)  
        mock_cycle.end_date = date(2024, 12, 22)  
        mock_cycle.supervisor = self.user  
        mock_create_cycle.return_value = mock_cycle

        response = self.client.post('/', data=json.dumps({
            'start_date': '2024-10-23',
            'end_date': '2024-12-22',
            'pond_fish_amount': [
                {
                    'pond_id': f"{uuid.uuid4()}",
                    'fish_amount': 10
                },
                {
                    'pond_id': f"{uuid.uuid4()}",
                    'fish_amount': 20
                }
            ]
        }), headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 200)

    @patch('cycle.services.cycle_service.CycleService.create_cycle')
    def test_create_cycle_invalid_fish_amount(self, mock_create_cycle):
        mock_create_cycle.side_effect = ValueError("Jumlah ikan harus lebih besar dari 0")

        response = self.client.post('/', data=json.dumps({
            'start_date': '2024-10-23',
            'end_date': '2024-12-22',
            'pond_fish_amount': [
                {
                    'pond_id': f"{uuid.uuid4()}",
                    'fish_amount': 0
                },
                {
                    'pond_id': f"{uuid.uuid4()}",
                    'fish_amount': 20
                }
            ]
        }), headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Jumlah ikan harus lebih besar dari 0'})
    
    @patch('cycle.services.cycle_service.CycleService.create_cycle')
    def test_create_cycle_invalid_date(self, mock_create_cycle):
        mock_create_cycle.side_effect = ValueError("Periode siklus harus 60 hari")

        response = self.client.post('/', data=json.dumps({
            'start_date': '2024-10-23',
            'end_date': '2024-10-24',
            'pond_fish_amount': [
                {
                    'pond_id': f"{uuid.uuid4()}",
                    'fish_amount': 10
                },
                {
                    'pond_id': f"{uuid.uuid4()}",
                    'fish_amount': 20
                }
            ]
        }), headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Periode siklus harus 60 hari'})

    @patch('cycle.services.cycle_service.CycleService.create_cycle')
    def test_create_cycle_generic_error(self, mock_create_cycle):
        mock_create_cycle.side_effect = Exception("Unexpected error")

        response = self.client.post('/', data=json.dumps({
            'start_date': '2024-10-23',
            'end_date': '2024-12-22',
            'pond_fish_amount': [
                {
                    'pond_id': f"{uuid.uuid4()}",
                    'fish_amount': 10
                },
                {
                    'pond_id': f"{uuid.uuid4()}",
                    'fish_amount': 20
                }
            ]
        }), headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Unexpected error'})
