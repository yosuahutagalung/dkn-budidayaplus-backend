from django.test import TestCase
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from datetime import date
from user_profile.services.update_service_impl import UpdateServiceImpl
from django.db.models.signals import post_save
from user_profile.signals import create_user_profile
class UpdateServiceImplTest(TestCase):
    def setUp(self):
        post_save.disconnect(create_user_profile, sender=User)
        self.user = User.objects.create_user(username='08123456789', password='admin1234')
        self.profile = UserProfile.objects.create(
            user=self.user,
            address='Jl. Jendral Sudirman No. 1', 
            image_name='profile.jpg',
            birthdate=date(2024, 1, 1), 
            gender='M' 
        )
        self.service = UpdateServiceImpl()
    
    def test_update_positive(self):
        service = self.service.update_profile('08123456789', self.profile, self.user)
        self.assertEqual(service["profile"], self.profile)
        self.assertEqual(service["user"], self.user)

    def test_update_profile_not_found(self):
        with self.assertRaises(UserProfile.DoesNotExist):
            service = self.service.update_profile('0888', self.profile, self.user)