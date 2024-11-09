from django.test import TestCase
from cycle.models import Cycle, PondFishAmount
from datetime import date, timedelta
from django.contrib.auth.models import User
from cycle.schemas import PondFishAmountInput
from pond.models import Pond
from cycle.repositories.pond_fish_amount_repo import PondFishAmountRepo

class PFARepoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='08123456789', password='test1234')
        self.pond1 = Pond.objects.create(
            owner=self.user,
            name='Test Pond 1',
            image_name='test_pond1.png',
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.pond2 = Pond.objects.create(
            owner=self.user,
            name='Test Pond 2',
            image_name='test_pond2.png',
            length=10.0,
            width=5.0,
            depth=2.0
        )
        self.cycle = Cycle.objects.create(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            supervisor=self.user 
        ) 
    
    def test_bulk_create(self):
        data = [
            PondFishAmountInput(
                pond_id=self.pond1.pond_id,
                fish_amount=10
            ),
            PondFishAmountInput(
                pond_id=self.pond2.pond_id,
                fish_amount=20
            )
        ] 

        PondFishAmountRepo.bulk_create(data, self.cycle)

        self.assertEqual(PondFishAmount.objects.count(), 2)
        self.assertEqual(PondFishAmount.objects.filter(cycle=self.cycle).count(), 2)
    
    def test_bulk_update(self):
        PondFishAmount.objects.create(
            cycle=self.cycle,
            pond=self.pond1,
            fish_amount=5
        )
        PondFishAmount.objects.create(
            cycle=self.cycle,
            pond=self.pond2,
            fish_amount=15
        )

        data = [
            PondFishAmountInput(
                pond_id=self.pond1.pond_id,
                fish_amount=10
            ),
            PondFishAmountInput(
                pond_id=self.pond2.pond_id,
                fish_amount=20
            )
        ]

        PondFishAmountRepo.bulk_update(data, self.cycle)

        self.assertEqual(PondFishAmount.objects.count(), 2)
        self.assertEqual(PondFishAmount.objects.filter(cycle=self.cycle).count(), 2)
        self.assertEqual(PondFishAmount.objects.get(cycle=self.cycle, pond=self.pond1).fish_amount, 10)
        self.assertEqual(PondFishAmount.objects.get(cycle=self.cycle, pond=self.pond2).fish_amount, 20)
