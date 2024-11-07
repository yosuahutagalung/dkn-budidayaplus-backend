from user_profile.models import UserProfile
from user_profile.services.update_service import UpdateService
from django.contrib.auth.models import User
from user_profile.schemas import UpdateProfileSchema


class UpdateServiceImpl(UpdateService):
    @staticmethod
    def update_profile(payload_profile: UpdateProfileSchema, user: User):
        profile = UserProfile.objects.get(user=user)
        user.first_name = payload_profile.first_name
        user.last_name = payload_profile.last_name
        profile.image_name = payload_profile.image_name
        user.save()
        profile.save()

        return profile
