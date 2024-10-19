from django.test import TestCase
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from datetime import date
from user_profile.services.retreive_service_impl import RetreiveServiceImpl

class RetreiveServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='08123456789', password='admin1234')
        self.profile = UserProfile.objects.create(
            user=self.user,
            address='Jl. Jendral Sudirman No. 1', 
            image_name='profile.jpg',
            birthdate=date(2024, 1, 1), 
            gender='M' 
        )
        self.service = RetreiveServiceImpl()
    
    def test_retreive_profile(self):
        profile = self.service.retreive_profile('08123456789')
        self.assertEqual(profile, self.profile)

    def test_retreive_profile_not_found(self):
        profile = self.service.retreive_profile('08123456788')
        self.assertIsNone(profile)