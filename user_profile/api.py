from typing import List
from django.core.exceptions import PermissionDenied, ValidationError
from ninja import Router
from user_profile.services.create_worker_service import CreateWorkerService
from user_profile.services.create_worker_service_impl import CreateWorkerServiceImpl
from user_profile.services.get_team_service_impl import GetTeamServiceImpl
from user_profile.services.retrieve_service_impl import RetrieveServiceImpl
from user_profile.services.update_service_impl import UpdateServiceImpl
from ninja_jwt.authentication import JWTAuth
from user_profile.models import UserProfile
from ninja.errors import HttpError
from user_profile.schemas import CreateWorkerSchema, ProfileSchema, UpdateProfileSchema

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


@router.get("/", response=List[ProfileSchema])
def get_workers(request):
    return handle_exceptions(GetTeamServiceImpl.get_team, request.auth)

@router.post("/create-worker", response=ProfileSchema)
def create_worker(request, payload_worker: CreateWorkerSchema):
    try: 
        return CreateWorkerServiceImpl.create_worker(payload_worker, request.auth)
    except ValidationError as e:
        raise HttpError(400, str(e))
    except PermissionDenied as e:
        raise HttpError(403, str(e))

