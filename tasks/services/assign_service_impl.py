from django.core.exceptions import PermissionDenied
from tasks.repositories.assign_repo import AssignRepo
from tasks.services.assign_service import AssignService


class AssignServiceImpl(AssignService):
    @staticmethod
    def assign_task(task_id, requester, assignee):
        if not requester.is_staff:
            raise PermissionDenied("Anda tidak memiliki izin untuk melakukan penugasan")

        return AssignRepo.assign_task(user=assignee, task_id=task_id)
