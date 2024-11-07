from django.test import TestCase
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from user_profile.services.update_service_impl import UpdateServiceImpl
from django.db.models.signals import post_save
from user_profile.signals import create_user_profile
from user_profile.schemas import UpdateProfileSchema


class UpdateServiceImplTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_user_profile, sender=User)
        self.user = User.objects.create_user(
            username='08123456789', password='admin1234')
        self.profile = UserProfile.objects.create(
            user=self.user,
            image_name='profile.jpg'
        )
        self.payload = UpdateProfileSchema(
            last_name="Heryanto",
            first_name="Kevin",
            image_name="test.jpg"
        )
        self.service = UpdateServiceImpl()

    def test_update_positive(self):

        profile = self.service.update_profile(self.payload, self.user)
        self.assertEqual(profile.user.first_name, self.payload.first_name)
        self.assertEqual(profile.image_name, self.payload.image_name)
        self.assertEqual(profile.user.last_name, self.payload.last_name)
