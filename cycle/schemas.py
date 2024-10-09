from ninja import Schema
from pydantic import UUID4
from datetime import datetime
from typing import List

class CycleFishDistributionInput(Schema):
    pond_id: UUID4
    fish_amount: int

class CycleInputSchema(Schema):
    start_date: datetime
    end_date: datetime
    pond_fish: List[CycleFishDistributionInput]

class CycleFishDistributionOutput(Schema):
    pond_id: UUID4
    fish_amount: int

class CycleOutputSchema(Schema):
    id: UUID4
    start_date: datetime
    end_date: datetime
    supervisor: str
    pond_fish: List[CycleFishDistributionOutput]
