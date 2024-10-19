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

class RetrieveUserProfileAPITest(TestCase):
    def setUp(self):
        post_save.disconnect(create_user_profile, sender=User)
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='08123456789', password='admin1234')
        self.profile = UserProfile.objects.create(
            user=self.user,
            address='Jl. Jendral Sudirman No. 1', 
            image_name='profile.jpg',
            birthdate=date(2024, 1, 1),
            gender='M'
        )

    @patch('user_profile.services.retrieve_service_impl.RetrieveServiceImpl.retrieve_profile')
    def test_retrieve_profile(self, mock_retrieve_profile):
        mock_retrieve_profile.return_value = self.profile

        response = self.client.get(
            f'/{self.user.username}/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['address'], 'Jl. Jendral Sudirman No. 1')
        self.assertEqual(data['image_name'], 'profile.jpg')
        self.assertEqual(data['birthdate'], '2024-01-01')
        self.assertEqual(data['gender'], 'M')

    @patch('user_profile.services.retrieve_service_impl.RetrieveServiceImpl.retrieve_profile')
    def test_retrieve_profile_not_found(self, mock_retrieve_profile):
        mock_retrieve_profile.side_effect = UserProfile.DoesNotExist

        response = self.client.get(
            f'/08123456788/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )
        self.assertEqual(response.status_code, 404)
    
    @patch('user_profile.services.retrieve_service_impl.RetrieveServiceImpl.retrieve_profile')
    def test_retrieve_profile_unauthorized(self, mock_retrieve_profile):
        mock_retrieve_profile.return_value = self.profile

        response = self.client.get(
            f'/{self.user.username}/',
            headers={"Authorization": "Bearer invalid_token"}
        )
        self.assertEqual(response.status_code, 401)

    @patch('user_profile.services.retrieve_service_impl.RetrieveServiceImpl.retrieve_profile')
    def test_retrieve_profile_generic_error(self, mock_retrieve_profile):
        """Test generic error handling when an unexpected exception occurs."""
        mock_retrieve_profile.side_effect = Exception("Unexpected error")

        response = self.client.get(
            f'/{self.user.username}/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("detail"), "Unexpected error")
