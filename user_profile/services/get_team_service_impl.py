from django.core.exceptions import PermissionDenied
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

    @staticmethod
    def get_workers_only_list(user):
        user_profile = UserProfile.objects.prefetch_related('workers').get(user=user)
        if user_profile.role == 'worker':
            raise PermissionDenied()
        return list(user_profile.workers.all())

    @staticmethod
    def is_in_team(user, supervisor):
        user_profile = UserProfile.objects.select_related('worker__assigned_supervisor').get(user=user)
        supervisor_profile = UserProfile.objects.get(user=supervisor)

        if hasattr(user_profile, 'worker'):
            return user_profile.worker.assigned_supervisor == supervisor_profile

        return user_profile == supervisor_profile
