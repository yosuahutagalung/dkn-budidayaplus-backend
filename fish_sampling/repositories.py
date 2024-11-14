from django.contrib.auth.models import User
from cycle.models import Cycle
from pond.models import Pond
from .models import FishSampling

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