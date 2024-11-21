from tasks.models import Task

class SetStatusRepo:
    @staticmethod
    def set_status(task_id: str, status: str):
        task = Task.objects.get(id=task_id)
        task.status = status
        task.save()
        return task