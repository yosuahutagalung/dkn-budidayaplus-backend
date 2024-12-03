from abc import ABC, abstractmethod
from typing import List
from django.contrib.auth.models import User
from user_profile.models import UserProfile

class GetTeamService(ABC):
    @staticmethod
    @abstractmethod
    def get_team(user: User) -> List[UserProfile]:
        """Retrieve list of team members"""
