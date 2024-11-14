from django.contrib.auth.models import User
from cycle.models import Cycle
from pond.models import Pond
from .models import FishSampling
from typing import Optional
from django.core.exceptions import ObjectDoesNotExist

class FishSamplingRepository:
    @staticmethod
    def create_fish_sampling(
        pond: Pond, 
        reporter: User, 
        cycle: Cycle, 
        fish_weight: float, 
        fish_length: float, 
        recorded_at
    ) -> FishSampling:
        return FishSampling.objects.create(
            pond=pond,
            reporter=reporter,
            cycle=cycle,
            fish_weight=fish_weight,
            fish_length=fish_length,
            recorded_at=recorded_at
        )
    
    @staticmethod
    def get_latest_fish_sampling(pond: Pond, cycle: Cycle) -> Optional[FishSampling]:
        try:
            return FishSampling.objects.filter(pond=pond, cycle=cycle).latest('recorded_at')
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def list_fish_samplings(cycle: Cycle, pond: Pond):
        return FishSampling.objects.filter(cycle=cycle, pond=pond)