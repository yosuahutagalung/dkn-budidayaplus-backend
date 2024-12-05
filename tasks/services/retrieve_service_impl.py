from tasks.services.retrieve_service import RetrieveService
from tasks.models import Task

class RetrieveServiceImpl(RetrieveService):
    @staticmethod
    def retrieve_task(task_id: str) -> Task:
        return Task.objects.get(id=task_id)
