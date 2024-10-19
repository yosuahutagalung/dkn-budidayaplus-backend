from user_profile.models import UserProfile
from user_profile.services.retreive_service import RetreiveService

class RetreiveServiceImpl(RetreiveService):
    @staticmethod
    def retreive_profile(username: str) -> UserProfile:
        return UserProfile.objects.get(user__username=username)
