from tasks.models import Task
from ninja.errors import HttpError
from django.contrib.auth.models import User

class AssignRepo:
    @staticmethod
    def assign_task(user: User, task_id: str) -> Task:
        try:
            task = Task.objects.get(id=task_id)
            task.assignee = user.username
            task.save()
            return task
        except Task.DoesNotExist:
            raise HttpError(404, "Task not found")

    @staticmethod
    def unassign_task(task_id: str) -> Task:
        try:
            task = Task.objects.get(id=task_id)
            task.assignee = ''
            task.save()
            return task
        except Task.DoesNotExist:
            raise HttpError(404, "Task not found")

