from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import FishSampling
from pond.models import Pond
from .schemas import FishSamplingCreateSchema, FishSamplingEditSchema, FishSamplingOutputSchema
from ninja_jwt.authentication import JWTAuth

router = Router()

@router.post("/{pond_id}/", auth=JWTAuth(), response={200: FishSamplingOutputSchema})
def create_fish_sampling(request, pond_id: str, payload: FishSamplingCreateSchema):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    reporter = get_object_or_404(User, id=request.auth.id)
    fish_sampling = FishSampling.objects.create(
        pond=pond,
        reporter=reporter,
        fish_weight=payload.fish_weight,
        fish_length=payload.fish_length,
        sample_date=payload.sample_date
    )
    return fish_sampling

@router.get("/{pond_id}/{sampling_id}/", auth=JWTAuth(), response={200: FishSamplingOutputSchema})
def get_fish_sampling(request, pond_id: str, sampling_id: str):
    fish_sampling = get_object_or_404(FishSampling, pond_id=pond_id, sampling_id=sampling_id)
    return fish_sampling


@router.get("/{pond_id}/", auth=JWTAuth(), response={200: List[FishSamplingOutputSchema]})
def list_fish_samplings(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    fish_samplings = FishSampling.objects.filter(pond=pond)
    return [sampling for sampling in fish_samplings]

@router.put("/{pond_id}/{sampling_id}/", auth=JWTAuth(), response={200: FishSamplingEditSchema})
def update_fish_sampling(request, pond_id: str, sampling_id: str, payload: FishSamplingEditSchema):
    fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)
    pond = get_object_or_404(Pond, pond_id=pond_id)
    reporter = get_object_or_404(User, id=request.auth.id)
    fish_sampling.pond = pond
    fish_sampling.reporter = reporter
    fish_sampling.fish_weight = payload.fish_weight
    fish_sampling.fish_length = payload.fish_length
    fish_sampling.sample_date = payload.sample_date
    fish_sampling.save()
    return fish_sampling

@router.delete("/{pond_id}/{sampling_id}/", auth=JWTAuth())
def delete_fish_sampling(request, pond_id: str, sampling_id: str):
    fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)
    fish_sampling.delete()
    return {"success": True}