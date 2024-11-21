from tasks.services.set_status_service import SetStatusService
from tasks.repositories.set_status_repo import SetStatusRepo

class SetStatusServiceImpl(SetStatusService):
    @staticmethod
    def set_status(task_id, status):
        return SetStatusRepo.set_status(task_id=task_id, status=status)