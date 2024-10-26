from django.db import models
from pond.models import Pond
from cycle.models import Cycle
from django.contrib.auth.models import User
import uuid

class FoodSampling(models.Model):
    sampling_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    food_quantity = models.PositiveIntegerField()
    sample_date = models.DateField()