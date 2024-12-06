from tasks.repositories.filter_repo import FilterRepo
from tasks.services.filter_service import FilterService
from datetime import date
from django.utils.timezone import now


class FilterServiceImpl(FilterService):
    @staticmethod
    def filter_tasks(cycle_id, period = None, assignee_username = None):
        return FilterRepo.filter_tasks(cycle_id=cycle_id, period=period, assignee_username=assignee_username)

    @staticmethod
    def filter_tasks_by_date(cycle_id: str, date: date | None = None):  
        if date is None:  
            date = now().date() 
        return FilterRepo.filter_tasks_by_date(cycle_id=cycle_id, date=date)