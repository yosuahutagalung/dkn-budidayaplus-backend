from ninja import Router
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Pond, FishSampling
from .schemas import FishSamplingCreateSchema, FishSamplingEditSchema, FishSamplingResponseSchema
from uuid import UUID
from typing import List

router = Router()

@router.post("/fish-sampling", response=FishSamplingResponseSchema)
def create_fish_sampling(request, payload: FishSamplingCreateSchema):
    pond = get_object_or_404(Pond, id=payload.pond_id)
    reporter = get_object_or_404(User, id=payload.reporter_id)
    fish_sampling = FishSampling.objects.create(
        pond=pond,
        reporter=reporter,
        fish_weight=payload.fish_weight,
        fish_length=payload.fish_length,
        sample_date=payload.sample_date
    )
    return fish_sampling

@router.get("/fish-sampling/{sampling_id}", response=FishSamplingResponseSchema)
def get_fish_sampling(request, sampling_id: UUID):
    fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)
    return fish_sampling

@router.get("/fish-sampling/", response=List[FishSamplingResponseSchema])
def list_fish_samplings(request):
    return FishSampling.objects.all()

@router.put("/fish-sampling/{sampling_id}", response=FishSamplingResponseSchema)
def update_fish_sampling(request, sampling_id: UUID, payload: FishSamplingEditSchema):
    fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)
    pond = get_object_or_404(Pond, id=payload.pond_id)
    reporter = get_object_or_404(User, id=payload.reporter_id)
    fish_sampling.pond = pond
    fish_sampling.reporter = reporter
    fish_sampling.fish_weight = payload.fish_weight
    fish_sampling.fish_length = payload.fish_length
    fish_sampling.sample_date = payload.sample_date
    fish_sampling.save()
    return fish_sampling

@router.delete("/fish-sampling/{sampling_id}")
def delete_fish_sampling(request, sampling_id: UUID):
    fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)
    fish_sampling.delete()
    return {"success": True}