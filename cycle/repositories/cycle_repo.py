from cycle.models import Cycle
from django.contrib.auth.models import User
from datetime import date

class CycleRepo:
    @staticmethod
    def is_active_cycle_exist(supervisor: User, start: date, end: date):
        pass

    @staticmethod
    def create(start: date, end: date, supervisor: User):
        pass