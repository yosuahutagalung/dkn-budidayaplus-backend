from ninja import Field, Schema
from datetime import date
from pydantic import UUID4

class FoodSamplingCreateSchema(Schema):
    food_quantity: int
    sample_date  : date = Field(default_factory=date.today)

class FoodSamplingOutputSchema(Schema):
    sampling_id: UUID4
    pond_id: UUID4
    cycle_id: UUID4
    reporter: str = Field(None, alias="reporter.username")
    food_quantity: int
    sample_date: date

class FoodSamplingHistory(Schema):
    food_sampling: List[FoodSamplingOutputSchema]
    cycle_id: UUID4