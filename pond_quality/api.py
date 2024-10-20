from datetime import datetime
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from cycle.models import Cycle
from pond.models import Pond
from pond_quality.models import PondQuality
from pond_quality.schemas import PondQualityInput, PondQualityOutput
from django.contrib.auth.models import User
from typing import List
from ninja.errors import HttpError
from django.core.exceptions import ObjectDoesNotExist

DATA_NOT_FOUND = "Data tidak ditemukan"
CYCLE_NOT_ACTIVE = "Siklus tidak aktif"

router = Router()

@router.get("/{cycle_id}/{pond_id}/", auth=JWTAuth(), response={200: List[PondQualityOutput]})
def list_pond_quality(request, cycle_id: str, pond_id: str):
    cycle = get_object_or_404(Cycle, id=cycle_id, supervisor=request.auth)
    pond = get_object_or_404(Pond, pond_id=pond_id)

    today = datetime.now().date()
    if not (cycle.start_date <= today <= cycle.end_date):
        raise HttpError(400, CYCLE_NOT_ACTIVE)
    
    pond_quality = PondQuality.objects.filter(cycle=cycle, pond=pond)
    return pond_quality


@router.post("/{cycle_id}/{pond_id}/", auth=JWTAuth(), response={200: PondQualityOutput})
def add_pond_quality(request, cycle_id: str, pond_id: str, payload: PondQualityInput):
    cycle = get_object_or_404(Cycle, id=cycle_id, supervisor=request.auth)

    today = datetime.now().date()
    if not (cycle.start_date <= today <= cycle.end_date):
        raise HttpError(400, CYCLE_NOT_ACTIVE)
    
    pond = get_object_or_404(Pond, pond_id=pond_id)
    reporter = get_object_or_404(User, id=request.auth.id)
    pond_quality = PondQuality.objects.create(
        cycle = cycle,
        pond = pond,
        reporter = reporter,
        **payload.dict()
    )
    return pond_quality


@router.get("/{cycle_id}/{pond_id}/{pond_quality_id}/", auth=JWTAuth(), response={200: PondQualityOutput})
def get_pond_quality(request, cycle_id: str, pond_id: str, pond_quality_id: str):
    cycle = Cycle.objects.get(id=cycle_id)
    pond = get_object_or_404(Pond, pond_id=pond_id)
    pond_quality = get_object_or_404(PondQuality, id=pond_quality_id)

    today = datetime.now().date()
    if not (cycle.start_date <= today <= cycle.end_date):
        raise HttpError(400, CYCLE_NOT_ACTIVE)
    
    if (pond_quality.cycle != cycle):
        raise HttpError(404, DATA_NOT_FOUND)
    
    if (pond_quality.pond != pond):
        raise HttpError(404, DATA_NOT_FOUND)
    
    if (pond_quality.reporter != request.auth or pond.owner != request.auth):
        raise HttpError(401, "Anda tidak memiliki akses untuk melihat data ini")
    
    return pond_quality


@router.get("/{pond_id}/latest", auth=JWTAuth(), response={200: PondQualityOutput})
def get_latest_pond_quality(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    
    try:
        pond_quality = PondQuality.objects.filter(pond=pond).latest('recorded_at')
    except ObjectDoesNotExist:
        raise HttpError(404, DATA_NOT_FOUND)

    if (pond_quality.reporter != request.auth or pond.owner != request.auth):
        raise HttpError(401, "Anda tidak memiliki akses untuk melihat data ini")
    
    return pond_quality