from ninja import Router 
from user_profile.services.retrieve_service_impl import RetrieveServiceImpl
from user_profile.services.update_service_impl import UpdateServiceImpl
from ninja_jwt.authentication import JWTAuth
from user_profile.models import UserProfile
from django.contrib.auth.models import User
from ninja.errors import HttpError
from user_profile.schemas import ProfileSchema, UpdateProfileSchema

router = Router(auth=JWTAuth())

def handle_exceptions(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except UserProfile.DoesNotExist:
        raise HttpError(404, "Profile tidak ditemukan")
    except Exception as e:
        raise HttpError(400, str(e))

@router.put("/", response=UpdateProfileSchema)
def update_profile(request, payload_profile: UpdateProfileSchema):
    return handle_exceptions(UpdateServiceImpl.update_profile, payload_profile, request.auth)

@router.get("/{username}/", response=ProfileSchema)
def get_profile(request, username: str):
    return handle_exceptions(RetrieveServiceImpl.retrieve_profile, username)

@router.get("/", response=ProfileSchema)
def get_profile_by_user(request):
    return handle_exceptions(RetrieveServiceImpl.retrieve_profile_by_user, request.auth)
