from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Pond
from ..repositories import PondRepository


class PondRepositoryTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
    
    def test_create_pond(self):
        pond = PondRepository.create_pond(self.user, "Pond 1", "image.jpg", 10.0, 5.0, 2.0)
        self.assertEqual(Pond.objects.count(), 1)
        self.assertEqual(pond.name, "Pond 1")
        self.assertEqual(pond.image_name, "image.jpg")
        self.assertEqual(pond.length, 10.0)
        self.assertEqual(pond.width, 5.0)
        self.assertEqual(pond.depth, 2.0)

    def test_delete_pond(self):
        pond = PondRepository.create_pond(self.user, "Pond 1", "image.jpg", 10.0, 5.0, 2.0)
        PondRepository.delete_pond(pond.pond_id)
        self.assertEqual(Pond.objects.count(), 0)
        self.assertFalse(Pond.objects.filter(pond_id=pond.pond_id).exists())