from ninja import Router
from .schemas import CycleInputSchema, CycleOutputSchema
from ninja_jwt.authentication import JWTAuth

router = Router()

@router.post('/', auth=JWTAuth(), response={200: CycleOutputSchema})
def create_cycle(request, payload: CycleInputSchema):
    return None

@router.get("/", auth=JWTAuth(), response={200: CycleOutputSchema})
def get_cycle(request, id: str):
    return None

@router.delete("/{id}/", auth=JWTAuth())
def delete_cycle(request, id: str):
    return None

@router.put("/{id}/", auth=JWTAuth(), response={200: CycleOutputSchema})
def update_pond(request, id: str):
    return None