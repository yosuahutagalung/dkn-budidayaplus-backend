from ninja import Schema

class PondSchema(Schema):
    name: str
    image_name: str
    length: float
    width: float
    depth: float