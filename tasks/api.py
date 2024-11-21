from ninja import Router
from ninja_jwt.authentication import JWTAuth
from tasks.schemas import TaskSchema, SortedTaskSchema
from tasks.services.list_service_impl import ListServiceImpl
from cycle.services.cycle_service import CycleService
from ninja.errors import HttpError
from typing import List

router = Router(auth=JWTAuth())

@router.get("/", response={200: List[TaskSchema]})
def list_tasks(request):
    try:
        cycle = CycleService.get_active_cycle(request.auth)
        tasks = ListServiceImpl.list_tasks(cycle.id)
        return tasks
    except:
        raise HttpError(400, "Data tidak ditemukan")


@router.get("/sorted", response={200: SortedTaskSchema})
def list_tasks_sorted(request):
    try:
        cycle = CycleService.get_active_cycle(request.auth)
        tasks = ListServiceImpl.list_tasks_sorted_date(cycle.id)
        return tasks
    except:
        raise HttpError(400, "Data tidak ditemukan")
    
@router.put("/{task_id}/status/", response={200: TaskSchema})
def set_status(request):
    return