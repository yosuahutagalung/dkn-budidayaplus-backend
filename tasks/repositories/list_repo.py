from abc import ABC, abstractmethod
from tasks.models import Task

class ListRepo(ABC):
    @staticmethod
    @abstractmethod
    def list_tasks(cycle_id: str):
        return Task.objects.filter(cycle_id=cycle_id)
