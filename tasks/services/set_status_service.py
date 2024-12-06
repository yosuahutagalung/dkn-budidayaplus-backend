from abc import ABC, abstractmethod
from tasks.models import Task

class SetStatusService(ABC):
    @staticmethod
    @abstractmethod
    def set_status(self, task_id: str, status: str) -> Task:
        """Set the status of a task"""