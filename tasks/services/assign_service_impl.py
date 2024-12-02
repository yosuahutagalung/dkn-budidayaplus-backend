from django.contrib.auth.models import User
from tasks.repositories.assign_repo import AssignRepo
from tasks.services.assign_service import AssignService


class AssignServiceImpl(AssignService):
    @staticmethod
    def assign_task(task_id: str, assignee: User):
        return AssignRepo.assign_task(user=assignee, task_id=task_id)
