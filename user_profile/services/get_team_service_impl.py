from user_profile.services.get_team_service import GetTeamService
from user_profile.models import UserProfile, Worker

class GetTeamServiceImpl(GetTeamService):
    @staticmethod
    def get_team(user):
        user_profile = UserProfile.objects.get(user=user)
        if isinstance(user_profile, Worker):
            return list(user_profile.assigned_supervisor) + list(Worker.objects.filter(assigned_supervisor=user_profile.assigned_supervisor))
        else:
            return [user_profile] + list(Worker.objects.filter(assigned_supervisor=user_profile))
