from typing import Optional
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
    def delete_pond(pond_id: str) -> None:
        get_object_or_404(Pond, pond_id=pond_id).delete()