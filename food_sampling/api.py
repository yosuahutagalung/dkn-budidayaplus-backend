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

@router.get("/{cycle_id}/{pond_id}/{sampling_id}/", auth=JWTAuth(), response={200: FoodSamplingOutputSchema})
def get_food_sampling(request, cycle_id: str, pond_id: str, sampling_id: str):
    try:
        return food_sampling_service.get_food_sampling(cycle_id, pond_id, sampling_id, request.auth)
    except HttpError as e:
        raise e
    except Exception:
        raise HttpError(500, "An unexpected error occurred")


@router.get("/{pond_id}/", auth=JWTAuth(), response={200: FoodSamplingList})
def list_food_samplings(request, pond_id: str):
    try:
        food_samplings = food_sampling_service.list_food_samplings(pond_id, request.auth)
        return food_samplings
    except HttpError as e:
        raise e
    except Exception:
        raise HttpError(500, "An unexpected error occurred")

@router.get("/{cycle_id}/{pond_id}/latest", auth=JWTAuth(), response={200: FoodSamplingOutputSchema})
def get_latest_food_sampling(request, pond_id: str, cycle_id: str):
    try:
        return food_sampling_service.get_latest_food_sampling(cycle_id, pond_id, request.auth)
    except HttpError as e:
        raise e
    except Exception:
        raise HttpError(500, "An unexpected error occurred")

@router.post("/{cycle_id}/{pond_id}/", auth=JWTAuth(), response={200: FoodSamplingOutputSchema})
def create_food_sampling(request, pond_id:str, cycle_id:str, payload:FoodSamplingCreateSchema):
    try:
        return food_sampling_service.create_food_sampling(pond_id, cycle_id, request.auth.id, payload)
    except HttpError as e:
        raise e
    except Exception:
        raise HttpError(500, "An unexpected error occurred")
