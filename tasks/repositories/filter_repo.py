from django.utils.timezone import now
from tasks.models import Task
from datetime import date

class FilterRepo:
    @staticmethod
    def filter_tasks(cycle_id: str, period: str|None = None, assignee_username: str|None = None):
        filters = {}
        today = now().date()

        if period == "today":
            filters['date'] = today
        elif period == "upcoming":
            filters['date__gt'] = today
        elif period == "past":
            filters['date__lt'] = today

        if assignee_username:
            filters['assignee'] = assignee_username

        return Task.objects.filter(**filters, cycle_id=cycle_id)

    @staticmethod
    def filter_tasks_by_date(cycle_id: str, date: date):
        return Task.objects.filter(cycle_id=cycle_id, date=date)
