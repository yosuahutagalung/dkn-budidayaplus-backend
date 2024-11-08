from abc import ABC, abstractmethod
from user_profile.schemas import UpdateProfileSchema
from django.contrib.auth.models import User

class UpdateService(ABC):
    @staticmethod
    @abstractmethod
    def update_profile(payload_profile: UpdateProfileSchema, user: User):
        """Update profile by username"""