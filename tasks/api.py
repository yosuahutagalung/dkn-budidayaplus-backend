from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from ninja import Query, Router
from ninja_jwt.authentication import JWTAuth
from tasks.models import Task
from tasks.schemas import AssignTaskSchema, TaskSchema, SortedTaskSchema, TaskStatusSchema, TaskFilterSchema
from tasks.services.retrieve_service_impl import RetrieveServiceImpl as TaskRetrieveServiceImpl
from tasks.services.assign_service_impl import AssignServiceImpl
from tasks.services.filter_service_impl import FilterServiceImpl
from tasks.services.list_service_impl import ListServiceImpl
from tasks.services.set_status_service_impl import SetStatusServiceImpl
from cycle.services.cycle_service import CycleService
from ninja.errors import HttpError
from typing import List

from user_profile.services.retrieve_service_impl import RetrieveServiceImpl
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

@router.put('/{task_id}/assign', response={200: TaskSchema})
def assign_task(request, task_id: str, payload: AssignTaskSchema):
    try:
        assignee = RetrieveServiceImpl.retrieve_user(payload.assignee)
        task = AssignServiceImpl.assign_task(task_id=task_id, requester=request.auth, assignee=assignee)
        return task
    except Task.DoesNotExist:
        raise HttpError(404, "Tugas tidak ditemukan")
    except User.DoesNotExist:
        raise HttpError(404, f"Pengguna tidak ditemukan")
    except PermissionDenied as e:
        raise HttpError(403, str(e))


@router.get("/{task_id}", response={200: TaskSchema})
def get_task_by_id(request, task_id: str):
    try:
        task = TaskRetrieveServiceImpl.retrieve_task(task_id)
        return task
    except Task.DoesNotExist:
        raise HttpError(404, "Tugas tidak ditemukan")

@router.put("/{task_id}/unassign", response={200: TaskSchema})
def unassign_task(request, task_id: str):
    try:
        task = AssignServiceImpl.unassign_task(task_id=task_id)
        return task
    except Task.DoesNotExist:
        raise HttpError(404, "Tugas tidak ditemukan")
@router.get("/filter-by-date", response={200: List[TaskSchema]})
def filter_tasks_by_date(request, date: date = Query(None)):
    try:
        cycle = CycleService.get_active_cycle(request.auth)
        tasks = FilterServiceImpl.filter_tasks_by_date(cycle.id, date)
        return tasks
    except:
        raise HttpError(400, "Data tidak ditemukan")
