from ninja import Schema, Field
from pydantic import UUID4
from datetime import date
from typing import List

class PondFishAmountInput(Schema):
    pond_id: UUID4
    fish_amount: int

class CycleInput(Schema):
    start_date: date
    end_date: date
    pond_fish_amount: List[PondFishAmountInput]

class PondFishAmountSchema(Schema):
    id: UUID4
    pond_id: UUID4
    fish_amount: int


class CycleSchema(Schema):
    id: UUID4
    start_date: date
    end_date: date
    status: str
    supervisor: str = Field(..., alias='supervisor.username')
    pond_fish_amount: List[PondFishAmountSchema]
