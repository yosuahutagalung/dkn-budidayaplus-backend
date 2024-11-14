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

    def test_get_pond_by_id(self):
        pond = PondRepository.create_pond(self.user, "Pond 1", "image.jpg", 10.0, 5.0, 2.0)
        retrieved_pond = PondRepository.get_pond_by_id(pond.pond_id)
        self.assertEqual(pond, retrieved_pond)
        self.assertEqual(pond.name, retrieved_pond.name)
        self.assertEqual(pond.image_name, retrieved_pond.image_name)
        self.assertEqual(pond.length, retrieved_pond.length)
        self.assertEqual(pond.width, retrieved_pond.width)
        self.assertEqual(pond.depth, retrieved_pond.depth)

    def test_list_ponds_by_user(self):
        pond1 = PondRepository.create_pond(self.user, "Pond 1", "image.jpg", 10.0, 5.0, 2.0)
        pond2 = PondRepository.create_pond(self.user, "Pond 2", "image.jpg", 10.0, 5.0, 2.0)
        ponds = PondRepository.list_ponds_by_user(self.user)
        self.assertEqual(len(ponds), 2)
        self.assertIn(pond1, ponds)
        self.assertIn(pond2, ponds)

    def test_delete_pond(self):
        pond = PondRepository.create_pond(self.user, "Pond 1", "image.jpg", 10.0, 5.0, 2.0)
        PondRepository.delete_pond(pond.pond_id)
        self.assertEqual(Pond.objects.count(), 0)
        self.assertFalse(Pond.objects.filter(pond_id=pond.pond_id).exists())

    def test_update_pond(self):
        pond = PondRepository.create_pond(self.user, "Pond 1", "image.jpg", 10.0, 5.0, 2.0)
        updated_pond = PondRepository.update_pond(pond, "Pond 2", "image2.jpg", 20.0, 10.0, 4.0)
        self.assertEqual(Pond.objects.count(), 1)
        self.assertEqual(updated_pond.name, "Pond 2")
        self.assertEqual(updated_pond.image_name, "image2.jpg")
        self.assertEqual(updated_pond.length, 20.0)
        self.assertEqual(updated_pond.width, 10.0)
        self.assertEqual(updated_pond.depth, 4.0)