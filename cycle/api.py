from ninja import Router
from cycle.schemas import CycleInput, CycleSchema
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
