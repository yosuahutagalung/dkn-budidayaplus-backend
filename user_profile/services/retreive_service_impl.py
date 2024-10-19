from user_profile.models import UserProfile
from user_profile.services.retreive_service import RetreiveService

class RetreiveServiceImpl(RetreiveService):
    def retreive_profile(self, username: str) -> UserProfile:
        return None
