from django.contrib.auth.models import User
from .models import Pond
from .schemas import PondSchema
from .repositories import PondRepository

class PondService:
    @staticmethod
    def add_pond(owner: User, payload: PondSchema) -> Pond:
        return PondRepository.create_pond(
            owner=owner,
            name=payload.name,
            image_name=payload.image_name,
            length=payload.length,
            width=payload.width,
            depth=payload.depth
        )