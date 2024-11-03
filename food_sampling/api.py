from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth
from .models import FoodSampling
from pond.models import Pond
from cycle.models import Cycle
from .schemas import FoodSamplingOutputSchema
from datetime import datetime
from ninja.errors import HttpError
from django.core.exceptions import ObjectDoesNotExist

DATA_NOT_FOUND = "Data tidak ditemukan"
CYCLE_NOT_ACTIVE = "Siklus tidak aktif"
UNAUTHORIZED_ACCESS = "Anda tidak memiliki akses untuk melihat data ini"

router = Router()

def check_cycle_active(cycle):
    today = datetime.now().date()
    if not (cycle.start_date <= today <= cycle.end_date):
        raise HttpError(400, CYCLE_NOT_ACTIVE)

@router.get("/{cycle_id}/{pond_id}/{food_id}/", auth=JWTAuth(), response={200: FoodSamplingOutputSchema})
def get_food_sampling(request, cycle_id: str, pond_id: str, food_id: str):
    cycle = Cycle.objects.get(id=cycle_id)
    pond = get_object_or_404(Pond, pond_id=pond_id)
    food_sampling = get_object_or_404(FoodSampling, food_id=food_id)

    check_cycle_active(cycle)

    if (food_sampling.cycle != cycle):
        raise HttpError(404, DATA_NOT_FOUND)
    
    if (food_sampling.pond != pond):
        raise HttpError(404, DATA_NOT_FOUND)
    
    if (food_sampling.reporter != request.auth or pond.owner != request.auth):
        raise HttpError(401, UNAUTHORIZED_ACCESS)

    return food_sampling


@router.get("/{cycle_id}/{pond_id}/", auth=JWTAuth(), response={200: List[FoodSamplingOutputSchema]})
def list_food_samplings(request, pond_id: str, cycle_id: str):
    cycle = get_object_or_404(Cycle, id=cycle_id, supervisor=request.auth)
    pond = get_object_or_404(Pond, pond_id=pond_id)

    check_cycle_active(cycle)

    food_samplings = FoodSampling.objects.filter(cycle=cycle, pond=pond)

    return [food for food in food_samplings]

@router.get("/{cycle_id}/{pond_id}/latest", auth=JWTAuth(), response={200: FoodSamplingOutputSchema})
def get_latest_food_sampling(request, pond_id: str, cycle_id: str):
    cycle = Cycle.objects.get(id=cycle_id)
    pond = get_object_or_404(Pond, pond_id=pond_id)

    check_cycle_active(cycle)

    try:
        food_sampling = FoodSampling.objects.filter(pond=pond, cycle=cycle).latest('date')
    except ObjectDoesNotExist:
        raise HttpError(404, DATA_NOT_FOUND)

    if (food_sampling.reporter != request.auth or pond.owner != request.auth):
        raise HttpError(401, UNAUTHORIZED_ACCESS)
    
    return food_sampling