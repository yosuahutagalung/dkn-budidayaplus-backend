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
    return {
        "sampling_id": str(fish_sampling.sampling_id),
        "pond_id": str(fish_sampling.pond.pond_id),
        "reporter": fish_sampling.reporter.username, 
        "fish_weight": fish_sampling.fish_weight,
        "fish_length": fish_sampling.fish_length,
        "sample_date": fish_sampling.sample_date
    }

@router.get("/{pond_id}/", auth=JWTAuth(), response={200: List[FishSamplingOutputSchema]})
def list_fish_samplings(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    fish_samplings = FishSampling.objects.filter(pond=pond)
    return [{
        "sampling_id": str(sampling.sampling_id),
        "pond_id": str(sampling.pond.pond_id),
        "reporter": sampling.reporter.username,
        "fish_weight": sampling.fish_weight,
        "fish_length": sampling.fish_length,
        "sample_date": sampling.sample_date
    } for sampling in fish_samplings]

@router.put("/{sampling_id}/", auth=JWTAuth())
def update_fish_sampling(request, sampling_id: str, payload: FishSamplingEditSchema):
    fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)
    pond = get_object_or_404(Pond, pond_id=payload.pond_id)
    reporter = get_object_or_404(User, id=payload.reporter_id)
    fish_sampling.pond = pond
    fish_sampling.reporter = reporter
    fish_sampling.fish_weight = payload.fish_weight
    fish_sampling.fish_length = payload.fish_length
    fish_sampling.sample_date = payload.sample_date
    fish_sampling.save()
    return fish_sampling

@router.delete("/{sampling_id}/", auth=JWTAuth())
def delete_fish_sampling(request, sampling_id: str):
    fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)
    fish_sampling.delete()
    return {"success": True}