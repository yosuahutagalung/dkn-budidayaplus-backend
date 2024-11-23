from abc import ABC, abstractmethod

from django.db.models import QuerySet

class ListService(ABC):
    @staticmethod
    @abstractmethod
    def list_tasks(cycle_id: str) -> QuerySet:
        """List all tasks for a given cycle"""

    @staticmethod
    @abstractmethod
    def list_tasks_sorted_date(cycle_id: str) -> dict:
        """
        List all tasks for a given 
        cycle sorted into upcoming and past
        tasks 
        """
