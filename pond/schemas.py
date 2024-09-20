from ninja import Schema
from authentication.schemas import UserSchema

class PondAddSchema(Schema):
    name: str
    image_name: str
    volume: float

class PondEditSchema(Schema):
    name: str
    image_name: str
    volume: float