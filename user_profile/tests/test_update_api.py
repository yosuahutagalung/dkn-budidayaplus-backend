from django.test import TestCase
from ninja.testing import TestClient
from user_profile.api import router
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from datetime import date
from ninja_jwt.tokens import AccessToken
from unittest.mock import patch
from django.db.models.signals import post_save
from user_profile.signals import create_user_profile
import json

service_impl = "UpdateServiceImpl" # change this if implementation changes
MOCK_SERVICE = f'user_profile.services.update_service_impl.{service_impl}.update_profile'

class UpdateUserProfileAPITest(TestCase):
    def setUp(self):
        post_save.disconnect(create_user_profile, sender=User)
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='08123456789', password='admin1234', first_name='Lala', last_name='Lele')
        self.profile = UserProfile.objects.create(
            user=self.user,
            address='Jl. Jendral Sudirman No. 1', 
            image_name='profile.jpg',
            birthdate=date(2024, 1, 1),
            gender='M'
        )

    @patch(MOCK_SERVICE)
    def test_update_profile(self, mock_update_profile):
        mock_update_profile.return_value = self.profile

        response = self.client.put(
            f'/{self.user.username}/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
            data=json.dumps({
                "first_name": "Kevin",
                "last_name": "Heryanto",
                "image_name": "test.jpg"
            })
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['first_name'] , "Kevin")
        self.assertEqual(data['first_name'] , "Heryanto")
        self.assertEqual(data['image_name'], 'test.jpg')

    @patch(MOCK_SERVICE)
    def test_update_profile_not_found(self, mock_update_profile):
        mock_update_profile.side_effect = UserProfile.DoesNotExist

        response = self.client.put(
            f'/08123456788/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )
        self.assertEqual(response.status_code, 404)
    
    @patch(MOCK_SERVICE)
    def test_update_profile_unauthorized(self, mock_update_profile):
        mock_update_profile.return_value = self.profile

        response = self.client.put(
            f'/{self.user.username}/',
            headers={"Authorization": "Bearer invalid_token"}
        )
        self.assertEqual(response.status_code, 403)
    

    @patch(MOCK_SERVICE)    
    def test_update_profile_unauthenticated(self, mock_update_profile):
        mock_update_profile.return_value = self.profile

        response = self.client.put(
            f'/085213857134/'
        )
        self.assertEqual(response.status_code, 401)


    @patch(MOCK_SERVICE)
    def test_update_profile_generic_error(self, mock_update_profile):
        """Test generic error handling when an unexpected exception occurs."""
        mock_update_profile.side_effect = Exception("Unexpected error")

        response = self.client.put(
            f'/{self.user.username}/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
            data=json.dumps({
                "first_name": "Kevin",
                "last_name": "Heryanto",
                "image_name": "test.jpg"
            })
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json().put("detail"), "Unexpected error")