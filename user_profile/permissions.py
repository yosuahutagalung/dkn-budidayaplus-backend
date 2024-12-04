from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from user_profile.services.get_team_service_impl import GetTeamServiceImpl

def check_supervisor_permission(user: User) -> bool:
    if not user.is_staff:
        raise PermissionDenied("Anda tidak memiliki akses")

    return True

def check_team_supervisor_permission(supervisor: User, worker: User) -> bool:
    check_supervisor_permission(supervisor)

    if not GetTeamServiceImpl.is_in_team(worker, supervisor):
        raise PermissionDenied("Anda tidak memiliki akses untuk melakukan ini")

    return True

