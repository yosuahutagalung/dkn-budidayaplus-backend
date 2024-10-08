from ninja import Schema
from pydantic import field_validator
from ninja.errors import HttpError

class RegisterSchema(Schema):
  phone_number: str
  first_name: str
  last_name: str
  password: str

  @field_validator("phone_number")
  def phone_number_validator(cls, value):
    if not value.isdigit() or not (10 <= len(value) <= 13):
      raise HttpError(400, "Phone number must be a number and between 10-13 characters")
    return value

class LoginSchema(Schema):
  phone_number: str
  password: str

class RefreshSchema(Schema):
  refresh: str
