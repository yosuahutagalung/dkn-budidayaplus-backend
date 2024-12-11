from datetime import datetime
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from cycle.models import Cycle
from cycle.services.cycle_service import CycleService
from pond.models import Pond
from pond_quality.models import PondQuality
from pond_quality.schemas import PondQualityInput, PondQualityOutput, PondQualityHistory
from django.contrib.auth.models import User
from ninja.errors import HttpError
from django.core.exceptions import ObjectDoesNotExist
from user_profile.utils import get_supervisor

DATA_NOT_FOUND = "Data tidak ditemukan"
CYCLE_NOT_ACTIVE = "Siklus tidak aktif"
UNAUTHORIZED_ACCESS = "Anda tidak memiliki akses untuk melihat data ini"

router = Router()

def check_cycle_active(cycle):
    today = datetime.now().date()
    if not (cycle.start_date <= today <= cycle.end_date):
        raise HttpError(400, CYCLE_NOT_ACTIVE)

@router.get("/{pond_id}/", auth=JWTAuth(), response={200: PondQualityHistory})
def list_pond_quality(request, pond_id: str):
    cycle = CycleService.get_active_cycle(request.auth)
    pond = get_object_or_404(Pond, pond_id=pond_id)

    check_cycle_active(cycle)

    pond_quality = PondQuality.objects.filter(cycle=cycle, pond=pond)

    return {
        "pond_qualities": pond_quality,
        "cycle_id": cycle.id
    }


@router.post("/{cycle_id}/{pond_id}/", auth=JWTAuth(), response={200: PondQualityOutput})
def add_pond_quality(request, cycle_id: str, pond_id: str, payload: PondQualityInput):
    supervisor = get_supervisor(user=request.auth)
    cycle = get_object_or_404(Cycle, id=cycle_id, supervisor=supervisor)
    check_cycle_active(cycle)

    pond = get_object_or_404(Pond, pond_id=pond_id)
    reporter = get_object_or_404(User, id=request.auth.id)

    today = datetime.now().date()
    existing_pond_quality = PondQuality.objects.filter(cycle=cycle, pond=pond, recorded_at__date=today).first()
    if existing_pond_quality:
        existing_pond_quality.delete()

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
    supervisor = get_supervisor(user=request.auth)

    check_cycle_active(cycle)
    
    if (pond_quality.cycle != cycle):
        raise HttpError(404, DATA_NOT_FOUND)
    
    if (pond_quality.pond != pond):
        raise HttpError(404, DATA_NOT_FOUND)
    
    if (pond.owner != supervisor):
        raise HttpError(401, UNAUTHORIZED_ACCESS)
    
    return pond_quality


@router.get("/{cycle_id}/{pond_id}/latest", auth=JWTAuth(), response={200: PondQualityOutput})
def get_latest_pond_quality(request, cycle_id: str, pond_id: str):
    cycle = Cycle.objects.get(id=cycle_id)
    pond = get_object_or_404(Pond, pond_id=pond_id)
    supervisor = get_supervisor(user=request.auth)

    check_cycle_active(cycle)

    try:
        pond_quality = PondQuality.objects.filter(pond=pond, cycle=cycle).select_related('reporter').latest('recorded_at')
    except ObjectDoesNotExist:
        raise HttpError(404, DATA_NOT_FOUND)

    if (pond.owner != supervisor):
        raise HttpError(401, UNAUTHORIZED_ACCESS)

    return pond_quality
