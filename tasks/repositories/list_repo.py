from tasks.models import Task

class ListRepo:
    @staticmethod
    def list_tasks(cycle_id: str):
        return Task.objects.filter(cycle_id=cycle_id)
