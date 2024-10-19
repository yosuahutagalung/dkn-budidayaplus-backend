from abc import ABC, abstractmethod
from user_profile.models import UserProfile

class RetreiveService(ABC):
    @abstractmethod
    def retreive_profile(self, username: str) -> UserProfile:
        """Retreive profile by username"""