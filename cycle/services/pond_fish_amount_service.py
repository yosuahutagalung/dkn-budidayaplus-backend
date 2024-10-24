from cycle.schemas import PondFishAmountInput
from cycle.models import Cycle
from typing import List
from cycle.repositories.pond_fish_amount_repo import PondFishAmountRepo
from cycle.utils import is_valid_fish_amount

class PondFishAmountService:
    @staticmethod
    def bulk_create(data: List[PondFishAmountInput], cycle: Cycle):
        pass


    @staticmethod
    def bulk_update(data: List[PondFishAmountInput], cycle: Cycle):
        pass