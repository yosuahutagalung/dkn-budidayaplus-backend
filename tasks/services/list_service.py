from abc import ABC, abstractmethod

class ListService(ABC):
    @staticmethod
    @abstractmethod
    def list_tasks(cycle_id: str):
        """List all tasks for a given cycle"""
