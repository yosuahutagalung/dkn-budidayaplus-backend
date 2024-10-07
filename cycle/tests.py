from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from ninja.testing import TestClient
from pond.models import Pond
from cycle.models import Cycle
from cycle.api import router
import json, uuid

# Create your tests here.
class CycleAPITest(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='08123456789', password='12345')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
            image_name='test_image.jpg',
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.cycle = Cycle.objects.create(
            owner=self.user,
            pond=self.pond,
            fish_amounts = 10,
            starting_date='2024-09-01',
            ending_date='2024-11-01'
        )
        self.cycle2 = Cycle.objects.create(
            owner=self.user,
            pond=self.pond,
            fish_amounts = 10,
            starting_date='2024-06-01',
            ending_date='2024-08-01'
        )
    
    def test_add_cycle(self):
        response = self.client.post(f'/{self.pond.pond_id}/', data=json.dumps({
            'fish_amounts': 10,
            'starting_date': '2024-09-01',
            'ending_date': '2024-11-01'
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['fish_amounts'], 10)

    def test_add_cycle_no_fishes(self):
        response = self.client.post(f'/{self.pond.pond_id}/', data=json.dumps({
            'starting_date': '2024-09-01',
            'ending_date': '2024-11-01'
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 422)

    def test_get_cycle(self):
        response = self.client.get(f'/{self.pond.pond_id}/cycle_id/{self.cycle.cycle_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['fish_amounts'], 10)

    def test_get_cycle_not_found(self):
        response = self.client.get(f'/{self.pond.pond_id}/cycle_id/{uuid.uuid4()}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_list_cycles_by_pond(self):
        response = self.client.get(f'/{self.pond.pond_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_list_cycles_by_user_invalid_token(self):
        response = self.client.get(f'/{self.pond.pond_id}/', headers={"Authorization": f"Bearer Invalid Token"})
        self.assertEqual(response.status_code, 401)

    def test_delete_cycle(self):
        response = self.client.delete(f'/{self.pond.pond_id}/cycle_id/{self.cycle.cycle_id}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_delete_cycle_not_found(self):
        response = self.client.delete(f'/{self.pond.pond_id}/cycle_id/{uuid.uuid4()}/', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_update_cycle(self):
        response = self.client.put(f'/{self.pond.pond_id}/cycle_id/{self.cycle.cycle_id}/', data=json.dumps({
            'fish_amounts': 20,
            'starting_date': '2024-12-01',
            'ending_date': '2025-02-01'
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['fish_amounts'], 20)

    def test_update_cycle_not_found(self):
        response = self.client.put(f'/{self.pond.pond_id}/cycle_id/{uuid.uuid4()}/', data=json.dumps({
            'fish_amounts': 20,
            'starting_date': '2024-12-01',
            'ending_date': '2025-02-01'
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 404)

    def test_update_cycle_no_fish(self):
        response = self.client.put(f'/{self.pond.pond_id}/cycle_id/{self.cycle.cycle_id}/', data=json.dumps({
            'starting_date': '2024-12-01',
            'ending_date': '2025-02-01'
        }), content_type='application/json', headers={"Authorization": f"Bearer {str(AccessToken.for_user(self.user))}"})
        self.assertEqual(response.status_code, 422)

class CycleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='08123456789', password='12345')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
            image_name='test_image.jpg',
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.cycle = Cycle.objects.create(
            owner=self.user,
            pond=self.pond,
            fish_amounts = 10,
            starting_date='2024-09-01',
            ending_date='2024-11-01'
        )

    def test_str_method(self):
        self.assertEqual(str(self.cycle), str(self.cycle.cycle_id))
