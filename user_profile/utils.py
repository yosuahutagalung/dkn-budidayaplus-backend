from user_profile.models import UserProfile
from django.contrib.auth.models import User

def get_supervisor(user: User):
    """
    Returns the supervisor of the user if the user is a worker, otherwise returns the user themselves
    """
    if user.is_staff:
        return user

    profile = UserProfile.objects.select_related('worker__assigned_supervisor__user').get(user=user)
    return profile.worker.assigned_supervisor.user

