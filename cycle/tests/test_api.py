from django.test import TestCase
from django.contrib.auth.models import User
from pond.models import Pond
from cycle.models import Cycle, PondFishAmount
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
        self.user = User.objects.create_user(username='08123456789', password='admin1234')
        self.pond = Pond.objects.create(
            pond_id='d5cdec09-4762-46cc-a6df-ae98b79c3284',
            name='Pond 1',
            width=1,
            length=3,
            depth=2,
            owner=self.user,
            image_name='test1.jpg'
        )
        self.pond2 = Pond.objects.create(
            pond_id='52723ad4-8900-42ad-aadf-51e62ad31b7d',
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
        self.cycle_fish_distribution = PondFishAmount.objects.create(
            cycle = self.cycle,
            pond = self.pond,
            fish_amount = 1000
        )

    def test_create_cycle(self):
        start_time = datetime.strptime('2025-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=60)

        response = self.client.post(
            "/",
            json.dumps({
                "start_date": start_time.strftime('%Y-%m-%d'),
                "end_date": end_time.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["start_date"], start_time.strftime('%Y-%m-%d'))
        self.assertEqual(data["end_date"], end_time.strftime('%Y-%m-%d'))
        self.assertEqual(data["supervisor"], self.user.username)

    def test_create_cycle_invalid_date(self):
        start_time = datetime.strptime('2025-11-01', '%Y-%m-%d')
        end_time = start_time - timedelta(days=60)

        response = self.client.post(
            "/",
            json.dumps({
                "start_date": start_time.strftime('%Y-%m-%d'),
                "end_date": end_time.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
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
        start_time = datetime.strptime('2025-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=59)

        response = self.client.post(
            "/",
            json.dumps({
                "start_date": start_time.strftime('%Y-%m-%d'),
                "end_date": end_time.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"], "Tanggal selesai harus tepat 60 hari setelah tanggal mulai")

    def test_create_cycle_overlapping(self):
        start_time = datetime.strptime('2024-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=60)

        response = self.client.post(
            "/",
            json.dumps({
                "start_date": start_time.strftime('%Y-%m-%d'),
                "end_date": end_time.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"], "Anda sudah memiliki siklus yang berlangsung saat ini")

    def test_create_cycle_invalid_token(self):
        start_time = datetime.strptime('2025-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=60)

        response = self.client.post(
            "/",
            json.dumps({
                "start_date": start_time.strftime('%Y-%m-%d'),
                "end_date": end_time.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": "Bearer invalidToken"},
        )

        self.assertEqual(response.status_code, 401)

    def test_create_one_blank_field(self):
        end_time = datetime.strptime('2025-09-01', '%Y-%m-%d') + timedelta(days=60)

        response = self.client.post(
            "/",
            json.dumps({
                "end_date": end_time.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 100},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 200}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )

        self.assertEqual(response.status_code, 422)

    def test_create_cycle_invalid_fish_amount(self):
        start_time = datetime.strptime('2025-09-01', '%Y-%m-%d')
        end_time = start_time + timedelta(days=60)

        response = self.client.post(
            "/",
            json.dumps({
                "start_date": start_time.strftime('%Y-%m-%d'),
                "end_date": end_time.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
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
        self.assertEqual(data["start_date"], self.cycle.start_date.strftime('%Y-%m-%d'))
        self.assertEqual(data["end_date"], self.cycle.end_date.strftime('%Y-%m-%d'))
        self.assertEqual(data["supervisor"], self.user.username)
        self.assertEqual(data['pond_fish_amount'][0]['fish_amount'], 1000)

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


    def test_delete_cycle(self):
        response = self.client.delete(
            f"/{self.cycle.id}/",
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Cycle.objects.filter(id=self.cycle.id).exists())

    def test_delete_cycle_invalid_token(self):
        response = self.client.delete(
            f"/{self.cycle.id}/",
            headers={"Authorization": "Bearer invalidToken"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertTrue(Cycle.objects.filter(id=self.cycle.id).exists())

    def test_delete_cycle_not_found(self):
        response = self.client.delete(
            f"/{uuid.uuid4()}/",
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_cycle_wrong_user(self):
        user = User.objects.create_user(username="08123456788", password="admin1234")
        response = self.client.delete(
            f"/{self.cycle.id}/",
            headers={"Authorization": f"Bearer {AccessToken.for_user(user)}"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], "Anda tidak memiliki akses untuk menghapus data ini")
        self.assertTrue(Cycle.objects.filter(id=self.cycle.id).exists())


    def test_update_cycle(self):
        new_start_date = datetime.strptime('2024-08-01', '%Y-%m-%d')
        new_end_date = new_start_date + timedelta(days=60)
        response = self.client.put(
            f"/{self.cycle.id}/",
            json.dumps({
                "start_date": new_start_date.strftime('%Y-%m-%d'),
                "end_date": new_end_date.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 300}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["start_date"], new_start_date.strftime('%Y-%m-%d'))
        self.assertEqual(data["end_date"], new_end_date.strftime('%Y-%m-%d'))
        self.assertEqual(data["supervisor"], self.user.username)
        self.assertEqual(data["pond_fish_amount"][0]['fish_amount'], 300)

    def test_update_invalid_date(self):
        new_start_date = datetime.strptime('2024-08-01', '%Y-%m-%d')
        new_end_date = new_start_date - timedelta(days=60)
        response = self.client.put(
            f"/{self.cycle.id}/",
            json.dumps({
                "start_date": new_start_date.strftime('%Y-%m-%d'),
                "end_date": new_end_date.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 300},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 400}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], "Tanggal selesai harus tepat 60 hari setelah tanggal mulai")

    def test_update_invalid_date2(self):
        new_start_date = datetime.strptime('2024-08-01', '%Y-%m-%d')
        new_end_date = new_start_date + timedelta(days=59)
        response = self.client.put(
            f"/{self.cycle.id}/",
            json.dumps({
                "start_date": new_start_date.strftime('%Y-%m-%d'),
                "end_date": new_end_date.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 300},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 400}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], "Tanggal selesai harus tepat 60 hari setelah tanggal mulai")

    def test_update_invalid_token(self):
        new_start_date = datetime.strptime('2024-08-01', '%Y-%m-%d')
        new_end_date = new_start_date + timedelta(days=60)
        response = self.client.put(
            f"/{self.cycle.id}/",
            json.dumps({
                "start_date": new_start_date.strftime('%Y-%m-%d'),
                "end_date": new_end_date.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 300},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 400}
                ]
            }),
            headers={"Authorization": "Bearer invalidToken"},
        )
        self.assertEqual(response.status_code, 401)

    def test_update_one_blank_field(self):
        new_end_date = datetime.strptime('2024-08-01', '%Y-%m-%d') + timedelta(days=60)
        response = self.client.put(
            f"/{self.cycle.id}/",
            json.dumps({
                "end_date": new_end_date.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 300},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 400}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 422)

    def test_update_invalid_fish_amount(self):
        new_start_date = datetime.strptime('2024-08-01', '%Y-%m-%d')
        new_end_date = new_start_date + timedelta(days=60)
        response = self.client.put(
            f"/{self.cycle.id}/",
            json.dumps({
                "start_date": new_start_date.strftime('%Y-%m-%d'),
                "end_date": new_end_date.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 0},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 400}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], "Jumlah ikan harus lebih dari 0")

    def test_update_cycle_not_found(self):  
        new_start_date = datetime.strptime('2024-08-01', '%Y-%m-%d')
        new_end_date = new_start_date + timedelta(days=60)
        response = self.client.put(
            f"/{uuid.uuid4()}/",
            json.dumps({
                "start_date": new_start_date.strftime('%Y-%m-%d'),
                "end_date": new_end_date.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 300},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 400}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 404)

    def test_update_cycle_wrong_user(self):
        user = User.objects.create_user(username="08123456788", password="admin1234")
        new_start_date = datetime.strptime('2024-08-01', '%Y-%m-%d')
        new_end_date = new_start_date + timedelta(days=60)
        response = self.client.put(
            f"/{self.cycle.id}/",
            json.dumps({
                "start_date": new_start_date.strftime('%Y-%m-%d'),
                "end_date": new_end_date.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 300},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 400}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(user)}"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], "Anda tidak memiliki akses untuk mengubah data ini")

    def test_update_cycle_overlapping(self):
        old_start_date = self.cycle.start_date
        old_end_date = self.cycle.end_date

        new_start_date = datetime.strptime('2025-09-01', '%Y-%m-%d').date()
        new_end_date = new_start_date + timedelta(days=60)

        Cycle.objects.create(
            supervisor=self.user,
            start_date=new_start_date,
            end_date=new_end_date
        )

        response = self.client.put(
            f"/{self.cycle.id}/",
            json.dumps({
                "start_date": new_start_date.strftime('%Y-%m-%d'),
                "end_date": new_end_date.strftime('%Y-%m-%d'),
                "pond_fish_amount": [
                    {"pond_id": str(self.pond.pond_id), "fish_amount": 300},
                    {"pond_id": str(self.pond2.pond_id), "fish_amount": 400}
                ]
            }),
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.cycle.start_date, old_start_date)
        self.assertEqual(self.cycle.end_date, old_end_date)
        self.assertEqual(response.json()['detail'], "Anda sudah memiliki siklus yang berlangsung saat ini")


    def test_get_cycle_by_id(self):
        response = self.client.get(
            f"/{self.cycle.id}/",
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["start_date"], self.cycle.start_date.strftime('%Y-%m-%d'))
        self.assertEqual(data["end_date"], self.cycle.end_date.strftime('%Y-%m-%d'))
        self.assertEqual(data["supervisor"], self.user.username)
        self.assertEqual(data['pond_fish_amount'][0]['fish_amount'], 1000)

    def test_get_cycle_by_id_not_exists(self):
        response = self.client.get(
            f"/{uuid.uuid4()}/",
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
        )
        self.assertEqual(response.status_code, 404)

    def test_get_cycle_by_id_invalid_token(self):
        response = self.client.get(
            f"/{self.cycle.id}/",
            headers={"Authorization ": "Bearer invalidToken"},
        )

        self.assertEqual(response.status_code, 401)

    def test_get_cycle_by_id_wrong_user(self):
        user = User.objects.create_user(username="08123456788", password="admin1234")
        response = self.client.get(
            f"/{self.cycle.id}/",
            headers={"Authorization": f"Bearer {AccessToken.for_user(user)}"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], "Anda tidak memiliki akses untuk melihat data ini")

