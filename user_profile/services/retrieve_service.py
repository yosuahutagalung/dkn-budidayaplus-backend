from abc import ABC, abstractmethod
from user_profile.models import UserProfile, Worker
from django.contrib.auth.models import User

class RetrieveService(ABC):
    @staticmethod
    @abstractmethod
    def retrieve_profile(username: str) -> UserProfile:
        """Retreive profile by username"""
    
    @staticmethod
    @abstractmethod
    def retrieve_profile_by_user(user: User) -> UserProfile:
        """Retrieve a profile by user's token""" 

    @staticmethod
    @abstractmethod
    def get_workers(user: User) -> list[Worker]:
        """Retrieve workers by user's token"""
