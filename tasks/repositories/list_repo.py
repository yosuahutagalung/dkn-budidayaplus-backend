from tasks.models import Task

class ListRepo:
    @staticmethod
    def list_tasks(cycle_id: str):
        return Task.objects.filter(cycle_id=cycle_id)

    @staticmethod
    def list_past_tasks(cycle_id: str):
        pass
    
    @staticmethod
    def list_upcoming_tasks(cycle_id: str):
        pass
