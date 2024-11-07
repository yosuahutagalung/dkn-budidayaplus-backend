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
from user_profile.schemas import UpdateProfileSchema
import json

service_impl = "UpdateServiceImpl" # change this if implementation changes
MOCK_SERVICE = f'user_profile.services.update_service_impl.{service_impl}.update_profile'

class UpdateUserProfileAPITest(TestCase):
    def setUp(self):
        post_save.disconnect(create_user_profile, sender=User)
        self.client = TestClient(router)
        self.user = User.objects.create_user(username='08123456789', password= 'admin1234', first_name='Lala', last_name='Lele')
        self.profile = UserProfile.objects.create(
            user=self.user,
            image_name='profile.jpg'
        )
    
    @patch(MOCK_SERVICE)
    def test_update_profile(self, mock_update_profile):
        result = UpdateProfileSchema(
            first_name= "Kevin",
            last_name= "Heryanto",
            image_name= "test.jpg"
        )
        mock_update_profile.return_value = result

        response = self.client.put(
            f'/',
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
        self.assertEqual(data['last_name'] , "Heryanto")
        self.assertEqual(data['image_name'], "test.jpg")

    @patch(MOCK_SERVICE)
    def test_update_profile_not_found(self, mock_update_profile):
        mock_update_profile.side_effect = UserProfile.DoesNotExist

        response = self.client.put(
            f'/',
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.user)}"},
            data=json.dumps({
                "first_name": "Kevin",
                "last_name": "Heryanto",
                "image_name": "test.jpg"
            })
        )
        self.assertEqual(response.status_code, 404)

    @patch(MOCK_SERVICE)    
    def test_update_profile_unauthenticated(self, mock_update_profile):
        mock_update_profile.return_value = self.profile

        response = self.client.put(
            f'/'
        )
        self.assertEqual(response.status_code, 401)