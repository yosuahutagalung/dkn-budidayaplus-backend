from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth
from .models import FoodSampling
from pond.models import Pond
from .schemas import FoodSamplingOutputSchema

router = Router()

@router.get("/{pond_id}/{food_id}/", auth=JWTAuth(), response={200: FoodSamplingOutputSchema})
def get_food_sampling(request, pond_id: str, food_id: str):
    food_sampling = get_object_or_404(FoodSampling, pond_id=pond_id, food_id=food_id)
    return food_sampling


@router.get("/{pond_id}/", auth=JWTAuth(), response={200: List[FoodSamplingOutputSchema]})
def list_food_samplings(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    food_samplings = FoodSampling.objects.filter(pond=pond)
    return [food for food in food_samplings]

@router.get("/{pond_id}/latest", auth=JWTAuth(), response={200: FoodSamplingOutputSchema})
def get_latest_food_sampling(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    food_sampling = FoodSampling.objects.filter(pond=pond).latest('date')
    return food_sampling