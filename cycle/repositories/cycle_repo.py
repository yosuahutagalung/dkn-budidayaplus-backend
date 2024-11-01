from cycle.models import Cycle
from django.contrib.auth.models import User
from datetime import date

class CycleRepo:
    @staticmethod
    def is_active_cycle_exist(supervisor: User, start: date, end: date):
        return Cycle.objects.filter(supervisor=supervisor, start_date__lte=end, end_date__gte=start).exists()

    @staticmethod
    def create(start: date, end: date, supervisor: User):
        cycle = Cycle.objects.create(
            start_date=start,
            end_date=end,
            supervisor=supervisor
        )
        return cycle

    @staticmethod
    def get_active_cycle(supervisor: User):
        return Cycle.objects.filter(supervisor=supervisor, start_date__lte=date.today(), end_date__gte=date.today()).first()
    
    @staticmethod
    def get_cycle_by_id(id: str):
        return Cycle.objects.filter(id=id).first()
