from django.db import models
from django.contrib.auth.models import User, Pond
import uuid

class FishSampling(models.Model):
    sampling_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    fish_weight = models.FloatField()
    fish_length = models.FloatField()
    sample_date = models.DateField()

    def __str__(self):
        return self.name
