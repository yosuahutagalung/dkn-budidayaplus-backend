from django.test import TestCase
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from user_profile.services.retrieve_service_impl import RetrieveServiceImpl
from django.db.models.signals import post_save
from user_profile.signals import create_user_profile

class RetrieveServiceImplTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_user_profile, sender=User)
        self.user = User.objects.create_user(username='08123456789', password='admin1234')
        self.profile = UserProfile.objects.create(
            user=self.user,
            image_name='profile.jpg',
        )
        self.service = RetrieveServiceImpl()
    
    def test_retrieve_positive(self):
        profile = self.service.retrieve_profile('08123456789')
        self.assertEqual(profile, self.profile)

    def test_retrieve_profile_not_found(self):
        with self.assertRaises(UserProfile.DoesNotExist):
            self.service.retrieve_profile('08123456788')

    def test_retrieve_profile_by_user(self):
        profile = self.service.retrieve_profile_by_user(self.user)
        self.assertEqual(profile, self.profile)

    def test_retrieve_profile_by_user_not_found(self):
        with self.assertRaises(UserProfile.DoesNotExist):
            self.service.retrieve_profile_by_user(User.objects.create_user(username='08123456788', password='admin1234'))
