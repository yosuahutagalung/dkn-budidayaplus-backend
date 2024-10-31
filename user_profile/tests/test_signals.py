from django.test import TestCase
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from django.db.models.signals import post_save
from user_profile.signals import create_user_profile


class UserProfileSignalTest(TestCase):

    def test_user_profile_created_on_user_creation(self):
        post_save.connect(create_user_profile, sender=User)
        user = User.objects.create_user(username='08123456789', password='admin1234')

        self.assertTrue(UserProfile.objects.filter(user=user).exists())

        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.address, "")
        self.assertEqual(profile.image_name, "")
        self.assertEqual(profile.gender, "")
        self.assertIsNone(profile.birthdate)
