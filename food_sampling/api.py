from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import FoodSampling
from pond.models import Pond
from cycle.models import Cycle
from .schemas import FoodSamplingCreateSchema, FoodSamplingOutputSchema
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError

router = Router()

@router.post("/{pond_id}/{cycle_id}/", auth=JWTAuth(), response={200: FoodSamplingOutputSchema})
def create_food_sampling(request, pond_id: str, cycle_id:str, payload: FoodSamplingCreateSchema):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    reporter = get_object_or_404(User, id=request.auth.id)
    cycle = get_object_or_404(Cycle, id=cycle_id)
    try:
        food_sampling = FoodSampling.objects.create(
            pond=pond,
            reporter=reporter,
            cycle=cycle,
            food_quantity=payload.food_quantity,
            sample_date=payload.sample_date
        )
    except:
        raise HttpError(400, "Input kuantitas makanan tidak valid")
    return food_sampling