from typing import List
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
    
    @staticmethod
    def get_pond(pond_id: str) -> Pond:
        return PondRepository.get_pond_by_id(pond_id)
    
    @staticmethod
    def list_ponds_by_user(user: User) -> List[Pond]:
        return PondRepository.list_ponds_by_user(user)
    
    @staticmethod
    def delete_pond(pond_id: str) -> None:
        PondRepository.delete_pond(pond_id)

    @staticmethod
    def update_pond(pond_id: str, payload: PondSchema) -> Pond:
        pond = PondRepository.get_pond_by_id(pond_id)
        return PondRepository.update_pond(
            pond=pond,
            **payload.dict()
        )