from django.test import TestCase
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from pond_quality.models import PondQuality
from pond.models import Pond
from cycle.models import Cycle
from pond_quality.repositories.pond_quality_repository import PondQualityRepository

class PondQualityRepositoryTest(TestCase):
    
    def setUp(self):
        date_now = datetime.now()
        start_date = date_now - timedelta(days=30)
        end_date = start_date + timedelta(days=60)

        self.user = User.objects.create_user(username='user', password='pass')
        self.pond = Pond.objects.create(
            owner=self.user,
            name='Pond',
            image_name='pond.png',
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.cycle = Cycle.objects.create(
            supervisor=self.user,
            start_date=start_date,
            end_date=end_date,
        )
        self.pond_quality = PondQuality.objects.create(
            pond = self.pond,
            reporter = self.user,
            cycle = self.cycle,
            image_name = 'test.jpg',
            ph_level = 7.0,
            salinity = 0.0,
            water_temperature = 25.0,
            water_clarity = 0.0,
            water_circulation = 0.0,
            dissolved_oxygen = 0.0,
            orp = 0.0,
            ammonia = 0.0,
            nitrate = 0.0,
            phosphate = 0.0
        )

    def test_get_pond(self):
        pond = PondQualityRepository.get_pond(self.pond.pond_id)
        self.assertEqual(pond, self.pond)
    
    def test_get_cycle(self):
        cycle = PondQualityRepository.get_cycle(self.cycle.id)
        self.assertEqual(cycle, self.cycle)
    
    def test_get_existing_pond_quality(self):
        existing_pond_quality = PondQualityRepository.get_existing_pond_quality(
            cycle=self.cycle,
            pond=self.pond,
            today=datetime.now().date()
        )
        self.assertEqual(existing_pond_quality, self.pond_quality)
    
    def test_create_pond_quality(self):
        new_pond_quality = PondQualityRepository.create_pond_quality(
            pond = self.pond,
            reporter = self.user,
            cycle = self.cycle,
            image_name = 'rest.jpg',
            ph_level = 9.0,
            salinity = 1.0,
            water_temperature = 20.0,
            water_clarity = 1.0,
            water_circulation = 0.0,
            dissolved_oxygen = 0.0,
            orp = 0.0,
            ammonia = 0.0,
            nitrate = 0.0,
            phosphate = 0.0
        )
        self.assertIsNotNone(new_pond_quality)
        self.assertEqual(new_pond_quality.ph_level, 9.0)

    def test_delete_pond_quality(self):
        PondQualityRepository.delete_pond_quality(self.pond_quality)
        with self.assertRaises(PondQuality.DoesNotExist):
            PondQuality.objects.get(sampling_id=self.pond_quality.sampling_id)