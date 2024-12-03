from user_profile.models import UserProfile
from user_profile.services.get_team_service import GetTeamService

class GetTeamServiceImpl(GetTeamService):
    @staticmethod
    def get_team(user):
        user_profile = UserProfile.objects.select_related(
            'worker__assigned_supervisor'
        ).prefetch_related('workers').get(user=user)

        if hasattr(user_profile, 'worker'):
            supervisor = user_profile.worker.assigned_supervisor
            return [supervisor] + list(supervisor.workers.all())

        return [user_profile] + list(user_profile.workers.all())

