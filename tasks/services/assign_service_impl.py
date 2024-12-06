from tasks.models import Task
from tasks.repositories.assign_repo import AssignRepo
from tasks.services.assign_service import AssignService
from user_profile.permissions import check_team_supervisor_permission

class AssignServiceImpl(AssignService):
    @staticmethod
    def assign_task(task_id, requester, assignee):
        check_team_supervisor_permission(requester, assignee)
        return AssignRepo.assign_task(user=assignee, task_id=task_id)

    @staticmethod
    def unassign_task(task_id: str) -> Task:
        return AssignRepo.unassign_task(task_id=task_id)

