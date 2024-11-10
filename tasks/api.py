from ninja import Router
from ninja_jwt.authentication import JWTAuth
from tasks.schemas import TaskSchema
from typing import List

router = Router(auth=JWTAuth())

@router.get("/", response={200: List[TaskSchema]})
def list_tasks(request):
    pass
