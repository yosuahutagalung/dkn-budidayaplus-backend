from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from pond.models import Pond
from pond_quality.models import PondQuality
from pond_quality.schemas import PondQualityInput, PondQualityOutput
from django.contrib.auth.models import User
from typing import List

router = Router()

@router.get("/{pond_id}/", auth=JWTAuth(), response={200: List[PondQualityOutput]})
def list_pond_quality(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    pond_quality = PondQuality.objects.filter(pond=pond)
    return pond_quality


@router.post("/{pond_id}/", auth=JWTAuth(), response={200: PondQualityOutput})
def add_pond_quality(request, pond_id: str, payload: PondQualityInput):
    return None


@router.get("/{pond_id}/{pond_quality_id}/", auth=JWTAuth(), response={200: PondQualityOutput})
def get_pond_quality(request, pond_quality_id: str):
    return None

@router.delete("/{pond_id}/{pond_quality_id}/", auth=JWTAuth())
def delete_pond_quality(request, pond_quality_id: str):
    return None

@router.put("/{pond_id}/{pond_quality_id}/", auth=JWTAuth(), response={200: PondQualityOutput})
def update_pond_quality(request, pond_quality_id: str, payload: PondQualityInput):
    return None