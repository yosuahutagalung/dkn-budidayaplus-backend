from user_profile.models import UserProfile
from user_profile.services.update_service import UpdateService
from django.contrib.auth.models import User


class UpdateServiceImpl(UpdateService):
    @staticmethod
    def update_profile(username: str, payload_profile: UserProfile, payload_user = User): 
        profile = UserProfile.objects.get(user__username=username)
        user = User.objects.get(username = username)
        user.first_name = payload_user.first_name
        user.last_name = payload_user.last_name
        profile.image_name = payload_profile.image_name
        user.save()
        profile.save()
        result = {}
        result["profile"] = profile
        result["user"] = user
        return result