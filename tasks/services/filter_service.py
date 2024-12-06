from abc import ABC, abstractmethod
from datetime import date

from django.db.models import QuerySet

class FilterService(ABC):
    @staticmethod
    @abstractmethod
    def filter_tasks(cycle_id: str, period: str|None = None, assignee_username: str|None = None) -> QuerySet:
        """Filter tasks by period and assignee"""

    @staticmethod
    @abstractmethod
    def filter_tasks_by_date(cycle_id: str, date: date | None = None) -> QuerySet:
        """Filter tasks for a specific date. Defaults to today's date if not provided."""