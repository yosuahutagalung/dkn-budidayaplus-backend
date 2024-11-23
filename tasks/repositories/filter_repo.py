from django.utils.timezone import now

from tasks.models import Task


class FilterRepo:
    @staticmethod
    def filter_tasks(period: str = "today", assignee_username: str = ""):
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

        return Task.objects.filter(**filters)

