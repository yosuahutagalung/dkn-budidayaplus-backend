from django.test import TestCase
from django.contrib.auth.models import User
from pond.models import Pond
from cycle.models import Cycle, CycleFishDistribution
from ninja_jwt.tokens import AccessToken
from ninja.testing import TestClient
from cycle.api import router
from datetime import datetime, timedelta
import json

class CycleAPITest(TestCase):
    def setUp(self):
        start_time = datetime.strptime('2024-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=60)

        self.client = TestClient(router)
        self.user = User.objects.create_user(username='08123456789', password='admin1234')
        self.pond = Pond.objects.create(
            name='Pond 1',
            width=1,
            length=3,
            depth=2,
            owner=self.user,
            image_name='test1.jpg'
        )
        self.pond2 = Pond.objects.create(
            name='Pond 2', 
            width=1,
            depth=2,
            length=3,
            owner=self.user,
            image_name='test2.jpg'
        )
        self.cycle = Cycle.objects.create(
            supervisor = self.user,
            start_date = start_time,
            end_date = end_time,
        )
        self.cycle_fish_distribution = CycleFishDistribution.objects.create(
            cycle = self.cycle,
            pond = self.pond,
            fish_amount = 1000
        )

    def test_create_cycle(self):
        start_time = datetime.strptime('2024-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=60)

        response = self.client.post(
            "/",
            json.dumps({
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "pond_fish": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["start_date"], start_time.isoformat())
        self.assertEqual(data["end_date"], end_time.isoformat())
        self.assertEqual(data["supervisor"], self.user.username)
        self.assertEqual(data["pond_fish"], [
            {"pond_id": str(self.pond.pond_id), "fish_amount": 100},
            {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
        ])

    def test_create_cycle_invalid_date(self):
        start_time = datetime.strptime('2024-09-01', '%Y-%m-%d')
        end_time = start_time - timedelta(days=60)

        response = self.client.post(
            "/",
            json.dumps({
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "pond_fish": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"], "Tanggal selesai harus tepat 60 hari setelah tanggal mulai")

    def test_create_cycle_invalid_date2(self):
        start_time = datetime.strptime('2024-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=59)

        response = self.client.post(
            "/",
            json.dumps({
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "pond_fish": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"], "Tanggal selesai harus tepat 60 hari setelah tanggal mulai")

    def test_create_cycle_invalid_token(self):
        start_time = datetime.strptime('2024-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=60)

        response = self.client.post(
            "/",
            json.dumps({
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "pond_fish": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": "Bearer invalidToken"},
        )

        self.assertEqual(response.status_code, 401)

    def test_create_one_blank_field(self):
        end_time = datetime.strptime('2024-09-01', '%Y-%m-%d') + timedelta(days=60)

        response = self.client.post(
            "/",
            json.dumps({
                "end_date": end_time.isoformat(),
                "pond_fish": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )

        self.assertEqual(response.status_code, 422)

    def test_create_cycle_invalid_fish_amount(self):
        start_time = datetime.strptime('2024-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=60)

        response = self.client.post(
            "/",
            json.dumps({
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "pond_fish": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 0},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], "Jumlah ikan harus lebih dari 0")


    def test_get_cycle(self):
        response = self.client.get(
            "/",
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["start_date"], self.cycle.start_date.isoformat())
        self.assertEqual(data["end_date"], self.cycle.end_date.isoformat())
        self.assertEqual(data["supervisor"], self.user.username)
        self.assertEqual(data["pond_fish"], [
            {"pond_id": str(self.pond.pond_id), "fish_amount": 1000}
        ])

    def test_get_cycle_expired(self):
        now = datetime.today().date()
        start_time = now - timedelta(days=61)
        end_time = start_time + timedelta(days=60)

        self.cycle.start_date = start_time
        self.cycle.end_date = end_time
        self.cycle.save()

        response = self.client.get(
            "/",
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 404)

    def test_get_cycle_invalid_token(self):
        response = self.client.get(
            "/",
            headers={"Authorization": "Bearer invalidToken"},
        )
        self.assertEqual(response.status_code, 401)
