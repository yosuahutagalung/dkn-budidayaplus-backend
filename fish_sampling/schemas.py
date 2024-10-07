from ninja import Field, Schema
from datetime import date

class FishSamplingCreateSchema(Schema):
    fish_weight: float
    fish_length: float
    sample_date: date = Field(default_factory=date.today)

class FishSamplingEditSchema(Schema): 
    fish_weight: float 
    fish_length: float
    sample_date: date

class FishSamplingOutputSchema(Schema):
    sampling_id: str
    pond_id: str
    reporter: str = Field(None, alias="reporter.username")
    fish_weight: float
    fish_length: float
    sample_date: date