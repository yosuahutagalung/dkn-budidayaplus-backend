from typing import Optional
from django.contrib.auth.models import User
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