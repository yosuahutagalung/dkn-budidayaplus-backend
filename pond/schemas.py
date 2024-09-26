from ninja import Schema, Field
from pydantic import UUID4

class PondSchema(Schema):
    name        : str
    image_name  : str
    length      : float
    width       : float
    depth       : float

class PondOutputSchema(PondSchema):
    pond_id          : UUID4
    owner       : str = Field(None, alias="owner.username")
    name        : str
    image_name  : str
    length      : float
    width       : float
    depth       : float