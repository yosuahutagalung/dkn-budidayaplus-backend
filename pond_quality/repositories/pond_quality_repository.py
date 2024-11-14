from datetime import date
from typing import Optional
from django.shortcuts import get_object_or_404
from pond_quality.models import PondQuality
from pond_quality.schemas import PondQualityInput
from pond.models import Pond
from cycle.models import Cycle
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class PondQualityRepository:
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
    def get_pond_quality_by_id(id: str) -> PondQuality:
        return get_object_or_404(PondQuality, id=id)
    
    @staticmethod
    def get_existing_pond_quality(cycle: Cycle, pond: Pond, today: date) -> Optional[PondQuality]:
        return PondQuality.objects.filter(cycle=cycle, pond=pond, recorded_at__date=today).first()
    
    @staticmethod
    def create_pond_quality(
        pond: Pond, 
        reporter: User, 
        cycle: Cycle, 
        image_name: str,
        ph_level: float,
        salinity: float,
        water_temperature: float,
        water_clarity: float,
        water_circulation: float,
        dissolved_oxygen: float,
        orp: float,
        ammonia: float,
        nitrate: float,
        phosphate: float
        ) -> PondQuality:
        return PondQuality.objects.create(
            pond = pond,
            reporter = reporter,
            cycle = cycle,
            image_name = image_name,
            ph_level = ph_level,
            salinity = salinity,
            water_temperature = water_temperature,
            water_clarity = water_clarity,
            water_circulation = water_circulation,
            dissolved_oxygen = dissolved_oxygen,
            orp = orp,
            ammonia = ammonia,
            nitrate = nitrate,
            phosphate = phosphate
        )
    
    @staticmethod
    def delete_pond_quality(pond_quality: PondQuality):
        pond_quality.delete()

    @staticmethod
    def get_latest_pond_quality(pond: Pond, cycle: Cycle) -> Optional[PondQuality]:
        try:
            return PondQuality.objects.filter(pond=pond, cycle=cycle).latest('recorded_at')
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def list_pond_qualities(cycle: Cycle, pond: Pond):
        return PondQuality.objects.filter(cycle=cycle, pond=pond)