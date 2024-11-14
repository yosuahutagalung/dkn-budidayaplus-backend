from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Pond

class PondModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='081234567890', password='password')

        self.pond = Pond.objects.create(
            owner=self.user,
            name='Test Pond',
            image_name='pond_image.jpg',
            length=10.0,
            width=5.0,
            depth=2.0
        )

    def test_str_method(self):
        self.assertEqual(str(self.pond), 'Test Pond')