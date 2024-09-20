from ninja import Router
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Pond
from .schemas import PondAddSchema, PondEditSchema
from authentication.models import JWTAuth

router = Router()

@router.post("/", auth=JWTAuth())
def add_pond(request, payload: PondAddSchema):
    owner = get_object_or_404(User, id=request.auth.id)
    pond = Pond.objects.create(
        owner=owner,
        name=payload.name,
        image_name=payload.image_name,
        volume=payload.volume,
    )
    return {"id": str(pond.pond_id), "name": pond.name, "owner": pond.owner.username}

@router.get("/{pond_id}/", auth=JWTAuth())
def get_pond(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    return {"id": str(pond.pond_id), "name": pond.name, "owner": pond.owner.username}

@router.get("/", auth=JWTAuth())
def list_ponds_by_user(request):
    user = request.auth
    ponds = Pond.objects.filter(owner=user)
    return [{"id": str(pond.pond_id), "name": pond.name, "owner": pond.owner.username} for pond in ponds]

@router.delete("/{pond_id}/", auth=JWTAuth())
def delete_pond(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    pond.delete()
    return {"success": True}

@router.put("/{pond_id}/", auth=JWTAuth())
def update_pond(request, pond_id: str, payload: PondEditSchema):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    pond.name = payload.name
    pond.image_name = payload.image_name
    pond.volume = payload.volume
    pond.save()
    return {"id": str(pond.pond_id), "name": pond.name, "owner": pond.owner.username}