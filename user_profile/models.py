from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=255, blank=True)
    image_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=1, blank=True)
    birthdate = models.DateField(blank=True)
