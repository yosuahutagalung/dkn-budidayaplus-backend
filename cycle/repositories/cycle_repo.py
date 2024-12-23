from typing import Literal
from django.db.models import QuerySet
from cycle.models import Cycle
from django.contrib.auth.models import User
from datetime import date

class CycleRepo:
    @staticmethod
    def is_active_cycle_exist(supervisor: User, start: date, end: date):
        return Cycle.objects.filter(supervisor=supervisor, start_date__lte=end, end_date__gte=start, is_stopped='False').exists()

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
        return Cycle.objects.filter(supervisor=supervisor, start_date__lte=date.today(), end_date__gte=date.today(), is_stopped='False').first()

    @staticmethod
    def get_active_cycle_safe(supervisor: User):
        return Cycle.objects.filter(supervisor=supervisor, start_date__lte=date.today(), end_date__gte=date.today(), is_stopped='False')

    @staticmethod
    def get_cycle_by_id(id: str):
        return Cycle.objects.filter(id=id).first()

    @staticmethod
    def get_cycle_past_or_future(supervisor: User, date: date, direction: Literal['past', 'future']):
        filters = {
            'past': {'end_date__lt': date},
            'future': {'start_date__gt': date}
        }
        return Cycle.objects.filter(supervisor=supervisor, **filters[direction])

    @staticmethod
    def stop_cycle(cycle_id: str):
        cycle = Cycle.objects.filter(id=cycle_id).first()
        if cycle:
            cycle.is_stopped = True
            cycle.save()
        return cycle

