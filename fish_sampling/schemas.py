from ninja import Schema
from uuid import UUID
from datetime import date

class FishSamplingCreateSchema(Schema):
    pond_id: UUID
    reporter_id: int
    fish_weight: float
    fish_length: float
    sample_date: date

class FishSamplingEditSchema(Schema):
    pond_id: int
    reporter_id: int
    fish_weight: float
    fish_length: float
    sample_date: date

class FishSamplingResponseSchema(Schema):
    sampling_id: UUID
    pond: str
    reporter: str
    fish_weight: float
    fish_length: float
    sample_date: date