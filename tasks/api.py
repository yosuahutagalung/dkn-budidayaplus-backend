from ninja import Query, Router
from ninja_jwt.authentication import JWTAuth
from tasks.schemas import TaskSchema, SortedTaskSchema, TaskFilterSchema
from tasks.services.filter_service_impl import FilterServiceImpl
from tasks.services.list_service_impl import ListServiceImpl
from cycle.services.cycle_service import CycleService
from ninja.errors import HttpError
from typing import List
from datetime import date

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


@router.get("/filter", response={200: List[TaskSchema]})
def filter_tasks(request, filters: Query[TaskFilterSchema]):
    try:
        cycle = CycleService.get_active_cycle(request.auth)
        tasks = FilterServiceImpl.filter_tasks(cycle.id, filters.period.value if filters.period else None, filters.assignee)
        return tasks[filters.offset : filters.offset + filters.limit]
    except:
        raise HttpError(400, "Data tidak ditemukan")

@router.get("/filter-by-date", response={200: List[TaskSchema]})
def filter_tasks_by_date(request, date: date = Query(None)):
    try:
        cycle = CycleService.get_active_cycle(request.auth)
        tasks = FilterServiceImpl.filter_tasks_by_date(cycle.id, date)
        return tasks
    except:
        raise HttpError(400, "Data tidak ditemukan")
