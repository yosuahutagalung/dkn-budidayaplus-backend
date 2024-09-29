from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Pond
from .schemas import PondSchema, PondOutputSchema
from ninja_jwt.authentication import JWTAuth
from typing import List
from ninja_extra import api_controller, route

@api_controller("/pond", tags=["Pond"], permissions=[])
class PondController:
    @route.post("/", auth=JWTAuth(), response={200: PondOutputSchema})
    def add_pond(self, payload: PondSchema, request):
        owner = get_object_or_404(User, id=request.auth.id)
        pond = Pond.objects.create(
            owner=owner,
            name=payload.name,
            image_name=payload.image_name,
            length=payload.length,
            width=payload.width,
            depth=payload.depth
        )
        return pond

    @route.get("/{pond_id}/", auth=JWTAuth(), response={200: PondOutputSchema})
    def get_pond(self, pond_id: str):
        pond = get_object_or_404(Pond, pond_id=pond_id)
        return pond

    @route.get("/", auth=JWTAuth(), response={200: List[PondOutputSchema]})
    def list_ponds_by_user(self, request):
        user = request.auth
        ponds = Pond.objects.filter(owner=user)
        return ponds

    @route.delete("/{pond_id}/", auth=JWTAuth())
    def delete_pond(self, pond_id: str):
        pond = get_object_or_404(Pond, pond_id=pond_id)
        pond.delete()
        return {"success": True}

    @route.put("/{pond_id}/", auth=JWTAuth(), response={200: PondOutputSchema})
    def update_pond(self, pond_id: str, payload: PondSchema):
        pond = get_object_or_404(Pond, pond_id=pond_id)
        
        data = payload.dict()
        for attr, value in data.items():
            if not value:
                continue
            setattr(pond, attr, value)

        pond.save()
        return pond
