from abc import ABC, abstractmethod

from tasks.models import Task 

class RetrieveService(ABC):
    @staticmethod
    @abstractmethod
    def retrieve_task(task_id: str) -> Task:
        """Retrieve task by ID"""
