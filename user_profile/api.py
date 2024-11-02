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

@router.put("/{username}/", response=UpdateProfileSchema)
def update_profile(request, username: str, payload_profile: UpdateProfileSchema):
    user = User(
        first_name = payload_profile.first_name,
        last_name = payload_profile.last_name,
        username = "08888888888"
    )
    user_profile = UserProfile(
        image_name = payload_profile.image_name
    )
    try:
        service = UpdateServiceImpl.update_profile(username, user_profile, user)
        result = UpdateProfileSchema(
            first_name=service["user"].first_name,
            last_name=service["user"].last_name,
            image_name=service["profile"].image_name
        )
        return result
    except UserProfile.DoesNotExist:
        raise HttpError(404, "Profile tidak ditemukan")
    except Exception as e:
        raise HttpError(500, str(e))
@router.get("/{username}/", response=ProfileSchema)
def get_profile(request, username: str):
    return handle_exceptions(RetrieveServiceImpl.retrieve_profile, username)

@router.get("/", response=ProfileSchema)
def get_profile_by_user(request):
    return handle_exceptions(RetrieveServiceImpl.retrieve_profile_by_user, request.auth)
