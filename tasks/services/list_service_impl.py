from tasks.services.list_service import ListService
from tasks.repositories.list_repo import ListRepo

class ListServiceImpl(ListService):
    @staticmethod
    def list_tasks(cycle_id):
        return ListRepo.list_tasks(cycle_id=cycle_id)
