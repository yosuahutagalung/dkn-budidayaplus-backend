from tasks.repositories.filter_repo import FilterRepo
from tasks.services.filter_service import FilterService


class FilterServiceImpl(FilterService):
    @staticmethod
    def filter_tasks(cycle_id, period = "today", assignee_username = ""):
        return FilterRepo.filter_tasks(cycle_id=cycle_id, period=period, assignee_username=assignee_username)
