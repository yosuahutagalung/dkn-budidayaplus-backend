from django.test import TestCase
from django.contrib.auth.models import User
from pond.models import Pond
from cycle.models import Cycle, CycleFishDistribution
from ninja_jwt.tokens import AccessToken
from ninja.testing import TestClient
from cycle.api import router
from datetime import datetime, timedelta
import json, uuid

class CycleAPITest(TestCase):
    def setUp(self):
        start_time = datetime.strptime('2024-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=60)

        self.client = TestClient(router)
        self.user = User.objects.create_user(username='08123456789', password='12345')
        self.pond = Pond.objects.create(
            name='Pond 1',
            area=1000,
            depth=2,
            owner=self.user
        )
        self.pond2 = Pond.objects.create(
            name='Pond 2',
            area=1000,
            depth=2,
            owner=self.user
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
            "/cycle/",
            json.dumps({
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "pond_fish": [
                    {"pond_id": str(self.pond.id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["start_date"], start_time.isoformat())
        self.assertEqual(data["end_date"], end_time.isoformat())
        self.assertEqual(data["supervisor"], self.user.username)
        self.assertEqual(data["fish_distribution"], [])

    def test_create_cycle_invalid_date(self):
        start_time = datetime.strptime('2024-09-01', '%Y-%m-%d')
        end_time = start_time - timedelta(days=60)

        response = self.client.post(
            "/cycle/",
            json.dumps({
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "pond_fish": [
                    {"pond_id": str(self.pond.id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.id), "fish_amount": 200}
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
            "/cycle/",
            json.dumps({
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "pond_fish": [
                    {"pond_id": str(self.pond.id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.id), "fish_amount": 200}
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
            "/cycle/",
            json.dumps({
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "pond_fish": [
                    {"pond_id": str(self.pond.id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": f"Bearer invalidToken"},
        )

        self.assertEqual(response.status_code, 401)
