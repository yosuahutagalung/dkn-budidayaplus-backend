from ninja import Schema, Field
from pydantic import UUID4
from datetime import datetime

class CycleSchema(Schema):
    fish_amounts   : int
    starting_date  : datetime
    ending_date    : datetime

    class Config:
        from_attributes = True

class CycleOutputSchema(CycleSchema):
    cycle_id       : UUID4
    owner          : str = Field(None, alias="owner.username")
    pond           : UUID4 = Field(None, alias="pond.pond_id")
    fish_amounts   : int
    starting_date  : datetime
    ending_date    : datetime

    class Config:
        from_attributes = True