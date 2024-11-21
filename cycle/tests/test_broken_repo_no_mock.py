from cycle.models import Cycle
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from cycle.repositories.cycle_repo import CycleRepo
import uuid

class BrokenRepoNoMockTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='test1234',
        )
        self.cycle = Cycle.objects.create(
            id = uuid.uuid4(),  
            start_date = timezone.now().date(),
            end_date = timezone.now().date(),
            supervisor=self.user
        )
        self.cycle2 = Cycle.objects.create(
            id = uuid.uuid4(),  
            start_date = timezone.now().date() + timezone.timedelta(days=61),
            end_date = timezone.now().date() + timezone.timedelta(days=121),
            supervisor=self.user
        )

    def test_get_cycle_active(self):
        cycle = CycleRepo.get_active_cycle(self.user)
        self.assertEqual(cycle, self.cycle)
