from django.test import TestCase
from ninja.testing import TestClient
from ..api import router
import json

class TestAuth(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.client.post("/register", data=json.dumps({
            "phone_number": "08123456789",
            "first_name": "Omar",
            "last_name": "Khalif",
            "password": "AkuAnakEmo"
        }))

    def test_register(self):
        response = self.client.post(
            "/register",
            data=json.dumps({
                "phone_number": "1234567890",
                "first_name": "John",
                "last_name": "Doe",
                "password": "password"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User created successfully")
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())


    def test_register_existing(self):
        response = self.client.post("/register", data=json.dumps({
            "phone_number": "08123456789",
            "first_name": "Rafif",
            "last_name": "Aulia",
            "password": "admin1234"
        }))

        self.assertEqual(response.status_code, 400)


    def test_login(self):
        response = self.client.post("/login", data=json.dumps({
            "phone_number": "08123456789",
            "password": "AkuAnakEmo"
        }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Login successful")
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())


    def test_login_password_invalid(self):
        response = self.client.post("/login", data=json.dumps({
            "phone_number": "08123456789",
            "password": "wrongpassword"
        }))
        self.assertEqual(response.status_code, 404)


    def test_login_user_not_found(self):
        response = self.client.post("/login", data=json.dumps({
            "phone_number": "1234567890",
            "password": "password"
        }))
        self.assertEqual(response.status_code, 404)