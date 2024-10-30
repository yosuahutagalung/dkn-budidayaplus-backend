from ninja import Schema, Field
from pydantic import UUID4
from typing import Optional
from datetime import date

class ProfileSchema(Schema):
    id: UUID4
    user: str = Field(None, alias='user.username')
    gender: Optional[str] = ''
    birthdate: Optional[date] = None
    address: Optional[str] = ''
    image_name: Optional[str] = ''

class ProfileInputSchema(Schema):
    gender: Optional[str] = ''
    birthdate: Optional[date] = None
    address: Optional[str] = ''
    image_name: Optional[str] = ''

class UpdateProfileSchema(Schema):
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    image_name: Optional[str] = ''