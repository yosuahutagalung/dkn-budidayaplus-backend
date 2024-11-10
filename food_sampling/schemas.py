from ninja import Field, Schema
from datetime import datetime
from pydantic import UUID4
from typing import List

class FoodSamplingCreateSchema(Schema):
    food_quantity: float
    recorded_at: datetime

class FoodSamplingOutputSchema(Schema):
    sampling_id: UUID4
    pond_id: UUID4
    cycle_id: UUID4
    reporter: str = Field(None, alias="reporter.username")
    food_quantity: float
    recorded_at: datetime

class FoodSamplingList(Schema):
    food_samplings: List[FoodSamplingOutputSchema]
    cycle_id: UUID4