from abc import ABC, abstractmethod
from typing import List
from django.contrib.auth.models import User
from user_profile.models import UserProfile

class GetTeamService(ABC):
    @staticmethod
    @abstractmethod
    def get_team(user: User) -> List[UserProfile]:
        """Retrieve list of team members"""

    @staticmethod
    @abstractmethod
    def get_workers_only_list(user: User) -> List[UserProfile]:
        """Retrieve list of workers, this method is only for supervisors"""

    @staticmethod
    @abstractmethod
    def is_in_team(user: User, supervisor: User) -> bool:
        """Check if the selected user is in the team of the selected supervisor"""
