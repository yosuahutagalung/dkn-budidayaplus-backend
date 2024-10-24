from django.contrib.auth.models import User
from cycle.utils import is_valid_fish_amount, is_valid_period
from cycle.repositories.cycle_repo import CycleRepo
from cycle.repositories.pond_fish_amount_repo import PondFishAmountRepo
from cycle.schemas import CycleInput


class CycleService:
    @staticmethod
    def create_cycle(supervisor: User, payload: CycleInput):
        pass