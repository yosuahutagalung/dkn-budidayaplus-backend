from cycle.models import PondFishAmount, Cycle
from cycle.schemas import PondFishAmountInput
from typing import List

class PondFishAmountRepo:
    @staticmethod
    def bulk_create(data: List[PondFishAmountInput], cycle: Cycle):
        pass


    @staticmethod
    def bulk_update(data: List[PondFishAmountInput], cycle: Cycle):
        pass
