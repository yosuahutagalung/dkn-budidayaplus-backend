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