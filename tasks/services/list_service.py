from abc import ABC, abstractmethod

class ListService(ABC):
    @staticmethod
    @abstractmethod
    def list_tasks(cycle_id: str):
        """List all tasks for a given cycle"""

    @staticmethod
    @abstractmethod
    def list_tasks_sorted_date(cycle_id: str) -> dict:
        """
        List all tasks for a given 
        cycle sorted into upcoming and past
        tasks 
        """
    
    @staticmethod
    @abstractmethod
    def assign_task(task_id: str, assignee: str):
        """
        Assign a task to an assignee
        """