from django.test import TestCase
from ninja.testing import TestClient
from user_profile.api import router
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from ninja_jwt.tokens import AccessToken
from unittest.mock import patch
from django.db.models.signals import post_save
from user_profile.signals import create_user_profile

service_impl = "RetrieveServiceImpl"
MOCK_SERVICE = f'user_profile.services.retrieve_service_impl.{service_impl}.retrieve_profile'
MOCK_SERVICE_BY_USER = f'user_profile.services.retrieve_service_impl.{service_impl}.retrieve_profile_by_user'

class RetrieveUserProfileAPITest(TestCase):
    def setUp(self):
        post_save.disconnect(create_user_profile, sender=User)
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='08123456789', password='admin1234')
        self.profile = UserProfile.objects.create(
            user=self.user,
            image_name='profile.jpg',
        )

    @patch(MOCK_SERVICE)
    def test_retrieve_profile(self, mock_retrieve_profile):
        mock_retrieve_profile.return_value = self.profile

        response = self.client.get(
            f'/{self.user.username}/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['image_name'], 'profile.jpg')

    @patch(MOCK_SERVICE)
    def test_retrieve_profile_not_found(self, mock_retrieve_profile):
        mock_retrieve_profile.side_effect = UserProfile.DoesNotExist

        response = self.client.get(
            f'/08123456788/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )
        self.assertEqual(response.status_code, 404)
    
    @patch(MOCK_SERVICE)
    def test_retrieve_profile_unauthorized(self, mock_retrieve_profile):
        mock_retrieve_profile.return_value = self.profile

        response = self.client.get(
            f'/{self.user.username}/',
            headers={"Authorization": "Bearer invalid_token"}
        )
        self.assertEqual(response.status_code, 401)

    @patch(MOCK_SERVICE)
    def test_retrieve_profile_generic_error(self, mock_retrieve_profile):
        """Test generic error handling when an unexpected exception occurs."""
        mock_retrieve_profile.side_effect = Exception("Unexpected error")

        response = self.client.get(
            f'/{self.user.username}/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("detail"), "Unexpected error")

    @patch(MOCK_SERVICE_BY_USER)
    def test_retrieve_profile_by_user(self, mock_retrieve_profile):
        mock_retrieve_profile.return_value = self.profile

        response = self.client.get(
            '/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['image_name'], 'profile.jpg')

    @patch(MOCK_SERVICE_BY_USER)
    def test_retrieve_profile_by_user_not_found(self, mock_retrieve_profile):
        mock_retrieve_profile.side_effect = UserProfile.DoesNotExist

        response = self.client.get(
            '/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(User.objects.create_user(username='08123456788', password='admin1234'))}"}
        )
        self.assertEqual(response.status_code, 404)
    
    @patch(MOCK_SERVICE_BY_USER)
    def test_retrieve_profile_by_user_unauthorized(self, mock_retrieve_profile):
        mock_retrieve_profile.return_value = self.profile

        response = self.client.get(
            '/',
            headers={"Authorization": "Bearer invalid_token"}
        )
        self.assertEqual(response.status_code, 401)

    @patch(MOCK_SERVICE_BY_USER)
    def test_retrieve_profile_by_user_generic_error(self, mock_retrieve_profile):
        """Test generic error handling when an unexpected exception occurs."""
        mock_retrieve_profile.side_effect = Exception("Unexpected error")

        response = self.client.get(
            '/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("detail"), "Unexpected error")