from django.db import models
from django.contrib.auth.models import User
import uuid
from user_profile.enums import Role

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=255, blank=True)

    @property
    def role(self):
        if isinstance(self, Worker):
            return Role.WORKER.value
        return Role.SUPERVISOR.value

class Worker(UserProfile):
    assigned_supervisor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='workers')
