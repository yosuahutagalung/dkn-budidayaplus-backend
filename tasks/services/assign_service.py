from abc import ABC, abstractmethod
from django.contrib.auth.models import User

from tasks.models import Task

class AssignService(ABC):
    @staticmethod
    @abstractmethod
    def assign_task(task_id: str, requester: User, assignee: User) -> Task:
        """
        Assigns a task to a user
        """

