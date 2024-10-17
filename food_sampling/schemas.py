from ninja import Field, Schema
from datetime import date
from pydantic import UUID4

class FoodSamplingOutputSchema(Schema):
    food_id: UUID4
    pond_id: UUID4
    reporter: str = Field(None, alias="reporter.username")
    food_amount: float
    date: date