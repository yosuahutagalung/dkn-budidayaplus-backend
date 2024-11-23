from abc import ABC, abstractmethod

from django.db.models import QuerySet

class FilterService(ABC):
    @staticmethod
    @abstractmethod
    def filter_tasks(cycle_id: str, period: str|None = None, assignee_username: str|None = None) -> QuerySet:
        """Filter tasks by period and assignee"""
