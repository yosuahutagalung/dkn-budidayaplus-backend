from ninja import Router 
from user_profile.services.retreive_service_impl import RetreiveServiceImpl
from ninja_jwt.authentication import JWTAuth

router = Router(auth=JWTAuth())
service = RetreiveServiceImpl()

@router.get("/{username}/")
def get_profile(request, username: str):
    pass