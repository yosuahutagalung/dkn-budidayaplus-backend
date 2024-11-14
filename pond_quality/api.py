from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth
from .schemas import PondQualityInput, PondQualityOutput, PondQualityHistory
from pond_quality.services.pond_quality_service import PondQualityService
from pond_quality.repositories.pond_quality_repository import PondQualityRepository
from ninja.errors import HttpError as NinjaHttpError
from django.http import Http404

DATA_NOT_FOUND = "Data tidak ditemukan"
CYCLE_NOT_ACTIVE = "Siklus tidak aktif"
UNAUTHORIZED_ACCESS = "Anda tidak memiliki akses untuk melihat data ini"

router = Router()
pond_quality_service = PondQualityService(PondQualityRepository())

@router.get("/{cycle_id}/{pond_id}/{pond_quality_id}/", auth=JWTAuth(), response={200: PondQualityOutput})
def get_pond_quality(request, cycle_id: str, pond_id: str, pond_quality_id: str):
    try:
        return pond_quality_service.get_pond_quality(cycle_id, pond_id, pond_quality_id, request.auth)
    except NinjaHttpError as e:
        raise e
    except Http404 as e:
        raise NinjaHttpError(404, "Not Found")
    except Exception:
        raise NinjaHttpError(500, "An unexpected error occurred")


@router.get("/{cycle_id}/{pond_id}/", auth=JWTAuth(), response={200: PondQualityHistory})
def list_pond_qualities(request, pond_id: str, cycle_id: str):
    try:
        pond_qualities = pond_quality_service.list_pond_qualities(cycle_id, pond_id, request.auth)
        return {
            "pond_qualities": pond_qualities,
            "cycle_id": cycle_id
        }
    except NinjaHttpError as e:
        raise e
    except Http404 as e:
        raise NinjaHttpError(404, "Not Found")
    except Exception:
        raise NinjaHttpError(500, "An unexpected error occurred")

@router.get("/{cycle_id}/{pond_id}/latest", auth=JWTAuth(), response={200: PondQualityOutput})
def get_latest_pond_quality(request, pond_id: str, cycle_id: str):
    try:
        return pond_quality_service.get_latest_pond_quality(cycle_id, pond_id, request.auth)
    except NinjaHttpError as e:
        raise e
    except Http404 as e:
        raise NinjaHttpError(404, "Not Found")
    except Exception:
        raise NinjaHttpError(500, "An unexpected error occurred")
        
@router.post("/{cycle_id}/{pond_id}/", auth=JWTAuth(), response={200: PondQualityOutput})
def create_pond_quality(request, pond_id:str, cycle_id:str, payload:PondQualityInput):
    try:
        return pond_quality_service.create_pond_quality(pond_id, cycle_id, request.auth.id, payload)
    except NinjaHttpError as e:
        raise e
    except Http404 as e:
        raise NinjaHttpError(404, "Not Found")
    except Exception:
        raise NinjaHttpError(500, "An unexpected error occurred")