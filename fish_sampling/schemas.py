from ninja import Field, Schema
from datetime import date
from pydantic import UUID4

class FishSamplingCreateSchema(Schema):
    fish_weight: float
    fish_length: float
    sample_date: date = Field(default_factory=date.today)

class FishSamplingEditSchema(Schema): 
    fish_weight: float 
    fish_length: float
    sample_date: date

class FishSamplingOutputSchema(Schema):
    sampling_id: UUID4
    pond_id: UUID4
    reporter: str = Field(None, alias="reporter.username")
    fish_weight: float
    fish_length: float
    sample_date: date