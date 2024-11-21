from tasks.services.list_service import ListService
from tasks.repositories.list_repo import ListRepo
from django.contrib.auth.models import User

class ListServiceImpl(ListService):
    @staticmethod
    def list_tasks(cycle_id):
        return ListRepo.list_tasks(cycle_id=cycle_id)

    @staticmethod
    def list_tasks_sorted_date(cycle_id: str) -> dict:
        return {
            "upcoming": ListRepo.list_upcoming_tasks(cycle_id=cycle_id),
            "past": ListRepo.list_past_tasks(cycle_id=cycle_id)
        }
    
    @staticmethod
    def assign_task(request, task_id: str):
        return ListRepo.assign_task(request=request, task_id=task_id)