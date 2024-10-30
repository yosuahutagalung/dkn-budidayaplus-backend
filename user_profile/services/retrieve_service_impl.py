from user_profile.models import UserProfile
from user_profile.services.retrieve_service import RetrieveService

class RetrieveServiceImpl(RetrieveService):
    @staticmethod
    def retrieve_profile(username): 
        return UserProfile.objects.get(user__username=username)

    @staticmethod
    def retrieve_profile_by_user(user):
        pass
