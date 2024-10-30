from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import FishSampling
from pond.models import Pond
from cycle.models import Cycle
from .schemas import FishSamplingCreateSchema, FishSamplingEditSchema, FishSamplingOutputSchema
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from datetime import datetime

DATA_NOT_FOUND = "Data tidak ditemukan"
CYCLE_NOT_ACTIVE = "Siklus tidak aktif"
UNAUTHORIZED_ACCESS = "Anda tidak memiliki akses untuk melihat data ini"

router = Router()

def check_cycle_active(cycle):
    today = datetime.now().date()
    if not (cycle.start_date <= today <= cycle.end_date):
        raise HttpError(400, CYCLE_NOT_ACTIVE)

@router.post("/{pond_id}/{cycle_id}/", auth=JWTAuth(), response={200: FishSamplingOutputSchema})
def create_fish_sampling(request, pond_id: str, cycle_id: str, payload: FishSamplingCreateSchema):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    reporter = get_object_or_404(User, id=request.auth.id)
    cycle = get_object_or_404(Cycle, id=cycle_id)

    check_cycle_active(cycle)

    fish_sampling = FishSampling.objects.create(
        pond=pond,
        reporter=reporter,
        fish_weight=payload.fish_weight,
        fish_length=payload.fish_length,
        sample_date=payload.sample_date,
        cycle=cycle
    )
    return fish_sampling

@router.get("/{pond_id}/{cycle_id}/{sampling_id}/", auth=JWTAuth(), response={200: FishSamplingOutputSchema})
def get_fish_sampling(request, pond_id: str, sampling_id: str, cycle_id: str):
    cycle = Cycle.objects.get(id=cycle_id)
    pond = get_object_or_404(Pond, pond_id=pond_id)
    fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)

    check_cycle_active(cycle)

    if (fish_sampling.cycle != cycle):
        raise HttpError(404, DATA_NOT_FOUND)
    
    if (fish_sampling.pond != pond):
        raise HttpError(404, DATA_NOT_FOUND)
    
    if (fish_sampling.reporter != request.auth or pond.owner != request.auth):
        raise HttpError(401, UNAUTHORIZED_ACCESS)
    
    return fish_sampling


@router.get("/{pond_id}/{cycle_id}/", auth=JWTAuth(), response={200: List[FishSamplingOutputSchema]})
def list_fish_samplings(request, pond_id: str, cycle_id: str):
    cycle = get_object_or_404(Cycle, id=cycle_id, supervisor=request.auth)
    pond = get_object_or_404(Pond, pond_id=pond_id)

    check_cycle_active(cycle)
    
    fish_samplings = FishSampling.objects.filter(cycle=cycle, pond=pond)
    return [sampling for sampling in fish_samplings]

@router.put("/{pond_id}/{cycle_id}/{sampling_id}/", auth=JWTAuth(), response={200: FishSamplingEditSchema})
def update_fish_sampling(request, pond_id: str, sampling_id: str, cycle_id: str, payload: FishSamplingEditSchema):
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

@router.delete("/{pond_id}/{cycle_id}/{sampling_id}/", auth=JWTAuth())
def delete_fish_sampling(request, pond_id: str, sampling_id: str, cycle_id: str):
    fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)
    fish_sampling.delete()
    return {"success": True}