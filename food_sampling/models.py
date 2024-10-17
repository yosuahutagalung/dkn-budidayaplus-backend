from django.db import models
from pond.models import Pond
from cycle.models import Cycle
from django.contrib.auth.models import User
import uuid

class FoodSampling(models.Model):
    food_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    food_amount = models.FloatField()
    date = models.DateField()

    def __str__(self):
        # return self.food_id
        return f"Food Sampling for {self.pond.name} on {self.date}"