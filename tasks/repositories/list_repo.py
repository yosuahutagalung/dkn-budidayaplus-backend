from tasks.models import Task
from django.utils import timezone
from ninja.errors import HttpError

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

    @staticmethod
    def assign_task(request, task_id: str) -> Task:
        try:
            task = Task.objects.get(id=task_id)
            task.assignee = request.auth.first_name
            task.save()
            return task
        except Task.DoesNotExist:
            raise HttpError(404, "Task not found")
