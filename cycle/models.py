from django.db import models
from pond.models import Pond
from django.contrib.auth.models import User
import uuid

class Cycle(models.Model):
    cycle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fish_amounts = models.IntegerField()
    starting_date = models.DateField()
    ending_date = models.DateField()
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.cycle_id)
