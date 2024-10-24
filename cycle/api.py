from ninja import Router
from cycle.schemas import CycleInput, CycleSchema
from ninja_jwt.authentication import JWTAuth
from cycle.services.cycle_service import CycleService
from ninja.errors import HttpError

router = Router()

@router.post('/', auth=JWTAuth())
def create_cycle(request, payload: CycleInput):
    pass
