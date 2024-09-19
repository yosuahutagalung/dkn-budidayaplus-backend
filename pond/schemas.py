from ninja import Schema

class PondAddSchema(Schema):
    owner_id: int
    name: str
    image_name: str
    volume: float

class PondEditSchema(Schema):
    name: str
    image_name: str
    volume: float