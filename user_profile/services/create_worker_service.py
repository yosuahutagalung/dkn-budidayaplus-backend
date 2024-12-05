from abc import ABC, abstractmethod
from user_profile.models import Worker
from django.contrib.auth.models import User
from user_profile.schemas import CreateWorkerSchema

class CreateWorkerService(ABC):
    @staticmethod
    @abstractmethod
    def create_worker(payload_worker: CreateWorkerSchema, supervisor: User) -> Worker:
        """Supervisor to create worker"""
