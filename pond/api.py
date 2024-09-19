from ninja import Router
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Pond
from .schemas import PondAddSchema, PondEditSchema

router = Router()

@router.post("/ponds/")
def add_pond(request, payload: PondAddSchema):
    owner = get_object_or_404(User, id=payload.owner_id)
    pond = Pond.objects.create(
        owner=owner,
        name=payload.name,
        image_name=payload.image_name,
        volume=payload.volume,
    )
    return {"id": str(pond.pond_id), "name": pond.name, "owner": pond.owner.username}

@router.get("/ponds/{pond_id}/")
def get_pond(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    return {"id": str(pond.pond_id), "name": pond.name, "owner": pond.owner.username}

@router.get("/ponds/")
def list_ponds(request):
    ponds = Pond.objects.all()
    return [{"id": str(pond.pond_id), "name": pond.name, "owner": pond.owner.username} for pond in ponds]

@router.delete("/ponds/{pond_id}/")
def delete_pond(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    pond.delete()
    return {"success": True}

@router.put("/ponds/{pond_id}/")
def update_pond(request, pond_id: str, payload: PondEditSchema):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    pond.name = payload.name
    pond.image_name = payload.image_name
    pond.volume = payload.volume
    pond.save()
    return {"id": str(pond.pond_id), "name": pond.name, "owner": pond.owner.username}