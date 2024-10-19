from abc import ABC, abstractmethod
from user_profile.models import UserProfile

class RetreiveService(ABC):
    @staticmethod
    @abstractmethod
    def retreive_profile(username: str) -> UserProfile:
        """Retreive profile by username"""