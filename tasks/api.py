from ninja import Query, Router
from ninja_jwt.authentication import JWTAuth
from tasks.models import Task
from tasks.schemas import TaskSchema, SortedTaskSchema, TaskStatusSchema, TaskFilterSchema
from tasks.services.filter_service_impl import FilterServiceImpl
from tasks.services.list_service_impl import ListServiceImpl
from tasks.services.set_status_service_impl import SetStatusServiceImpl
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
def set_status(request, task_id: str, payload: TaskStatusSchema):
    try:
        task = SetStatusServiceImpl.set_status(task_id=task_id, status=payload.status)
        return task
    except Task.DoesNotExist:
        raise HttpError(404, f"Task with ID {task_id} does not exist")


@router.get("/filter", response={200: List[TaskSchema]})
def filter_tasks(request, filters: Query[TaskFilterSchema]):
    try:
        cycle = CycleService.get_active_cycle(request.auth)
        tasks = FilterServiceImpl.filter_tasks(cycle.id, filters.period.value if filters.period else None, filters.assignee)
        return tasks[filters.offset : filters.offset + filters.limit]
    except:
        raise HttpError(400, "Data tidak ditemukan")

