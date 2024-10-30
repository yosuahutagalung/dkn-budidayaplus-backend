from abc import ABC, abstractmethod
from user_profile.models import UserProfile

class UpdateService(ABC):
    @staticmethod
    @abstractmethod
    def update_profile(username: str, payload: UserProfile):
        """Update profile by username"""