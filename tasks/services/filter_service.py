from abc import ABC, abstractmethod

from django.db.models import QuerySet

class FilterService(ABC):
    @staticmethod
    @abstractmethod
    def filter_tasks(cycle_id: str, period: str = "today", assignee_username: str = "") -> QuerySet:
        """Filter tasks by period and assignee"""
