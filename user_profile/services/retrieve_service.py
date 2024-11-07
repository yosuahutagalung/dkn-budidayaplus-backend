from abc import ABC, abstractmethod
from user_profile.models import UserProfile

class RetrieveService(ABC):
    @staticmethod
    @abstractmethod
    def retrieve_profile(username: str) -> UserProfile:
        """Retreive profile by username"""