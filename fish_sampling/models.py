from django.db import models
from pond.models import Pond
from cycle.models import Cycle
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import uuid

class FishSampling(models.Model):
    sampling_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    fish_weight = models.FloatField(validators=[MinValueValidator(0.0)])
    fish_length = models.FloatField(validators=[MinValueValidator(0.0)])
    recorded_at = models.DateTimeField()

    def __str__(self):
        return str(self.sampling_id)
