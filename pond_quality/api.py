from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from pond.models import Pond
from pond_quality.models import PondQuality
from pond_quality.schemas import PondQualityInput, PondQualityOutput
from django.contrib.auth.models import User
from typing import List
from ninja.errors import HttpError

router = Router()

@router.get("/{pond_id}/", auth=JWTAuth(), response={200: List[PondQualityOutput]})
def list_pond_quality(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    pond_quality = PondQuality.objects.filter(pond=pond)
    return pond_quality


@router.post("/{pond_id}/", auth=JWTAuth(), response={200: PondQualityOutput})
def add_pond_quality(request, pond_id: str, payload: PondQualityInput):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    reporter = get_object_or_404(User, id=request.auth.id)
    pond_quality = PondQuality.objects.create(
        pond = pond,
        reporter = reporter,
        **payload.dict()
    )
    return pond_quality


@router.get("/{pond_id}/{pond_quality_id}/", auth=JWTAuth(), response={200: PondQualityOutput})
def get_pond_quality(request, pond_id: str, pond_quality_id: str):
    return None


@router.delete("/{pond_id}/{pond_quality_id}/", auth=JWTAuth())
def delete_pond_quality(request, pond_id: str, pond_quality_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    pond_quality = get_object_or_404(PondQuality, id=pond_quality_id)

    if (pond_quality.reporter != request.auth or pond.owner != request.auth):
        return HttpError(401, "Anda tidak memiliki akses untuk menghapus data ini")
    
    if (pond_quality.pond != pond):
        return HttpError(404, "Data tidak ditemukan")
    
    pond_quality.delete()
    return {"success": True}


@router.put("/{pond_id}/{pond_quality_id}/", auth=JWTAuth(), response={200: PondQualityOutput})
def update_pond_quality(request, pond_quality_id: str, payload: PondQualityInput):
    return None