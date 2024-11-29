from datetime import date
from typing import Optional
from django.shortcuts import get_object_or_404
from food_sampling.models import FoodSampling
from pond.models import Pond
from cycle.models import Cycle
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

class FoodSamplingRepository:
    @staticmethod
    def get_pond(pond_id: str) -> Pond:
        return get_object_or_404(Pond, pond_id=pond_id)
    
    @staticmethod
    def get_cycle(cycle_id: str) -> Cycle:
        return get_object_or_404(Cycle, id=cycle_id)
    
    @staticmethod
    def get_reporter(user_id: int) -> User:
        return get_object_or_404(User, id=user_id)

    @staticmethod
    def get_food_sampling_by_id(sampling_id: str) -> FoodSampling:
        return get_object_or_404(FoodSampling, sampling_id=sampling_id)
    
    @staticmethod
    def get_existing_food_sampling(cycle: Cycle, pond: Pond, today: date) -> Optional[FoodSampling]:
        return FoodSampling.objects.filter(cycle=cycle, pond=pond, recorded_at__date=today).first()
    
    @staticmethod
    def create_food_sampling(pond: Pond, reporter: User, cycle: Cycle, food_quantity: int, recorded_at: date) -> FoodSampling:
        return FoodSampling.objects.create(
            pond=pond,
            reporter=reporter,
            cycle=cycle,
            food_quantity=food_quantity,
            recorded_at=recorded_at
        )
    
    @staticmethod
    def delete_food_sampling(food_sampling: FoodSampling):
        food_sampling.delete()

    @staticmethod
    def get_latest_food_sampling(pond: Pond, cycle: Cycle) -> Optional[FoodSampling]:
        try:
            return FoodSampling.objects.filter(pond=pond, cycle=cycle).latest('recorded_at')
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def list_food_samplings(cycle: Cycle, pond: Pond):
        return FoodSampling.objects.filter(cycle=cycle, pond=pond)
