from tasks.services.set_status_service import SetStatusService

class SetStatusServiceImpl(SetStatusService):
    @staticmethod
    def set_status(task_id, status):
        return