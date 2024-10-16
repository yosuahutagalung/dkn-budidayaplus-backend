from datetime import datetime
from django.shortcuts import get_object_or_404
from ninja import Router
from pond.models import Pond
from cycle.schemas import CycleInput, CycleSchema
from ninja_jwt.authentication import JWTAuth
from cycle.models import Cycle, PondFishAmount
from ninja.errors import HttpError
from django.contrib.auth.models import User

router = Router()

@router.post('/', auth=JWTAuth())
def create_cycle(request, payload: CycleInput):
    supervisor = get_object_or_404(User, id=request.auth.id)
    active_cycles = Cycle.objects.filter(start_date__lte=payload.start_date, end_date__gte=payload.end_date, supervisor=supervisor)
    
    if active_cycles.exists():
        raise HttpError(400, "Anda sudah memiliki siklus yang berlangsung saat ini")
    
    try:     
        cycle = Cycle.objects.create(
            start_date=payload.start_date,
            end_date=payload.end_date,
            supervisor=supervisor
        )
    except:
        raise HttpError(400, "Tanggal selesai harus tepat 60 hari setelah tanggal mulai")

    try:
        pond_fish_amount_list = payload.pond_fish_amount
        for pond_fish_amt in pond_fish_amount_list:
            pond = Pond.objects.get(pond_id=pond_fish_amt.pond_id)
            PondFishAmount.objects.create(
                cycle=cycle,
                pond=pond,
                fish_amount=pond_fish_amt.fish_amount
            )
    except:
        cycle.delete()
        raise HttpError(400, "Jumlah ikan harus lebih dari 0")

    return CycleSchema.from_orm(cycle)

@router.get("/", auth=JWTAuth())
def get_cycle(request):
    supervisor = get_object_or_404(User, id=request.auth.id)
    today = datetime.today().date()
    cycle = Cycle.objects.filter(start_date__lte=today, end_date__gte=today, supervisor=supervisor).order_by('-start_date').first()

    if not cycle:
        raise HttpError(404, "Tidak ada siklus yang berlangsung saat ini")
    
    return CycleSchema.from_orm(cycle)
    
@router.delete("/{id}/", auth=JWTAuth())
def delete_cycle(request, id: str):
    cycle = get_object_or_404(Cycle, id=id)
    if cycle.supervisor != request.auth:
        raise HttpError(403, "Anda tidak memiliki akses untuk menghapus data ini")
    cycle.delete()
    return 200, "Cycle deleted"

@router.put("/{id}/", auth=JWTAuth())
def update_cycle(request, id: str, payload: CycleInput):
    cycle = get_object_or_404(Cycle, id=id)
    supervisor = get_object_or_404(User, id=request.auth.id)
    active_cycles = Cycle.objects.filter(start_date__lte=payload.start_date, end_date__gte=payload.end_date, supervisor=supervisor).exclude(id=id)
    
    if active_cycles.exists():
        raise HttpError(400, "Anda sudah memiliki siklus yang berlangsung saat ini")

    if cycle.supervisor != supervisor:
        raise HttpError(403, "Anda tidak memiliki akses untuk mengubah data ini")
    
    try:
        cycle.start_date = payload.start_date
        cycle.end_date = payload.end_date
        cycle.save()
    except:
        raise HttpError(400, "Tanggal selesai harus tepat 60 hari setelah tanggal mulai")

    try:
        pond_fish_amount_list = payload.pond_fish_amount
        for pond_fish_amt in pond_fish_amount_list:
            pond = Pond.objects.get(pond_id=pond_fish_amt.pond_id)
            pond_fish = PondFishAmount.objects.get(cycle=cycle, pond=pond)
            pond_fish.fish_amount = pond_fish_amt.fish_amount
            pond_fish.save()
    except:
        raise HttpError(400, "Jumlah ikan harus lebih dari 0")
    
    return CycleSchema.from_orm(cycle)

@router.get("/{id}/", auth=JWTAuth())
def get_cycle_by_id(request, id: str):
    cycle = get_object_or_404(Cycle, id=id)
    if cycle.supervisor != request.auth:
        raise HttpError(403, "Anda tidak memiliki akses untuk melihat data ini")
    return CycleSchema.from_orm(cycle)