from ninja import Router
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Cycle, Pond
from .schemas import CycleSchema, CycleOutputSchema
from ninja_jwt.authentication import JWTAuth
from typing import List

router = Router()

@router.post("/{pond_id}/", auth=JWTAuth(), response={200: CycleOutputSchema})
def add_cycle(request, pond_id: str, payload: CycleSchema):
    owner = get_object_or_404(User, id=request.auth.id)
    pond = get_object_or_404(Pond, pond_id=pond_id)
    cycle = Cycle.objects.create(
        owner=owner,
        pond=pond,
        fish_amounts=payload.fish_amounts,
        starting_date=payload.starting_date,
        ending_date=payload.ending_date,
    )
    return cycle

@router.get("/{pond_id}/cycle_id/{cycle_id}/", auth=JWTAuth(), response={200: CycleOutputSchema})
def get_cycle(request, pond_id: str, cycle_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    cycle = get_object_or_404(Cycle, pond=pond, cycle_id=cycle_id)
    return cycle

@router.get("/{pond_id}/", auth=JWTAuth(), response={200: List[CycleOutputSchema]})
def list_cycles_by_pond(request, pond_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    cycles = Cycle.objects.filter(pond=pond)

    return cycles

@router.delete("/{pond_id}/cycle_id/{cycle_id}/", auth=JWTAuth())
def delete_cycle(request, pond_id: str, cycle_id: str):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    cycle = get_object_or_404(Cycle, pond=pond, cycle_id=cycle_id)
    cycle.delete()
    return {"success": True}

@router.put("/{pond_id}/cycle_id/{cycle_id}/", auth=JWTAuth(), response={200: CycleOutputSchema})
def update_pond(request, pond_id: str, cycle_id: str, payload: CycleSchema):
    pond = get_object_or_404(Pond, pond_id=pond_id)
    cycle = get_object_or_404(Cycle, pond=pond, cycle_id=cycle_id)
    data = payload.dict()
    for attr, value in data.items():
        if not value:
            continue
        setattr(cycle, attr, value)

    cycle.save()
    return cycle