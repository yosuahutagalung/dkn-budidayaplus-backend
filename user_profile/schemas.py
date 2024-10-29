from ninja import Schema, Field
from pydantic import UUID4
from typing import Optional

class ProfileSchema(Schema):
    id: UUID4
    user: str = Field(None, alias='user.username')
    image_name: Optional[str] = ''

class ProfileInputSchema(Schema):
    image_name: Optional[str] = ''
