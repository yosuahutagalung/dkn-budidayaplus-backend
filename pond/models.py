from django.db import models
from django.contrib.auth.models import User
import uuid

class Pond(models.Model):
    pond_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image_name = models.CharField(max_length=255, blank=True)
    length = models.FloatField()
    width = models.FloatField()
    depth = models.FloatField()

    def __str__(self):
        return self.name