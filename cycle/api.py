from django.utils import timezone
from ninja import Router
from cycle.schemas import CycleInput, CycleListSchema, CycleSchema
from ninja_jwt.authentication import JWTAuth
from cycle.services.cycle_service import CycleService
from ninja.errors import HttpError

router = Router()

@router.post('/', auth=JWTAuth())
def create_cycle(request, payload: CycleInput):
    try:
        cycle = CycleService.create_cycle(request.auth, payload)
        return CycleSchema.from_orm(cycle)
    except ValueError as e:
        raise HttpError(400, str(e)) 
    except Exception as e:
        raise HttpError(400, str(e))

@router.get('/', auth=JWTAuth())
def get_active_cycle(request):
    try:
        cycle = CycleService.get_active_cycle(request.auth)
        return CycleSchema.from_orm(cycle)
    except ValueError as e:
        raise HttpError(404, 'Tidak ada siklus yang aktif')
    except Exception as e:
        raise HttpError(400, str(e))

@router.get('/{id}/', auth=JWTAuth())
def get_cycle_by_id(request, id: str):
    try:
        cycle = CycleService.get_cycle_by_id(id)
        return CycleSchema.from_orm(cycle)
    except ValueError as e:
        raise HttpError(404, 'Siklus tidak ditemukan')
    except Exception as e:
        raise HttpError(400, str(e))


@router.get('/list', auth=JWTAuth(), response={200: CycleListSchema})
def get_cycle_list(request):
    try:
        active_cycles = CycleService.get_active_cycle_safe(request.auth)
        past_cycles = CycleService.get_cycle_past_or_future(request.auth, timezone.now().date(), 'past')
        future_cycles = CycleService.get_cycle_past_or_future(request.auth, timezone.now().date(), 'future')
        stopped_cycles = CycleService.get_stopped_cycle(request.auth)
        return {
            'active': active_cycles,
            'past': past_cycles,
            'future': future_cycles
            'stopped': stopped_cycles
        }
    except Exception as e:
        raise HttpError(400, str(e))


@router.post('/stop/{id}/', auth=JWTAuth())
def stop_cycle(request, id: str):
    try:
        CycleService.stop_cycle(id, request.auth)
        return {"message": "Siklus berhasil dihentikan"}
    except ValueError as e:
        raise HttpError(400, str(e))
    except Exception as e:
        raise HttpError(400, str(e))

