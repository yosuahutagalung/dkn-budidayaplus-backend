from ninja import Router 
from user_profile.services.retrieve_service_impl import RetrieveServiceImpl
from ninja_jwt.authentication import JWTAuth
from user_profile.models import UserProfile
from ninja.errors import HttpError
from user_profile.schemas import ProfileSchema

router = Router(auth=JWTAuth())
service = RetrieveServiceImpl()

@router.get("/{username}/", response=ProfileSchema)
def get_profile(request, username: str):
    try:
        profile = service.retrieve_profile(username)
        return profile
    except UserProfile.DoesNotExist:
        raise HttpError(404, "Profile tidak ditemukan")
    except Exception as e:
        raise HttpError(400, str(e))