from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth.models import User
from .models import FoodSampling
from pond.models import Pond
from cycle.models import Cycle
from .schemas import FoodSamplingCreateSchema, FoodSamplingOutputSchema, FoodSamplingList
from food_sampling.services.food_sampling_service import FoodSamplingService
from food_sampling.repositories.food_sampling_repository import FoodSamplingRepository
from datetime import datetime
from ninja.errors import HttpError
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth.models import User

DATA_NOT_FOUND = "Data tidak ditemukan"
CYCLE_NOT_ACTIVE = "Siklus tidak aktif"
UNAUTHORIZED_ACCESS = "Anda tidak memiliki akses untuk melihat data ini"

router = Router()
food_sampling_service = FoodSamplingService(FoodSamplingRepository())

def check_cycle_active(cycle):
    today = datetime.now().date()
    if not (cycle.start_date <= today <= cycle.end_date):
        raise HttpError(400, CYCLE_NOT_ACTIVE)

@router.get("/{cycle_id}/{pond_id}/{sampling_id}/", auth=JWTAuth(), response={200: FoodSamplingOutputSchema})
def get_food_sampling(request, cycle_id: str, pond_id: str, sampling_id: str):
    cycle = Cycle.objects.get(id=cycle_id)
    pond = get_object_or_404(Pond, pond_id=pond_id)
    food_sampling = get_object_or_404(FoodSampling, sampling_id=sampling_id)

    check_cycle_active(cycle)

    if (food_sampling.cycle != cycle):
        raise HttpError(404, DATA_NOT_FOUND)
    
    if (food_sampling.pond != pond):
        raise HttpError(404, DATA_NOT_FOUND)
    
    if (food_sampling.reporter != request.auth or pond.owner != request.auth):
        raise HttpError(401, UNAUTHORIZED_ACCESS)

    return food_sampling


@router.get("/{cycle_id}/{pond_id}/", auth=JWTAuth(), response={200: FoodSamplingList})
def list_food_samplings(request, pond_id: str, cycle_id: str):
    cycle = get_object_or_404(Cycle, id=cycle_id, supervisor=request.auth)
    pond = get_object_or_404(Pond, pond_id=pond_id)

    check_cycle_active(cycle)

    food_samplings = FoodSampling.objects.filter(cycle=cycle, pond=pond)

    return {
        "food_samplings": food_samplings,
        "cycle_id": cycle_id
    }

@router.get("/{cycle_id}/{pond_id}/latest", auth=JWTAuth(), response={200: FoodSamplingOutputSchema})
def get_latest_food_sampling(request, pond_id: str, cycle_id: str):
    cycle = Cycle.objects.get(id=cycle_id)
    pond = get_object_or_404(Pond, pond_id=pond_id)

    check_cycle_active(cycle)

    try:
        food_sampling = FoodSampling.objects.filter(pond=pond, cycle=cycle).latest('recorded_at')
    except ObjectDoesNotExist:
        raise HttpError(404, DATA_NOT_FOUND)

    if (food_sampling.reporter != request.auth or pond.owner != request.auth):
        raise HttpError(401, UNAUTHORIZED_ACCESS)
    
    return food_sampling

@router.post("/{cycle_id}/{pond_id}/", auth=JWTAuth(), response={200: FoodSamplingOutputSchema})
def create_food_sampling(request, pond_id:str, cycle_id:str, payload:FoodSamplingCreateSchema):
    try:
        return food_sampling_service.create_food_sampling(pond_id, cycle_id, request.auth.id, payload)
    except HttpError as e:
        raise e
    except Exception:
        raise HttpError(500, "An unexpected error occurred")