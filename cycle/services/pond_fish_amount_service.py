from cycle.schemas import PondFishAmountInput
from cycle.models import Cycle
from typing import List
from cycle.repositories.pond_fish_amount_repo import PondFishAmountRepo
from cycle.utils import is_valid_fish_amount

class PondFishAmountService:
    @staticmethod
    def bulk_create(data: List[PondFishAmountInput], cycle: Cycle):
        for pond_fish_amt in data:
            if not is_valid_fish_amount(pond_fish_amt.fish_amount):
                raise ValueError("Jumlah ikan harus lebih dari 0")

        PondFishAmountRepo.bulk_create(data, cycle)


    @staticmethod
    def bulk_update(data: List[PondFishAmountInput], cycle: Cycle):
        for pond_fish_amt in data:
            if not is_valid_fish_amount(pond_fish_amt.fish_amount):
                raise ValueError("Jumlah ikan harus lebih dari 0")

        PondFishAmountRepo.bulk_update(data, cycle)