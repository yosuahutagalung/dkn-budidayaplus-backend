from ninja import Schema
from datetime import datetime

class FishSamplingCreateSchema(Schema):
    pond_id: str
    reporter_id: int
    fish_weight: float
    fish_length: float
    sample_date: datetime

class FishSamplingEditSchema(Schema):
    pond_id: str
    reporter_id: int
    fish_weight: float
    fish_length: float
    sample_date: datetime