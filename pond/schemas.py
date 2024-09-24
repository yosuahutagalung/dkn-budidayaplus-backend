from ninja import Schema

class PondAddSchema(Schema):
    name: str
    image_name: str
    volume: float

class PondEditSchema(Schema):
    name: str
    image_name: str
    volume: float