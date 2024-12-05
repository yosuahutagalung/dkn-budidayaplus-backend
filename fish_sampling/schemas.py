from typing import List
from ninja import Schema
from datetime import datetime
from pydantic import UUID4

from user_profile.schemas import UserSchema

class FishSamplingCreateSchema(Schema):
    fish_weight: float
    fish_length: float

class FishSamplingOutputSchema(Schema):
    sampling_id: UUID4
    pond_id: UUID4
    reporter: UserSchema 
    fish_weight: float
    fish_length: float
    recorded_at: datetime

class FishSamplingList(Schema):
    fish_samplings: List[FishSamplingOutputSchema]
    cycle_id: UUID4
