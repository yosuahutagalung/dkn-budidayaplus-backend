from cycle.models import PondFishAmount, Cycle
from cycle.schemas import PondFishAmountInput
from typing import List

class PondFishAmountRepo:
    @staticmethod
    def bulk_create(data: List[PondFishAmountInput], cycle: Cycle):
        PondFishAmount.objects.bulk_create(
            [PondFishAmount(cycle=cycle, pond_id=pfa.pond_id, fish_amount=pfa.fish_amount) for pfa in data]
        )


    @staticmethod
    def bulk_update(data: List[PondFishAmountInput], cycle: Cycle):
        update_data = []
        
        for pfa in data:
            pond_fish_amount = PondFishAmount.objects.get(cycle=cycle, pond_id=pfa.pond_id)
            pond_fish_amount.fish_amount = pfa.fish_amount
            update_data.append(pond_fish_amount)
            
        PondFishAmount.objects.bulk_update(update_data, ['fish_amount'])
