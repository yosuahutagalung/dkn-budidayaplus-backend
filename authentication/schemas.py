from ninja import Schema

class RegisterSchema(Schema):
  phone_number: str
  first_name: str
  last_name: str
  password: str

class LoginSchema(Schema):
  phone_number: str
  password: str

class RefreshSchema(Schema):
  refresh: str