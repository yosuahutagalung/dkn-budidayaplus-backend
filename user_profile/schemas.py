from ninja import Schema, Field
from pydantic import UUID4
from typing import Optional

class ProfileInputSchema(Schema):
    image_name: Optional[str] = ''

class UserSchema(Schema):
    id: int
    phone_number: str = Field(alias='username')
    first_name: str
    last_name: str

class ProfileSchema(Schema):
    id: UUID4
    user: UserSchema
    image_name: Optional[str] = ''

class UpdateProfileSchema(Schema):
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    image_name: Optional[str] = ''