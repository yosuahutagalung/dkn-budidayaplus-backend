from tasks.models import Task
from django.utils import timezone

class ListRepo:
    @staticmethod
    def list_tasks(cycle_id: str):
        return Task.objects.filter(cycle_id=cycle_id)

    @staticmethod
    def list_past_tasks(cycle_id: str):
        return Task.objects.filter(cycle_id=cycle_id, date__lt=timezone.now().date())

    @staticmethod
    def list_upcoming_tasks(cycle_id: str):
        return Task.objects.filter(cycle_id=cycle_id, date__gte=timezone.now().date())

