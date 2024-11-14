from ninja import Router
from django.shortcuts import get_object_or_404
from pond.services import PondService
from .models import Pond
from .schemas import PondSchema, PondOutputSchema
from ninja_jwt.authentication import JWTAuth
from typing import List

router = Router()

@router.post("/", auth=JWTAuth(), response={200: PondOutputSchema})
def add_pond(request, payload: PondSchema):
    owner = request.auth
    pond = PondService.add_pond(owner=owner, payload=payload)
    return pond

@router.get("/{pond_id}/", auth=JWTAuth(), response={200: PondOutputSchema})
def get_pond(request, pond_id: str):
    pond = PondService.get_pond(pond_id)
    return pond

@router.get("/", auth=JWTAuth(), response={200: List[PondOutputSchema]})
def list_ponds_by_user(request):
    user = request.auth
    ponds = PondService.list_ponds_by_user(user)
    return ponds

@router.delete("/{pond_id}/", auth=JWTAuth())
def delete_pond(request, pond_id: str):
    PondService.delete_pond(pond_id)
    return {"success": True}

@router.put("/{pond_id}/", auth=JWTAuth(), response={200: PondOutputSchema})
def update_pond(request, pond_id: str, payload: PondSchema):
    pond = PondService.update_pond(pond_id, payload)
    return pond