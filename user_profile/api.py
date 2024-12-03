from typing import List
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from ninja import Router
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
    except UserProfile.DoesNotExist as e:
        raise HttpError(404, "Profile tidak ditemukan")
    except PermissionDenied as e:
        raise HttpError(403, "Anda tidak memiliki akses untuk melakukan ini")
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
    handle_exceptions(CreateWorkerServiceImpl.create_worker, payload_worker, request.auth)

@router.get("/workers-only")
def get_workers_only(request):
    return handle_exceptions(GetTeamServiceImpl.get_workers_only_list, request.auth)

@router.get("/is-in-team/{supervisor_username}")
def is_in_team(request, supervisor_username: str):
    supervisor = RetrieveServiceImpl.retrieve_user(supervisor_username)
    return handle_exceptions(GetTeamServiceImpl.is_in_team, request.auth, supervisor)

@router.get("/is-supervisor/{username}")
def is_supervisor(request, username: str):
    return RetrieveServiceImpl.retrieve_profile(username).role == 'supervisor'
