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

class CycleAPITest(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='08123456789', password='admin1234')
        self.data_input = {
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
        }
        
    @patch('cycle.services.cycle_service.CycleService.create_cycle')
    def test_create_cycle(self, mock_create_cycle):
        mock_cycle = MagicMock(spec=Cycle)
        mock_cycle.id = uuid.uuid4()  
        mock_cycle.start_date = date(2024, 10, 23)  
        mock_cycle.end_date = date(2024, 12, 22)  
        mock_cycle.supervisor = self.user  
        mock_create_cycle.return_value = mock_cycle

        response = self.client.post(
            '/', 
            data=json.dumps(self.data_input),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )

        self.assertEqual(response.status_code, 200)
    
    @patch('cycle.services.cycle_service.CycleService.create_cycle')
    def test_create_cycle_active_cycle_exist(self, mock_create_cycle):
        mock_create_cycle.side_effect = ValueError("Anda sudah memiliki siklus yang aktif")

        response = self.client.post('/', data=json.dumps(self.data_input), headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Anda sudah memiliki siklus yang aktif'})

    @patch('cycle.services.cycle_service.CycleService.create_cycle')
    def test_create_cycle_invalid_fish_amount(self, mock_create_cycle):
        mock_create_cycle.side_effect = ValueError("Jumlah ikan harus lebih besar dari 0")
        self.data_input['pond_fish_amount'][0]['fish_amount'] = 0

        response = self.client.post('/', data=json.dumps(self.data_input), headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Jumlah ikan harus lebih besar dari 0'})
    
    @patch('cycle.services.cycle_service.CycleService.create_cycle')
    def test_create_cycle_invalid_date(self, mock_create_cycle):
        mock_create_cycle.side_effect = ValueError("Periode siklus harus 60 hari")
        self.data_input['end_date'] = '2024-10-24'

        response = self.client.post('/', data=json.dumps(self.data_input), headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Periode siklus harus 60 hari'})

    @patch('cycle.services.cycle_service.CycleService.create_cycle')
    def test_create_cycle_generic_error(self, mock_create_cycle):
        mock_create_cycle.side_effect = Exception("Unexpected error")

        response = self.client.post('/', data=json.dumps(self.data_input), headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Unexpected error'})


    @patch('cycle.services.cycle_service.CycleService.get_active_cycle')
    def test_get_active_cycle_exists(self, mock_get):
        mock_cycle = MagicMock(spec=Cycle)
        mock_cycle.id = uuid.uuid4()  
        mock_cycle.start_date = date(2024, 10, 23)  
        mock_cycle.end_date = date(2024, 12, 22)  
        mock_cycle.supervisor = self.user  
        mock_get.return_value = mock_cycle

        response = self.client.get('/', headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'id': str(mock_cycle.id),
            'start_date': '2024-10-23',
            'end_date': '2024-12-22',
            'supervisor': self.user.username,
            'pond_fish_amount': []
        })

    @patch('cycle.services.cycle_service.CycleService.get_active_cycle')
    def test_get_active_cycle_not_exists(self, mock_get):
        mock_get.return_value = None
        response = self.client.get('/', headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Tidak ada siklus yang aktif'})

    @patch('cycle.services.cycle_service.CycleService.get_active_cycle')
    def test_get_active_cycle_generic_error(self, mock_get):
        mock_get.side_effect = Exception("Unexpected error")
        response = self.client.get('/', headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})
        self.assertEqual(response.status_code, 400)
    
    @patch('cycle.services.cycle_service.CycleService.get_cycle_by_id')
    def test_get_cycle_by_id(self, mock_get):
        mock_cycle = MagicMock(spec=Cycle)
        mock_cycle.id = uuid.uuid4()  
        mock_cycle.start_date = date(2024, 10, 23)  
        mock_cycle.end_date = date(2024, 12, 22)  
        mock_cycle.supervisor = self.user  
        mock_get.return_value = mock_cycle

        response = self.client.get(f'/{mock_cycle.id}/', headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'id': str(mock_cycle.id),
            'start_date': '2024-10-23',
            'end_date': '2024-12-22',
            'supervisor': self.user.username,
            'pond_fish_amount': []
        })
    
    @patch('cycle.services.cycle_service.CycleService.get_cycle_by_id')
    def test_get_cycle_by_id_not_found(self, mock_get):
        mock_get.return_value = None

        response = self.client.get(f'/{uuid.uuid4()}/', headers = {"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Siklus tidak ditemukan'})

    @patch('cycle.services.cycle_service.CycleService.get_cycle_by_id')
    def test_get_cycle_by_id_generic_error(self, mock_get):
        mock_get.side_effect = Exception("Unexpected error")

        response = self.client.get(f'/{uuid.uuid4()}/', headers = {"Authorization": f"Bearer {AccessToken.for_user(self.user)}"})

        self.assertEqual(response.status_code, 400)

    @patch('cycle.services.cycle_service.CycleService.stop_cycle')
    def test_stop_cycle(self, mock_stop_cycle):
        mock_cycle = MagicMock(spec=Cycle)
        mock_cycle.id = uuid.uuid4()
        mock_cycle.is_stopped = True
        mock_stop_cycle.return_value = mock_cycle

        response = self.client.post(
            f'/stop/{mock_cycle.id}/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Siklus berhasil dihentikan"})

    @patch('cycle.services.cycle_service.CycleService.get_cycle_by_id')
    def test_get_cycle_by_id(self, mock_get_cycle_by_id):
        mock_cycle = MagicMock(spec=Cycle)
        mock_cycle.id = uuid.uuid4()
        mock_cycle.start_date = date(2024, 10, 23)
        mock_cycle.end_date = date(2024, 12, 22)
        mock_cycle.supervisor = self.user
        mock_get_cycle_by_id.return_value = mock_cycle

        response = self.client.get(
            f'/{mock_cycle.id}/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )
        self.assertEqual(response.status_code, 200)

    @patch('cycle.services.cycle_service.CycleService.get_cycle_by_id')
    def test_get_cycle_by_id_not_found(self, mock_get_cycle_by_id):
        mock_get_cycle_by_id.return_value = None

        response = self.client.get(
            f'/{uuid.uuid4()}/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )
        self.assertEqual(response.status_code, 404)

    @patch('cycle.services.cycle_service.CycleService.stop_cycle')
    def test_stop_cycle_value_error(self, mock_stop_cycle):
        mock_stop_cycle.side_effect = ValueError("Cycle not found or unauthorized")
    
        response = self.client.post(
            f'/stop/{uuid.uuid4()}/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )
    
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Cycle not found or unauthorized'})

    @patch('cycle.services.cycle_service.CycleService.stop_cycle')
    def test_stop_cycle_generic_exception(self, mock_stop_cycle):
        mock_stop_cycle.side_effect = Exception("Unexpected error occurred")
    
        response = self.client.post(
            f'/stop/{uuid.uuid4()}/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )
    
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Unexpected error occurred'})



