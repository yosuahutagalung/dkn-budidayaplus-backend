from ninja import Schema
from datetime import datetime
from pydantic import UUID4
from typing import List
from user_profile.schemas import UserSchema

class FoodSamplingCreateSchema(Schema):
    food_quantity: int
    recorded_at: datetime

class FoodSamplingOutputSchema(Schema):
    sampling_id: UUID4
    pond_id: UUID4
    cycle_id: UUID4
    reporter: UserSchema
    food_quantity: int
    recorded_at: datetime

class FoodSamplingList(Schema):
    food_samplings: List[FoodSamplingOutputSchema]
    cycle_id: UUID4
