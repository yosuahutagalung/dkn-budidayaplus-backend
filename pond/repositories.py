from typing import List, Optional
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from typing import Optional
from .models import Pond

class PondRepository:    
    @staticmethod
    def create_pond(owner: User, name: str, image_name: Optional[str], length: float, width: float, depth: float) -> Pond:
        return Pond.objects.create(
            owner=owner,
            name=name,
            image_name=image_name,
            length=length,
            width=width,
            depth=depth
        )
    
    @staticmethod
    def get_pond_by_id(pond_id: str) -> Pond:
        return get_object_or_404(Pond, pond_id=pond_id)
    
    @staticmethod
    def list_ponds_by_user(user: User) -> List[Pond]:
        return Pond.objects.filter(owner=user)
    
    @staticmethod
    def delete_pond(pond_id: str) -> None:
        get_object_or_404(Pond, pond_id=pond_id).delete()

    @staticmethod
    def update_pond(pond: Pond, name: Optional[str], image_name: Optional[str], length: Optional[float], width: Optional[float], depth: Optional[float]) -> Pond:
        if name:
            pond.name = name
        if image_name:
            pond.image_name = image_name
        if length:
            pond.length = length
        if width:
            pond.width = width
        if depth:
            pond.depth = depth
        pond.save()
        return pond